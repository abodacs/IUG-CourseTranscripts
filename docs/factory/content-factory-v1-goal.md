# Content Factory v1 — goal and acceptance contract

**Quick read:** What v1 must deliver, which decisions are fixed, and what blocks acceptance. Start here when scope is unclear.


Status: goal definition with blindspot resolutions adopted; v1 is not implemented or validated yet. Narrow legacy migration safeguards have been added and are tested separately.

**Operator budget update (2026-09-07):** artifact hosting/operations may cost at most **$5/month total**, confirmed by the operator. Model work should start on authorized free/provider-included quota; paid model APIs require a separate explicit cash cap. The proposed free baseline, fixed-quota archive and reviewer/publication boundary are in [artifact-storage-review.md](../platform/artifact-storage-review.md); no paid service is provisioned or hard-cap guarantee inferred from usage alerts.

**Operator execution update (2026-09-07):** zIDE and ZCode desktop are both approved execution environments. Live model access should use a provider-agnostic adapter with an OpenAI-compatible API shape, starting with authorized Gemini free-tier quota and allowing other explicitly approved compatible providers. “OpenAI-compatible” describes the interface; it does not itself authorize paid OpenAI service or any other paid API. Every account, project, and key must be operator-authorized and used within the provider's terms and assigned limits; do not rotate keys to evade enforcement. For free model access, work may continue until every configured, authorized free quota is confirmed exhausted; then dispatch stops. An uncertain quota is unavailable, not permission to continue.

Inputs: [platform-map-brief.md](../platform/platform-map-brief.md), [skills-map.md](../research/skills-map.md), and the existing Python pipeline. The current implementation is **Content Factory v0**. The immediate target is **Content Factory v1**, supplying the broader courses platform described in the brief.

## Goal

Build Content Factory v1 from v0: a resumable, measurable pipeline that turns existing course transcripts into publishable, skill-based Arabic-first Markdown lessons, with Apple-grade quality control from ingestion through publication and a bounded cost per accepted lesson. Reprocess the selected course from its transcripts to build new v1 teaching artifacts. Preserve legacy files for inventory and audit; old generated chapters, lessons, and completion flags do not replace this processing. Cache verified results from the new v1 workflow for subsequent reruns. Cost optimization must preserve the same release quality bar.

“Apple-grade” means complete, correct, useful, carefully edited, accessible, and dependable. It is a project acceptance standard, demonstrated through tests, calibrated evaluations, and human review; an LLM score alone cannot certify it.

## Allowed teaching sources — user-confirmed

1. **Transcripts are the teaching source.** Rebuild course structure, lessons, explanations, practice, quizzes, wiki, and graph from the course transcripts — the raw whisper JSON plus, per video, its cleaned counterparts in the mirrored `GeminiLongContext/<playlist_id>/` tree (`_chapters.json`, `_v2_content.json` with its earlier `_content.json` variant, and `_lecture_context.json`). Raw transcript revisions remain canonical for segmentation, timestamps, and evidence spans; where a cleaned counterpart and the raw JSON disagree, the raw JSON wins. Cite cleaned material by video ID and file.
2. **Use the matching YouTube lecture only when a needed diagram is missing or unclear in the transcript.** Recover the relevant diagram, slide, or board drawing from that video; record the video ID, timestamp/range, captured evidence, and the lesson need. Redraw it for clarity without inventing labels, relationships, or values. Whole-video analysis is not the default.
3. **Do not add outside teaching sources.** Websites, textbooks, papers, separate slide decks, unrelated videos, and model memory cannot supply missing course facts. Metadata may identify/order lectures or provide keyframe capture hints, including hints from legacy chapter JSON; a hint is not proof of what the frame shows; engineering and pedagogy references may guide the tooling/rubric, but they do not become course subject content.
4. **Transform and derive within the evidence.** Clearer wording, reorganized lessons, new practice questions, and illustrative diagrams are allowed when their concepts, methods, and answers are supported by transcript spans or the permitted video visuals. Record reasoning for derived examples; do not expand the curriculum with unsupported concepts.
5. **Keep unresolved gaps visible.** If allowed sources cannot establish an essential fact, diagram, prerequisite, or correction, flag the affected material and block its release. A reviewer can identify an error but cannot authorize outside material under this policy. Preserve original assertions; require allowed evidence for a correction.

This policy supersedes earlier supplemental-source and legacy-lesson-reuse recommendations. It applies to the pilot and later corpus expansion; reprocessing starts with the selected pilot and expands in measured batches.

