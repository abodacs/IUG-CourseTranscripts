# OPTO 2311 pilot — full execution plan

**Quick read:** the complete ticket-by-ticket plan for reprocessing **OPTO 2311 — البصريات الهندسية** into an accepted, published v1 pilot course. It decomposes the [four milestones](NEXT_STEPS.md) into tickets CF-01…CF-13 (including CF-02A and CF-11A), and names every action, artifact, gate, command, owner, and open human input. [Ticket CF-01](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest) is still the immediate action; this plan orders everything after it.

Status: planning document, adopted 2026-09-06. It sequences and details work defined by the [goal](content-factory-v1-goal.md), [resolution](content-factory-v1-resolution.md), and [pilot packet](content-factory-v1-pilot.md); it changes no fixed decision. Durations are planning estimates, not commitments. Values marked **OPEN** are required evidence or authorization — they are recorded when obtained, never invented.

**Production-cycle integration (2026-09-06):** this plan now includes source normalization, full-course sufficiency, durable artifact/release controls, and the operate → repair → republish cycle. The 21 findings and their required closure proofs are retained in §19; discovery drills are in §20. These are implementation requirements, not evidence of completion. Publishing permissions, empirical inputs, and unresolved release/holdout decisions remain OPEN. The goal still owns fixed scope.

**Execution rule:** every ticket includes its assigned §19 controls and §20 proofs, including when copied into a fresh session. “Offline” or “no model calls” in a script brief means no provider calls from that script; model-assisted agent preparation still consumes the accounted zIDE allowance. Record a bounded preparation allowance before such work, and reconcile prior attributable usage without inventing measurements.

---

## 1. Fixed frame (copy-paste reference)

| Item | Value |
|---|---|
| Course | OPTO 2311 — البصريات الهندسية, كلية العلوم الصحية |
| Playlist ID | `PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-` |
| DB linkage | `playlists.source_id` (row `id=84`); `sync_github.playlist_id` for the 106 memberships |
| Playlist metadata | title `كلية العلوم الصحية |  OPTO 2311 - البصريات الهندسية`; `instructor` **empty**; `description` = `nan`; `entries` truncated at 32,767 chars; `enriched=1` |
| Videos | 106 recorded IDs; 105 with raw JSON + raw SRT + `_postprocess.srt` + normalized `.srt` (420 files in `data/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/`) |
| Skipped source | `SAq013FtOLQ` (`skip=1`, `downloaded_r2=0`, no raw file) — disposition unresolved |
| Legacy artifacts | 105 chapter JSONs, 83 `_v2_content.json` (audit-only, never teaching inputs) |
| Keyframe hints | 420 distinct chosen timestamps, 897 with candidates, 131 chapter-range warnings across the 105 chapter JSONs |
| Raw JSON format | faster-whisper output: `segments[]` with `start/end/text/avg_logprob/compression_ratio/no_speech_prob/temperature/words` |
| Sibling optics playlists | `بصريات هندسية` `PL9fwy3NUQKwb_KOrEPbVXCHcPMZKR0uEY` (30 videos), `البصريات الهندسية` / عمرو أبو عمارة `PL9fwy3NUQKwZZYWdO8xTBLJBmEjaQDzzb` (25 videos) — **zero video-ID overlap** with the pilot, but same course name ⇒ near-duplicate *content family* risk for holdout grouping |
| Order evidence | `sync_github.created_at` values span one 34-second batch import (2024-08-31 15:21:57–15:22:31) — **download order, not lecture order; unusable for sequencing** |
| Teaching sources | Transcripts only; matching YouTube lectures only for needed diagrams (with video ID + timestamp + captured evidence). No external supplements, no legacy lesson reuse. [Policy](content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed) |
| Budget | Zero incremental cash; zIDE subscription only; stated total **300,000,000 tokens**; remaining balance **OPEN**; run/pilot allocations **OPEN** until measured |
| Delivery | This repo; static artifacts; Cloudflare Pages (atomic promotion, preview validation, rollback) |
| Test baseline | 181 passing (`.venv/bin/python -m pytest`, verified 2026-09-06) |
| Runner-up course | جبر حديث 1, `PL9fwy3NUQKwZKOpj354PRgwYPWWgxchnI` — switch requires an explicit documented decision, never an automatic one |

## 2. Roles and the human-dependency map

| Role | Holder | First needed at | If absent |
|---|---|---|---|
| Operator | Abdullah | CF-01 (repo access); CF-04 (quota evidence); CF-11 (Pages access) | All model dispatch and release blocked |
| Agent (zIDE sessions) | one ticket per session | CF-01 onward | — |
| Optics subject reviewer | **OPEN** — recruit from day 1 | CF-02 step 6 (first review); every lesson review; correction authority | Lectures can be prepared, but scope freeze, verdicts, and release are blocked |
| Arabic editorial/visual reviewer | **OPEN** (may be the subject reviewer if qualified) | CF-07 onward | Release blocked |
| Learners (5–8) | **OPEN** — recruit early | Phase 8 | Final course promotion and acceptance blocked |
| Production owner / backup | Abdullah / **OPEN** | CF-04 storage preflight; CF-11 handover; CF-13 operations | Production readiness blocked without coverage and response targets |
| Challenge-domain reviewers | **OPEN** — verify competence per reference case | CF-06 | Affected reference labels and evaluation blocked |
| Rights confirmation (transcripts, diagram captures, Thmanyah font license) | **OPEN** — operator | Before CF-11 promotion | Release blocked; offline work continues |

Rule from the resolution: a reviewer can flag an error but cannot authorize outside teaching material. Reference decisions are made **before** seeing judge scores.

## 3. The whole pilot on one page

| Phase | Ticket(s) | Produces | Gate to pass | Depends on |
|---|---|---|---|---|
| 0. Source manifest | [CF-01](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest) | `scripts/build_pilot_manifest.py`, `artifacts/opto-2311/source-manifest.json`, `docs/opto-2311-source-review.md` | Stable manifest hash on unchanged rerun; all gaps visible | — |
| 1. Order & selection | CF-02 | `artifacts/opto-2311/lecture-order.json`, three-lecture skill sheet | Order table has no invented positions; reviewer's first review done | CF-01 |
| 1A. Evidence preparation | CF-02A | Normalization/correction records, eligible evidence packets | Raw lineage preserved; ambiguities blocked; full-source preparation accounted for | CF-01/02; protected-family access policy |
| 2. Scope freeze | CF-03 | `docs/opto-2311-scope-freeze.md` + outcome matrix | Operator + reviewer sign-off; every outcome `supported` / `needs_youtube_diagram` / `unsupported` | CF-02/02A, reviewer, CF-04 allocations |
| 3. Quota & ledger | CF-04 | SQLite spend ledger + fake-provider failure tests + recorded allocations | Failure probes pass; dispatch refuses without reservation | Operator preflight starts before model-assisted preparation; ledger development parallel with 1–2 |
| 4. Format & rubric | CF-05, CF-06 | Markdown dialect + validators; `COURSE_RUBRIC.md`; judge harness; reference sets; split manifest | Conformance fixtures pass; thresholds calibrated on dev data | CF-03; CF-04 before any live judge/calibration dispatch |
| 5. Trial lesson | CF-07 | One complete accepted lesson + unit-economics report | Unchanged rerun = zero model calls; reviewer accepts; seeded failures block | 2, 3, 4 |
| 6. Production | CF-08 | All frozen lessons authored + reviewed + cached | Zero unresolved critical defects; budget never exceeded | 5; CF-11 scaffold in parallel |
| 7. Course evaluation | CF-09 | Challenge-set + holdout report, coverage audit | All seeded criticals correctly blocked; thresholds not tuned post-hoc | 6 |
| 8. Learner trial | CF-10 | Formative trial report | Critical teaching failures resolved; limitations stated | 6 (lessons stable) |
| 9. Qualification & release | CF-11A/CF-11 | Exact approved bundle, clean restore, promoted release | Current CF-09/10 evidence, rights, closure, preview approval, withdrawal/restore proof | 7 and 8; scaffold from 5 |
| 10. Operate & repair | CF-13 | Incident/runbook records; independently accepted repaired release | Full report → containment → repair → review → republish rehearsal; response targets measured | CF-11; preparation starts before promotion |
| 11. Report & expansion | CF-12 | Pilot report + initial/maintenance economics + expansion decision | Every goal checkbox and operational rehearsal has evidence | all, including CF-13 rehearsal |

Mapping to [NEXT_STEPS.md](NEXT_STEPS.md): milestone 1 = Phases 1–2, milestone 2 = Phase 3, milestone 3 = Phases 4–5, milestone 4 = Phases 6–11. Ticket numbers preserve the original IDs; CF-13 executes before CF-12 final acceptance.

**Release states and gates:** private engineering previews are not course acceptance. Final course promotion requires current CF-09 and CF-10 evidence for the candidate revision, complete prerequisite-closed scope, valid reviews/verdicts, rights, and preview qualification. The earlier “3+ lessons” public-release shortcut is removed. Interim public teaching remains blocked until CF-03 records a reviewed standalone module scope and explicitly reconciles staged publication with the authoritative complete-course contract; a STATUS banner alone does not authorize it. Apply the same release predicate to every promotion path.

## 4. Phase 0 — CF-01, source manifest (offline, no model calls)

The full brief lives in [NEXT_STEPS.md](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest). Execution details that the session must honor:

1. **DB reads:** copy `youtube-iug.db` to a temp dir; open with `mode=ro&immutable=1`; refuse a nonempty WAL (existing scanner pattern). Join `sync_github.playlist_id` → `playlists.source_id` (verified linkage; `playlists.id` is a rowid, not the YouTube ID).
2. **Order fields:** record `sync_github.created_at`/`modified_at` as *download* evidence only, and mark lecture order `unknown` — the timestamps are one batch import.
3. **Variant mapping per video ID:** `*_raw.json` (canonical whisper output), `*_raw.srt`, `*_postprocess.srt` (needs fidelity check), plain `*.srt` (normalized variant — classify, do not trust), `GeminiLongContext/*_chapters.json` (hint source, audit), `*_v2_content.json` (audit-only). Record path, size, SHA-256, role, eligibility.
4. **Integrity probes:** segment counts raw JSON vs raw SRT; `_postprocess.srt` time coverage vs raw; faster-whisper flags (`no_speech_prob`, `compression_ratio`, `avg_logprob`) as *screening hints*, not verdicts; flag malformed/duplicate/out-of-order/invalid-timestamp units.
5. **Family appendix:** record the two sibling optics playlists (IDs above) as candidate near-duplicate families for the CF-06 split manifest — no extra processing of them.
6. **Outputs stay local:** `.gitignore` ignores JSON globally; the manifest stays untracked, inspection timestamps live outside the hashed payload; only `docs/opto-2311-source-review.md` (Markdown) is committed. No corpus, DB, or credential commits.
7. **Tests:** membership alias (`L9fwy3NUQKw…` missing `P`), shared IDs, skip flags, conflicting variants, malformed content, truncated metadata, unchanged-rerun hash stability. Existing suite must stay green (181 baseline).

