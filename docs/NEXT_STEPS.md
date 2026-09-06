# Next steps — Content Factory v1

**Status (2026-09-06): offline preparation exists; the pilot is not accepted.** CF-01 source inventory and CF-02…CF-06 helpers are merged. Validators, worksheets, a ledger prototype, and a dry judge harness do not complete those tickets' evidence requirements.

## Next task: prepare the scope-review evidence

Use the [source review](opto-2311-source-review.md), [first-review sheet](opto-2311-first-review.md), and [scope-freeze draft](opto-2311-scope-freeze.md). Prepare the evidence before requesting approval:

1. Draft the outcome matrix from all 105 available raw transcript sets: tangible tasks, exact evidence spans, prerequisites, required examples/practice/transfer tasks, and source-sufficiency blockers. The existing chapter-hint worksheet is a discovery aid, not this matrix.
2. Record needed diagrams with matching lecture IDs and time ranges. Recover visuals only for those needs. Keep the skipped source's curriculum impact unresolved until allowed evidence supports a decision.
3. Retain playlist order as metadata evidence. Transcript mentions of lecture numbers are review hints, not proof of the current lecture's identity or an ordering conflict.
4. Prepare reference cases locally from reserved development families, with source context and traceable construction records. `references.build_worksheet` creates blank slots; intended classes are preparation metadata, not correct answers. Do not reuse the old generated worksheet without re-preparing its cases: its embedded examples were not validated reference evidence. Give labelers the stripped view plus neutral source context, without intended classes or construction notes.

**Completion proof:** a transcript-backed matrix and reference packet that reviewers can assess, with gaps visible. No agent-created labels or approvals. Keep private excerpts and generated artifacts local.

## Human inputs and live execution

Reviewer recruitment and operator measurements can proceed alongside preparation:

- Named subject and Arabic editorial reviewers; learner/prerequisite confirmation; review of the completed scope packet. Signing a draft does not freeze scope.
- Observable zIDE submission, model identity, output export, usage, recovery, and remaining quota. Record measured allocations in [allocations.toml](../allocations.toml); placeholders are not authorization to dispatch.
- Independent human reference labels before any judge scores; then calibration on development data.

**Live execution remains unimplemented.** The judge harness supports only the local `FakeJudge`; it has no live-provider or ledger integration. The ledger and dispatch helpers are fake-provider prototypes. Before live use, prove shared run/pilot accounting, atomic concurrent reservations, outside-usage accounting, durable attempt limits, crash reconciliation, and output persistence through the observed zIDE workflow. Current tests are not proof of these complete guarantees.

## Remaining milestones

Follow [the production plan](pilot-opto-2311-plan.md) §15 for ticket dependencies. Keep the [goal](content-factory-v1-goal.md) and [resolution](content-factory-v1-resolution.md) as the acceptance authority.

### 1. Freeze source sufficiency and skill outcomes

Complete the full-source matrix and every [freeze checklist](opto-2311-scope-freeze.md) item, then obtain operator and subject-reviewer approval. Three sampled lectures cannot accept the whole course.

### 2. Prove quota accounting through the actual zIDE workflow

Finish the ledger guarantees above and verify integration against measured quota. If observability cannot support the guarantee, keep automated dispatch disabled. zIDE only; zero incremental cash.

### 3. Produce and evaluate one complete lesson as an engineering trial

After the prerequisites are met: author from allowed evidence, calibrate judgments, verify Arabic rendering and assessments, demonstrate unchanged-rerun reuse and restart recovery, and measure tokens and human review time. Dry tests are not teaching-quality acceptance.

### 4. Complete the pilot and demonstrate Cloudflare Pages release recovery

Complete production, independent subject/editorial review and learner evaluation. Release the complete accepted prerequisite-closed artifact set after preview checks; demonstrate failed-update isolation, rollback, withdrawal, and independent-backup restoration. Report fixed outcome coverage and first-accepted lesson IDs.

## Ticket CF-01: build the optics source manifest

**Completed source-inventory task; retained here as a link target for historical references.** The exporter is [build_pilot_manifest.py](../scripts/build_pilot_manifest.py); findings and reproducibility evidence are in the [source review](opto-2311-source-review.md). Recorded counts: 106 expected IDs, 105 raw sets, 105 chapter files, 83 audit-only v2 outputs, one skipped source. The full requirements remain in [the plan](pilot-opto-2311-plan.md#4-phase-0--cf-01-source-manifest-offline-no-model-calls).

Do not rebuild the exporter from the old session brief. Rerun it only when source changes or verification require a new manifest. Legacy outputs never become authoring evidence or reduce fresh v1 scope.

## Verification

```bash
.venv/bin/python -m pytest
```

Use synthetic fixtures and fake providers; do not dispatch models or regenerate the corpus. Passing tests establish only the behavior they exercise, not v1 acceptance.
