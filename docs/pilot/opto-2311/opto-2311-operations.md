# OPTO 2311 — operations runbook (CF-13 skeleton)

**STATUS: DRAFT skeleton — prepared ahead of CF-11 promotion per plan §14. Owner names, response targets, and cadences are OPEN; an agent cannot choose them. Nothing here is operational until the human gates in [scope freeze](opto-2311-scope-freeze.md) clear and CF-11/11A qualify the release path.**

## 1. Problem reporting

- Public route: `/report` page + mailto fallback, capturing `lesson_id`, `node_id`, `release_id` (all three required fields; pre-filled from the page footer on lesson pages).
- Intake → private incident record (never public): `incident_id`, reporter contact (optional), affected lesson/node/release, description, timestamp, severity (assigner: operator), status lifecycle `received → triaged → contained → repaired → republished → verified → closed`.

## 2. Severity and response targets — OPEN

| Severity | Definition | Acknowledge | Contain | Restore | Owner |
|---|---|---|---|---|---|
| S1 correctness/rights | wrong teaching content, rights breach, contaminated source | **OPEN** | **OPEN** | **OPEN** | **OPEN** (operator + named backup) |
| S2 availability | site down, assets broken, quiz unusable | **OPEN** | **OPEN** | **OPEN** | **OPEN** |
| S3 cosmetic/UX | rendering, typos, non-blocking | **OPEN** | **OPEN** | **OPEN** | **OPEN** |

Targets are chosen by the operator; unattended monitoring must not be implied beyond what an occasional check provides (F10/F11).

## 3. Monitoring checks — owner and cadence OPEN

- Public availability of the site and expected release ID.
- Asset links resolve; quiz interaction works without revealing answers.
- Backup freshness: independent backup exists, checksum matches, restore spot-check within cadence.
- Drift triggers: source video edited/deleted, rights status change, provider/model/parser/schema change → recanary/recalibration decision (F19).

## 4. Repair loop (per plan §14; rehearsed before CF-12 acceptance)

1. Report → identify affected evidence, dependencies (build-dependency graph), and every release/derivative.
2. Contain: withdraw affected public versions where no safe accepted version exists; invalidate unsafe rollback targets.
3. Repair via append-only correction (CF-02A ledger) backed by allowed evidence; bounded budget through the CF-04 ledger.
4. Independent review (subject/editorial) of the repair; reopen CF-09/CF-10 checks where teaching or evaluation changed.
5. Republish only the eligible exact bundle through CF-11; verify the public fix; publish a correction note.
6. Record regression case, response/recovery times, and maintenance cost separately.

## 5. Backup and handover — OPEN

- Independent backup of evidence, editable content, ledger, verdicts, reviews, configuration (F08), cadence **OPEN**, capacity/retention **OPEN**, restore-drill cadence **OPEN**.
- Backup owner + absence coverage: **OPEN**.
- Credentials recover through a separate documented route, never via content backups.

## 6. Rehearsal (before CF-12 acceptance)

Seed a defect in a private production-equivalent environment; run the full loop; measure detection/containment/restoration against §2 targets; record the maintenance cost and the correction note. Do not expose learners to known-invalid teaching.
