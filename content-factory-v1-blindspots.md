# Content Factory v1 — blindspots and discovery probes

Review date: 2026-09-05. Historical code findings refer to baseline commit `39a04f2`; subsequent safeguards and adopted decisions are tracked in [the resolution](content-factory-v1-resolution.md). Reviewed [the goal](content-factory-v1-goal.md), both supporting maps, v0 source, local metadata, and selected transcripts. Findings distinguish omissions in the proposed v1 contract from observed v0 behavior. v1 is not implemented. Recommendations below do not change the goal or implementation.

**The main blindspot:** the factory can produce complete, traceable, rubric-approved artifacts without yet establishing that source evidence is sufficient, teaching is independently correct, or learners can perform the promised skill. Operational acceptance needs explicit connections to those three claims.

The goal already recognizes rights, cost caps, Arabic review, missing chunks, cache invalidation, and atomic release. The findings below identify decisions and failure cases that those requirements do not yet settle.

**Priority:** resolve source sufficiency and correction authority (C1, E1), migration and coverage semantics (C2–C3), and learner/quality evidence (E2–E5) before designing the pilot. Resolve C4–C7 before paid execution or publication; use C8 to bound expansion.

## Local evidence collected

Read-only inventory found 340 playlist rows and 8,269 `sync_github` rows representing 8,129 distinct video IDs. Playlist statuses are 316 `FINISHED`, 22 `FINISHED_2`, and 2 `SKIP`. Under `data/`, there are 8,250 `*_raw.json` files with 8,120 distinct filenames across 340 parent directories. These counts do **not** reconcile missing videos: repeated course memberships, skip flags, revisions, and snapshot currency still need matching. They establish that playlist count alone is an inadequate inventory model. Sources: local `youtube-iug.db` opened read-only without remote sync, and filesystem enumeration.

The same enumeration found 24,713 SRT files with several naming conventions, including `_raw`, `_postprocess`, `_flash`, and a named experimental model suffix. It found no `*_chapters.json` or `*_v2_content.json` under `data/`; those outputs might exist in other storage.

`src/etl/.transcript_processing_state.json` contains 32,644 completed item IDs and 145 failed items; the state files at the repository root and under `src/` contain zero of either. These are processing markers, not accepted lesson counts. No model calls, database synchronization, or pipeline jobs were run. Two v0 behaviors in C2 were reproduced by evaluating source functions/conditions in isolation.

## Evaluation findings

### E1. A faithful transcript can still teach a false or obsolete claim

**Already covered:** correctness, source ambiguity, approved supplements, and grounding back to original transcripts (goal lines 35–43).

**Omission:** no decision rule for an unambiguous but incorrect lecture statement, a statement correct only for an old software version, or a practice task requiring knowledge absent from the source. A paragraph can satisfy grounding while failing correctness. This is a contract inference, not a claim that the corpus contains such errors.

**Close it:** record source fidelity and subject correctness separately; give a named subject reviewer authority to approve a documented correction, supplement, historical framing, or quarantine. Include one deliberately wrong source statement and one version-sensitive example in the reference set. Evidence of citation alone must not make either pass.

### E2. “Separate held-out set” does not specify an independent holdout

**Already covered:** human-reviewed references, held-out evaluation, and thresholds fixed before release (goal line 48).

**Omission:** paragraphs, paraphrases, and quiz variants from the same lecture could land in both rubric/prompt development and the final evaluation. Repeated model/prompt selection against the same holdout also turns it into development data. A single pilot cannot establish generalization across unrelated subjects or instructors.

