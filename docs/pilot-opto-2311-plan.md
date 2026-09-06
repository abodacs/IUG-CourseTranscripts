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

Relative weeks from adoption (2026-09-06); dates stretch/compress on human availability, not on agent time.

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

Each block is copied into a fresh zIDE session, one ticket per session, after its dependencies pass. CF-01's brief is in [NEXT_STEPS.md](NEXT_STEPS.md).

**CF-02 — lecture order and selection**

```text
Implement CF-02 for OPTO 2311 (playlist PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-).
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

No model calls. No lecture downloads. Transcripts are the only teaching
source; metadata is for order/hints only. Report ordering evidence quality
and what the reviewer must decide.
```

**CF-03 — scope freeze**

```text
Implement CF-03 for OPTO 2311. Read docs/pilot-opto-2311-plan.md §6, the
CF-02 outputs, and docs/content-factory-v1-resolution.md (source and
curriculum contract).

Build artifacts/opto-2311/outcome-matrix.json: one record per promised
outcome (outcome_id, tangible task, prerequisites, intended learner,
evidence refs, required explanation/example/practice/transfer-task IDs,
sufficiency status supported|needs_youtube_diagram|unsupported). Group
outcomes into prereq-closed lessons in verified lecture order. Record the
SAq013FtOLQ disposition decision path. Reserve the three challenge
excerpts (فيزياء عامة أ video `1noCDAkxHwg`; اللغة الإنجليزية video `0mkSe0xrqKk`; digital-logic `Kzxd5D8ZgnQ` at 13:37) as
development-only data and list candidate holdout families from pilot
videos not exposed so far, grouped by source-video family (include the
sibling optics playlists from the CF-01 appendix in the family watchlist).

Write docs/opto-2311-scope-freeze.md summarizing the matrix, lesson plan,
reserved families, and every remaining OPEN input (reviewer names, token
allocations). Mark the freeze as DRAFT until operator + reviewer sign-off.
No model calls, no authoring.
```

**CF-04 — quota ledger**

```text
Implement CF-04. Read docs/pilot-opto-2311-plan.md §7 and
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

Do not call any real model. The operator's zIDE observations (remaining
quota, usage export behavior) are operator inputs; leave an
allocations.toml-style config with OPEN placeholders and document the
mediated-reconciliation workflow. Report what the fake-adapter suite
proves and what it cannot.
```

**CF-05 — format and validators**

```text
Implement CF-05. Read docs/pilot-opto-2311-plan.md §8 (CF-05) and
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

No model calls. Report conformance results and any dialect decision the
reviewer/operator must ratify.
```

**CF-06 — rubric and evaluation harness**

```text
Implement CF-06. Read docs/pilot-opto-2311-plan.md §8 (CF-06),
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
decision. Coordinate with CF-11 for interim build-in-public releases of
the complete accepted set so far.
```

**CF-09 — course-level evaluation**

```text
Implement CF-09. Read docs/pilot-opto-2311-plan.md §11 and
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

**CF-12 — pilot report**

```text
Implement CF-12. Read docs/pilot-opto-2311-plan.md §14 and §18 and the
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
