# Outcome-matrix pass — session prompt (OPTO 2311)

A self-contained work prompt for advancing the transcript-backed outcome matrix, plus the offline CLI it runs on. The CLI commands are local Python with no database, env vars, or network. Model-assisted drafting is a separate execution concern and remains bound by the goal's authorized-free-quota and exhaustion contract.

**Execution rule:** ZCode is an approved execution environment. Model-assisted drafting may continue across the configured, operator-authorized free-quota pool. A confirmed quota-exhaustion response disables that provider/key until its recorded reset; use only another configured authorized quota, and stop when all are exhausted or any remaining quota state is uncertain. Never rotate keys to evade a provider limit.

## Offline CLI setup

```bash
git clone https://github.com/abodacs/IUG-CourseTranscripts && cd IUG-CourseTranscripts
uv sync
# copy the PRIVATE corpus in (never committed, never uploaded):
#   data/                 raw whisper JSON  (canonical evidence)
#   GeminiLongContext/    cleaned counterparts (approved teaching sources 2026-09-07)
.venv/bin/python scripts/outcome_matrix.py next --window 2   # read-only sanity check
```

Where the corpus sits: **raw** `data/<playlist_id>/<video_id>_raw.json` (canonical for segmentation, timestamps, evidence spans) and **cleaned** `GeminiLongContext/<playlist_id>/<video_id>_{chapters,v2_content,lecture_context}.json` (see [README § corpus layout](../README.md#corpus-layout-local-only--never-commit)). The CLI resolves every path via `src/etl/cleaned_store.py` — no path guessing.

## Window history

| Window | Started | Scope | Outcome |
|---|---|---|---|
| 1 (2026-09-07) | position 1 | manual pass, ~370K tokens/video | 29 positions drafted (1–7, 9–30); archived to `artifacts/opto-2311/outcome-matrix-window1.json` |
| 2 (current) | position 1 | fresh matrix via `start-window`, target ≤ 50K tokens/video | in progress — this prompt |

Exposure events are window-namespaced (`exp-matrix-w2-p001`, `recorded_by: session:outcome-matrix-pass-w2`), so re-drafting a window-1 position never collides with the append-only exposure log.

## The prompt (paste as the session goal)

```text
/goal advance the transcript-backed outcome matrix for OPTO 2311, starting from the
beginning of the current pass window, as far as quality allows. It is the authorized
next task — see GitHub issues #11 and #14 in abodacs/IUG-CourseTranscripts (gh is
authenticated): the exposure policy is ratified there and 10 holdout families are
reserved.

GROUND RULES (violating any invalidates the pilot):
- First read docs/NEXT_STEPS.md ("Next task") and the resolution comments on issues
  #11 and #14.
- Teaching sources are the LOCAL transcripts ONLY. Per video: the raw whisper JSON
  data/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/<video_id>_raw.json — canonical for
  segmentation, timestamps, and evidence spans — plus its cleaned counterparts
  GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/<video_id>_chapters.json,
  _v2_content.json (earlier variant _content.json; 83/105 coverage), and
  _lecture_context.json (approved teaching sources 2026-09-07; most files are
  Python-literal, not strict JSON — read leniently). Reach them only through the
  outcome-matrix CLI, which resolves every path. No outside teaching material. Read
  matched cleaned counterparts as teaching sources, but never treat a legacy v2
  lesson as accepted v1 output or as a reason to skip fresh processing. Never invent
  a source fact.
- Everything stays local: never commit, paste, or upload transcript content anywhere.
  data/, GeminiLongContext/, and artifacts/ are git-ignored on purpose. No git
  commits, no pushes.
- No factory pipeline dispatch — your session is the only consumer. ZCode is an
  approved execution environment. Continue only across the configured authorized
  free quotas. When one provider/key returns confirmed quota exhaustion, record it
  and disable that route until its reset; stop when every route is exhausted or any
  remaining quota is uncertain. The <=50K-token/video target remains an efficiency
  target, not permission to bypass provider limits.
- The 10 reserved holdout families (artifacts/opto-2311/evaluation-families.json) MAY
  be read at mining grade for matrix drafting — but nothing in them may later
  influence reference or calibration work.

OFFLINE COMMANDS RUN ANYWHERE: every matrix CLI command is local Python (no DB, no
env vars, no network). On a fresh machine, clone the repo and copy the private corpus
folders data/ and GeminiLongContext/ in. This portability does not authorize
model-assisted work outside the environment and budget boundary selected in the
binding goal.

WORK LOOP — repeat while at least one configured authorized free quota is confirmed
available; stop when all are exhausted, remaining state is uncertain, the operator
stops, or the window ends:
1. .venv/bin/python scripts/outcome_matrix.py next --window N
   (first run of a new window: ... start-window --window N first — it archives the
   previous pass and starts a fresh matrix). Take the next unprocessed batch of 8-12
   videos in position order from its output. It already skips position 8
   (unavailable source) and 105-106 (exam-logistics notices) and every position with
   a persisted lesson. Positions 105-106 still require explicit source accounting;
   the queue's administrative-notice skip is not a curriculum disposition or scope
   approval.
2. For each video in the batch:
   .venv/bin/python scripts/outcome_matrix.py dump <video_id>
   gives the numbered raw segments (canonical evidence), approved cleaned chapter
   material and capture hints,
   and the resolved cleaned-source paths. Read the cleaned counterparts at those
   resolved paths for teaching content. Draft outcome rows: tangible task; exact
   evidence span (segment[i] @seconds, cited from the RAW segments); cognitive level
   (remember/understand/apply/analyze/evaluate/create); prerequisites (O-p ids or
   NONE); needed example, practice, and transfer task; required diagram (video id +
   time range) only when the transcript alone cannot carry the outcome;
   source-sufficiency blocker if any. Follow the schema enforced by
   src/factory/outcomes.py (validate_outcome_matrix). Keep drafts in
   artifacts/opto-2311/pass-drafts/p<position:03d>.json. Every row is a DRAFT — the
   reviewer approves, never you.
3. Verify before persisting — this must print OK:
   .venv/bin/python scripts/outcome_matrix.py verify <video_id> <draft.json>
   (excerpt checks run verbatim against the raw segment text).
4. Persist — write after EVERY video, not at the end (crash-safe):
   .venv/bin/python scripts/outcome_matrix.py persist <draft.json> --window N
   This upserts the rows + lesson into artifacts/opto-2311/outcome-matrix.json and
   appends one exposure event per touched family to exposure-log.json (append-only;
   access_kind "transcript_text_read", recorded_by
   "session:outcome-matrix-pass-w<N>"). Re-running a position is idempotent.
5. When an authorized window ends (or a stop condition fires), post ONE progress comment on
   issue #14: positions completed this window, cumulative out of 105, blockers seen.
   Counts only — never transcript text. Then append the window record (usage tokens,
   positions, average per position) to allocations.toml.
```

## Command reference — `scripts/outcome_matrix.py`

| Command | Purpose |
|---|---|
| `start-window --window N [--force]` | Archive the current matrix to `outcome-matrix-window{N-1}.json`, write a fresh one. Exposure log is never rewritten. |
| `next --window N [--batch-size 10]` | Next unprocessed positions in order (currently omits unavailable 8, administrative notices 105–106, and persisted lessons); flags missing raw/cleaned sources. The two available omitted notices still require explicit source accounting before completion. |
| `dump <video_id>` | Numbered raw segments + approved cleaned chapter material/capture hints + resolved cleaned counterpart paths with policy notes. |
| `segments <video_id> <out>` | Write the raw-segment text map (JSON) for drafters. |
| `verify <video_id> <rows.json>` | Mechanical row checks: required fields, enums, component lists, evidence existence + verbatim excerpts vs raw, diagram/blocker rules, prerequisite prefixes. |
| `persist <draft.json> --window N` | Idempotent per-position upsert into the matrix + one window-namespaced exposure event per touched family. |

Common flags: `--root` (repo root; defaults to this checkout), `--playlist`, `--date`. Requires only the repo plus the local corpus — no DB, no `.env`, no network.
