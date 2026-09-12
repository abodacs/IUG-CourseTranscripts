# OPTO 2311 — scope freeze (CF-03)

**STATUS: DRAFT — NOT FROZEN. Sign-off (operator + subject reviewer) is OPEN. This document freezes nothing yet.**

## What is already verified (recorded evidence)

| Input | State | Evidence |
|---|---|---|
| Source manifest: 106 videos, 105 raw sets, gaps visible | recorded | [source review](opto-2311-source-review.md); manifest `fe35da7e…` |
| Lecture order: 106 positions verified against live playlist (0 missing either direction) | recorded | `artifacts/opto-2311/lecture-order.json`; [first review](opto-2311-first-review.md) |
| Authoring-evidence decision (2026-09-07: raw JSON + cleaned GeminiLongContext counterparts) + evidence index (105 sets, 5,399 segments, stable IDs) | recorded | [CF-02A](../../../src/factory/evidence.py); `artifacts/opto-2311/evidence-index.json` |
| Evaluation families: 5 initially exposed development families; 10 holdout families reserved before the broader pass; all semantic access recorded | recorded policy, enforcement proof pending | `artifacts/opto-2311/evaluation-families.json`; `artifacts/opto-2311/exposure-log.json`; issues #11/#14 |
| Discovery worksheet seeded for all 106 ordered positions (421 hint topics, unapproved) | draft, pending review | `artifacts/opto-2311/outcome-worksheet.json` |
| `SAq013FtOLQ` (position 8) unavailable at fetch, disposition | OPEN — reviewer/operator decide curriculum impact | lecture-order reconciliation |
| Skipped-source completeness blocker (F05) | OPEN — full-source sufficiency audit not closed | this document |

## Freeze checklist (per plan §6.5) — each item must be recorded before CF-07 dispatch

1. **Outcome IDs** — OPEN. The matrix schema and validators exist ([outcomes.py](../../../src/factory/outcomes.py)); the full-source discovery pass over all 105 sets is in progress as `outcome-worksheet.json` rows (hint-seeded, unapproved). No outcome is approved; hint topics are pointers, not teaching facts.
2. **Lesson scope** — OPEN. Lessons will group outcomes in prereq-closed verified lecture order (validator enforces closure + acyclicity).
3. **Assessment requirements** — OPEN (per-outcome worked example / practice / transfer task IDs).
4. **Required diagrams with video IDs/ranges** — partially drafted for positions 1/53/104 in [first review](opto-2311-first-review.md); full set OPEN. Keyframe hints are pointers only (one proven unreliable: `N-78zzBlTYU` hint @1400 s > 905 s duration).
5. **Per-course/per-lesson wiki coverage** — OPEN scope decision in CF-03; CF-05 implements the approved schema and validator.
6. **Graph edge types** — OPEN scope decision in CF-03; CF-05 implements the approved types and validator.
7. **Learner assumption + prerequisites** — OPEN; the reviewer's first-review observations feed this ([first review](opto-2311-first-review.md) §reviewer decisions).
8. **Provider/key quota pool and exhaustion policy** — operator decision recorded: continue across configured authorized free quotas until all are confirmed exhausted; stop on uncertainty. [allocations.toml](../../../allocations.toml) retains historical measurements. Freeze still requires the provider/key allowlist, reset semantics, terms-compliant authorization record, and tested enforcement.
9. **Reviewer names** — OPEN. Subject reviewer and Arabic editorial reviewer not yet recruited (blocks scope freeze, verdicts, and release; recruitment is the standing day-1 dependency).

## Plan-rule reminders this draft obeys

- All 105 available sources contribute to the sufficiency/disposition audit; three-lecture inspection estimates risk only (F05).
- The skipped video's topic is never invented; impact is decided from allowed evidence or stays an explicit blocker.
- Challenge excerpts (فيزياء عامة أ `1noCDAkxHwg`; اللغة الإنجليزية `0mkSe0xrqKk`; digital-logic `Kzxd5D8ZgnQ` 13:37) remain development-only data.
- Any later scope change = new scope revision + repeated review + invalidation of affected artifacts.

## Sign-off (required to freeze)

Complete all nine checklist items and identify the reviewed matrix/scope revision before requesting sign-off. Each signer records their name, date, and approval of that completed revision (or required changes). Approval of this draft alone does not freeze scope. An agent cannot sign on your behalf — plan controls F08/F13 forbid agent-created approvals.

```
Operator (Abdullah):  ____________________  date: ________  decision: ________
Subject reviewer:     ____________________  date: ________  decision: ________
```

- Operator (Abdullah): OPEN — not signed.
- Subject reviewer: OPEN — not recruited, therefore not signed. (Recruiting checklist: optics-teaching competence; 30–45 min first review — the packet is [opto-2311-first-review.md](opto-2311-first-review.md); name + per-domain competence recorded per F13.)

Nothing downstream (CF-07 dispatch, production, evaluation, release) may treat this draft as a freeze.
