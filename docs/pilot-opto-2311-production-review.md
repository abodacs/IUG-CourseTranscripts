# OPTO 2311 — production-cycle blind spots and discovery plan

Review date: 2026-09-06. **The execution plan is a strong first-publication plan, but not yet a complete production operating plan.** Its largest gap is the closed loop from a real learner or source defect through impact analysis, withdrawal, repair, independent review, republication, and verified recovery.

This is a document review, not a runtime audit or proof that a vulnerability exists. Findings below compare the [pilot plan](pilot-opto-2311-plan.md) with all 12 other top-level Markdown documents in `docs/`. The existing screenshots and wireframes are design references, not tested product behavior; they were not visually audited here. Dated provider, tool, quota, and hosting observations have not been reverified. No model-production run or deployment was performed.

The [goal](content-factory-v1-goal.md) remains authoritative. Proposed changes below do not grant publishing permission, change the teaching-source policy, select new dependencies, or widen the pilot into the entire platform. The [historical blindspot review](content-factory-v1-blindspots.md) already identified many underlying risks; this review asks whether the newer tickets actually implement and prove their adopted resolutions.

Priority: **P0** closes a gap before dependent dispatch or public promotion; **P1** closes a gap before calling the pilot operationally production-ready; **P2** improves repeatability and expansion. Existing OPEN inputs are listed separately from newly identified omissions.

## Findings that block a dependable end-to-end cycle

### F01 — P0: release eligibility has contradictory definitions