**Done:** every expected video has a record; gaps and unknowns visible; zero network/model calls; report names what still blocks scope freeze. *Estimate: 2–4 focused hours.*

## 5. Phase 1 — lecture order and three-lecture selection (CF-02)

Before semantic discovery, reserve candidate evaluation families and record existing exposure, including prior capture inspections. CF-03/06 must resolve protected access for full-course coverage versus the pilot packet’s strict exposure rule (F03). No source already used for tuning can become an unseen holdout.

1. **Primary order evidence — YouTube playlist metadata** (permitted use: identity/order only). Fetch with the pinned toolchain:
   ```bash
   uv run --isolated --no-project --with 'yt-dlp[default]==2026.8.19' \
     yt-dlp --flat-playlist --print '%(playlist_index)s\t%(id)s\t%(title)s\t%(duration)s' \
     'https://www.youtube.com/playlist?list=PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-'
   ```
   Save as `artifacts/opto-2311/lecture-order.json` with fetch date and tool version. Titles/dates are metadata for ordering and capture hints — **not teaching facts**.
2. **Cross-check without invention:** verbal sequence references inside transcripts ("المحاضرة السابقة/القادمة"), chapter JSON hints, upload dates if exposed. Any conflict ⇒ position recorded as `unknown` with the conflicting evidence listed; the affected lecture keeps an explicit unknown slot.
3. **Reconcile counts:** playlist order list vs 105 local transcripts vs the 106th ID `SAq013FtOLQ` (keep visible, still `skip=1`). If the live playlist differs from the local set, record the delta; do not download lectures.
4. **Select first / middle / final** lectures from the verified order. For each, the agent drafts candidate **tangible skills** from transcript skims + chapter hints, with original evidence spans and, where a diagram is needed, the timestamp (start from the 420 chosen keyframe hints; a hint is not proof of what the frame shows).
5. **Classify each candidate skill:** `supported` / `needs_youtube_diagram` (must name the missing visual + video ID + time range) / `unsupported`.
6. **Reviewer first review (30–45 min):** reviewer works one worked example and one unseen task per lecture, independently, before any judge exists. Record prerequisite observations for the learner assumption.
7. **Capture drill (optional, bounded):** for one needed diagram, run the [capture CLI](KEYFRAME_CAPTURE.md) on that lecture only; reviewer verifies the pixels. This proves the diagram pipeline before scale.

**Gate:** order table complete (or unknowns explicit); three-lecture skill sheet exists; reviewer risk note written. *Estimate: 1–2 h agent + 45 min reviewer + 15 min operator fallback if yt-dlp fails (manual playlist-page transcription).*

### CF-02A — normalization, corrections, and eligible evidence

Choose and document raw-only authoring or implement a versioned normalization path. Preserve immutable raw text, segment IDs and timestamps; record aligned transformations, uncertain spans, and append-only corrections with allowed evidence/derivation, reviewer disposition and affected artifact IDs. Enforce input eligibility at authoring and helper-tool boundaries; legacy prose cannot supply teaching facts. Prepare all 105 available sets under the protected-family access policy, not just the three discovery samples.

Bind diagrams to captured bytes, matching-lecture identity evidence, time alignment, capture metadata and visual review. Edited media or replacement captures create a new revision. Independently check the course’s own sign conventions, units, labels and ray directions.

**Gate:** same-length semantic corruption is detected; unsupported corrections quarantine outcomes; source-to-teaching coverage is validated through references, not equal counts. Required controls: F04/F05/F15. Agent prepares; subject reviewer approves. Estimate after source-integrity findings.

## 6. Phase 2 — scope freeze (CF-03)

1. **Full-course discovery and outcome matrix** (`artifacts/opto-2311/outcome-matrix.json`, local; summarized in the committed scope doc): per outcome — `outcome_id`, tangible task, prerequisites, intended learner, evidence refs (transcript spans; diagram video ID + range), required explanation/example/practice/transfer-task IDs, sufficiency status (`supported` / `needs_youtube_diagram` / `unsupported`).
2. **Skipped-video disposition:** reviewer + operator establish its curriculum impact only from allowed evidence. Do not invent the missing lecture’s topic or declare it irrelevant without support. Retain an explicit completeness blocker/limitation where impact cannot be established; required unsupported outcomes block acceptance unless a smaller scope is explicitly reviewed.
3. **Lesson plan:** group outcomes into lessons in prereq-closed order following verified lecture order; target ~1 lesson per teaching unit, no outcome dropped to improve yield.
4. **Confirm evaluation families reserved before discovery:** challenge excerpts (فيزياء عامة أ `1noCDAkxHwg`; اللغة الإنجليزية `0mkSe0xrqKk`; Digital-logic `Kzxd5D8ZgnQ` 13:37) are **development data only**; holdout families for the pilot are drawn from pilot-course videos not exposed during tuning, grouped by source-video/near-duplicate family (watch the sibling-playlist families from CF-01).
5. **Freeze checklist (all must be recorded before CF-07 dispatch):** outcome IDs; lesson scope; assessment requirements; required diagrams with video IDs/ranges; per-course/per-lesson wiki coverage; graph edge types; learner assumption + prerequisites; numeric run/pilot token allocations (from Phase 3); reviewer names.
6. **Sign-off:** operator + subject reviewer record approval in `docs/opto-2311-scope-freeze.md`. All 105 available sources must contribute to the sufficiency/disposition audit; three lectures estimate risk only. Record reviewed teaching order separately from unknown historical positions. Include the factory/platform delivery matrix, release membership rules, review capacity and protected-family access decision. Later changes = a new scope revision repeating the review.

**Gate:** frozen scope; every promised outcome has evidence and prerequisites or an explicit blocker. *Estimate: OPEN until full-source volume and reviewer capacity are measured; the earlier sample-based estimate did not cover full-course discovery.*

## 7. Phase 3 — quota truth and the spend ledger (CF-04, parallel with Phases 1–2)