**Close it:** persist a split manifest; keep near-duplicate examples and their source lecture together; reserve unseen courses/instructors when claiming wider generalization. Use development cases for iteration and fresh held-out cases for the release decision after tuning. Report which subject/language/source conditions remain unevaluated. This applies the grouped-evaluation principle: dependent samples require groups absent from the paired training/development fold. [scikit-learn grouped cross-validation documentation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

### E3. Escalating uncertainty misses confident shared errors

**Already covered:** separate authoring/evaluation and escalation of uncertain or disputed cases; pilot human review (goal line 49).

**Omission:** role separation does not guarantee error independence, and the author and judge may agree confidently on a plausible wrong answer. The cited judge study demonstrates answer-induced reasoning errors even when a judge can solve the problem separately; its limited experiments also leave errors after supplying a reference. The paper does **not** establish error rates for this Arabic pipeline, and explicitly says its evidence cannot conclusively establish self-enhancement bias. [Zheng et al., sections 3.3–3.4](https://arxiv.org/html/2306.05685v4#S3.SS3).

**Close it:** human-audit a bounded sample of confident accepted items, including repaired items; have reference reviewers decide independently before seeing model verdicts. Use independently checked reference solutions and execution where applicable. Seed plausible wrong answers with correct-looking citations and persuasive explanations. Budget discovery audits separately from disagreement escalation. Different model names alone are not acceptance evidence; routine multi-model councils are unnecessary.

### E4. False accepts need denominators, sample uncertainty, and a release unit

**Already covered:** measure false accepts/rejects and judge every released paragraph/question (goal lines 47–48, 72).

**Omission:** “false accepts” could mean bad cases accepted divided by all bad cases, or bad cases divided by all accepted cases. Those answer different questions. Artificially balanced good/bad references do not establish production contamination. Paragraph counts also do not establish how often an entire lesson contains a critical error.

**Close it:** name both denominators; report counts, severity, subject/language strata, and lesson-level critical-defect results. Keep adversarial challenge-set performance separate from representative audit estimates. Use confidence intervals, accounting for clustering by source rather than treating neighboring paragraphs as independent.

**Illustration, not a required sample target:** with zero misses in 100 independent known-bad cases, the exact one-sided 95% upper bound on the miss rate is `1 - 0.05^(1/100) ≈ 2.95%`. Even zero misses requires 299 independent cases for that bound to fall below 1%. These are calculations from the binomial model; correlated or unrepresentative cases do not justify those bounds for deployment. NIST explains why normal approximations may be inaccurate with few failures/small samples and supplies exact binomial bounds. [NIST exact binomial confidence limits](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm).

As a separate illustration, if each of 100 released units independently had a 1% residual defect probability, the chance of at least one defect would be `1 - 0.99^100 ≈ 63.4%`. This uses a hypothetical residual defect rate, **not** a measured judge false-accept rate, and makes an independence assumption. It motivates direct lesson audits rather than converting paragraph scores into a course guarantee.

### E5. Reviewers can certify teaching artifacts without showing that learners acquire the skill

**Already covered:** prerequisites, worked examples, aligned practice, useful explanations, and human acceptance (goal lines 36–38, 47, 73).

**Omission:** no named learner population, baseline skill check, independent transfer task, or delayed check. “Aha contribution” and editorial acceptance are proxies; success on a nearby practice question may not show independent skill use.

**Close it:** for a small target-learner pilot, define prerequisites and an observable skill task; compare baseline with a fresh task completed without the worked solution; include a delayed variant where retention matters. Record comprehension failures and revise the rubric. Treat this as formative evidence; a small uncontrolled pilot cannot establish causal superiority over the original lecture. Alternatively, explicitly limit v1's claim to content acceptance and require learner validation before wider pedagogical claims.

The IES practice guide supports spacing, alternating worked examples with independent problem solving, and active retrieval for durable memory; it does not validate this proposed Arabic product or prescribe a universal pilot size/pass score. The learner-validation procedure above is this review's recommendation, not a quoted requirement from IES. [IES: Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/practiceguide/1).

## Content and execution findings

### C1. Complete subtitles can still omit essential teaching evidence

**Already covered:** source inventory, segment accounting, ambiguity, and diagrams.

**Observed signal:** a local lecture says “بيطلعلي مخطط هي شايفين كيف؟” at 13:37, referring to a diagram; another says “slide مش مبينة” at 53:16. Those subtitle spans do not supply the visual being discussed. [Diagram reference](PL9fwy3NUQKwa0n4HCNAxivyXFUhxLtL-l/Kzxd5D8ZgnQ_raw.srt#L677), [slide reference](PL9fwy3NUQKwa0n4HCNAxivyXFUhxLtL-l/l6u-C3bZa5w_raw.srt#L2505).

**Omission:** no source-sufficiency gate establishes which outcomes can be reconstructed from transcripts alone. Missing circuits, equations, demonstrations, or lab procedures can leave every available subtitle accounted for while the lesson remains impossible to ground. Generating a replacement diagram cannot establish what the original showed.

**Close it:** before lesson design, classify proposed outcomes as transcript-supported, requiring original media, requiring approved supplements, or unsupported. Preserve time-linked evidence and access status. Measure media-recovery and new-teaching costs before final judging discovers insufficient input.

### C2. The reusable v0 baseline includes another execution path and incompatible state

**Already covered:** the partial-success bug in `transform.py`, explicit v1 entrypoint, resumability, and reuse-first inventory.

**Observed:** [main.py](main.py#L45) leaves JSON-to-SRT conversion as a placeholder. The separate chapter extractor has behavior the goal's findings table does not discuss:

- It accepts only subtitles fully contained within a chapter. Evaluating its actual condition with a subtitle at 59–61 seconds and chapters at 0–60 and 60–120 seconds returns `False` for both. [Selector](src/etl/transcript_chapter_extractor.py#L621).
- A completed chapter returns raw input instead of loading its cleaned result. Calling that function with a completed-state stub reproduced the return of `RAW INPUT`. An interruption between chapter completion and video-output persistence can therefore substitute raw text on resume. [Resume branch](src/etl/transcript_chapter_extractor.py#L342).
- Output-file existence alone returns success, and the request loop has no attempt limit. [Existence check](src/etl/transcript_chapter_extractor.py#L568), [retry loop](src/etl/transcript_chapter_extractor.py#L358).

**Close it:** inventory every entrypoint, artifact family, and state location. Map video identity separately from playlist membership. Import old artifacts as candidates with reconstructible lineage; markers and file existence cannot confer approval. Demonstrate interruption recovery and cross-boundary segment migration before estimating trustworthy reuse. Unknown provenance can force revalidation or reconstruction even when prose looks good.

### C3. “Accounted for” and “complete release” need semantic definitions

**Already covered:** segment accounting, outcome alignment, quarantine, and complete versioned releases.

**Omission:** no rule defines intentionally excluded greetings, repeated explanations, or administrative asides. Counting segments also differs from teaching every promised outcome: paragraph approval cannot detect an absent topic. A quarantined prerequisite creates a decision about blocking the course versus changing its declared scope.

**Close it:** record explicit segment dispositions: included, duplicate, excluded-with-reason, unresolved. Separately require an outcome-to-explanation/example/practice matrix. Freeze promised outcomes and release membership before scoring; deleting a requirement cannot erase an omission. Define lesson versus course blockers and check prerequisite closure. Audit whole lessons for contradictions and terminology. Preserve the goal's allowance for necessary scaffolding rather than manufacturing an “aha” in every paragraph.

### C4. Budget reservations must survive ambiguous outcomes and reruns

**Already covered:** reservations, in-flight cost, retry bounds, uncertain-allowance stops, and recovery.

**Omission:** durability and ordering are unspecified. A request may finish at the provider before connection loss or a crash prevents response/usage persistence. Restart cannot infer that it was free. Limits stored only in a run can also reset on every invocation. A zero-call rerun of a fully accepted artifact proves neither property.

**Close it:** persist attempt IDs, reservations, and lifetime retry/repair counts before dispatch. Retain unknown-outcome states and uncertain reservations until reconciled. Verify the selected provider's request recovery/idempotency before promising no duplicate paid work. Share pilot caps across restarts and workers. Fault-inject around dispatch, response receipt, and artifact commit. Bound elapsed time and review backlog as well: a cash-capped pipeline can stall indefinitely.

### C5. Canonical Markdown does not yet define the interchange contract

**Already covered:** schemas, stable paragraph IDs, quiz/wiki format decisions, editable diagrams, and rendered acceptance.

**Omission:** Markdown alone leaves math, tables, code, quiz payloads, captions, glossary entries, and accessibility text outside a clearly enumerated verdict unit. Paragraph splits/merges affect identity and review provenance. If lessons, wikis, graphs, and simplified explanations independently restate a claim, the authoritative edit is unclear. The pilot preview and future platform can also interpret the same file differently.

**Close it:** define a small versioned Markdown dialect and parsed schema before bulk authoring. Enumerate teaching-bearing node types and their evidence/verdict requirements. Distinguish concepts, source spans, and editable paragraph IDs. Declare authoritative fields versus derived representations; invalidate derivatives after manual edits. Freeze the quiz/math/asset/link/accessibility contract shared by preview and platform without requiring the full framework decision.

### C6. Semantic graph dependencies may defeat local repairs

**Already covered:** typed edges, provenance, context-aware keys, and dependency invalidation.

**Omission:** no rule decides when Arabic/English terms denote the same concept, or identical terms denote different concepts across subjects. No boundary determines how far glossary, prerequisite, or outline changes must invalidate results. Passing individual edges does not establish a traversable prerequisite graph. Whole-course cache keys may invalidate too much; narrow keys may miss real dependencies.

**Close it:** define namespaced concept IDs, aliases, merge/split review, and edge-specific invariants. Distinguish the knowledge graph from the build-dependency graph. List dependencies by artifact type and escalation rules for broader reevaluation. Exercise a shared-term correction, paragraph move, concept merge, and prerequisite cycle; measure stale artifacts and reevaluation fan-out. For mutable model aliases, specify the selected provider's version/fingerprint and audit policy rather than assuming the identifier proves unchanged behavior.

### C7. Teaching content crosses execution and publication trust boundaries

**Already covered:** malformed output, correct answers, rendering, and executable-answer checks.

**Omission:** no explicit boundary separates source text from evaluator instructions, or teaching artifacts from executable build/runtime content. A transcript about prompt injection might quote instructions to the judge. A plausible generated answer is not permission to execute code with credentials, filesystem, or network access. These are design gaps, not demonstrated repository exploits. External-file instructions can influence model behavior; structured output alone does not settle this. [OWASP prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

**Close it:** keep sources in the data role, validate verdict membership/evidence independently, and test instruction-like source passages. Define allowed markup, URLs, paths, and components. Run executable examples in a disposable environment with explicit resource/access limits. If MDX is selected, account for its documented JavaScript execution model. [MDX security documentation](https://mdxjs.com/packages/mdx/#security). Add these cases to the existing release-failure suite.

### C8. A good pilot can conceal poor yield and unaffordable maintenance

**Already covered:** representative pilot, stratified forecasts, human minutes, lesson unit cost, updates, and rollback.

**Omission:** strong source coverage can hide difficult inputs. “Lesson” has no fixed size/skill scope, so splitting lessons can improve the cost denominator without improving teaching. Repeated accepted revisions can inflate yield unless maintenance is separate. Human minutes do not establish reviewer availability or publication delay. Rollback also assumes an old release remains valid: discovered teaching errors or withdrawn source permission can invalidate all available releases.

**Close it:** keep one main pilot plus a bounded challenge set spanning subjects, poor sources, dialect/code-switching, equations/code, and missing visuals. Report first-accepted distinct lessons, fixed outcome coverage, source hours, quarantined outcomes, reviewer throughput, and maintenance separately. Assign subject/editorial approval and unresolved-case ownership. Add withdrawal of affected content and derivatives when no safe release exists. Test restoration from an independent backup as well as local rollback. Bound v1 wiki/graph/diagram deliverables so optional tooling cannot silently determine whether a lesson ships.

## Discovery probes for unknown unknowns

Unknown unknowns are uncovered by testing across boundaries; this list is not exhaustive. This is a proposed small discovery set, with sizes and paid caps still to be agreed.

| Probe | Surprise it is designed to expose | Evidence to retain |
|---|---|---|
| Trace actual outcomes from original media through the exercise, including a diagram-heavy passage. | Essential evidence missing from transcripts; transcription errors treated as truth. | Gaps, recovered assets, correction decisions, time/cost. |
| Reconcile one video across two playlists and migrate an existing processed SRT. | Wrong context, duplicate spend, incomparable revisions, unrecoverable provenance. | Identity mapping and reuse dispositions. |
| Seed source errors, convincing wrong answers, and instruction-like text; independently review confident passes and repairs. | Shared author/judge errors, evidence laundering, injection, repair regressions. | Grouped holdout, verdicts, independent subject decisions. |
| Audit a complete lesson/prerequisite chain; have target learners perform a fresh task without the worked solution. | Missing topics, contradictions, answer leakage, difficulty mismatched to the learner. | Outcome matrix, observed failures, baseline and transfer results. |
| Interrupt around dispatch/accounting/checkpoints; resume, then run two workers against one cap. | Duplicate paid work, forgotten reservations, reset limits, lost outputs. | Durable ledger and artifact hashes before/after. |
| Change a shared concept, move a paragraph, and revoke an approved source. | Stale derivatives, excessive reevaluation, broken links, invalid rollback targets. | Expected versus actual affected artifacts, cost, withdrawal behavior. |
| Read the same quiz/math/diagram lesson on narrow mobile and with an Arabic screen reader; validate allowed markup. | Inaccessible teaching despite visual approval; format mismatch; executable markup. | Reproducible fixtures and interaction failures. |

These probes supplement existing gates. They do not certify the wider corpus, demonstrate a production exploit, or replace the numeric thresholds and spend caps already required by the goal.