**Reversal recorded 2026-09-07 (user-confirmed):** the earlier raw-only rule — never use anything but raw whisper JSON as teaching evidence; SRT variants, chapter hints, and v2 lessons are audit-only — is withdrawn for the cleaned `GeminiLongContext/` counterparts. Chapter hints, v2 content, and lecture context are now allowed teaching sources bound per video; raw whisper JSON stays canonical for segmentation and timestamps. Derived SRT variants remain excluded: the CF-01 damage measurements (zero-duration cues, malformed blocks, truncation) still stand. The YouTube-diagram and no-external-sources rules are unchanged.

## Findings from reviewing both maps and v0

| Finding | Required v1 resolution |
|---|---|
| The brief requires every paragraph to be judged; the skills map proposes sampling reused content. | Every released paragraph and question needs a valid passing verdict, whether reused or generated. Sampling is for additional deep audits and preflight estimation. |
| Both maps understate costs; prompt skills are described as having zero runtime cost. | Separate software license fees, model usage, local compute, storage, hosting, and human review. Track the full cost of producing accepted content. |
| The skills map counts only graphify image ingestion as model usage. | Budget semantic extraction from lesson Markdown too. Graphify's upstream README states that docs and media use a model; local code AST parsing is the deterministic path. [Source](https://github.com/Graphify-Labs/graphify#readme). |
| The skills map recommends copying material it identifies as unlicensed. | Verify reuse permission at the chosen revision, obtain permission, or write an independent alternative. Attribution does not supply a missing license. [Source](https://choosealicense.com/no-permission/). |
| Content-hash-only verdict caching ignores changed evidence and evaluation rules. | Version all verdict dependencies and invalidate affected downstream outputs. |
| The selected-passage ELI5 feature implies live model usage. | Prefer precomputed, reviewed explanations for v1. Live generation requires a separately bounded service and quality design. |
| v0 saves successful chunks and reports success even when another chunk fails. | A partial result is resumable work, never a complete or releasable artifact. See [transform.py](../../src/etl/transform.py#L51) and the existing [partial-success test](../../tests/unit/test_etl_transform.py#L337). |
| v0's model wrapper logs text but has no explicit spend ledger or verdict cache; exceptions inside its try block become `None`. | Introduce structured outcomes, usage accounting, bounded retries, and explicit failure states. The current retry decorator is not evidence that swallowed API errors are retried. See [gemini.py](../../src/ai/gemini.py#L23). |

This is a focused consistency, cost, and v0-readiness review. Candidate popularity, all upstream licenses, pedagogy references, and corpus readiness still require verification during the relevant implementation tickets. The local source/output inventory is now documented in [content-factory-v1-inventory.md](content-factory-v1-inventory.md); its metadata counts are not accepted course counts.

## Binding decisions from the blindspot review

[content-factory-v1-resolution.md](content-factory-v1-resolution.md) defines the source/correction policy, independent evaluation protocol, curriculum coverage, Markdown interchange contract, dependency boundaries, durable spending states, and withdrawal behavior. Its technical decisions supplement this acceptance contract; named approvals, a configured authorized-free-quota pool with a deterministic exhaustion stop, learner evidence, and implementation proofs remain required. [The blindspot review](content-factory-v1-blindspots.md) is the historical rationale, not current proof of implementation.

## Quality control across the whole pipeline

Every stage emits an artifact, provenance, status, and validation evidence. Missing evidence, incomplete processing, malformed judge output, or a failed hard requirement blocks release. Scores cannot average away a critical defect.

| Stage | Required controls | Release-blocking examples |
|---|---|---|
| Inventory and ingestion | Stable course/video IDs; immutable raw sources; hashes; source metadata and rights status; expected-file and segment inventory; deduplication. | Missing source, corrupted input, wrong course association, unresolved publishing rights. |
| Transcript normalization | Account for every source segment; preserve order and timestamps; validate Arabic encoding, equations, and mixed-direction text; record corrections and uncertain transcription. | Silently dropped chunk, reordered explanation, unsupported correction, unresolved source ambiguity that affects correctness. |
| Course design | Prerequisites, tangible skill outcomes, lesson sequence, worked examples, and practice aligned with each outcome. Research and version the course rubric. | Explanation-only lesson, missing prerequisite, exercises unrelated to the promised skill. |
| Lesson authoring | Canonical Markdown; stable paragraph IDs; trace claims to original source spans; Arabic editorial review; clear explanations and identifiable aha passages. | Unsupported claim, incorrect example, misleading simplification, filler, or broken Markdown. |
| Assessment | Validate every answer and rationale; judge placement, challenge, engagement, ambiguity, and skill alignment; check executable answers where applicable. | Incorrect key, multiple unintended answers, unavailable prerequisite, question that merely echoes nearby wording. |
| Diagrams, wiki, and graph | Editable Excalidraw sources plus exports; visual/text agreement; accessible alternatives; valid links and typed edges with provenance; course/lesson wiki coverage. Evaluate OKF representation. | Misleading diagram, unreadable Arabic label, missing asset, invented relationship, or broken reference. |
| Rendering and publication | Arabic/English and mobile/desktop checks; Thmanyah glyph coverage; keyboard use, focus, contrast, reduced motion; working quizzes; publish only a complete versioned artifact set. | Clipped RTL content, broken interaction, inaccessible teaching content, stale/mixed artifacts, or missing verdicts. |
| Operations and updates | Checkpoints; bounded timeouts/retries; dependency-aware invalidation; budget enforcement; failure reports; atomic promotion; rollback to an accepted version. | A failed job reports success, rerun repeats accepted model work, budget is exceeded by newly scheduled work, or an update silently publishes stale content. |

Grounding must trace back to transcript spans — raw whisper JSON or the video's cleaned `GeminiLongContext/` counterparts — and, only for needed diagrams, time-linked visual evidence from the matching YouTube lecture. Check evidence sufficiency per promised outcome before authoring. Source fidelity and subject correctness require separate verdicts; record source errors and corrections supported by the allowed sources without rewriting immutable evidence. External supplements and derived SRT variants are excluded as teaching evidence. Segment dispositions and an outcome-to-explanation/example/practice matrix must both be complete; paragraph approval cannot certify missing curriculum.

## Evaluation and release contract

1. Research and version `COURSE_RUBRIC.md`, with explicit hard failures and calibrated thresholds. Judge every paragraph for grounding and aha contribution, every quiz for the brief's assessment criteria, and every lesson for demonstrated skill practice. Evaluate paragraphs in lesson context so necessary scaffolding is assessed fairly.
2. Build a human-reviewed Arabic-first reference set containing good content and known failures, plus English and mixed-direction cases. Use a separate held-out set grouped by original video/near-duplicate family across all course memberships to measure false accepts, false rejects, and disagreements. Keep candidate selection on development data; retire holdouts exposed during tuning. Set acceptance thresholds before the release evaluation.
3. Keep authoring and evaluation separate. Route uncertain or disputed cases to deeper evaluation or human review; quarantine unresolved cases. A named subject reviewer and Arabic editorial/visual reviewers inspect every complete pilot lesson; reference decisions precede exposure to judge scores. Audit confident accepted and repaired items as well as disagreements during expansion.
4. Run deterministic validation and cached-verdict validation in ordinary tests. Run missing or invalidated LLM evaluations as a budgeted release job. An offline test pass alone never grants release when required verdicts are missing.
5. Define target learners, prerequisites, baseline and independent transfer tasks, and a delayed task where retention is claimed. Complete a formative learner trial; report its limitations and resolve observed critical teaching failures.
6. Report quality counts with explicit denominators, severity, source-group uncertainty, and whole-lesson critical defects. Seeded challenge results do not estimate production contamination. Require zero unresolved critical defects and correct blocking of all critical challenge cases, with model-score cutoffs calibrated before the final holdout.
7. Enumerate all teaching-bearing nodes, including math, code, tables, quiz choices/keys/rationales, diagrams and accessible alternatives, wiki entries, and simplified explanations. Every released node requires applicable evidence and verdicts.
8. Record per artifact: source/content hashes, rubric and prompt versions, model identifier/settings, code/schema version, verdicts with evidence, usage, cost, and reviewer disposition. Quiz placement and graph dependencies must be included in the relevant cache key.

## Cost controls

Use the existing Python/uv pipeline and local files/SQLite where suitable. Install only skills needed for the current stage; establish Arabic quality and dependency/license fit before adoption. Multi-model councils and repeated whole-corpus analysis are not default steps.

- **Reprocess once, then resume:** inventory transcripts before model calls and build fresh v1 teaching artifacts for the selected scope. Legacy output presence never skips this first pass. On later runs, reuse valid v1 checkpoints and verdicts; process only missing, failed, or invalidated units. Repairing a unit triggers validation of that unit and its affected dependants.
- **Efficient judging:** deterministic checks first, then a calibrated inexpensive judge with complete coverage. Batch within context limits using stable IDs and explicit per-item verdicts; missing IDs fail validation. Reserve premium usage for generation, escalations, and bounded deep audits.
- **Correct caching:** key on content, source evidence, relevant lesson context, rubric, prompt, model/settings, and schema/tool versions. Identical accepted reruns make zero generation or judging calls unless an explicitly scheduled audit is due.
- **Bounded work:** proposed default is at most two retries for transient failures, one targeted repair cycle, and one premium escalation per failed unit. Every attempt shares the same durable pilot budget and unit lineage limits across restarts and workers. Exhaustion quarantines the unit; it never relaxes the rubric.
- **Budget currency:** v1 model work runs at zero incremental cash unless a later paid-model cap is explicitly approved. Model work may run in zIDE or ZCode through the provider-agnostic adapter, initially against authorized Gemini free-tier quota and later against other explicitly approved compatible providers. The recorded 300,000,000-token Z.ai quota is one historical/available allowance, not the sole provider budget. The binding free-tier ceiling is the sum of legitimately authorized provider quotas, not a separately invented token number. Artifact hosting/operations has the separate operator-confirmed ceiling of $5/month; introducing any other paid path requires a new cap decision first.
- **Spend enforcement:** configure an explicit allowlist of authorized providers, accounts/projects, and key aliases before dispatch. Track tokens where providers expose them and requests/output where they do not. Apply per-request output, concurrency, timeout, retry, and repair limits across every key. Persist provider, account/project alias, key alias (never the secret), quota state, and attempt identity transactionally before dispatch. A confirmed quota-exhaustion response disables that key until its recorded reset; fail over only to another configured authorized quota. Retain unknown outcomes after timeouts/crashes until reconciled; do not infer zero use or automatically replay ambiguous requests. Stop the run when all authorized free quotas are exhausted or any remaining quota state is uncertain.
- **Full accounting:** count generation, judging, graph/wiki extraction, retries, and discarded outputs across every provider and key. Track provider/model identity, requests, input/output tokens when observable, rate/quota exhaustion, and unknown usage. Track human review time and local compute/storage separately. If a paid tool or API is ever introduced, track its cash charges and provider caching fees separately.
- **Static delivery:** precompute approved content and deterministic SVG/HTML assets, deployed to Cloudflare Pages (atomic promotion, preview validation, rollback) within its published limits rather than assuming unlimited free service. [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/).

Report total model usage across all providers/keys and **LLM cost per accepted lesson = all attributable LLM usage or cash spend, including failed attempts and shared overhead, divided by accepted lessons**. Separate free-quota usage from paid cash and report hosting/operations against the $5/month ceiling. If no lessons pass, report no accepted yield rather than zero unit cost. Count first-accepted distinct lesson IDs against a frozen outcome/lesson scope; report accepted outcome coverage and maintenance separately so splitting lessons or accepting revisions cannot inflate yield. Also report reuse/cache hit rates, repair rate, judge disagreement, human minutes per lesson, review queue age/throughput, and actual source/lesson volumes.

Forecast the wider corpus from measured token volumes, subject/language strata, and observed repair rates, with low/base/high scenarios. Playlist count alone is not a cost estimate. No numerical affordability claim is justified until the pilot is measured against an agreed cap.

## v1 definition of done

- [ ] An agreed pilot course is reprocessed from transcripts, with matching YouTube visuals only where needed for diagrams, to complete Markdown lessons, inline assessments, editable diagrams, and course/lesson wiki and graph artifacts, with a working rendered preview.
- [ ] Every pilot source segment is accounted for; every released paragraph and quiz has a valid passing verdict; all required artifact and provenance fields exist.
- [ ] Course structure, teaching quality, Arabic prose, and rendered usability pass the calibrated rubric and pilot human review. There are no unresolved critical defects.
- [ ] Failure tests demonstrate that missing chunks, bad JSON, incorrect quiz keys, unsupported claims, broken assets, unavailable models, interrupted jobs, and exhausted budgets block promotion without destroying accepted work.
- [ ] A repeated unchanged run makes zero generation/judging calls; a source, rubric, or model change invalidates the appropriate results. Restart resumes safely from checkpoints.
- [ ] A release contains one consistent set of approved artifacts; an intentionally failed update leaves the last accepted release usable; rollback is demonstrated.
- [ ] A solid Cloudflare Pages deployment is demonstrated: one complete versioned artifact set promoted atomically with preview validation before promotion, and rollback to the last accepted release shown after an intentional failure.
- [ ] The pilot stays within the approved cross-provider model allowance, uses no paid model API without an explicit cash cap, stays within the separate $5/month hosting/operations ceiling, and reports full unit economics (usage and any cash per accepted lesson, reuse/cache hit rates) and measured quality. Reprocessing expands to the remaining corpus in measured batches after the pilot.
- [ ] Source sufficiency, corrections, exclusions, and the frozen curriculum outcome matrix are reviewed; no required outcome or prerequisite disappears to improve acceptance yield.
- [ ] Source-grouped holdouts, independent subject review, complete teaching-node coverage, and a formative learner trial demonstrate the stated pilot quality with explicit limits.
- [ ] Crash-boundary and concurrent-worker tests prove durable budget reservations, unknown-outcome handling, and lifetime retry limits using a fake provider before any live model execution.
- [ ] Shared-concept/context changes invalidate the expected artifact closure; forbidden content execution fails safely; withdrawal excludes invalid rollback targets; independent-backup restore is demonstrated.
- [ ] The two maps, v1 operating instructions, dependency/license inventory, and reproducible validation commands describe the implemented behavior.

## Delivery sequence

1. Reconcile all v0 source/output/state roots and duplicate memberships; choose pilot and challenge set; check source sufficiency; name reviewers/learners; freeze scope, schemas, rubric, grouped reference splits, and the authorized provider/key pool with its exhaustion/reset rules.
2. Build reliable execution: manifests, checkpoints, structured failures, cache, usage ledger, budget stop.
3. Add lesson/quiz/visual/wiki/graph stages and calibrated quality gates; produce the pilot.
4. Validate content, rendered experience, failure recovery, and costs; release v1; estimate wider rollout.

The broader platform UI, stack-comparison blog, and whole-corpus launch remain in the platform map. This goal supplies their accepted content and includes enough rendering to validate it.

## Decisions

Resolved for v1:

- **Pilot course:** `OPTO 2311 — البصريات الهندسية` (playlist `PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-`, كلية العلوم الصحية), 105 post-processed transcripts with `FINISHED_2` status in `youtube-iug.db`. Local inspection also found 106 recorded video IDs, one skipped source without raw files, 105 chapter files, 83 v2 outputs, and a truncated playlist `entries` field. Confirm segment accounting, source order, and the skipped-source disposition during the inventory ticket and include a small English/mixed-direction validation set. Runner-up if it proves unrepresentative: `جبر حديث 1` (59 transcripts, `PL9fwy3NUQKwZKOpj354PRgwYPWWgxchnI`).
- **Budget:** no paid model/API work without a separately approved cash cap. Model work may run in zIDE or ZCode through an OpenAI-compatible provider adapter, beginning with authorized Gemini free-tier quota and allowing other explicitly approved compatible providers. The recorded 300,000,000-token Z.ai allowance is one possible quota source. Free model work may continue across the configured authorized pool until every quota is confirmed exhausted; provider-aware accounting and deterministic stop/reset handling remain required. Artifact hosting/operations has a separate $5/month ceiling.
- **Reprocess from transcripts:** confirmed by the user. The repo holds 339 normally named playlist folders plus a 34-video folder missing its leading `P`, with raw and post-processed SRTs, prior model outputs under `GeminiLongContext/`, and playlist metadata in `youtube-iug.db`. Inventory all of them; use raw whisper JSON plus the matching cleaned `GeminiLongContext/` counterparts as the teaching inputs, and recover needed diagrams only from matching YouTube lectures. Other prior generated outputs remain audit artifacts. No legacy artifact skips fresh v1 processing; reuse applies only to valid checkpoints from the new v1 workflow.
- **v1 location:** this repository, reusing v0 assets and tests, with versioned outputs and an explicit v1 entrypoint.
- **Hosting and deployment:** Cloudflare Pages. "Solid" means atomic promotion of one complete versioned artifact set, preview validation before promotion, and demonstrated rollback to the last accepted release, within published Pages limits.

Still unresolved before the relevant work:

- Who supplies independent subject review, Arabic editorial/visual review, and target learners for the formative trial? Confirm learner prerequisites and the task-performance criterion; calibrate model-score cutoffs before opening the holdout.
- Resolve source/font/dependency publishing rights and the quiz/wiki formats before the relevant release work. The stack comparison remains platform-map scope; Cloudflare Pages is the chosen hosting target.
