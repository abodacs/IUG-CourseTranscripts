"""CF-04 failure probes: every plan-required fault, proven against a FAKE
provider. No real provider is ever contacted."""
import pytest

from src.factory import dispatch
from src.factory.dispatch import PersistenceFailed, ProviderUnavailable, ResponseLost
from src.factory.ledger import Ledger, LedgerPolicyError, LineageExhausted


class FakeProvider:
    """Scripted provider: behavior per call, one call recorded."""

    def __init__(self, behavior="ok", usage=None):
        self.behavior = behavior
        self.usage_value = usage or {"in": 100, "out": 40}
        self.calls = 0

    def call(self, model, reserved_in, reserved_out):
        self.calls += 1
        if self.behavior == "unavailable":
            raise ProviderUnavailable("provider refused the connection")
        if self.behavior == "lost":
            raise ResponseLost("the response never arrived")
        if isinstance(self.behavior, BaseException):
            raise self.behavior
        return {"text": "cached accepted content"}

    def usage(self, response):
        return dict(self.usage_value)


@pytest.fixture
def ledger(tmp_path):
    book = Ledger(tmp_path / "spend.sqlite")
    book.set_allocation("pilot", 10_000, "test cap; real value stays OPEN until operator measures")
    return book


def test_dispatch_refused_without_recorded_allocation(tmp_path):
    book = Ledger(tmp_path / "open.sqlite")  # allocation never recorded (OPEN)
    with pytest.raises(LedgerPolicyError, match="allocation_pilot_open"):
        book.reserve("u1", "model-x", 100, 40)


def test_happy_path_persists_usage_and_success(ledger):
    attempt, response, usage = dispatch.guarded_dispatch(
        ledger, FakeProvider(), unit_id="u1", model="m", reserved_in=100, reserved_out=40,
        persist_output=lambda r: "out/lesson-1.md",
    )
    row = ledger.get(attempt)
    assert row["state"] == "succeeded"
    assert (row["usage_in"], row["usage_out"], row["output_ref"]) == (100, 40, "out/lesson-1.md")


def test_dispatched_is_committed_before_the_external_call(ledger):
    provider = FakeProvider(behavior=KeyboardInterrupt("process died right after dispatch"))
    ledger.register_unit("u1")
    attempt = ledger.reserve("u1", "m", 100, 40)
    ledger.mark_dispatched(attempt)
    with pytest.raises(KeyboardInterrupt):
        provider.call("m", 100, 40)
    fresh = Ledger(ledger.path)  # simulate restart
    assert fresh.get(attempt)["state"] == "dispatched"  # durable, never 'reserved' or lost


def test_crash_before_dispatch_is_confirmed_and_releases(ledger, monkeypatch):
    def boom(*a, **k):
        raise KeyboardInterrupt("process died before dispatch")
    monkeypatch.setattr(ledger, "mark_dispatched", boom)
    with pytest.raises(KeyboardInterrupt):
        dispatch.guarded_dispatch(ledger, FakeProvider(), unit_id="u1", model="m",
                                  reserved_in=100, reserved_out=40)
    fresh = Ledger(ledger.path)
    row = fresh.conn.execute("SELECT attempt_id, state FROM reservations").fetchone()
    assert row["state"] == "reserved"  # provider never called
    fresh.fail_confirmed(row["attempt_id"])  # recovery confirms non-dispatch
    assert fresh.get(row["attempt_id"])["state"] == "failed_confirmed"
    assert fresh.consumed("pilot") == 0  # reservation released


def test_response_loss_keeps_unknown_reservation_and_blocks_dispatch(ledger):
    with pytest.raises(ResponseLost):
        dispatch.guarded_dispatch(ledger, FakeProvider(behavior="lost"), unit_id="u1",
                                  model="m", reserved_in=100, reserved_out=40)
    fresh = Ledger(ledger.path)
    assert fresh.dispatch_blocked_reason() == "unresolved_outcome_or_inflight"
    with pytest.raises(LedgerPolicyError, match="unresolved_outcome_or_inflight"):
        fresh.reserve("u2", "m", 10, 10)  # unknown outcome stops ALL new dispatch
    attempt = fresh.conn.execute("SELECT attempt_id FROM reservations").fetchone()["attempt_id"]
    fresh.reconcile_unknown(attempt, 100, 40)
    assert fresh.dispatch_blocked_reason() is None
    fresh.reserve("u2", "m", 10, 10)  # now dispatch can resume


