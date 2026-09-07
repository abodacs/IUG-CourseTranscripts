# COURSE_RUBRIC — OPTO 2311 v1 (CF-06)

**Version:** 1.0-draft (2026-09-06). Threshold fields are **OPEN until calibrated** on development data (CF-07/CF-06 calibration); they are never tuned after a holdout opens. This rubric binds every judge verdict, human review, and promotion decision for the v1 pilot.

## Foundations (why the checks look for what they look for)

- **Bloom's taxonomy:** every promised outcome names a cognitive level; quizzes and transfer tasks must test at or above the outcome's level, not just recall of wording.
- **Backward design:** outcomes come from the frozen scope; lessons and assessments derive from outcomes — any content that serves no recorded outcome is editorial drift, not bonus.
- **Cognitive load:** one concept move at a time; worked examples before independent practice; no decorative complexity in derivations.
- **Retrieval practice:** practice and quizzes ask the learner to produce or choose, not to re-read; feedback explains, never teases.
- **Worked examples:** each worked step cites its evidence span; a step that cannot be traced to the source (or to declared mathematics from taught steps) is unsupported.

## The four checks (every teaching-bearing unit is judged on all four)

1. **Evidence support** — the unit's claims trace to transcript spans (or captured-diagram revisions) recorded in provenance; numbers, signs, and conventions come from the course's own sources, never model memory.
2. **Subject correctness** — equations, units, ray directions, sign conventions, labels, and quiz keys are right per optics and per this course's own conventions; independent subject review owns this check (competence verified per domain, F13).
3. **Editorial/pedagogical contribution** — Arabic prose is clear and correctly directed; the unit teaches (definition → example → practice arc), simplifications do not distort, and the unit serves a recorded outcome.
4. **Cross-lesson coherence** — terms, notation, and sign conventions agree with the rest of the course; prerequisite links point to material actually taught earlier; no lesson contradicts another.

## Hard failures (any one blocks promotion of the affected artifact)

| # | Class | Example signal |
|---|---|---|
| H1 | Wrong assertion | a stated fact contradicts the source evidence |
| H2 | Outdated/incorrect version | a formula or convention stated against the course's own later correction |
| H3 | Transcription ambiguity asserted as fact | an ASR-ambiguous span presented without uncertainty or correction record |
| H4 | Absent visual treated as present | describing a diagram that was never captured/approved |
| H5 | Contamination | content derived from outside sources, exposed holdout families, or unmatched/unbound legacy outputs; matched cleaned counterparts are allowed only through their canonical raw-source binding |
| H6 | Wrong quiz key | the recorded answer index does not match the defensibly correct choice |
| H7 | Persuasive wrong solution | a fluent, confident derivation that reaches a wrong result |
| H8 | Missing prerequisite taught past | the unit builds on an outcome never taught (or taught later) |
| H9 | Cross-lesson contradiction | notation/claim conflicting with another lesson |
| H10 | Harmful simplification | a simplification that creates a lasting misconception |
| H11 | Invalid repair | a post-release fix applied without evidence, review, or invalidation of dependents |
| H12 | Instruction-like text in source | transcript/prompt-injection text treated as course content |

## Teaching-bearing nodes (each is judged; none is exempt)

Prose paragraphs; math spans; code blocks; tables; quiz choices, keys, and rationales; diagrams **and their accessible alternatives**; wiki entries; simplified explanations.

## Judge plan

- **Calibrated inexpensive judge** produces coverage verdicts: batched, stable per-unit IDs ([judging.py](../../src/factory/judging.py)), whole-lesson context in every call, and a strict output contract — a missing ID, unknown ID, malformed payload, or invalid verdict fails the whole batch.
- **Premium model** is reserved for generation, bounded escalations, and deep audits — never for routine coverage verdicts.
- **Implementation boundary:** the harness supports only the local scripted `FakeJudge`. Live judging still needs an observed OpenAI-compatible provider adapter, authorized provider/key configuration, durable reservations, output persistence, failover controls, and aggregate usage reconciliation; recording an allocation alone cannot enable it.
- **Verdict cache keys** include content hash, evidence refs, lesson context, rubric version, prompt version, schema version, and model — identical accepted reruns make zero calls.
- **Human reference sets:** Arabic-first good + the 12 hard-failure classes + English + mixed-direction cases, prepared locally with source context and labeled by humans **before** any judge score (F13). The worksheet supplies blank slots; intended construction classes are not ground truth. Compare judge verdicts with independent human labels.

## Threshold fields — OPEN until calibration

| Threshold | Value | Filled at |
|---|---|---|
| `min_node_pass_ratio_per_lesson` | **OPEN** | calibration on dev lessons (CF-07) |
| `max_judge_human_disagreement_rate` | **OPEN** | reference-set calibration (CF-06) |
| `quiz_key_agreement_required` | **OPEN** (expected: 1.0 — H6 is a hard failure) | calibration |
| `min_evidence_coverage_ratio` | **OPEN** | calibration |
| `escalation_trigger_disagreement` | **OPEN** | calibration |
| `holdout_false_accept_tolerance` | **OPEN** | frozen before CF-09 opens the holdout |

Calibration records thresholds, judge disagreement, and the derivation in the calibration report; post-hoc tuning retires the holdout (plan §11).