1. **Operator capability check (20–30 min), recorded as observations:** how zIDE exposes work submission, model identity, per-task usage, export, quota period/reset, remaining balance, interrupted-job recovery. No API is assumed.
2. **Integration decision:** automated adapter only for behavior actually observed; otherwise an **operator-mediated workflow** (periodic usage export reconciled against the local ledger) with its limits written down. If observability cannot support the guarantee, automatic dispatch stays disabled and the unresolved integration is recorded.
3. **Ledger (SQLite, integer tokens):** tables for `pilot_allowance`, `run_allocations`, `reservations(attempt_id, unit_id, model, reserved_in, reserved_out, state, run_id, timestamps)`, `observed_usage`, `unit_lineage(attempt/repair/escalation counters)`. Attempt states: `reserved → dispatched → succeeded | failed_confirmed | outcome_unknown`. Mark `dispatched` durably **before** the external call; persist output + usage **before** success; retain `outcome_unknown` reservations across restarts; release only with measured usage or confirmed non-dispatch.
4. **Fake-provider failure probes (all required):** crash before dispatch / after dispatch / after receipt / before usage commit; response loss; two workers contending for the last allowance; restart after repair exhaustion; provider unavailable; artifact-persistence failure.
5. **Bounded lineage:** ≤2 transient retries, 1 repair cycle, 1 premium escalation per unit — durable across restarts and workers; exhaustion quarantines the unit, never relaxes the rubric.
6. **Allocation setting (before any dispatch):** measure token volumes on the three Phase-1 lectures; compute per-lesson generation + judging estimates including retries; derive `run_cap` and `pilot_cap` ≤ remaining measured quota with an explicit safety margin. Record numbers + derivation in the ledger config. *Values are OPEN until this measurement; the formula and a worked example are in [§17](#17-budget-checkpoints-and-allocation-method).*

**Accounting and durability:** include preparatory agent sessions, tool/context overhead, nested model routes, calibration and graph/wiki work. Verify actual quota currency, observation lag, other operator usage and period resets. Allocate CF-06 before calibration; unknown usage or actual usage above reservation stops new dispatch pending reconciliation. Start independent backup of evidence, editable content, ledger, verdicts, reviews and configuration before live production; define consistent snapshots, retention and capacity. Test quota rollover, late responses, outside usage and over-reservation consumption (F02/F08/F20).

**Gate:** fake-adapter probes pass; real boundary documented; bounded real-workflow reconciliation recorded; allocations recorded; a dispatch attempt with insufficient allowance is refused by test. *Estimate: 4–8 h agent + operator iterations.*

## 8. Phase 4 — format, rubric, evaluation harness (CF-05 + CF-06)

### CF-05 — Markdown dialect, validators, preview

- Constrained Markdown + declared extensions: math (`$$…$$` subset validated), tables, stable teaching-node IDs with split/merge history (never paragraph ordinals or content hashes as identity), fenced `quiz` payloads validated against a schema (stable IDs, skill refs, prompt, choices/task, answer, rationale, feedback; answer not displayed through normal UI/accessibility paths before an attempt). No arbitrary JS/MDX/raw HTML/event handlers.
- Provenance sidecars: per-lesson JSON mapping every teaching node → transcript spans / diagram evidence; durable private storage with versioned backup. Public bundles contain only allowlisted learner-facing artifacts; recovery bundles also retain the private acceptance evidence.
- Segment-disposition recorder: `included` / `duplicate_of` / `excluded_with_reason` / `unresolved` per source segment, completed per lecture during Phase 6.
- Renderer for v1 = minimal static HTML generator conforming to the dialect, **RTL-first**, Thmanyah typefaces (license verification is an open rights item), WCAG-minded (contrast, keyboard, reduced motion), framework-agnostic — the platform stack comparison stays platform-map scope.
- Bounded OKF v0.2 evaluation for the wiki layer; graph output as `graph.json` (+ HTML view later) with typed edges and provenance; prerequisite edges acyclic.

- Artifact states and dependency engine: separate provider success, validation, review, acceptance, quarantine, supersession, invalidation and publication. Bind approvals to exact revisions; implement transitive build dependencies separately from semantic edges. Use revision-checked commits and output ownership so ledger-safe workers cannot overwrite accepted work or reset repair lineage through new IDs (F06/F07).
- Runtime conformance: declare browser/device/assistive-technology coverage; test Arabic screen reading, math, reflow and font fallback. Static practice hides answers from normal interaction but cannot promise exam secrecy; independent trial answers remain private. Define numeric tolerances, units and valid alternatives (F14/F16).
- Trust boundaries: allowlist URLs/paths/assets and validate generated SVG as well as Markdown. Reject instruction-driven verdict membership and oversized inputs. Reject executable content unless an explicit isolated, resource-limited worker is implemented for an approved exercise (F17).
- Persistent schemas and model/tool changes require versioned migration, canaries, invalidation and recovery rules (F19).

### CF-06 — rubric, judges, reference sets, splits

- Research + version `docs/COURSE_RUBRIC.md`: grounded in Bloom's taxonomy, backward design, cognitive load, retrieval practice, worked examples; four checks (evidence support, subject correctness, editorial/pedagogical contribution, cross-lesson coherence); explicit hard-failure list; threshold fields filled during calibration. Teaching-bearing nodes = prose paragraphs **and** math, code, tables, quiz choices/keys/rationales, diagrams + accessible alternatives, wiki entries, simplified explanations.
- Judge plan: calibrated inexpensive judge for coverage verdicts (batched, stable IDs, explicit per-item verdicts; missing IDs fail; malformed judge output = failure); premium reserved for generation, escalations, bounded deep audits. Whole-lesson context in every verdict (conservative cache boundary at pilot scale).
- Reference sets: Arabic-first good + known failures + English + mixed-direction cases, labeled by humans **before** judge scores; all 12 required failure classes represented (wrong assertion, outdated version, transcription ambiguity, absent visual, contamination, wrong quiz key, persuasive wrong solution, missing prerequisite, cross-lesson contradiction, harmful simplification, invalid repair, instruction-like text in source).
- Split manifest and access log grouped transitively by source-video/near-duplicate family, including multi-source lessons and shared glossary evidence. Record prior exposure. Resolve protected coverage/reference access before full-course discovery; if the strict exposure rule leaves no eligible families, block a holdout claim and settle the design. Freeze prompts, rubric, model/settings and thresholds before isolated holdout production/evaluation. Candidate tuning only uses development data (F03).
- Reference decisions require competence per subject/domain, revision-bound assignments, independent labeling before scores, and recorded disagreement resolution (F13).
- Cache keys: content hash + evidence refs + lesson context + rubric version + prompt version + model/settings + schema/tool versions; quiz placement and graph dependencies inside the relevant keys. Identical accepted reruns make **zero** calls.

**Gate:** validators pass conformance fixtures; rubric v1 committed; calibration report records thresholds + judge disagreement on dev data. *Estimate: 12–20 h agent + 2–3 h reviewer labeling.*

## 9. Phase 5 — the engineering trial lesson (CF-07)

One complete lesson from the strongest Phase-1 skill (middle lecture), end to end:

1. **Evidence packet:** segment accounting for the lecture; transcript spans + captured diagrams (video ID + timestamp + PNG hash) assembled first; outline drafted from evidence only.
2. **Diagrams:** capture needed timestamps (CLI, pinned yt-dlp `2026.8.19`, exit-code discipline); reviewer verifies pixels; reviewed redraw in Excalidraw with editable source + export + Arabic alt text; no invented labels/values.
3. **Authoring:** one section at a time with source-coverage checks per section (the adopted two-stage workflow); worked example, practice, and an independent transfer task per promised outcome; inline quizzes at pedagogically correct points; precomputed simplified explanations.
4. **Derivatives:** wiki entry, graph nodes/edges with provenance, disposition records for the lecture's segments.
5. **Evaluation:** deterministic validators → judge verdicts (whole-lesson context) → subject + editorial review (reference decisions before scores).
6. **Engineering proofs:** unchanged rerun = zero generation/judging calls; interrupted restart resumes without repeat work; full token ledger trail; unit-economics report (tokens per stage, review minutes).
7. **Seeded-failure probes on this lesson:** wrong quiz key, unsupported claim, broken asset link, missing verdict, injected markup — each must block promotion. Also prove the expected invalidation closure for a shared convention, paragraph move, concept split and diagram replacement; race two workers against the same revision; test source instructions, forbidden paths/URLs/SVG, context truncation and actual Arabic assistive-technology use (F06/F07/F14–F17). Keep intentionally invalid candidates private.

**Gate:** accepted trial lesson + measured economics + all probes block correctly. Rubric/prompt tuning happens **now**, before any holdout opens. *Estimate: 1–2 days agent + 1–2 h reviewers.*

## 10. Phase 6 — course production (CF-08)

- Per-lesson loop identical to the trial, in prereq-closed course order; parallel workers only after ledger and artifact-ownership concurrency are proven. Capture output directories remain single-writer. Process protected families only under the frozen CF-06 protocol.
- Gates per lesson; durable lineage limits; quarantine on exhaustion; budget stop when run allowance is exhausted (stop, report, decide — never relax the rubric).
- Segment dispositions completed per lecture; weekly status report: tokens vs caps, accepted/quarantined counts, review queue age, cache hit rate.
- Reviewer cadence agreed (batch size per week); editorial review of **every** complete lesson — sampling is only for deep audits during later expansion.
- Build-in-public surfaces may be prepared with CF-11 after CF-07. Public teaching follows §3 release eligibility; lesson count and STATUS banners do not bypass scope, rights, evaluation or learner gates. Keep engineering candidates private while public eligibility is unresolved.
- Apply review backpressure, stage timeouts, stuck-job and disk-capacity stops, durable backups and revision-bound review queues. Record disagreements and reviewer availability; no agent-created approval (F08/F11/F13).
- Any scope change (outcome added/dropped/corrected) = new scope revision + repeated review + invalidation of affected artifacts.

**Gate:** all frozen lessons authored, verdicted, and reviewed; zero unresolved critical defects. *Estimate: dominated by reviewer throughput — assume 1–3 h agent + 20–40 min reviewer per lesson; scale after the first ten lessons report actuals.*

## 11. Phase 7 — course-level evaluation (CF-09)

1. Challenge-set runs (the three bounded cases): report `bad_accepted / known_bad`, `good_rejected / known_good`; seeded criticals must all be correctly blocked.
2. Open the final holdout (thresholds frozen): false accepts, false rejects, judge–human disagreements by family. Any post-hoc tuning ⇒ holdout becomes development data and a fresh holdout is required.
3. Course-coherence audit: prerequisite chain closed and acyclic; cross-lesson contradiction probe; concept merge/alias review; whole-coverage check — every teaching node has applicable verdicts; outcome matrix fully closed with explicit denominators; lessons-with-any-critical-defect count.
4. Publish counts + severity + source-group uncertainty; no population-error claims from a small pilot.

**Gate:** zero unresolved criticals; challenge cases blocked; threshold report recorded for the candidate revision. CF-10 or CF-13 changes reopen affected checks; prompt/rubric tuning requires retiring the exposed holdout and resolving a fresh evaluation design. *Estimate: 1–2 days.*

## 12. Phase 8 — formative learner trial (CF-10)

1. Recruit 5–8 Arabic-speaking undergraduates holding the actual course prerequisites (screen against the reviewer-confirmed prerequisite list from Phase 1).
2. Instruments, all written **before** the trial: prerequisite/baseline check; lesson reading + practice; fresh unaided transfer task scored with a prewritten rubric; delayed variant (1–2 weeks) if retention is claimed.
3. Protocol: structured observation or think-aloud; record every failure; revise teaching; resolve observed critical failures; report limitations (formative evidence, not causal superiority).

4. Bind trial instruments/results to the tested revision and named outcomes. Keep answer keys out of public artifacts; record participant choices and identifiable observations privately with retention/deletion handling. Report which outcomes have learner evidence. Critical failures return through correction, invalidation, independent review and fresh task reassessment; tuning reopens CF-09 holdout policy (F12/F14/F18).

**Gate:** trial criterion verdict and remediation/reassessment evidence apply to the release candidate; superseded evidence cannot silently clear final promotion. *Estimate: 1–2 weeks wall-clock scheduling; agent-time minimal.*

## 13. Phase 9 — release engineering on Cloudflare Pages (CF-11; scaffold starts in parallel after CF-07)

1. Static site build from accepted artifacts only (one consistent versioned set); verify current Pages limits during this task.
2. Pipeline: build → deterministic checks → **preview deployment** → preview validation checklist (Arabic/English rendering, RTL clipping at mobile/desktop widths, keyboard use, focus, contrast, reduced motion, quiz interaction without answer leakage) → **atomic promotion** → rollback path proven.
3. Failure drills: intentionally failed update leaves the last accepted release usable; withdrawal when every available version is invalid (rollback cannot select an invalid release); restore from an independent backup.
4. Build-in-public surfaces (adopted from [fanout-feature-analysis.md](fanout-feature-analysis.md) §3.12/§4): STATUS banner on every page; public working-notes page listing accepted lessons; the pilot roadmap graph once graph artifacts exist; one coherent **free module** (a standalone path, not a crippled sample) as the public taste test; an illustrated release-notes page as the blog seed. All rebuilt RTL-first in Thmanyah; presentation changes never lower the bar.

### CF-11A — production qualification before promotion

Restore evidence, editable content, ledger and approvals into an empty workspace from an independent backup; rebuild the accepted bundle without model calls and retain uncertain reservations. Verify public/private bundle allowlists, dependency/license/rights records, actual accessibility behavior and runtime security probes. Record supported environments and current hosting controls for preview access, historic URLs, caching and withdrawal. Restore credentials through a separate procedure.

Promote the exact preview-approved bundle by release ID/hash. Serialize production promotion and recheck rights, scope and current revision-bound approvals at commit time. Test concurrent promotions, late invalidation, ambiguous deployment completion, private-file inclusion and accessible historic URLs after withdrawal. Already downloaded copies cannot be recalled. Run live release/asset/quiz checks after promotion.

Prepare CF-13 ownership, problem reporting, monitoring, response targets and backup cadence before release. Require current CF-09/10 evidence under §3. Controls F01/F08–F11/F16–F19 are mandatory.

**Gate:** complete eligible set promoted; exact-byte preview/live identity, rollback, withdrawal, clean backup restore and operating handover demonstrated. *Estimate: re-estimate from restore/hosting/accessibility findings; the earlier 4–8 h estimate covered scaffolding only.*

## 14. Phases 10–11 — operations, pilot report and expansion

### CF-13 — operate, repair and republish

**Owners:** operator, named backup, subject and Arabic editorial reviewers. Prepare the runbook before CF-11 promotion; rehearse after the release path is qualified.

1. Expose a problem-report route carrying lesson/node/release IDs; retain private incident records. Set severity, acknowledgement/containment/restoration targets, monitoring and review cadence, backup freshness checks, and coverage when an owner is absent. Keep targets OPEN until agreed.
2. Detect learner, source, correctness, rights, provider/model or parser/schema changes. Resolve affected evidence, dependencies and every release/derivative. Invalidate unsafe rollback targets and withdraw affected public versions where no safe accepted version exists.
3. Record append-only corrections backed by allowed evidence; preserve old artifacts. Reserve a bounded maintenance allowance; repair and invalidate through CF-02A/05/07. Renew independent reviews and rendering checks; reopen CF-09/10 where the changed teaching or evaluation requires it.
4. Republish only the eligible exact bundle through CF-11, verify the public fix and publish an appropriate correction note. Retain a regression case and initial/maintenance costs separately.
5. Rehearse the full report → impact → containment → repair → independent acceptance → republish → verification loop with a seeded defect in a private production-equivalent environment. Do not intentionally expose learners to known-invalid teaching. Measure response/recovery against the chosen targets; test backup recovery and update/migration canaries.

**Artifacts:** `docs/opto-2311-operations.md`, private incident/change records, revision-bound repair approvals, rehearsal evidence and maintenance-cost report.

**Gate:** runbook and owner/backup established; public health checks work; full operational rehearsal passes; maintenance costs and response times measured. Controls F10–F13/F18–F20 and §20 drills apply. Ongoing operation continues after the report.

### CF-12 — pilot report and expansion decision

- Economics: **LLM cost per accepted lesson** = all attributable token spend (including failures and shared overhead) ÷ first-accepted distinct lesson IDs; accepted outcome coverage reported separately (splitting lessons cannot inflate yield); reuse/cache hit rates; repair and quarantine rates; judge disagreement; reviewer minutes + queue age/throughput; human time vs machine time.
- Quality: defect counts with named denominators and severity; challenge vs holdout vs audit results kept separate; explicit limitations.
- Source record: `SAq013FtOLQ` disposition; all exclusions with reasons; rights status (transcripts, diagram captures, fonts).
- Definition-of-done map: every [goal checkbox](content-factory-v1-goal.md#v1-definition-of-done) → its evidence pointer (see §18).
- Corpus forecast from measured token volumes with low/base/high scenarios — playlist counts are never a cost estimate; no affordability claim beyond pilot evidence.
- Expansion decision: measured batch sizing for the next courses; the runner-up جبر حديث 1 is chosen only via a documented rationale if optics proved unrepresentative.

- Operational evidence: CF-13 rehearsal, incident response/recovery times, backup freshness and migration proofs, measured maintenance costs, remaining operational limitations, and the explicit deferred-platform delivery matrix.

**Gate:** report accepted after CF-13 rehearsal; expansion or retirement decision recorded with evidence retention and safe withdrawal handling. *Estimate: half a day.*

## 15. Schedule and critical path

Relative weeks from adoption (2026-09-06); dates depend on measured production volume, source issues, quota integration and human availability.

| Week | Agent track | Human track (parallel from day 1) |
|---|---|---|
| 1 | CF-04 preparation/accounting preflight; CF-01 → CF-02; protect evaluation families | Recruit subject reviewer; operator zIDE quota observations (CF-04 step 1) |
| 2 | CF-02A + full-source CF-03 discovery; CF-04 ledger + backups/probes | Reviewer first review (45 min); rights confirmations; learner recruitment starts |
| 3 | CF-05 format + CF-06 rubric/harness | Reviewer labels reference sets (2–3 h) |
| 4 | CF-07 trial lesson → CF-11 scaffold | Trial-lesson reviews; calibrate thresholds on dev data |
| 5–7 | CF-08 production batches + private qualification previews | Per-lesson reviews; weekly queue triage |
| 8 | CF-09 evaluation → CF-10 trial prep | Holdout unaffected; learner trial runs |
| 9+ | CF-11A qualification → eligible CF-11 release → CF-13 rehearsal → CF-12 report | Final reviews; delayed learner task if claimed; operating handover |

Critical path: manifest → eligible evidence/full-source sufficiency → scope freeze → trial lesson → bounded production → course and learner acceptance → production qualification → release → operational rehearsal → report. Actual quota integration, reviewer capacity, protected evaluation access and restoration proof are blocking dependencies wherever required. Parallel ledger/scaffold development does not remove those gates. The week table is provisional; re-estimate full-source and reviewer effort after CF-07.

## 16. Risk register

| Risk | Signal | Fallback | Blocks |
|---|---|---|---|
| Lecture order unresolvable | yt-dlp fails; playlist page contradicts local set | Record `unknown` positions; operator manual transcription of playlist page; scope freeze proceeds only with explicit unknown slots | Scope freeze, lesson sequencing |
| `SAq013FtOLQ` covered required outcomes | Reviewer says its topic is in the promised curriculum | Outcome marked `unsupported` → blocked, or explicitly reviewed scope revision | Those outcomes only |
| No qualified reviewer found | Recruitment stalls past Week 2 | Authoring may continue into quarantine; scope freeze, verdicts, release blocked; escalate to operator | Release, scope freeze |
| zIDE observability insufficient | No usage export / no model identity | Operator-mediated ledger reconciliation; automatic dispatch stays disabled | All model dispatch beyond manual |
| Token forecast blowout mid-pilot | Run cap hits >80% before 50% of lessons | Budget stop; re-estimate from actuals; operator decides revised allocation or scope revision | Further dispatch |
| Sibling-playlist near-duplicates contaminate holdout | Split-manifest probe finds cross-playlist near-matches | Group those videos into one family before freezing splits | Holdout validity |
| yt-dlp/FFmpeg breakage on capture | Live capture exit 2 / lookup failure | Pin stays `2026.8.19` (verified); local-video capture path; record failure, block affected outcomes | Affected diagrams |
| Reviewer queue saturation | Queue age grows week over week | Reduce authoring batch rate, never skip whole-lesson review | Release cadence |
| Learners unavailable | Phase 8 stalls | Hold release at "engineering-accepted"; acceptance stays incomplete; report honestly | Final acceptance |
| JSON git-ignore traps | Required evidence silently absent from recovery store | Versioned private backups, checksums, clean-workspace restore and separate public allowlist | Live production / recovery qualification |
| Holdout already exposed | Semantic discovery or shared evidence entered tuning | Retire exposed family; resolve protected access and replacement design | Evaluation claim / final acceptance |
| Stale approval or competing publisher | Candidate hash differs or release invalidated | Revision-bound approvals and serialized promotion | Promotion |
| Post-launch defect or owner absence | Learner report, failed check, unresolved incident | CF-13 containment, backup owner, bounded repair and requalification | Affected releases / production readiness |

## 17. Budget checkpoints and allocation method

Enforcement points: (a) bounded preparation allowance before model-assisted work, including agent sessions; (b) CF-04 reservation before every production/calibration dispatch, including CF-06; (c) reconcile subscription observations and outside usage at a cadence compatible with the cap, not merely weekly if that is insufficient; (d) stop at exhaustion, unresolved usage or reservation overrun; (e) separate maintenance headroom before CF-13.

Initial estimation method (heuristics below must be replaced by measured full-workflow usage in CF-04/07):

1. Measure input volume: mean transcript tokens per lecture × 105 → `corpus_input`.
2. Estimate generation: tokens_in (evidence packet) + tokens_out (lesson + quizzes + diagrams specs) per lesson × lesson count.
3. Estimate judging: coverage verdicts ≈ 2–3× lesson tokens (paragraph + quiz + lesson-context passes) on the inexpensive judge; reserve premium for generation, escalations, deep audits.
4. Add measured session/tool/context overhead, nested model work, retries, repair/escalation, images, graph/wiki extraction, discarded candidates and shared indexing. Record review time, local storage/backup growth and compute separately. Use long/difficult development sources for tail estimates and preflight usable context limits without exposing protected families.
5. `pilot_cap` = min(remaining measured quota − safety margin, estimated total need including evaluation and maintenance). This is a ceiling, not affordability proof: report a shortfall if estimated need exceeds available quota. Allocate each `run_cap` by expected bounded work within the shared remaining pilot allowance; do not rely on equal division alone.
6. Record both in the ledger config with the derivation; the CF-12 report reconciles forecast vs actual.

| Allocation | Value | Set at |
|---|---|---|
| Remaining zIDE quota | **OPEN** | CF-04 operator observation |
| Preparation allowance and prior attributable usage | **OPEN** | Operator preflight before model-assisted preparation |
| Pilot allowance | **OPEN** | CF-04 after measurement |
| Calibration / maintenance headroom | **OPEN** | CF-04 before CF-06 / CF-13 |
| Per-run allowance | **OPEN** | CF-04 after measurement |
| Measured cost per accepted lesson | **OPEN** | CF-07 then CF-12 |

## 18. Definition-of-done evidence map

| Goal checkbox | Evidence produced in |
|---|---|
| Course reprocessed from transcripts (+ needed diagrams) into lessons, quizzes, diagrams, wiki/graph, working preview | Phases 5–6; CF-07/CF-08 artifacts |
| Every segment accounted for; every released paragraph/quiz verdicted; provenance complete | CF-05 recorder + CF-08 dispositions + CF-09 coverage audit |
| Structure, teaching, Arabic prose, rendered usability pass rubric + human review; zero criticals | CF-06/CF-07 calibration + CF-08/CF-09 reviews |
| Failure tests block promotion without destroying accepted work | CF-04 probes + CF-07 seeded failures |
| Unchanged rerun = zero calls; invalidation on change; restart resumes | CF-07 proofs + CF-04 ledger tests |
| One consistent accepted set; failed update leaves last release usable; rollback shown | CF-11 drills |
| Cloudflare Pages: atomic promotion, preview validation, rollback | CF-11 |
| Zero-cash cap + 300M quota respected; unit economics reported | §17 + CF-12 |
| Source sufficiency, corrections, exclusions, frozen matrix reviewed | CF-02/02A/03 + all-source coverage and scope-revision log |
| Source-grouped holdouts, independent review, node coverage, learner trial | CF-06 splits + CF-08/CF-09 + CF-10 |
| Crash/concurrency proofs with fake provider before live dispatch | CF-04 |
| Invalidations, safe execution, withdrawal, backup restore | CF-05/07 closure and trust probes + CF-11A clean restore + CF-11 withdrawal |
| Operational cycle, ownership, monitoring, bounded maintenance, drift and migration | CF-13 runbook/rehearsal + CF-04/05 version/usage controls + §20 discovery evidence |
| Docs, license inventory, reproducible validation commands | CF-12 + updates to README/docs |

## 19. Production control register — findings and closure proofs

Integrated 2026-09-06 from a review of this plan against the other 12 top-level Markdown documents in `docs/`. This register preserves the reasons for the requirements now assigned in §§3–18 and Appendix B. **Pre-integration findings describe the earlier plan**, not a claim that its revised text still omits those requirements. All controls remain unproved until their ticket evidence is recorded; editing this plan does not close them.

This was a document review, not a runtime or visual audit. Screenshots and the [platform wireframes](wireframes/index.html) remain design references; dated provider/tool/quota/hosting observations were not reverified. The goal owns fixed scope; required controls do not grant permissions or supply missing empirical inputs. The historical blindspot review remains the rationale for earlier resolutions.

Priority: **P0** before dependent dispatch/public promotion; **P1** before production-readiness acceptance; **P2** for repeatability and measured expansion. Each finding's required work and proof is part of the named tickets. Resolve OPEN decisions within those gates; do not invent approvals.


### F01 — P0: release eligibility has contradictory definitions

**Pre-integration finding:** plan §3 makes CF-11 depend on course evaluation, without CF-10 learner acceptance. §10 permits public working notes after any three lessons are accepted. §16 says learner unavailability holds the release at engineering acceptance. [NEXT_STEPS milestone 4](NEXT_STEPS.md#4-complete-the-pilot-and-demonstrate-cloudflare-pages-release-recovery) also permits staged public lessons, while the [resolution lifecycle](content-factory-v1-resolution.md#pilot-economics-and-release-lifecycle) requires a complete prerequisite-closed course. This conflict spans documents; the original plan did not create all of it.

**Failure:** three individually accepted lessons ship with an absent prerequisite, or final publication precedes learner evidence. A STATUS banner cannot supply missing release checks.

**Required work — CF-03/09/10/11, operator and reviewers:** distinguish private engineering preview, any explicitly authorized public module, and final accepted course. Define each release's frozen membership and required evidence. Under the current authoritative contract, final course promotion requires CF-09, CF-10, current rights, prerequisite closure, and preview acceptance. If interim teaching publication is retained, reconcile it explicitly with the goal and require a reviewed standalone module scope; “3+ lessons” is not a release criterion. Use one machine-readable release predicate for manual and automated promotion.

**Proof:** missing learner evidence, a quarantined prerequisite, stale review, or pending rights blocks the appropriate promotion path. Public metadata must accurately describe incomplete scope.

### F02 — P0: the accounting boundary starts after some model work

**Pre-integration finding:** plan §17 names allocation enforcement before CF-07, but CF-06 calibration needs judges earlier. Appendix B calls agent-drafted skills and outcome matrices “No model calls.” The [quota contract](content-factory-v1-resolution.md#durable-spending-and-execution-contract) covers all v1 model work. The earlier review recorded 31,152 input tokens for one fresh empty-prompt session in a particular local setup; its context-cost report is no longer present in this checkout. Treat this as historical context and remeasure the actual zIDE workflow before allocation.

**Failure:** the ledger caps explicit pipeline calls while agent drafting, rubric research, tool results, repairs, wiki extraction, and session overhead consume the same subscription outside that ledger. “Offline” does not mean an LLM-assisted task is token-free. The historical 31,152 measurement is a warning signal, not a zIDE billing conversion.

**Required work — CF-04/06, operator:** define “no provider calls from the script” separately from “no model-assisted work.” Account for preparatory sessions and every nested model route. Establish the actual quota currency, cached/reasoning token treatment where applicable, external operator usage, observation lag, and quota-period rollover. Give CF-06 a real allocation before live calibration; all earlier model-assisted preparation needs its own accounted allowance. Unobservable usage stays an explicit limitation, with dispatch stopped where the required guarantee cannot be supported.

**Proof:** reconcile a bounded real workflow against observed subscription consumption, including agent overhead. Test quota rollover, external usage changes, and actual usage exceeding the reservation; block new work on unresolved overspend.

### F03 — P0: scope discovery can consume the supposedly sealed holdout

**Pre-integration finding:** plan §6 reserves pilot videos “not exposed during tuning,” then builds full-course outcomes; §10 processes every frozen lesson before CF-09 opens the holdout. The [pilot packet](content-factory-v1-pilot.md#bounded-challenge-cases) says reading or analyzing an excerpt makes its source family development data. The capture guide already documents inspection of `-AsaJEAav4s`.

**Failure:** a family is labeled unseen although its source, quiz answers, or defects already influenced planning or prompt changes. Full-course coverage and the current strict exposure rule can leave no eligible holdout. Merely adding a split JSON does not resolve this tension.

**Required work — CF-02/03/06, evaluation owner:** reserve families before semantic discovery; record existing exposure, including capture inspections. Define who can access protected evidence for coverage/reference work without feeding candidate selection, or explicitly reconcile the exposure rule with the evaluation protocol. Freeze prompts, rubric, model/settings and thresholds before isolated holdout production/evaluation. Record access and exposure events. If sufficient independent families cannot be preserved, report that limitation and resolve the evaluation design before claiming a valid holdout.

**Proof:** an exposure log, transitive source-family membership checks, a frozen candidate fingerprint, and rejection of an exposed replacement holdout. Multi-source lessons and shared glossary content count when checking leakage.

### F04 — P0: normalization and correction handling have no complete implementation ticket

**Pre-integration finding:** CF-01 inventories and screens variants; CF-07 starts from an evidence packet. The [goal's normalization stage](content-factory-v1-goal.md#quality-control-across-the-whole-pipeline) and [resolution correction contract](content-factory-v1-resolution.md#source-and-curriculum-contract) require traceable normalization and append-only corrections. No ticket clearly owns that entire path.

**Failure:** equal segment counts conceal a lost negation or minus sign; postprocessed text silently becomes authoritative; a reviewer approves a correction without the required source-based derivation.

**Required work — CF-02A before scope approval and repeat per source:** explicitly choose raw-only authoring or implement a versioned normalization path. Preserve immutable raw spans; record aligned transformations, uncertain text, correction evidence, reviewer disposition, and downstream impact. Enforce eligible-input selection at the actual authoring boundary, including helper tools, not just in the manifest. Coverage validation must check references, not counts alone.

**Proof:** legacy prose is rejected as evidence; a same-length altered equation is flagged; an unsupported correction quarantines the affected outcome; included/excluded/duplicate dispositions cannot hide an uncovered skill.

### F05 — P0: three-lecture discovery does not specify full-course sufficiency work

**Pre-integration finding:** CF-02 inspects first/middle/final lectures; CF-03 jumps to a frozen full outcome matrix. [NEXT_STEPS](NEXT_STEPS.md#1-freeze-source-sufficiency-and-skill-outcomes) explicitly warns that three lectures cannot accept the course. The skipped lecture's contents cannot be established from its missing transcript.

**Failure:** the matrix includes only outcomes discovered in easy samples, missing a required topic or prerequisite from the other sources. An unknown source is incorrectly declared irrelevant.

**Required work — CF-03, agent prepares and subject reviewer decides:** add full-source outcome discovery and sufficiency accounting for all 105 available sets, with review effort and evidence per outcome. Resolve the 106th record's effect from allowed evidence or retain an explicit completeness limitation/blocker; do not invent its topic. Distinguish verified historical lecture order from reviewed teaching order. Unknown historical position alone need not imply a missing prerequisite, but the plan must explain how sequencing is approved when positions remain unknown.

**Proof:** every available source contributes to the coverage/disposition audit, including sources outside the three examples; no required outcome disappears through selection. Coordinate this work with F03's protected-family access rules.

### F06 — P0: valid cache keys do not implement dependency invalidation

**Pre-integration finding:** CF-05/06 list cache-key inputs; the [resolution invalidation table](content-factory-v1-resolution.md#format-identity-and-dependency-boundaries) requires shared-term, source, paragraph-placement, prerequisite, and concept-merge propagation. The plan's §18 assigns this proof without a corresponding complete ticket.

**Failure:** the edited lesson is rejudged while a wiki definition, simplified explanation, assessment, or another lesson remains stale. Approval records survive a content edit because only model verdicts were invalidated.

**Required work — CF-05/07:** implement a build-dependency graph distinct from the semantic graph, typed change events, transitive invalidation, and approval records bound to exact artifact/release revisions. Source corrections, review changes, rubric/model changes, and rendering-only changes need explicit rules. Reject undeclared dependencies and references to absent nodes.

**Proof:** change a shared sign convention, move a paragraph, split a concept, and replace a diagram. Compare expected and actual invalidation closure, including human reviews and rendered checks. Unchanged unaffected artifacts retain valid cached work.

### F07 — P0: request states are specified; artifact and release states are not

**Pre-integration finding:** CF-04 defines provider-attempt transitions; CF-08 allows parallel production after ledger concurrency tests. The [resolution](content-factory-v1-resolution.md#durable-spending-and-execution-contract) explicitly separates request success, valid output, acceptance, and publication. The [capture guide](KEYFRAME_CAPTURE.md#failure-and-review-behavior) requires one process per output-video directory.

**Failure:** quota-safe workers overwrite the same lesson/capture; an old worker commits after a newer review; an exhausted repair lineage is reset by creating a new unit ID. A successful API call is accidentally promoted as accepted content.

**Required work — CF-04/05/08:** define candidate, validated, reviewed, accepted, quarantined, superseded, and invalidated artifact transitions; define release transitions separately. Use revision-checked commits and exclusive ownership/leases where workers share output paths. Tie split/merge lineage to retry and repair limits; define what an authorized new revision can reset. Preserve successful outputs before retrying downstream persistence work.

**Proof:** two workers target the same unit; a stale worker attempts to publish; capture workers contend; a reviewer signs revision A while revision B is written. Only the intended current revision can become accepted.

### F08 — P0: production evidence lives outside Git without an early recovery contract

**Pre-integration finding:** plan §4 keeps manifests local; §8 keeps provenance sidecars local; §16 treats globally ignored JSON as having no blocker. CF-11 specifies backup restore, but does not name the full recoverable state. [Inventory](content-factory-v1-inventory.md#reproducible-method) also depends on a consistent private local DB snapshot.

**Failure:** a new clone or lost workstation cannot reconstruct why a published lesson passed, recover unknown spend reservations, or rebuild editable diagrams. Restoring HTML alone restores a website, not the factory.

**Required work — CF-04/05, prove in CF-11:** define separate durable stores for immutable evidence, editable content, verdicts/reviews, ledger, configuration, and public bundles. Start backup before live production. Specify consistent snapshot/restore order, checksums, schema versions, retention, storage capacity, and independently stored copies. Keep sensitive records out of public bundles. Credentials need a separate recovery procedure, not inclusion in content backups.

**Proof:** restore into an empty workspace from the independent copy, validate evidence and ledger consistency, reproduce the accepted bundle using cached artifacts without model calls, and preserve uncertain reservations. Narrowly version synthetic fixtures/config schemas where appropriate; local JSON is not automatically disposable.

### F09 — P0: deployment drills do not yet define the production control boundary

**Pre-integration finding:** CF-11 says preview → validation → atomic promotion, rollback, withdrawal. It does not identify the immutable candidate, competing-release handling, public bundle allowlist, or all reachable old deployment URLs.

**Failure:** preview approval applies to different bytes than production; a second publisher promotes stale content; source packets, judge answers, or learner data enter the static directory; withdrawal fixes the primary URL but leaves an invalid preview publicly accessible.

**Required work — CF-11, release operator:** promote the exact validated bundle by release ID/hash, serialize production promotion, recheck current approvals/rights immediately before promotion, and record deployment identity. Allowlist public files and scan the actual bundle. Verify available hosting controls for preview access, historic deployments, redirects, caching, withdrawal, and failed/ambiguous promotion. Do not assume current Cloudflare behavior from this review.

**Proof:** concurrent promotions, a last-minute invalidation, an injected private fixture, ambiguous deployment completion, and access to old URLs after withdrawal. Document limits: already downloaded copies cannot be remotely recalled.

### Ongoing production controls

### F10 — P1: the plan ends at a report, not an operating handover

**Pre-integration finding:** CF-12 ends with economics and expansion. Existing rollback/withdrawal drills do not specify day-to-day detection, triage, or ownership after launch.

**Required work — CF-13, operator and named reviewers:** add a visible “report a problem” route carrying lesson/node/release IDs; a private incident record; severity and acknowledgement/containment targets; a review cadence; and a backup owner. Correctness and rights incidents must find every affected derivative/release, invalidate unsafe rollback targets, withdraw as needed, repair using allowed evidence, re-review, republish, and verify the public result. Record a regression case and maintenance cost. Choose response targets explicitly; do not imply unattended monitoring from an occasional operator check.

**Proof:** run that entire loop on one deliberately seeded post-publication defect, including the learner-facing correction note. Measure detection, containment, and restoration times against the chosen targets.

### F11 — P1: monitoring covers production throughput, not learner service health

**Pre-integration finding:** CF-08's weekly report covers tokens, queue age, accepted counts and cache hits. CF-11 validates preview, with no recurring public checks.

**Required work — CF-11/13:** define lightweight checks for public availability, expected release ID, broken assets/routes, quiz behavior, and backup freshness, with an owner and cadence. Add stage timeouts, stuck-job detection, queue limits and disk-capacity stops. Define what happens when the operator, reviewer, model service, or host is unavailable for an extended period. Monitoring must fit the zero-cash boundary and its actual unattended capabilities.

**Proof:** break a public asset, fill the output volume in a disposable fixture, stall a job, and miss a scheduled backup. Each produces an actionable record rather than a misleading success status.

### F12 — P1: learner findings do not have a defined return path to acceptance

**Pre-integration finding:** CF-10 says observe, revise, resolve critical failures. CF-09 runs earlier; there is no explicit reevaluation loop after those revisions. Five to eight learners are specified without assigning outcome/task coverage.

**Required work — CF-10/09/11:** bind the trial to the tested release and selected outcomes; define the performance criterion and task coverage before use. Keep fresh unaided tasks separate from worked solutions, hints and public quizzes. A critical finding reopens affected artifact/review gates; prompt or rubric tuning also exposes the holdout and triggers F03. Reassess revised teaching with an appropriate fresh task and record which outcomes have direct learner evidence versus only review evidence. Avoid implying that every outcome was learner-tested by a small sample.

**Proof:** one trial failure leads to a tracked revision, correct invalidation, independent acceptance, and a documented reassessment. No final release consumes superseded learner evidence silently.

### F13 — P1: human review is a role list, not a workable review system

**Pre-integration finding:** the plan names reviewer vacancies and per-lesson review, but no review queue schema, disagreement resolution, substitute authority, or challenge-domain reviewer coverage. The [inventory challenge notes](content-factory-v1-inventory.md#earlier-pilotchallenge-candidates--historical) specifically call out physics expertise.

**Required work — CF-03/06/08:** retain assignments, competency by case/domain, content revision, independent reference decision, disposition, timestamps and discrepancy resolution. An optics title alone does not establish English/digital-logic expertise. Separate blind reference labeling from review after model feedback. Agree measurable weekly capacity and stop/backpressure rules. Schedule full-course sufficiency review as well as final lesson review.

**Proof:** a disputed answer and an unavailable reviewer have an explicit routing/blocking outcome; an agent cannot synthesize approval. Replace calendar guesses with measured lesson/outcome volume and reviewer availability after the engineering trial.

### F14 — P1: static quizzes have an unresolved answer-visibility contract

**Pre-integration finding:** CF-05/11 require answers not exposed before an attempt, while delivering static client-side artifacts. No threat model or distinction between practice and assessment is stated.

**Required work — CF-05/10:** for formative practice, define no premature answer display through the normal UI, accessibility tree, hints, search snippets, or print view. A self-contained static quiz that evaluates answers locally necessarily gives the client enough information to inspect them; it cannot promise exam secrecy. Keep the learner trial's independent task/answer materials outside the public bundle. Define numerical tolerance, units, multiple valid answers, retry/hint behavior, and how free-response optics work is scored.

**Proof:** keyboard/screen-reader attempts and print/search paths do not reveal practice answers prematurely; the trial answer packet is absent from every public artifact. Independently check derived task solutions and convention-dependent answers.

### F15 — P1: diagram identity and teaching correctness can drift together

**Pre-integration finding:** the [capture guide](KEYFRAME_CAPTURE.md#failure-and-review-behavior) says YouTube ID is not an immutable media revision, local identity is caller-supplied, timestamps are not guaranteed frame-exact, and caches need refresh after edits. CF-07 mainly records ID/time/PNG hash.

**Required work — CF-02A/07:** bind each accepted visual to the captured bytes, fetch/capture metadata, matching-lecture identity evidence, reviewed timestamp alignment and reviewer disposition. Preserve evidence when a live video changes. Record source-supported derivations for redraws and new exercises. An optics checklist should cover the course's own sign conventions, units, ray directions, labels and diagram/text agreement; do not import missing conventions from model memory.

**Proof:** simulate an edited/retimed upload or wrong local file, unreadable labels, and a redraw with a reversed ray. Refresh must create a new evidence revision and invalidate affected outputs, never silently replace accepted pixels.

### F16 — P1: accessibility is a checklist without a declared test environment

**Pre-integration finding:** CF-05 says “WCAG-minded”; CF-11 lists visual and interaction checks. The [historical discovery probes](content-factory-v1-blindspots.md#discovery-probes-for-unknown-unknowns) explicitly included an Arabic screen reader.

**Required work — CF-05/07/11:** declare supported browser/device/assistive-technology combinations and concrete acceptance criteria. Include Arabic reading order, mixed-direction equations, accessible math/diagram alternatives, zoom/reflow, keyboard quizzes, feedback announcement, missing-font fallback, slow assets and long lessons. Test one difficult real lesson early, then the final bundle. Adopt a dated accessibility reference during implementation; do not claim conformance from “WCAG-minded.”

**Proof:** retain reproducible failures and reviewer checks from actual assistive-technology use, not just screenshots or automated contrast output.

### F17 — P1: content execution controls lost their required failure probes

**Pre-integration finding:** CF-07 tests injected markup, but the [resolution execution contract](content-factory-v1-resolution.md#durable-spending-and-execution-contract) also requires path/URL allowlists, instruction isolation, and restricted executable examples. §18 claims safe-execution evidence without an explicit implementation path for all of it.

**Required work — CF-05/07:** enforce these boundaries in the parser, asset resolver, judge membership validator and any execution worker. Include diagram/SVG exports and generated derivatives. If the pilot executes no code, record that and reject executable content; do not build an unnecessary general sandbox. If challenge cases execute code, the disposable resource-limited worker is required there.

**Proof:** source instructions cannot select verdict IDs or invoke tools; traversal, forbidden URL schemes, active SVG content and oversized inputs fail safely. Where execution exists, time/memory/process and filesystem/network limits are exercised.

### F18 — P1: rights and learner records need artifact-level handling

**Pre-integration finding:** rights are OPEN until promotion; CF-10 records learner failures; CF-11 ships public working/release notes. There is no artifact-level permission record or public/private data rule.

**Required work — CF-01/10/11/13:** link permission evidence and unresolved status to source/asset revisions and affected releases; inventory selected dependencies/fonts and required notices. Record learner participation/recording choices, restrict identifiable observations to a private store, choose retention/deletion handling, and publish aggregate findings. Do not infer permission from file availability or put review packets into public working notes.

**Proof:** expired/revoked/missing approval blocks or withdraws the affected bundle; a synthetic learner identifier and private review attachment cannot enter public output. This is an operational records requirement, not a legal determination of permission.

### F19 — P1: provider and schema drift have no maintenance policy

**Pre-integration finding:** cache keys include versions, but the [resolution](content-factory-v1-resolution.md#format-identity-and-dependency-boundaries) also requires mutable-model resolution/fingerprint where available and drift audits. The plan provides no update cadence, canary, or schema migration procedure.

**Required work — CF-04/05/13:** record observable model/settings and tool/schema versions; keep representative development canaries; define what change triggers recalibration and invalidation. Version persistent ledger/artifact schemas and prove migration from a backed-up prior version. Distinguish rebuilding a published bundle from reproducing a historical model response, which may be impossible.

**Proof:** simulate a model alias change, parser upgrade and interrupted schema migration. Stale acceptance is rejected, prior durable artifacts survive, and the cost of required reevaluation is recorded.

### F20 — P2: the capacity model omits the expensive tails and ongoing work

**Pre-integration finding:** plan §17 extrapolates three lectures and uses approximate judging multiples; §15 gives a nine-week schedule. [Skills-map costs](skills-map.md#cost-picture-cost-effective-by-design) include extraction, local resources and human work; the context report adds material per-session overhead. CF-12 reports maintenance separately but no maintenance cycle generates that evidence.

**Required work — CF-04/07/08/12/13:** measure full assembled prompts, context limits, batch overhead, tool/agent usage, reasoning/output where observable, repair tails, images, wiki/graph, discarded candidates, human minutes, storage and backup growth. Sample difficult sources beyond the strongest trial lesson without exposing protected families. Include maintenance, evaluation and emergency-repair headroom. Treat `min(remaining quota, estimated need)` as a spending ceiling, not proof the scope is affordable; report the funding/quota shortfall explicitly. Allocate runs by expected work rather than equal division alone.

**Proof:** low/base/high forecasts use measured volumes and queue throughput; one maintenance repair has a recorded cost; a long lesson exceeding usable context fails before dispatch or is split through a tested coverage-preserving path.

### F21 — P2: “full production” needs an explicit boundary with platform v1

**Pre-integration finding:** the [goal's delivery sequence](content-factory-v1-goal.md#delivery-sequence) defers the broader platform and framework comparison. The [platform brief](platform-map-brief.md) includes persistent progress, reader navigation, richer graph interaction and a stack-comparison blog; CF-11 supplies a minimal renderer and selected public surfaces. [Fanout's mapping](fanout-feature-analysis.md#5-mapping-to-the-iug-platform) also mixes immediate and later patterns.

**Required work — CF-03/05/11:** publish a small delivery matrix: required for this factory pilot, explicitly deferred platform capability, or unresolved product decision. The [platform wireframes](wireframes/index.html) do not confer implementation or acceptance. For features actually shipped, specify behavior and tests: resume/progress reset and revision migration if progress exists; stable lesson/node routes and moved-link handling; glossary/graph navigation and empty states. Do not introduce accounts, payments, live tutoring or the whole-corpus graph merely to call the pilot production-ready.

**Proof:** the delivered course supports its promised learner journey end to end, and the completion report states which broader platform capabilities remain deferred.

## 20. Discovery drills and operational qualification

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

## 21. Open decisions and execution handoff

The plan already identifies reviewer/learner availability, source and font permissions, lecture order, skipped-source disposition, actual zIDE capabilities and remaining quota, numeric allocations and calibrated thresholds. They remain dependencies, not findings to relabel as surprises.

Additional decisions to record during the existing tickets: final versus interim release contract; holdout access/exposure policy; full model-accounting boundary; production owner/backup and response targets; independent backup capacity and retention; learner-record handling; static assessment semantics; supported accessibility environments; and the exact factory/platform boundary. None should be filled with invented approvals or measurements.

CF-01 remains the immediate offline implementation task. Apply this plan's accounting rule to any model-assisted preparation. Resolve F01–F03 decisions before their dependent work; implement F04–F09 before dependent production/promotion. CF-13's complete operational rehearsal precedes CF-12 production-readiness acceptance. Record completion evidence beside each finding ID in the pilot report; a checklist entry is not proof.

## Appendix A — commands verified on this machine (2026-09-06)

```bash
# Tests (baseline now 181 passing)
.venv/bin/python -m pytest

# Inventory snapshot (offline, refuses nonempty WAL)
python3 scripts/inventory_content_factory.py --output /tmp/content-factory-inventory.json

# Keyframe capture — plan, then capture (FFmpeg required)
python3 scripts/capture_keyframes.py GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/-AsaJEAav4s_chapters.json --dry-run
uv run --isolated --no-project --with 'yt-dlp[default]==2026.8.19' \
  python scripts/capture_keyframes.py GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/-AsaJEAav4s_chapters.json
# exit 0 = all captured/reused · 1 = some failed · 2 = setup error

# Playlist-order metadata fetch (Phase 1; identity/order only)
uv run --isolated --no-project --with 'yt-dlp[default]==2026.8.19' \
  yt-dlp --flat-playlist --print '%(playlist_index)s\t%(id)s\t%(title)s\t%(duration)s' \
  'https://www.youtube.com/playlist?list=PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-'
```

Read-only DB pattern (used for every fact in §1): copy `youtube-iug.db` to a temp dir, open `mode=ro&immutable=1`, refuse a nonempty WAL, and select only non-private columns.

## Appendix B — session briefs for the remaining tickets

Each block is copied into a fresh zIDE session, one ticket per session, after its dependencies pass. Every brief includes its assigned §19 controls and §20 proofs. CF-01's brief is in [NEXT_STEPS.md](NEXT_STEPS.md); also apply this plan's §4 and preparation-accounting rule. “No model calls” means no provider dispatch from the implementation script; it never excludes agent-session usage from the allowance.

**CF-02 — lecture order and selection**

```text
Implement CF-02 for OPTO 2311 (playlist PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-).

Mandatory integrated controls: Before semantic discovery, reserve candidate evaluation families and record prior exposure, including capture inspections. Follow F03/F05; metadata access does not authorize teaching evidence. Account for agent preparation under CF-04 preflight.
Read docs/README.md, docs/NEXT_STEPS.md, docs/content-factory-v1-goal.md,
docs/content-factory-v1-pilot.md, docs/pilot-opto-2311-plan.md §5, and the
CF-01 manifest/report if present.

Fetch the YouTube playlist order with the pinned yt-dlp 2026.8.19 isolated
environment (--flat-playlist, metadata only). Save
artifacts/opto-2311/lecture-order.json with fetch date + tool version.
Cross-check transcript verbal sequence references and chapter hints;
record any position you cannot establish as unknown — never invent order.
Reconcile the ordered list against the 105 local transcript sets and the
skipped ID SAq013FtOLQ (keep it visible, skip=1).

Then select first/middle/final lectures by verified order. For each, draft
2-3 candidate tangible skills with original transcript spans, required
diagrams (video ID + timestamp; keyframe hints are hints, not proof), and a
supported/needs_youtube_diagram/unsupported classification. Write the
three-lecture skill sheet to docs/opto-2311-first-review.md for the subject
reviewer, including one worked example and one unseen task per lecture.

No provider calls from the script. No lecture downloads. Transcripts are the only teaching
source; metadata is for order/hints only. Report ordering evidence quality
and what the reviewer must decide.
```

**CF-02A — normalization and evidence preparation**

```text
Implement CF-02A. Read this plan §5 (CF-02A), §19 F03-F05/F15,
the CF-01/02 outputs, and the resolution source/correction contract.

Choose raw-only authoring or implement versioned normalization with
immutable segment identities, traceable transformations, uncertain spans,
and append-only correction records. Enforce eligible input roles at every
authoring/helper boundary; reject legacy/external teaching evidence.
Prepare all available source sets under the protected-family access policy.
Bind permitted diagrams to captured bytes, matching identity, time alignment
and review; changed media creates a new revision.

Test same-length semantic corruption, unsupported corrections, excluded
outcome coverage, wrong media identity and changed captures. Record outputs
separately and preserve raw evidence. Required reviewers supply approvals;
agent preparation uses its accounted allowance. No production authoring.
```

**CF-03 — scope freeze**

```text
Implement CF-03 for OPTO 2311. Read docs/pilot-opto-2311-plan.md §6, the

Mandatory integrated controls: Require CF-02A evidence and full-source discovery across all 105 available sets; three lectures cannot freeze the full curriculum. Resolve F01/F03/F05/F13/F21: release membership, protected-family access, skipped-source limitations, reviewer capacity, and the factory/platform delivery matrix. Do not relabel exposed families as unseen.
CF-02 outputs, and docs/content-factory-v1-resolution.md (source and
curriculum contract).

Build artifacts/opto-2311/outcome-matrix.json: one record per promised
outcome (outcome_id, tangible task, prerequisites, intended learner,
evidence refs, required explanation/example/practice/transfer-task IDs,
sufficiency status supported|needs_youtube_diagram|unsupported). Group
outcomes into prereq-closed lessons in verified lecture order. Record the
SAq013FtOLQ disposition decision path. Keep the three challenge
excerpts (فيزياء عامة أ video `1noCDAkxHwg`; اللغة الإنجليزية video `0mkSe0xrqKk`; digital-logic `Kzxd5D8ZgnQ` at 13:37) as
development-only data and confirm the pre-discovery candidate holdout families and exposure log, grouped by source-video family (include the
sibling optics playlists from the CF-01 appendix in the family watchlist).

Write docs/opto-2311-scope-freeze.md summarizing the matrix, lesson plan,
reserved families, and every remaining OPEN input (reviewer names, token
allocations). Mark the freeze as DRAFT until operator + reviewer sign-off.
No provider calls from the script; no lesson authoring. Agent preparation usage remains accounted.
```

**CF-04 — quota ledger**

```text
Implement CF-04. Read docs/pilot-opto-2311-plan.md §7 and

Mandatory integrated controls: Apply F02/F07/F08/F19/F20. Account for preparation sessions and nested model/context usage; allocate live CF-06 calibration before dispatch. Test quota rollover, outside usage and reservation overruns; establish durable private backups before live work. Observe and reconcile a bounded real workflow only after the fake probes and allocation gate pass. Missing observability remains a blocker.
docs/content-factory-v1-resolution.md (durable spending contract).

Build a SQLite spend ledger in this repo: pilot allowance, run
allocations, integer-token reservations with states
reserved|dispatched|succeeded|failed_confirmed|outcome_unknown, durable
per-unit attempt/repair/escalation lineage, and reconciliation of observed
usage. Dispatch is refused without a successful reservation; unknown
outcomes retain their reservation across restarts.

Write failure-probe tests with a FAKE provider adapter: crash before
dispatch / after dispatch / after receipt / before usage commit; response
loss; two workers contending for the last allowance; restart after repair
exhaustion; provider unavailable; artifact persistence failure. All must
block or quarantine without losing accepted work or silently releasing
reservations.

Keep implementation and failure probes fake-only. The operator's zIDE
observations (remaining quota, usage export behavior) are operator inputs;
leave an allocations.toml-style config with OPEN placeholders until measured.
After fake probes pass and a bounded allowance is recorded, qualify the
real boundary through observed workflow reconciliation. Document the mediated
workflow and distinguish fake proof from the real capabilities still OPEN.
```

**CF-05 — format and validators**

```text
Implement CF-05. Read docs/pilot-opto-2311-plan.md §8 (CF-05) and

Mandatory integrated controls: Implement F06/F07/F08/F14/F16/F17/F19/F21: artifact states, revision-bound approvals, dependency invalidation, output ownership, durable schemas/backups, static practice semantics, accessibility environments, and trust boundaries for paths/URLs/SVG/execution. Preserve private evaluation answers outside public bundles. A content hash alone is not approval.
docs/content-factory-v1-resolution.md (format/identity/dependency
sections).

Define the versioned lesson Markdown dialect: math subset, tables, stable
teaching-node IDs with split/merge history, fenced quiz payloads
(stable ID, skill refs, prompt, choices/task, answer, rationale, feedback;
no answer leakage before an attempt), provenance sidecar schema, and a
segment-disposition record (included|duplicate_of|excluded_with_reason|
unresolved). No arbitrary JS/MDX/raw HTML/event handlers.

Implement deterministic validators + conformance fixtures (valid docs,
each violation class, RTL/mixed-direction cases, quiz schema failures,
ID split/merge cases). Build the minimal static RTL-first HTML preview
renderer (Thmanyah faces, WCAG-minded checks) conforming to the dialect.
Cache keys must include content hash, evidence refs, lesson context,
rubric/prompt/model/schema versions; quiz placement and graph deps in the
relevant keys.

No provider dispatch from the implementation script. Report conformance
results and any dialect decision the
reviewer/operator must ratify.
```

**CF-06 — rubric and evaluation harness**

```text
Implement CF-06. Read docs/pilot-opto-2311-plan.md §8 (CF-06),

Mandatory integrated controls: Apply F02/F03/F13/F19: allocated real calibration, protected-family exposure log and transitive grouping, competent independent reference reviewers, frozen prompt/rubric/model/settings, and drift canaries. Full-course production must respect the protected access protocol. Report a blocked evaluation design if no eligible families remain.
docs/content-factory-v1-resolution.md (evaluation protocol), and
docs/skills-map.md §7.

Research and write docs/COURSE_RUBRIC.md (Bloom, backward design,
cognitive load, retrieval practice, worked examples): four checks
(evidence support, subject correctness, editorial/pedagogical
contribution, cross-lesson coherence), an explicit hard-failure list,
teaching-bearing node coverage (paragraphs, math, code, tables, quiz
choices/keys/rationales, diagrams+alternatives, wiki entries,
simplified explanations), and threshold fields to be calibrated.

Build the judge harness: batched inexpensive-judge coverage verdicts with
stable IDs (missing ID = failure; malformed judge output = failure),
whole-lesson context, premium-escalation path, verdict caching per the
CF-05 key rules, and report generation with named denominators
(bad_accepted/known_bad, good_rejected/known_good, lessons-with-criticals).

Construct the Arabic-first reference sets (good + the 12 required failure
classes + English + mixed-direction cases) with a human-labeling worksheet
— labels are recorded BEFORE any judge score. Build the source-family
split manifest (development vs holdout; holdout stays sealed).

Dispatching judges requires the CF-04 ledger; without recorded allocations,
run in fake/dry mode only. Report calibration plan and OPEN thresholds.
```

**CF-07 — engineering trial lesson**

```text
Implement CF-07. Read docs/pilot-opto-2311-plan.md §9, the frozen scope

Mandatory integrated controls: Apply F04/F06/F07/F14/F15/F16/F17/F20 and relevant §20 drills: prove shared-convention/paragraph/concept/diagram invalidation closure, stale-worker rejection, media revision identity, Arabic assistive-technology behavior and input/execution isolation. Measure full prompts, overhead and context limits; keep deliberately invalid candidates private.
(sign-off required before dispatch), COURSE_RUBRIC.md, and the CF-05/06
implementations.

Produce ONE complete lesson end-to-end from the scope's strongest middle-
lecture outcome: evidence packet (transcript spans + captured diagrams
with video ID/timestamp/hash), outline, section-by-section authoring with
source-coverage checks, worked example + practice + independent transfer
task, inline quizzes, one Excalidraw diagram (editable source + export +
Arabic alt text, redrawn without invented labels), wiki entry, graph
nodes/edges, and segment dispositions for the lecture.

Run deterministic validators, then judge verdicts (whole-lesson context)
through the CF-04 ledger with reservations. Produce the unit-economics
report (tokens per stage incl. retries, review minutes placeholder).

Prove: unchanged rerun makes zero generation/judging calls; interrupted
run resumes; seeded failures (wrong quiz key, unsupported claim, broken
asset, missing verdict, injected markup) each block promotion. Submit the
lesson to the subject + editorial reviewers with reference decisions
recorded before judge scores. Report defects and rubric/prompt tuning
needed BEFORE any holdout opens.
```

**CF-08 — course production**

```text
Implement CF-08. Read docs/pilot-opto-2311-plan.md §10 and the frozen

Mandatory integrated controls: Apply F07/F08/F11/F13/F20. Parallelize only after artifact ownership as well as ledger concurrency passes; capture directories remain single-writer. Enforce review backpressure, stuck-job/time/disk limits and backups. Public teaching must satisfy §3; no lesson-count shortcut. Protect CF-06 families during production.
scope. Use the proven CF-07 loop per lesson in prereq-closed course order.

Enforce per lesson: reservations + lineage limits (<=2 retries, 1 repair,
1 premium escalation — durable), quarantine on exhaustion, segment
dispositions, whole-lesson verdicts, reviewer queue entries. Parallel
workers only after CF-04 concurrency tests pass. Emit a weekly status
report: tokens vs run cap, accepted/quarantined counts, queue age, cache
hit rate.

Any scope change = new scope revision + re-review + invalidation of
affected artifacts (per the resolution invalidation table). Never skip
whole-lesson review; never relax the rubric to improve yield. If the run
cap is exhausted, STOP, report, and wait for an operator allocation
decision. Coordinate CF-11 previews; public teaching follows §3 eligibility
and requires explicit resolution of the interim-module contract.
```

**CF-09 — course-level evaluation**

```text
Implement CF-09. Read docs/pilot-opto-2311-plan.md §11 and

Mandatory integrated controls: Apply F03/F06/F12/F13. Bind results to the exact candidate; include the exposure log and independently competent labels. Reopen affected checks after learner or maintenance changes. Any tuning retires the exposed holdout; unresolved replacement design blocks the claim.
docs/content-factory-v1-resolution.md (evaluation + release thresholds).

Run the challenge set (three bounded cases) with the frozen thresholds;
then open the sealed holdout. Report bad_accepted/known_bad,
good_rejected/known_good, judge-human disagreement by source family, and
lessons-with-any-critical-defect. If any result drives a tuning change,
declare the holdout exposed: it becomes development data and a fresh
holdout is required.

Complete the course-coherence audit: prerequisite closure and acyclicity,
cross-lesson contradiction probe, concept merge/alias review, full
teaching-node verdict coverage, outcome-matrix closure, and explicit
denominators everywhere. Block release on any unresolved critical defect.
```

**CF-10 — learner trial**

```text
Prepare CF-10. Read docs/pilot-opto-2311-plan.md §12 and

Mandatory integrated controls: Apply F12/F14/F18. Bind trial and outcome coverage to the tested revision, keep answer keys and identifiable observations private, record participant choices/retention handling, and report untested outcomes. Critical findings return through invalidation, repair, independent review and fresh-task reassessment before final promotion.
docs/content-factory-v1-resolution.md (learner protocol).

Draft before the trial: recruitment screen (Arabic-speaking
undergraduates with the reviewer-confirmed optics prerequisites, 5-8
learners), prerequisite/baseline task, reading+practice session script,
fresh unaided transfer task with its scoring rubric, observation sheets,
and the delayed-retention variant (only if retention is claimed).
Define the learner-performance criterion in writing BEFORE administering
the final task.

Agent work is preparation and the report template only — the operator
recruits and schedules learners. After the trial: record every observed
failure, the revisions made, and the report's explicit limitations
(formative evidence, not causal claims).
```

**CF-11 — release engineering**

```text
Implement CF-11. Read docs/pilot-opto-2311-plan.md §13,

Mandatory integrated controls: Complete CF-11A qualification in §13 before promotion. Apply F01/F08/F09/F10/F11/F16/F17/F18/F19 and §20: restore into an empty workspace, rebuild with cached evidence and preserved reservations, allowlist public files, and verify historic-URL withdrawal behavior. Serialize promotion of the exact preview-approved hash and recheck current CF-09/10, rights and reviews. Prepare CF-13 ownership/runbook before launch; verify the live release afterward.
docs/content-factory-v1-goal.md (deployment rules), and
docs/fanout-feature-analysis.md §3.12/§4.

Build the static release pipeline: build one complete versioned artifact
set from accepted artifacts only -> deterministic checks -> Cloudflare
Pages preview -> recorded preview-validation checklist (Arabic/English,
mobile/desktop RTL clipping, keyboard, focus, contrast, reduced motion,
quiz interaction without answer leakage) -> atomic promotion. Verify
current Pages limits in this task.

Demonstrate with recorded evidence: an intentionally failed update leaves
the last accepted release usable; rollback to the accepted version;
withdrawal when every available version is invalid; restore from an
independent backup.

Add the build-in-public surfaces (RTL-first, Thmanyah): STATUS banner,
public working-notes page listing accepted lessons, pilot roadmap graph
page once graph artifacts exist, one coherent free module as the public
taste test, and an illustrated release-notes page. Presentation never
lowers the acceptance bar: only accepted lessons are public.
```

**CF-13 — operate, repair and republish (before CF-12 final acceptance)**

```text
Implement CF-13. Read §14, §19 F10-F13/F18-F20 and §20, plus the
CF-11 qualification/release record. Prepare the runbook before promotion.

Create docs/opto-2311-operations.md, private incident/change records,
release-linked problem reporting and lightweight public health/backup
checks. Name operator/backup/reviewer coverage and record actual response
targets and cadence; leave missing human decisions OPEN.

Rehearse a seeded defect in a private production-equivalent environment:
report -> affected evidence/dependencies/releases -> containment and
invalid rollback exclusion -> source-supported append-only correction ->
budgeted repair -> independent reviews and required evaluation/learner
rechecks -> exact-bundle promotion -> verified fix and correction note.
Never intentionally publish known-invalid teaching to learners.

Record regression evidence, response/recovery times, actual maintenance
spend, backup/restore and model/parser/schema drift/migration probes.
Unknown usage, absent approval or failed qualification blocks the repair
release. Hand the evidence to CF-12; ongoing operations continue afterward.
```

**CF-12 — pilot report**

```text
Implement CF-12. Read docs/pilot-opto-2311-plan.md §14 and §18 and the

Mandatory integrated controls: Complete CF-13 operational rehearsal first. Include every F01-F21 closure/limitation and relevant §20 drill evidence, measured maintenance cost and response times, clean restore/migration proofs, owner/backup coverage, and the explicit deferred-platform matrix. Record an evidence-based expansion or retirement decision; never mark missing empirical proofs complete.
goal's v1 definition of done.

Write docs/opto-2311-pilot-report.md: first-accepted lesson IDs and
accepted outcome coverage (revisions/maintenance separate); tokens per
accepted lesson including failures and shared overhead; reuse/cache hit
rates; repair and quarantine rates; judge disagreement; reviewer minutes
and queue stats; learner-trial results with limitations; defect counts
with named denominators (challenge/holdout/audit separate); source
record (SAq013FtOLQ disposition, exclusions with reasons, rights status).

Map every goal definition-of-done checkbox to its evidence pointer
(docs/pilot-opto-2311-plan.md §18). Forecast the wider corpus from
measured token volumes with low/base/high scenarios; playlist counts are
not cost estimates; no affordability claim beyond pilot evidence. Close
with the expansion decision: measured batch sizing, and the documented
rationale if the runner-up course replaces optics as representative.
```