def test_crash_after_receipt_before_usage_commit_leaves_dispatched(ledger):
    def failing_persist(response):
        raise OSError("disk full while writing the artifact")
    with pytest.raises(PersistenceFailed) as caught:
        dispatch.guarded_dispatch(ledger, FakeProvider(), unit_id="u1", model="m",
                                  reserved_in=100, reserved_out=40, persist_output=failing_persist)
    fresh = Ledger(ledger.path)
    row = fresh.get(caught.value.attempt_id)
    assert row["state"] == "dispatched"  # never silently successful
    # response is carried in the exception: retry persistence, then complete
    fresh.complete(caught.value.attempt_id, caught.value.usage["in"], caught.value.usage["out"],
                   "out/lesson-1.md")
    assert fresh.get(caught.value.attempt_id)["state"] == "succeeded"


def test_two_workers_contending_for_last_allowance(ledger):
    ledger.set_allocation("pilot", 200, "tiny test cap")
    ledger.reserve("u1", "m", 120, 80)  # consumes the whole cap as a hold
    with pytest.raises(LedgerPolicyError, match="allowance pilot"):
        ledger.reserve("u2", "m", 10, 10)  # second worker is refused


def test_provider_unavailable_confirms_failure_and_counts_retry(ledger):
    for _ in range(2):
        with pytest.raises(ProviderUnavailable):
            dispatch.guarded_dispatch(ledger, FakeProvider(behavior="unavailable"), unit_id="u1",
                                      model="m", reserved_in=50, reserved_out=20)
    assert ledger.lineage("u1")["transient_retries"] == 2
    with pytest.raises(LineageExhausted):
        dispatch.guarded_dispatch(ledger, FakeProvider(behavior="unavailable"), unit_id="u1",
                                  model="m", reserved_in=50, reserved_out=20)
    assert ledger.lineage("u1")["status"] == "quarantined"
    with pytest.raises(LedgerPolicyError, match="quarantined"):
        ledger.reserve("u1", "m", 50, 20)


def test_lineage_exhaustion_survives_restart(ledger):
    for _ in range(2):
        ledger.count_event("u1", "transient_retry")
    ledger.count_event("u1", "repair")
    ledger.count_event("u1", "premium_escalation")
    with pytest.raises(LineageExhausted, match="transient_retry"):
        ledger.count_event("u1", "transient_retry")
    fresh = Ledger(ledger.path)  # durable across restart
    assert fresh.lineage("u1")["status"] == "quarantined"
    with pytest.raises(LedgerPolicyError, match="quarantined"):
        fresh.reserve("u1", "m", 10, 10)


def test_usage_above_reservation_is_recorded_and_stops_dispatch(ledger):
    ledger.set_allocation("pilot", 200, "tight cap")
    attempt, _, usage = dispatch.guarded_dispatch(
        ledger, FakeProvider(usage={"in": 900, "out": 900}), unit_id="u1", model="m",
        reserved_in=100, reserved_out=40,
    )
    assert ledger.get(attempt)["state"] == "succeeded"
    # actual 1800 > cap 200: consumed uses real usage, new dispatch is blocked
    assert ledger.consumed("pilot") == 1800
    assert ledger.dispatch_blocked_reason() == "over_reservation_reconcile"
    with pytest.raises(LedgerPolicyError, match="over_reservation"):
        ledger.reserve("u2", "m", 10, 10)


def test_unknown_reconciliation_above_reservation_writes_observed_usage(ledger):
    with pytest.raises(ResponseLost):
        dispatch.guarded_dispatch(ledger, FakeProvider(behavior="lost"), unit_id="u1",
                                  model="m", reserved_in=100, reserved_out=40)
    attempt = ledger.conn.execute("SELECT attempt_id FROM reservations").fetchone()["attempt_id"]
    ledger.reconcile_unknown(attempt, 150, 60)  # actual 210 > reserved 140
    notes = ledger.conn.execute("SELECT note FROM observed_usage").fetchall()
    assert any("exceeded its reservation" in row["note"] for row in notes)
    assert ledger.get(attempt)["state"] == "succeeded"


def test_allocations_stay_open_until_measured(ledger):
    assert ledger.allocation("run:cf07") is None
    with pytest.raises(LedgerPolicyError, match="OPEN"):
        ledger.remaining("run:cf07")
    ledger.set_allocation("run:cf07", 1_000, "measured from CF-07 actuals (placeholder evidence)")
    assert ledger.remaining("run:cf07") == 1_000
