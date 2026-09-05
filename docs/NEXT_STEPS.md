# Next steps — Content Factory v1

**Start Ticket CF-01: build a trustworthy source manifest for the optics pilot.** Copy the task brief at the end into your next zIDE session. Allow about 5 minutes to read this guide.

**Current position: preparation, before v1 execution.** Existing inventory and legacy integrity safeguards are available. The source manifest, zIDE quota integration, quality gates, lesson renderer, and deployment still need implementation or proof.

## Decisions already made

| Item | Current choice |
|---|---|
| Pilot | OPTO 2311 — البصريات الهندسية, `PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-`. |
| Model work | zIDE subscription only; zero incremental cash. |
| Budget | Stated 300M-token total quota; verify remaining balance and assign smaller run/pilot token caps. |
| Delivery | This repository; static teaching artifacts; Cloudflare Pages. |

The [goal](content-factory-v1-goal.md) owns these decisions. The [resolution](content-factory-v1-resolution.md) defines required controls. The [pilot packet](content-factory-v1-pilot.md) supplies course-specific evidence and review fields.

## Ticket CF-01: build the optics source manifest

**Purpose:** make every reuse, repair, and missing-source decision traceable before model work begins. This task needs local files and metadata; it does not need a reviewer, a chosen frontend framework, or live model access.

**Planning estimate:** 2–4 focused implementation hours for the exporter, fixtures, and report. Recovering trustworthy lecture-order evidence is a separate unknown; the exporter must represent that uncertainty rather than invent an order.

### Already checked

The local course has **106 recorded video IDs**, **105 raw JSON/SRT/post-processed sets**, **105 chapter files**, and **83 v2 outputs**. One skipped video, `SAq013FtOLQ`, has no raw file. Another 22 videos have source material but no v2 output. Its playlist `entries` field is truncated at 32,767 characters.

