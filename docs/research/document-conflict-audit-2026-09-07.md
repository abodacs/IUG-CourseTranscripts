# Documentation conflict audit — 2026-09-07

This audit records a consistency pass across `docs/`. It is documentation evidence only: it does not prove the factory is implemented, the pilot is accepted, or any release gate has passed.

## Authority used

The audit followed [the documented precedence](../README.md#which-document-wins): the [goal](../factory/content-factory-v1-goal.md) owns v1 scope and fixed decisions; the [resolution](../factory/content-factory-v1-resolution.md) supplies implementation rules; the [pilot packet](../pilot/opto-2311/content-factory-v1-pilot.md) applies them; [NEXT_STEPS](../NEXT_STEPS.md) owns current execution order. Inventory and blindspot material remain dated or historical evidence.

## Conflicts reconciled

- **Teaching sources:** current docs consistently allow raw whisper JSON plus each video's matched cleaned `GeminiLongContext/` counterparts, while raw remains canonical for segmentation, timestamps, and exact evidence spans. Unmatched/unbound legacy outputs, derived SRTs, and outside course material remain excluded. Cleaned counterparts are neither accepted v1 output nor permission to skip fresh processing. See [goal source policy](../factory/content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed), [resolution source contract](../factory/content-factory-v1-resolution.md#source-and-curriculum-contract), [rubric hard failures](../factory/COURSE_RUBRIC.md#hard-failures-any-one-blocks-promotion-of-the-affected-artifact), and the [outcome-matrix prompt](../factory/outcome-matrix-pass.md#the-prompt-paste-as-the-session-goal).
- **Model execution update:** zIDE and ZCode are approved execution environments. The target is a provider-agnostic OpenAI-compatible adapter, beginning with authorized Gemini free-tier quota and allowing other explicitly approved compatible providers. OpenAI-compatible is an interface choice, not paid-service authorization. Paid model use still needs a cash cap; artifact hosting and operations retain their separate **$5/month total** ceiling. See the [goal execution/budget updates](../factory/content-factory-v1-goal.md#cost-controls), [documentation authority summary](../README.md#which-document-wins), and [current quota milestone](../NEXT_STEPS.md#2-prove-quota-accounting-through-the-actual-zidezcode-provider-workflow).
- **Counts and coverage:** the pilot is consistently described as 106 recorded IDs, 105 available raw source sets, 105 chapter files, 83 v2 outputs, one absent skipped source, and 22 available-source videos without v2 output. All 105 available sets require fresh scope accounting; administrative notices cannot disappear without an explicit disposition. See [known counts](../README.md#already-known), [recomputed source-review counts](../pilot/opto-2311/opto-2311-source-review.md#counts-recomputed-not-assumed), and the [scope-freeze evidence](../pilot/opto-2311/opto-2311-scope-freeze.md#what-is-already-verified-recorded-evidence).
- **Order:** live playlist reconciliation establishes 106 positions, while transcript lecture-number mentions remain review hints rather than identity/order proof. The missing position-8 source and positions 105–106 still need their documented curriculum dispositions. See [first-review order evidence](../pilot/opto-2311/opto-2311-first-review.md#lecture-order--evidence-quality) and [current preparation step 3](../NEXT_STEPS.md#next-task-prepare-the-scope-review-evidence).
- **Status and current task:** CF-01 inventory is complete, but preparation helpers and passing tests do not complete downstream evidence gates. The current task is the full transcript-backed outcome matrix and reviewable reference packet; live runtime, calibrated gates, learner trial, and deployment remain unfinished. See [current status and task](../NEXT_STEPS.md#next-task-prepare-the-scope-review-evidence) and [documentation map](../README.md#start-here).
- **Dependencies and release order:** the production plan now makes CF-13 precede CF-12 final acceptance, distinguishes private preview from accepted release, and requires current evaluation, learner, rights, prerequisite-closure, review, and preview evidence before final promotion. See [pilot sequence and release gates](../pilot/opto-2311/pilot-opto-2311-plan.md#3-the-whole-pilot-on-one-page).

The historical [blindspot review](../factory/content-factory-v1-blindspots.md) and dated [inventory](../factory/content-factory-v1-inventory.md) were left intact. Their headers now direct readers to current authority; their older observations and superseded recommendations remain useful provenance, not live instructions.

## Verification performed

- Compared live wording across the documentation map, goal, resolution, next steps, factory guides, pilot packet, production plan, platform plans, and research notes.
- Searched for stale source-policy, budget, count, order, status, dependency, and current-task language after reconciliation.
- Ran `.venv/bin/python -m pytest`: **335 passed** on 2026-09-07. This verifies only behavior covered by those tests, not teaching quality or v1 acceptance.

## Later operator decisions recorded

1. **Free-quota stop:** model work may continue across configured, operator-authorized free quotas until every route is confirmed exhausted; uncertainty stops dispatch. Provider/key transitions and reset evidence remain logged. Paid model usage still requires a separate cash cap.
2. **Execution environment:** ZCode desktop counts as an approved zIDE-family environment.
3. **Public-before-final policy:** before full-course acceptance, publish only one non-teaching status page. Keep teaching, working notes, roadmap detail, release notes, and private evidence private. No standalone teaching module ships before the complete prerequisite-closed course is accepted.
