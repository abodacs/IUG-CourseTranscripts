"""CF-04: the durable token spend ledger with bounded lineage.

Integer-token reservations in SQLite. Dispatch is refused without a
successful reservation; the `dispatched` transition is committed before the
external call; usage is persisted in the same transaction that marks success;
an attempt whose outcome cannot be proven stays `outcome_unknown` (across
restarts) and blocks all new dispatch until reconciled. Per-unit lineage
(<=2 transient retries, 1 repair, 1 premium escalation) is durable; exhaustion
quarantines the unit instead of relaxing any quality gate.

Allocations are operator-measured inputs; until measured they stay OPEN and
any dispatch attempt is refused. No provider calls happen in this module.
"""
from pathlib import Path
import datetime
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS allocations (
    scope TEXT PRIMARY KEY,
    token_cap INTEGER NOT NULL,
    derivation TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reservations (
    attempt_id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL,
    model TEXT NOT NULL,
    reserved_in INTEGER NOT NULL,
    reserved_out INTEGER NOT NULL,
    state TEXT NOT NULL CHECK (state IN
        ('reserved','dispatched','succeeded','failed_confirmed','outcome_unknown')),
    run_id TEXT,
    created_at TEXT NOT NULL,
    dispatched_at TEXT,
    finished_at TEXT,
    usage_in INTEGER,
    usage_out INTEGER,
    output_ref TEXT
);
CREATE TABLE IF NOT EXISTS observed_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    source TEXT NOT NULL,
    in_tokens INTEGER NOT NULL,
    out_tokens INTEGER NOT NULL,
    note TEXT
);
CREATE TABLE IF NOT EXISTS unit_lineage (
    unit_id TEXT PRIMARY KEY,
    transient_retries INTEGER NOT NULL DEFAULT 0,
    repairs INTEGER NOT NULL DEFAULT 0,
    premium_escalations INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT ('active') CHECK (status IN ('active','quarantined'))
);
"""

LIMITS = {"transient_retries": 2, "repairs": 1, "premium_escalations": 1}


class LedgerPolicyError(RuntimeError):
    """Dispatch/refusal decision: no reservation, exhausted allowance,
    unresolved unknown outcome, or quarantined unit."""


class LineageExhausted(RuntimeError):
    """The unit consumed its bounded retries/repair/escalation and is
    quarantined; the rubric is never relaxed to continue."""


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA busy_timeout = 5000")
        self.conn.executescript(SCHEMA)

    def _begin_write(self):
        """Serialize check-then-write sequences across workers: BEGIN
        IMMEDIATE takes the write lock up front, so an allowance check and
        its insert (or a lineage check and its increment) are atomic even
        against another process holding its own connection."""
        self.conn.execute("BEGIN IMMEDIATE")

    def close(self):
        self.conn.close()

    # -- allocations -------------------------------------------------------
    def set_allocation(self, scope, token_cap, derivation):
        if token_cap is None:
            raise LedgerPolicyError(f"allocation for {scope} is OPEN; record a measured cap first")
        self.conn.execute(
            "INSERT INTO allocations (scope, token_cap, derivation, recorded_at) VALUES (?,?,?,?)"
            " ON CONFLICT(scope) DO UPDATE SET token_cap=excluded.token_cap,"
            " derivation=excluded.derivation, recorded_at=excluded.recorded_at",
            (scope, int(token_cap), derivation, _now()),
        )

    def allocation(self, scope):
        row = self.conn.execute("SELECT token_cap FROM allocations WHERE scope=?", (scope,)).fetchone()
        return row["token_cap"] if row else None

    def consumed(self, scope):
        """Tokens held or spent under a scope. Actual measured usage counts
        once known — an attempt that truly spent more than reserved keeps
        consuming at its real size, and over-reservation blocks new dispatch."""
        row = self.conn.execute(
            "SELECT COALESCE(SUM(COALESCE(usage_in + usage_out, reserved_in + reserved_out)), 0)"
            " AS total FROM reservations"
            " WHERE run_id = ? AND state IN ('reserved','dispatched','succeeded','outcome_unknown')",
            (scope,),
        ).fetchone()
        return row["total"]

    def remaining(self, scope):
        cap = self.allocation(scope)
        if cap is None:
            raise LedgerPolicyError(f"allocation for {scope} is OPEN; dispatch is disabled")
        return cap - self.consumed(scope)

    # -- lineage -----------------------------------------------------------
    def register_unit(self, unit_id):
        self.conn.execute("INSERT OR IGNORE INTO unit_lineage (unit_id) VALUES (?)", (unit_id,))

    def lineage(self, unit_id):
        row = self.conn.execute("SELECT * FROM unit_lineage WHERE unit_id=?", (unit_id,)).fetchone()
        if row is None:
            self.register_unit(unit_id)
            row = self.conn.execute("SELECT * FROM unit_lineage WHERE unit_id=?", (unit_id,)).fetchone()
        return dict(row)

    def count_event(self, unit_id, kind):
        column = {"transient_retry": "transient_retries", "repair": "repairs", "premium_escalation": "premium_escalations"}[kind]
        self._begin_write()
        try:
            lineage = self.lineage(unit_id)
            if lineage["status"] == "quarantined":
                self.conn.execute("ROLLBACK")
                raise LineageExhausted(f"{unit_id} is quarantined")
            if lineage[column] >= LIMITS[column]:
                self.conn.execute(
                    "UPDATE unit_lineage SET status='quarantined' WHERE unit_id=?", (unit_id,)
                )
                self.conn.execute("COMMIT")  # the quarantine itself must persist
                raise LineageExhausted(
                    f"{unit_id}: {kind} would exceed the bound of {LIMITS[column]}; unit quarantined"
                )
            self.conn.execute(
                f"UPDATE unit_lineage SET {column} = {column} + 1 WHERE unit_id=?", (unit_id,)
            )
            self.conn.execute("COMMIT")
        except LineageExhausted:
            raise
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise

    # -- reservation lifecycle ---------------------------------------------
    def dispatch_blocked_reason(self):
        """Global stop conditions: an unproven outcome (work whose spend
        cannot be measured) stops new dispatch; ordinary in-flight
        `dispatched` attempts are normal concurrent operation. Outside
        observed usage eats the same subscription cap."""
        row = self.conn.execute(
            "SELECT COUNT(*) AS n FROM reservations WHERE state = 'outcome_unknown'"
        ).fetchone()
        if row["n"]:
            return "unresolved_unknown_outcome"
        for scope in ("pilot",):
            cap = self.allocation(scope)
            if cap is None:
                return f"allocation_{scope}_open"
            if self.consumed(scope) > cap:
                return "over_reservation_reconcile"
        outside = self.observed_outside_total()
        if cap is not None and outside and self.consumed(scope) + outside > cap:
            return "outside_usage_unreconciled"
        return None

    def observed_outside_total(self):
        row = self.conn.execute(
            "SELECT COALESCE(SUM(in_tokens + out_tokens), 0) AS total FROM observed_usage"
            " WHERE source != 'reconciliation'"
        ).fetchone()
        return row["total"]

    def reserve(self, unit_id, model, reserved_in, reserved_out, run_id="pilot"):
        if reserved_in < 0 or reserved_out < 0:
            raise LedgerPolicyError("reservations are non-negative integer tokens")
        self._begin_write()
        try:
            blocked = self.dispatch_blocked_reason()
            if blocked:
                raise LedgerPolicyError(f"dispatch refused: {blocked}")
            lineage = self.lineage(unit_id)
            if lineage["status"] == "quarantined":
                raise LedgerPolicyError(f"dispatch refused: unit {unit_id} is quarantined")
            needed = int(reserved_in) + int(reserved_out)
            for scope in {run_id, "pilot"}:
                if self.remaining(scope) < needed:
                    raise LedgerPolicyError(
                        f"dispatch refused: allowance {scope} has {self.remaining(scope)} < {needed} tokens"
                    )
            row = self.conn.execute("SELECT COALESCE(MAX(rowid), 0) + 1 AS next FROM reservations").fetchone()
            attempt_id = f"a-{row['next']:06d}"
            self.conn.execute(
                "INSERT INTO reservations (attempt_id, unit_id, model, reserved_in, reserved_out,"
                " state, run_id, created_at) VALUES (?,?,?,?,?,?,?,?)",
                (attempt_id, unit_id, model, int(reserved_in), int(reserved_out), "reserved", run_id, _now()),
            )
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")
        return attempt_id

    def _get(self, attempt_id):
        row = self.conn.execute("SELECT * FROM reservations WHERE attempt_id=?", (attempt_id,)).fetchone()
        if row is None:
            raise KeyError(attempt_id)
        return dict(row)

    def get(self, attempt_id):
        return self._get(attempt_id)

    def mark_dispatched(self, attempt_id):
        """Must be committed before the external call leaves this process."""
        row = self._get(attempt_id)
        if row["state"] != "reserved":
            raise LedgerPolicyError(f"{attempt_id}: cannot dispatch from state {row['state']}")
        self.conn.execute(
            "UPDATE reservations SET state='dispatched', dispatched_at=? WHERE attempt_id=?",
            (_now(), attempt_id),
        )

    def complete(self, attempt_id, usage_in, usage_out, output_ref=None):
        """Persist usage and success atomically; a crash here leaves the
        attempt dispatched (never silently successful)."""
        row = self._get(attempt_id)
        if row["state"] != "dispatched":
            raise LedgerPolicyError(f"{attempt_id}: cannot complete from state {row['state']}")
        self.conn.execute(
            "UPDATE reservations SET state='succeeded', finished_at=?, usage_in=?, usage_out=?,"
            " output_ref=COALESCE(?, output_ref) WHERE attempt_id=?",
            (_now(), int(usage_in), int(usage_out), output_ref, attempt_id),
        )

    def fail_confirmed(self, attempt_id):
        """Proves non-dispatch or a refused call; releases the reservation."""
        row = self._get(attempt_id)
        if row["state"] not in ("reserved", "dispatched"):
            raise LedgerPolicyError(f"{attempt_id}: cannot fail from state {row['state']}")
        self.conn.execute(
            "UPDATE reservations SET state='failed_confirmed', finished_at=? WHERE attempt_id=?",
            (_now(), attempt_id),
        )

    def mark_unknown(self, attempt_id):
        """Response lost after dispatch: the reservation is retained across
        restarts until reconciliation measures what was actually spent."""
        row = self._get(attempt_id)
        if row["state"] not in ("dispatched", "succeeded"):
            raise LedgerPolicyError(f"{attempt_id}: cannot mark unknown from state {row['state']}")
        self.conn.execute(
            "UPDATE reservations SET state='outcome_unknown', finished_at=? WHERE attempt_id=?",
            (_now(), attempt_id),
        )

    def reconcile_unknown(self, attempt_id, usage_in, usage_out):
        """Fold measured (or operator-confirmed) usage into the ledger."""
        row = self._get(attempt_id)
        if row["state"] != "outcome_unknown":
            raise LedgerPolicyError(f"{attempt_id}: not in outcome_unknown state")
        actual = int(usage_in) + int(usage_out)
        if actual > row["reserved_in"] + row["reserved_out"]:
            self.conn.execute(
                "INSERT INTO observed_usage (recorded_at, source, in_tokens, out_tokens, note)"
                " VALUES (?,?,?,?,?)",
                (_now(), "reconciliation", int(usage_in), int(usage_out),
                 f"{attempt_id} exceeded its reservation"),
            )
        self.conn.execute(
            "UPDATE reservations SET state='succeeded', finished_at=?, usage_in=?, usage_out=?"
            " WHERE attempt_id=?",
            (_now(), int(usage_in), int(usage_out), attempt_id),
        )

    def record_observed_usage(self, source, in_tokens, out_tokens, note=None):
        self.conn.execute(
            "INSERT INTO observed_usage (recorded_at, source, in_tokens, out_tokens, note)"
            " VALUES (?,?,?,?,?)",
            (_now(), source, int(in_tokens), int(out_tokens), note),
        )