**Evidence:** plan §3 makes CF-11 depend on course evaluation, without CF-10 learner acceptance. §10 permits public working notes after any three lessons are accepted. §16 says learner unavailability holds the release at engineering acceptance. [NEXT_STEPS milestone 4](NEXT_STEPS.md#4-complete-the-pilot-and-demonstrate-cloudflare-pages-release-recovery) also permits staged public lessons, while the [resolution lifecycle](content-factory-v1-resolution.md#pilot-economics-and-release-lifecycle) requires a complete prerequisite-closed course. This conflict spans documents; the plan did not create all of it.

**Failure:** three individually accepted lessons ship with an absent prerequisite, or final publication precedes learner evidence. A STATUS banner cannot supply missing release checks.

**Close — CF-03/09/10/11, operator and reviewers:** distinguish private engineering preview, any explicitly authorized public module, and final accepted course. Define each release's frozen membership and required evidence. Under the current authoritative contract, final course promotion requires CF-09, CF-10, current rights, prerequisite closure, and preview acceptance. If interim teaching publication is retained, reconcile it explicitly with the goal and require a reviewed standalone module scope; “3+ lessons” is not a release criterion. Use one machine-readable release predicate for manual and automated promotion.

**Proof:** missing learner evidence, a quarantined prerequisite, stale review, or pending rights blocks the appropriate promotion path. Public metadata must accurately describe incomplete scope.

### F02 — P0: the accounting boundary starts after some model work

**Evidence:** plan §17 names allocation enforcement before CF-07, but CF-06 calibration needs judges earlier. Appendix B calls agent-drafted skills and outcome matrices “No model calls.” The [quota contract](content-factory-v1-resolution.md#durable-spending-and-execution-contract) covers all v1 model work. The [context-cost report](context-management-mcp-token-cost.md#applied-2026-09-06-global-mcp-slimmed-target-hit) records 31,152 input tokens for one fresh empty-prompt session in a particular local setup.

**Failure:** the ledger caps explicit pipeline calls while agent drafting, rubric research, tool results, repairs, wiki extraction, and session overhead consume the same subscription outside that ledger. “Offline” does not mean an LLM-assisted task is token-free. The historical 31,152 measurement is a warning signal, not a zIDE billing conversion.

**Close — CF-04/06, operator:** define “no provider calls from the script” separately from “no model-assisted work.” Account for preparatory sessions and every nested model route. Establish the actual quota currency, cached/reasoning token treatment where applicable, external operator usage, observation lag, and quota-period rollover. Give CF-06 a real allocation before live calibration; all earlier model-assisted preparation needs its own accounted allowance. Unobservable usage stays an explicit limitation, with dispatch stopped where the required guarantee cannot be supported.

**Proof:** reconcile a bounded real workflow against observed subscription consumption, including agent overhead. Test quota rollover, external usage changes, and actual usage exceeding the reservation; block new work on unresolved overspend.

### F03 — P0: scope discovery can consume the supposedly sealed holdout

**Evidence:** plan §6 reserves pilot videos “not exposed during tuning,” then builds full-course outcomes; §10 processes every frozen lesson before CF-09 opens the holdout. The [pilot packet](content-factory-v1-pilot.md#bounded-challenge-cases) says reading or analyzing an excerpt makes its source family development data. The capture guide already documents inspection of `-AsaJEAav4s`.

**Failure:** a family is labeled unseen although its source, quiz answers, or defects already influenced planning or prompt changes. Full-course coverage and the current strict exposure rule can leave no eligible holdout. Merely adding a split JSON does not resolve this tension.

**Close — CF-02/03/06, evaluation owner:** reserve families before semantic discovery; record existing exposure, including capture inspections. Define who can access protected evidence for coverage/reference work without feeding candidate selection, or explicitly reconcile the exposure rule with the evaluation protocol. Freeze prompts, rubric, model/settings and thresholds before isolated holdout production/evaluation. Record access and exposure events. If sufficient independent families cannot be preserved, report that limitation and resolve the evaluation design before claiming a valid holdout.

**Proof:** an exposure log, transitive source-family membership checks, a frozen candidate fingerprint, and rejection of an exposed replacement holdout. Multi-source lessons and shared glossary content count when checking leakage.

### F04 — P0: normalization and correction handling have no complete implementation ticket

**Evidence:** CF-01 inventories and screens variants; CF-07 starts from an evidence packet. The [goal's normalization stage](content-factory-v1-goal.md#quality-control-across-the-whole-pipeline) and [resolution correction contract](content-factory-v1-resolution.md#source-and-curriculum-contract) require traceable normalization and append-only corrections. No ticket clearly owns that entire path.

**Failure:** equal segment counts conceal a lost negation or minus sign; postprocessed text silently becomes authoritative; a reviewer approves a correction without the required source-based derivation.

**Close — add CF-02A before scope approval and repeat per source:** explicitly choose raw-only authoring or implement a versioned normalization path. Preserve immutable raw spans; record aligned transformations, uncertain text, correction evidence, reviewer disposition, and downstream impact. Enforce eligible-input selection at the actual authoring boundary, including helper tools, not just in the manifest. Coverage validation must check references, not counts alone.

**Proof:** legacy prose is rejected as evidence; a same-length altered equation is flagged; an unsupported correction quarantines the affected outcome; included/excluded/duplicate dispositions cannot hide an uncovered skill.

### F05 — P0: three-lecture discovery does not specify full-course sufficiency work

**Evidence:** CF-02 inspects first/middle/final lectures; CF-03 jumps to a frozen full outcome matrix. [NEXT_STEPS](NEXT_STEPS.md#1-freeze-source-sufficiency-and-skill-outcomes) explicitly warns that three lectures cannot accept the course. The skipped lecture's contents cannot be established from its missing transcript.

**Failure:** the matrix includes only outcomes discovered in easy samples, missing a required topic or prerequisite from the other sources. An unknown source is incorrectly declared irrelevant.

**Close — CF-03, agent prepares and subject reviewer decides:** add full-source outcome discovery and sufficiency accounting for all 105 available sets, with review effort and evidence per outcome. Resolve the 106th record's effect from allowed evidence or retain an explicit completeness limitation/blocker; do not invent its topic. Distinguish verified historical lecture order from reviewed teaching order. Unknown historical position alone need not imply a missing prerequisite, but the plan must explain how sequencing is approved when positions remain unknown.

**Proof:** every available source contributes to the coverage/disposition audit, including sources outside the three examples; no required outcome disappears through selection. Coordinate this work with F03's protected-family access rules.

### F06 — P0: valid cache keys do not implement dependency invalidation

**Evidence:** CF-05/06 list cache-key inputs; the [resolution invalidation table](content-factory-v1-resolution.md#format-identity-and-dependency-boundaries) requires shared-term, source, paragraph-placement, prerequisite, and concept-merge propagation. The plan's §18 assigns this proof without a corresponding complete ticket.

**Failure:** the edited lesson is rejudged while a wiki definition, simplified explanation, assessment, or another lesson remains stale. Approval records survive a content edit because only model verdicts were invalidated.

**Close — CF-05/07:** implement a build-dependency graph distinct from the semantic graph, typed change events, transitive invalidation, and approval records bound to exact artifact/release revisions. Source corrections, review changes, rubric/model changes, and rendering-only changes need explicit rules. Reject undeclared dependencies and references to absent nodes.

**Proof:** change a shared sign convention, move a paragraph, split a concept, and replace a diagram. Compare expected and actual invalidation closure, including human reviews and rendered checks. Unchanged unaffected artifacts retain valid cached work.

### F07 — P0: request states are specified; artifact and release states are not

**Evidence:** CF-04 defines provider-attempt transitions; CF-08 allows parallel production after ledger concurrency tests. The [resolution](content-factory-v1-resolution.md#durable-spending-and-execution-contract) explicitly separates request success, valid output, acceptance, and publication. The [capture guide](KEYFRAME_CAPTURE.md#failure-and-review-behavior) requires one process per output-video directory.

**Failure:** quota-safe workers overwrite the same lesson/capture; an old worker commits after a newer review; an exhausted repair lineage is reset by creating a new unit ID. A successful API call is accidentally promoted as accepted content.

**Close — CF-04/05/08:** define candidate, validated, reviewed, accepted, quarantined, superseded, and invalidated artifact transitions; define release transitions separately. Use revision-checked commits and exclusive ownership/leases where workers share output paths. Tie split/merge lineage to retry and repair limits; define what an authorized new revision can reset. Preserve successful outputs before retrying downstream persistence work.

**Proof:** two workers target the same unit; a stale worker attempts to publish; capture workers contend; a reviewer signs revision A while revision B is written. Only the intended current revision can become accepted.

### F08 — P0: production evidence lives outside Git without an early recovery contract

**Evidence:** plan §4 keeps manifests local; §8 keeps provenance sidecars local; §16 treats globally ignored JSON as having no blocker. CF-11 specifies backup restore, but does not name the full recoverable state. [Inventory](content-factory-v1-inventory.md#reproducible-method) also depends on a consistent private local DB snapshot.

**Failure:** a new clone or lost workstation cannot reconstruct why a published lesson passed, recover unknown spend reservations, or rebuild editable diagrams. Restoring HTML alone restores a website, not the factory.

**Close — CF-04/05, prove in CF-11:** define separate durable stores for immutable evidence, editable content, verdicts/reviews, ledger, configuration, and public bundles. Start backup before live production. Specify consistent snapshot/restore order, checksums, schema versions, retention, storage capacity, and independently stored copies. Keep sensitive records out of public bundles. Credentials need a separate recovery procedure, not inclusion in content backups.

**Proof:** restore into an empty workspace from the independent copy, validate evidence and ledger consistency, reproduce the accepted bundle using cached artifacts without model calls, and preserve uncertain reservations. Narrowly version synthetic fixtures/config schemas where appropriate; local JSON is not automatically disposable.

### F09 — P0: deployment drills do not yet define the production control boundary

**Evidence:** CF-11 says preview → validation → atomic promotion, rollback, withdrawal. It does not identify the immutable candidate, competing-release handling, public bundle allowlist, or all reachable old deployment URLs.

**Failure:** preview approval applies to different bytes than production; a second publisher promotes stale content; source packets, judge answers, or learner data enter the static directory; withdrawal fixes the primary URL but leaves an invalid preview publicly accessible.

**Close — CF-11, release operator:** promote the exact validated bundle by release ID/hash, serialize production promotion, recheck current approvals/rights immediately before promotion, and record deployment identity. Allowlist public files and scan the actual bundle. Verify available hosting controls for preview access, historic deployments, redirects, caching, withdrawal, and failed/ambiguous promotion. Do not assume current Cloudflare behavior from this review.

**Proof:** concurrent promotions, a last-minute invalidation, an injected private fixture, ambiguous deployment completion, and access to old URLs after withdrawal. Document limits: already downloaded copies cannot be remotely recalled.

## Missing parts of ongoing production

### F10 — P1: the plan ends at a report, not an operating handover

**Evidence:** CF-12 ends with economics and expansion. Existing rollback/withdrawal drills do not specify day-to-day detection, triage, or ownership after launch.

**Close — proposed CF-13, operator and named reviewers:** add a visible “report a problem” route carrying lesson/node/release IDs; a private incident record; severity and acknowledgement/containment targets; a review cadence; and a backup owner. Correctness and rights incidents must find every affected derivative/release, invalidate unsafe rollback targets, withdraw as needed, repair using allowed evidence, re-review, republish, and verify the public result. Record a regression case and maintenance cost. Choose response targets explicitly; do not imply unattended monitoring from an occasional operator check.

**Proof:** run that entire loop on one deliberately seeded post-publication defect, including the learner-facing correction note. Measure detection, containment, and restoration times against the chosen targets.

### F11 — P1: monitoring covers production throughput, not learner service health

**Evidence:** CF-08's weekly report covers tokens, queue age, accepted counts and cache hits. CF-11 validates preview, with no recurring public checks.

**Close — CF-11/13:** define lightweight checks for public availability, expected release ID, broken assets/routes, quiz behavior, and backup freshness, with an owner and cadence. Add stage timeouts, stuck-job detection, queue limits and disk-capacity stops. Define what happens when the operator, reviewer, model service, or host is unavailable for an extended period. Monitoring must fit the zero-cash boundary and its actual unattended capabilities.

**Proof:** break a public asset, fill the output volume in a disposable fixture, stall a job, and miss a scheduled backup. Each produces an actionable record rather than a misleading success status.

### F12 — P1: learner findings do not have a defined return path to acceptance

**Evidence:** CF-10 says observe, revise, resolve critical failures. CF-09 runs earlier; there is no explicit reevaluation loop after those revisions. Five to eight learners are specified without assigning outcome/task coverage.

**Close — CF-10/09/11:** bind the trial to the tested release and selected outcomes; define the performance criterion and task coverage before use. Keep fresh unaided tasks separate from worked solutions, hints and public quizzes. A critical finding reopens affected artifact/review gates; prompt or rubric tuning also exposes the holdout and triggers F03. Reassess revised teaching with an appropriate fresh task and record which outcomes have direct learner evidence versus only review evidence. Avoid implying that every outcome was learner-tested by a small sample.

**Proof:** one trial failure leads to a tracked revision, correct invalidation, independent acceptance, and a documented reassessment. No final release consumes superseded learner evidence silently.

### F13 — P1: human review is a role list, not a workable review system

**Evidence:** the plan names reviewer vacancies and per-lesson review, but no review queue schema, disagreement resolution, substitute authority, or challenge-domain reviewer coverage. The [inventory challenge notes](content-factory-v1-inventory.md#earlier-pilotchallenge-candidates--historical) specifically call out physics expertise.

**Close — CF-03/06/08:** retain assignments, competency by case/domain, content revision, independent reference decision, disposition, timestamps and discrepancy resolution. An optics title alone does not establish English/digital-logic expertise. Separate blind reference labeling from review after model feedback. Agree measurable weekly capacity and stop/backpressure rules. Schedule full-course sufficiency review as well as final lesson review.

**Proof:** a disputed answer and an unavailable reviewer have an explicit routing/blocking outcome; an agent cannot synthesize approval. Replace calendar guesses with measured lesson/outcome volume and reviewer availability after the engineering trial.

### F14 — P1: static quizzes have an unresolved answer-visibility contract

**Evidence:** CF-05/11 require answers not exposed before an attempt, while delivering static client-side artifacts. No threat model or distinction between practice and assessment is stated.

**Close — CF-05/10:** for formative practice, define no premature answer display through the normal UI, accessibility tree, hints, search snippets, or print view. A self-contained static quiz that evaluates answers locally necessarily gives the client enough information to inspect them; it cannot promise exam secrecy. Keep the learner trial's independent task/answer materials outside the public bundle. Define numerical tolerance, units, multiple valid answers, retry/hint behavior, and how free-response optics work is scored.

**Proof:** keyboard/screen-reader attempts and print/search paths do not reveal practice answers prematurely; the trial answer packet is absent from every public artifact. Independently check derived task solutions and convention-dependent answers.

### F15 — P1: diagram identity and teaching correctness can drift together

**Evidence:** the [capture guide](KEYFRAME_CAPTURE.md#failure-and-review-behavior) says YouTube ID is not an immutable media revision, local identity is caller-supplied, timestamps are not guaranteed frame-exact, and caches need refresh after edits. CF-07 mainly records ID/time/PNG hash.

**Close — CF-02A/07:** bind each accepted visual to the captured bytes, fetch/capture metadata, matching-lecture identity evidence, reviewed timestamp alignment and reviewer disposition. Preserve evidence when a live video changes. Record source-supported derivations for redraws and new exercises. An optics checklist should cover the course's own sign conventions, units, ray directions, labels and diagram/text agreement; do not import missing conventions from model memory.

**Proof:** simulate an edited/retimed upload or wrong local file, unreadable labels, and a redraw with a reversed ray. Refresh must create a new evidence revision and invalidate affected outputs, never silently replace accepted pixels.

### F16 — P1: accessibility is a checklist without a declared test environment

**Evidence:** CF-05 says “WCAG-minded”; CF-11 lists visual and interaction checks. The [historical discovery probes](content-factory-v1-blindspots.md#discovery-probes-for-unknown-unknowns) explicitly included an Arabic screen reader.

**Close — CF-05/07/11:** declare supported browser/device/assistive-technology combinations and concrete acceptance criteria. Include Arabic reading order, mixed-direction equations, accessible math/diagram alternatives, zoom/reflow, keyboard quizzes, feedback announcement, missing-font fallback, slow assets and long lessons. Test one difficult real lesson early, then the final bundle. Adopt a dated accessibility reference during implementation; do not claim conformance from “WCAG-minded.”

**Proof:** retain reproducible failures and reviewer checks from actual assistive-technology use, not just screenshots or automated contrast output.

### F17 — P1: content execution controls lost their required failure probes

**Evidence:** CF-07 tests injected markup, but the [resolution execution contract](content-factory-v1-resolution.md#durable-spending-and-execution-contract) also requires path/URL allowlists, instruction isolation, and restricted executable examples. §18 claims safe-execution evidence without an explicit implementation path for all of it.

**Close — CF-05/07:** enforce these boundaries in the parser, asset resolver, judge membership validator and any execution worker. Include diagram/SVG exports and generated derivatives. If the pilot executes no code, record that and reject executable content; do not build an unnecessary general sandbox. If challenge cases execute code, the disposable resource-limited worker is required there.

**Proof:** source instructions cannot select verdict IDs or invoke tools; traversal, forbidden URL schemes, active SVG content and oversized inputs fail safely. Where execution exists, time/memory/process and filesystem/network limits are exercised.

### F18 — P1: rights and learner records need artifact-level handling

**Evidence:** rights are OPEN until promotion; CF-10 records learner failures; CF-11 ships public working/release notes. There is no artifact-level permission record or public/private data rule.

**Close — CF-01/10/11/13:** link permission evidence and unresolved status to source/asset revisions and affected releases; inventory selected dependencies/fonts and required notices. Record learner participation/recording choices, restrict identifiable observations to a private store, choose retention/deletion handling, and publish aggregate findings. Do not infer permission from file availability or put review packets into public working notes.

**Proof:** expired/revoked/missing approval blocks or withdraws the affected bundle; a synthetic learner identifier and private review attachment cannot enter public output. This is an operational records requirement, not a legal determination of permission.

### F19 — P1: provider and schema drift have no maintenance policy

**Evidence:** cache keys include versions, but the [resolution](content-factory-v1-resolution.md#format-identity-and-dependency-boundaries) also requires mutable-model resolution/fingerprint where available and drift audits. The plan provides no update cadence, canary, or schema migration procedure.

**Close — CF-04/05/13:** record observable model/settings and tool/schema versions; keep representative development canaries; define what change triggers recalibration and invalidation. Version persistent ledger/artifact schemas and prove migration from a backed-up prior version. Distinguish rebuilding a published bundle from reproducing a historical model response, which may be impossible.

**Proof:** simulate a model alias change, parser upgrade and interrupted schema migration. Stale acceptance is rejected, prior durable artifacts survive, and the cost of required reevaluation is recorded.

### F20 — P2: the capacity model omits the expensive tails and ongoing work

**Evidence:** plan §17 extrapolates three lectures and uses approximate judging multiples; §15 gives a nine-week schedule. [Skills-map costs](skills-map.md#cost-picture-cost-effective-by-design) include extraction, local resources and human work; the context report adds material per-session overhead. CF-12 reports maintenance separately but no maintenance cycle generates that evidence.

**Close — CF-04/07/08/12/13:** measure full assembled prompts, context limits, batch overhead, tool/agent usage, reasoning/output where observable, repair tails, images, wiki/graph, discarded candidates, human minutes, storage and backup growth. Sample difficult sources beyond the strongest trial lesson without exposing protected families. Include maintenance, evaluation and emergency-repair headroom. Treat `min(remaining quota, estimated need)` as a spending ceiling, not proof the scope is affordable; report the funding/quota shortfall explicitly. Allocate runs by expected work rather than equal division alone.

**Proof:** low/base/high forecasts use measured volumes and queue throughput; one maintenance repair has a recorded cost; a long lesson exceeding usable context fails before dispatch or is split through a tested coverage-preserving path.

### F21 — P2: “full production” needs an explicit boundary with platform v1

**Evidence:** the [goal's delivery sequence](content-factory-v1-goal.md#delivery-sequence) defers the broader platform and framework comparison. The [platform brief](platform-map-brief.md) includes persistent progress, reader navigation, richer graph interaction and a stack-comparison blog; CF-11 supplies a minimal renderer and selected public surfaces. [Fanout's mapping](fanout-feature-analysis.md#5-mapping-to-the-iug-platform) also mixes immediate and later patterns.

**Close — CF-03/05/11:** publish a small delivery matrix: required for this factory pilot, explicitly deferred platform capability, or unresolved product decision. Wireframes do not confer implementation or acceptance. For features actually shipped, specify behavior and tests: resume/progress reset and revision migration if progress exists; stable lesson/node routes and moved-link handling; glossary/graph navigation and empty states. Do not introduce accounts, payments, live tutoring or the whole-corpus graph merely to call the pilot production-ready.

**Proof:** the delivered course supports its promised learner journey end to end, and the completion report states which broader platform capabilities remain deferred.

## Proposed complete production cycle

This extends the existing tickets rather than restarting the project. Ticket additions and decisions below are proposals for adoption, not completed controls.

| Stage | Work and accountable role | Durable evidence / exit gate |
|---|---|---|
| 0. Operating boundary | CF-04 preflight; operator defines quota accounting, durable storage, roles and release authority. Offline manifest work can proceed independently. | Observed capabilities, preparation allowance, backup location, explicit blockers. |
| 1. Intake and evidence | CF-01/02 + proposed CF-02A; agent prepares, subject reviewer resolves. Reserve evaluation access before semantic discovery. | Immutable source manifest, normalization/correction records, reviewed visual evidence, exposure log. |
| 2. Full curriculum freeze | CF-03; operator + subject reviewer. | All-source sufficiency matrix, prerequisites, promised assessments, explicit unresolved gaps, signed scope revision. |
| 3. Runtime and contracts | CF-04/05/06; agent implements, operator/reviewers supply empirical inputs. | Budgeted adapter, artifact states, dependency graph, schemas, calibrated rubric and protected evaluation protocol. |
| 4. Engineering vertical slice | CF-07; one real difficult-enough lesson through all required derivatives. | Accepted lesson; exact rendered candidate; zero-call rerun; interruption/invalidation/concurrency proofs; measured costs. |
| 5. Bounded course production | CF-08; agent produces within reviewer and quota capacity. | Revision-bound reviews/verdicts, segment/outcome closure, resumable artifacts, reconciled spend and backups. |
| 6. Course and learner acceptance | CF-09/10; independent reviewers and learners. | Frozen evaluation results and trial evidence. Defects return to stages 1–5 as needed; tuning reopens evaluation design. |
| 7. Production qualification | Proposed CF-11A within CF-11; release operator. | Clean restore/rebuild, public/private bundle checks, accessibility and security probes, exact preview approval, rollback/withdrawal proof. |
| 8. Promotion and verification | CF-11; release operator. | Serialized promotion of approved hash, live release/asset/quiz checks, release notes and rollback identity. |
| 9. Operate and respond | Proposed CF-13; operator, backup owner and subject/editorial reviewers. | Problem reports, service checks, incidents, source/rights/version changes, containment and maintenance ledger. |
| 10. Repair and republish | CF-13 reuses CF-02A/05/07/09/10/11 according to impact. | Append-only correction → invalidation → bounded repair → independent checks → approved new release → verified public fix. |
| 11. Retire or expand | CF-12 after the operational rehearsal; operator decision. | Actual first-publication and maintenance costs, retained evidence, safe withdrawal/archival path, measured next-batch size. |

The critical path therefore includes **real quota integration, full-source sufficiency, reviewer capacity, learner acceptance, and restoration proof**, wherever their gates actually block work. Labeling the ledger “off the critical path” does not remove its dependency before live dispatch.

## Discovery drills for unknown unknowns

Unknown unknowns cannot be enumerated in advance. These are bounded experiments designed to expose interactions that the individual checklists miss. Use synthetic faults and fake-provider calls first; budget any real model work through CF-04. Keep invalid teaching out of public releases.

| Drill | Boundary crossed / unexpected failure sought | Pass evidence |
|---|---|---|
| Empty-workspace handover | Local ignored files → another operator; missing evidence, fonts, configs, quota state. | Restore accepted bundle and audit trail without original workstation or model calls; unavailable credentials are recoverable through a documented route. |
| One changed sign convention | Raw evidence → correction → multiple lessons, quizzes, diagrams, wiki, graph → released pages. | Exact expected invalidation closure; invalid releases excluded from rollback; only affected work reprocessed. |
| Crash, late response, second worker | Provider execution → ledger → artifact store → reviewer approval. | No released unknown reservation, duplicate accepted revision, lost durable success, or stale worker overwrite. |
| Quota reset plus outside usage | Subscription accounting → session overhead → shared allowance. | Unknown or insufficient allowance stops new work; prior reservations/periods remain auditable. |
| Edited video and identical ID | Live media → cached frame → source-derived diagram. | Timing/identity mismatch becomes a reviewed new revision, not an unnoticed cache hit. |
| Holdout family through a shared glossary | Cross-lesson dependencies → split boundary → prompt development. | Exposure detected transitively; contaminated result is not reported as unseen. |
| Learner finds a convincing wrong solution | User report → independent correction → incident → republish. | Time to containment/recovery measured; feedback retained; fresh verification of the repaired outcome. |
| Withdrawal during promotion | Rights/correctness invalidation → release lock → old preview URLs/cache. | Promotion aborts or is contained; affected accessible versions handled with recorded limitations. |
| Weak device and assistive technology | Large Arabic lesson + equations + failed font/asset + quiz. | Core teaching remains accessible; no hidden-answer announcement, unusable focus, or unreported asset failure. |
| Long/damaged source with strong-looking verdicts | Context truncation → omitted IDs/spans → coverage → apparent acceptance. | Independent deterministic membership/coverage checks reject missing work despite high model scores. |
| Private file in build staging | Review/learner/evaluation store → public bundle. | Build rejects it before upload, including indirect assets, generated indexes and source maps if present. |
| Silent model/parser update | Version identity → cached acceptance → rendered meaning. | Canary or version checks trigger the correct reevaluation; clean prior artifacts survive rollback/migration. |

## Known OPEN inputs, not newly discovered blind spots

The plan already identifies reviewer/learner availability, source and font permissions, lecture order, skipped-source disposition, actual zIDE capabilities and remaining quota, numeric allocations and calibrated thresholds. They remain dependencies, not findings to relabel as surprises.

Additional decisions to record during the existing tickets: final versus interim release contract; holdout access/exposure policy; full model-accounting boundary; production owner/backup and response targets; independent backup capacity and retention; learner-record handling; static assessment semantics; supported accessibility environments; and the exact factory/platform boundary. None should be filled with invented approvals or measurements.

## Recommended next action

Keep **CF-01** as the immediate offline implementation task. Before downstream tickets execute, reconcile F01–F03 and give F04–F09 explicit ticket ownership and acceptance probes. Add **CF-13 operate/repair/republish** and require one complete operational rehearsal before CF-12 claims production readiness. Update §3, §18 and Appendix B together so fresh-session briefs enforce the same gates as the main plan.