These facts are a starting snapshot. Recompute them during the task and report any drift. They do not show that the raw text, processed text, or old outputs are complete or correct. See [inventory evidence](content-factory-v1-inventory.md#selected-optics-pilot--follow-up-inspection).

### Do these five actions

1. **Freeze expected membership.** Read a consistent local metadata snapshot. Record all 106 distinct video IDs, playlist membership, skip flags, and source-order evidence. Separate video identity from course membership; preserve the known folder-alias behavior in discovery.
2. **Map every available variant.** Find raw JSON, raw SRT, normalized/plain SRT, `_postprocess.srt`, chapter JSON, and v2 output by exact video ID. Record repository-relative path, size, SHA-256, artifact type, and any known producer/revision. Keep conflicting variants separate.
3. **Check source integrity offline.** Parse raw segments/subtitles; flag malformed, duplicate, missing, out-of-order, or invalid-timestamp units. Compare original versus processed coverage where an alignment is defensible. Keep uncertain alignment explicitly unresolved. Never treat equal counts as proof of equal meaning.
4. **Record dispositions.** Keep `SAq013FtOLQ` visible with its recorded skip flag and unresolved reason. Classify old outputs as unreviewed reuse candidates. Mark absent outputs as missing work; do not regenerate them. Mark unknown lecture order explicitly and list the evidence needed to resolve it.
5. **Write a reproducible manifest and readable report.** Save new outputs separately from the corpus/state/database. Repeated unchanged scans must produce the same semantic manifest hash; keep inspection timestamps outside that hash. Summarize the blockers that prevent freezing course scope.

### Deliverables to create

| Deliverable | Expected content |
|---|---|
| `scripts/build_pilot_manifest.py` | A proposed new offline exporter with an explicit playlist/root/output interface. This file does not exist yet. |
| `artifacts/opto-2311/source-manifest.json` | One record per expected video plus linked source/artifact revisions, segment findings, and unresolved evidence. Proposed generated output. |
| `docs/opto-2311-source-review.md` | A short human report: counts, reusable candidates, missing/ambiguous sources, order evidence, and the first review targets. Proposed report. |
| Focused regression fixtures/tests | Membership aliases, shared IDs, missing/skipped files, conflicting revisions, malformed content, truncated metadata, and unchanged reruns. |

The current general scanner does not classify `_postprocess.srt`; extend its reusable discovery logic or share that logic with the exporter. The new tool must not import the model/network-capable pipeline. `.gitignore` currently ignores JSON globally: keep generated manifests local, and use narrow exceptions if small synthetic JSON test fixtures need to be versioned. Do not commit the corpus or credentials.

### Done means

1. Every expected video has a record; file gaps and skip flags remain visible.
2. Each available artifact has an exact identity/hash, and no old completion flag confers approval.
3. Truncated ordering metadata and uncertain segment alignment are reported without invented replacements.
4. The source corpus, historical outputs/state, and original database are unchanged; no network or model calls occur.
5. Focused tests and the existing suite pass; the report identifies the next evidence needed to freeze the pilot.

### Commands that work now

Run from the repository root. These are existing tools, not the proposed exporter:

```bash
python3 scripts/inventory_content_factory.py --output /tmp/content-factory-inventory.json
```

The scanner uses local data, refuses a nonempty database WAL, and stores its report/snapshot separately. A new clone needs access to the local corpus/database first. Running it alone does not complete CF-01's variant hashes or segment checks.

```bash
.venv/bin/python -m pytest
```

Use the normal project setup in [the root README](../README.md) if dependencies are missing. The previously verified baseline was 161 passing tests; confirm the current result when implementation changes.

## After CF-01: four milestones

### 1. Freeze source sufficiency and skill outcomes

**Owner:** agent prepares evidence; optics subject reviewer decides correctness and adequacy. **First review estimate:** 30–45 minutes for three selected lectures once lecture order is verified; full-course review takes additional measured time.

Use verified first/middle/final lectures to identify tangible skills. Map each skill to original spans, required diagrams/media, a worked example, practice, and an independent task. Record any unsupported equations, conventions, or missing visuals. Resolve the skipped video's impact on the promised curriculum. Create the full outcome matrix and a source-grouped development/holdout manifest before authoring.

**Completion proof:** every promised outcome has adequate evidence and prerequisites, or an explicit blocker. A three-lecture inspection estimates risk; it cannot accept the whole course. Reviewer recruitment can run alongside CF-01.

### 2. Prove quota accounting through the actual zIDE workflow

**Owner:** agent builds local ledger/tests; operator supplies observable zIDE usage and quota details. **First capability check estimate:** 20–30 minutes; integration effort depends on what the installed product actually exposes.

Verify submission/export, model identity, usage reporting, quota period/reset, remaining balance, and interrupted-work recovery. The docs do not establish an API or a per-request usage export. Choose an automated adapter only if its behavior is observed; otherwise define an operator-mediated workflow and its limits. A local ledger cannot control unobserved model work elsewhere in the subscription.

Implement integer-token reservations in SQLite with run and pilot allocations. Persist attempts and retry/repair limits before dispatch; retain unknown-outcome reservations across restarts. Exercise crashes and competing workers with a fake adapter first. If observation cannot support the required quota guarantee, keep automatic dispatch disabled and record the unresolved integration.

**Completion proof:** fake-adapter failure tests pass, the real integration boundary is documented, and explicit run/pilot allocations fit the measured remaining quota. Direct paid Gemini/OpenAI calls remain outside v1's chosen scope.

### 3. Produce and evaluate one complete lesson as an engineering trial

**Owner:** agent implements artifacts/preview; independent reviewers calibrate and assess teaching. **Suggested checkpoint:** one skill-based lesson before processing the remaining course.

Define the constrained Markdown/quiz schema, stable teaching-node IDs, provenance sidecars, rubric, and deterministic validators. Use supported evidence to produce one lesson with practice, an editable diagram and accessible alternative, and its wiki/graph derivatives. Include whole-lesson context in evaluation and cache invalidation.

Keep development cases separate from the untouched final holdout. Independently validate equations and quiz answers; test Arabic/mixed-direction rendering and keyboard interaction. Seed known failures and inspect confidently accepted/repair outputs. Record actual token usage and review time.

**Completion proof:** one lesson meets the engineering/content checks, demonstrates an unchanged rerun without repeated model work, and exposes measured unit economics. It remains an engineering trial; the goal still requires a complete accepted pilot course and learner evidence.

### 4. Complete the pilot and demonstrate Cloudflare Pages release recovery

**Owner:** agent prepares the complete artifact set and previews; reviewers/learners provide acceptance evidence; operator provides deployment access when needed.

Apply measured authoring/evaluation rules to the frozen pilot scope. Finish subject/editorial/visual review and a formative learner trial with an unaided task. Fix observed critical defects. Publish only the complete accepted artifact set after preview checks on Arabic/English, mobile/desktop, quizzes, and accessibility.

Verify current Pages capabilities/limits during the deployment task. Demonstrate an intentionally failed update, rollback to an accepted safe version, withdrawal when all available versions are invalid, and restoration from an independent backup.

**Completion proof:** every required goal checkbox has recorded evidence; cost reporting uses first-accepted lesson IDs and outcome coverage. Expansion follows measured results.

## Copy this into the next zIDE session

```text
Implement CF-01: an offline source manifest for OPTO 2311 — البصريات الهندسية.

Read docs/README.md, docs/NEXT_STEPS.md, docs/content-factory-v1-goal.md,
docs/content-factory-v1-pilot.md, and docs/content-factory-v1-resolution.md.

Use playlist PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-.
Recompute the current snapshot: 106 expected video IDs, 105 available raw/
post-processed sets, 105 chapter files, 83 v2 outputs; skipped video
SAq013FtOLQ lacks raw data; playlist entries are truncated.

Create scripts/build_pilot_manifest.py, a generated local manifest, and
an evidence report at docs/opto-2311-source-review.md. Record exact variant
hashes, segment findings, skip/source gaps, and unknown ordering. Preserve
all existing source/output/state/database files. Do not call models, sync
remote metadata, generate missing lessons, or infer approval from old flags.

Add focused tests for the integrity/reconciliation cases in CF-01 and run
the existing suite. Report what passed and what still prevents scope freeze.
Keep zero incremental cash and zIDE-only model execution as the v1 policy;
this ticket itself is offline and must not dispatch any model work.
```

**Next action — under 2 minutes:** copy that brief into a new zIDE session. It starts one bounded task while reviewer availability is being arranged.
