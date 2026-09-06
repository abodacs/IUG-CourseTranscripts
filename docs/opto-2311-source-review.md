# OPTO 2311 — source review (CF-01)

**Status:** implemented 2026-09-06 by [`scripts/build_pilot_manifest.py`](../scripts/build_pilot_manifest.py); offline, read-only, zero network/model calls. The machine-readable manifest is `artifacts/opto-2311/source-manifest.json` (local; `*.json` is git-ignored by policy). This report and the script/tests are the committed deliverables.

- Manifest sha256 `fe35da7e7acd31044cd191cb54a063c0a65f86f1988ee836a6bbd0489e5525ba` — **identical on unchanged rerun** (inspection timestamps live outside the hashed payload).
- Evidence database `youtube-iug.db` sha256 `c01ad8cfcb52fd59…` (full value recorded in the manifest's `inspection` block); read from a verified immutable snapshot after refusing a nonempty WAL.

## Counts (recomputed, not assumed)

| Measure | Value |
|---|---|
| Expected video IDs (sync_github memberships) | 106 |
| With raw whisper JSON (`_raw.json`) | 105 |
| With raw SRT (`_raw.srt`) | 105 |
| With `_postprocess.srt` | 105 |
| With plain/normalized `.srt` | 105 |
| With legacy chapter hints (`_chapters.json`) | 105 |
| With legacy v2 lesson (`_v2_content.json`) | 83 |
| Source gaps (no raw transcript at all) | 1 — `SAq013FtOLQ` |
| Skipped records (`skip=1`) | 1 — `SAq013FtOLQ` |
| Shared video IDs (also member of another playlist) | 0 |

This matches the historical snapshot in [NEXT_STEPS](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest) (106 / 105 / 105 / 83 / 1 skipped; 22 videos historically without v2 output = 105 − 83). No drift in membership.

## Eligible teaching candidates

**105 videos with raw JSON + raw SRT are the only teaching-eligible sources.** All 105 need fresh v1 processing; no legacy output or completion flag skips any of them.

Measured facts that constrain later tickets:

- **Raw JSON and raw SRT are not unit-aligned.** In 0 of 105 videos does the JSON segment count equal the SRT cue count (example: `0Ca8cjsIysc` — 38 JSON segments vs 195 SRT cues). The SRTs were exported at a finer granularity. Never align the two unit-to-unit; use the raw JSON as the canonical segmentation for evidence spans, and treat count mismatches as expected structure, not corruption.
- **Postprocessed SRTs split 45 byte-identical to raw SRT / 60 that differ** and therefore still need the CF-02A fidelity check before any use beyond raw text. A differing postprocess file is neither trusted nor condemned — it is unresolved.
- **The plain `.srt` variant is damaged in places.** All 73 malformed cue blocks live in this variant (example: `-AsaJEAav4s.srt` cue 191 is cut off mid-timestamp), plus 61 videos with non-sequential cue numbering and 621 zero-duration cues across 60 videos. This validates the plan's "classify, do not trust" classification: normalized SRT stays `classify_only`, never an authoring input.
- **Whisper quality flags (screening hints, not verdicts):** 187 segments with `compression_ratio > 2.5`, 44 with `no_speech_prob > 0.6`, 12 with `avg_logprob < −1.0`. These prioritize CF-02A review spans; they prove nothing by themselves.

Integrity findings total 626 warnings and **0 criticals**. Every video with data carries at least one warning, dominated by the systematic JSON↔SRT granularity difference (315 of the findings = 105 videos × 3 cross-checks). Findings carry a `variant` tag so each can be traced to the file that produced it.

## Audit-only legacy artifacts (never teaching inputs)

- **105 chapter-hint JSONs**: 421 chapters, 421 `chosen_keyframe` hints, 744 candidate timestamps, 0 chapter-range warnings (every chapter range parses and is monotonic). A hint is a capture pointer, not proof of what the frame shows. *Drift note:* the historical figures "420 chosen / 897 candidates" do not reproduce under the manifest's explicit definitions (occurrences of `chosen_keyframe`; summed lengths of `candidates_keyframes`; no `key_moments` fields exist anywhere). The recomputed numbers with their definitions are authoritative here.
- **83 legacy v2 lessons** plus generated `_content.json` / `_lecture_context.json` files: audit-only. The historical 22-video output gap is unchanged coverage information, not permission to skip first-pass v1 work.

## Source gaps

- **`SAq013FtOLQ`** — `skip=1`, `downloaded_r2=0`, no raw file, disposition **unresolved**. Its curriculum impact may only be established by the reviewer + operator from allowed evidence (CF-03); until then it remains an explicit completeness blocker. Its topic must not be invented.
- **Playlist `entries` metadata is truncated** at the 32,767-character storage limit, so membership completeness rests entirely on the 106 `sync_github` rows. The live YouTube playlist count (CF-02) is the cross-check.

## Order evidence

**Lecture order is unknown for all 106 records.** Every membership was created in one 34-second batch import (2024-08-31 15:21:57 → 15:22:31) — download order, not lecture order. All manifest records store `lecture_order: unknown`. Resolution paths, in order of trust: (1) CF-02 playlist metadata via pinned yt-dlp 2026.8.19 (identity/order use only), (2) verbal sequence references inside transcripts, (3) chapter hints (weakest). Positions that stay unresolved keep explicit unknown slots.

## Near-duplicate family watchlist (for CF-06)

Two sibling playlists share the course name and are recorded as candidate near-duplicate families for the split manifest (metadata only; not processed here): `PL9fwy3NUQKwb_KOrEPbVXCHcPMZKR0uEY` «بصريات هندسية» (30 local memberships) and `PL9fwy3NUQKwZZYWdO8xTBLJBmEjaQDzzb` «البصريات الهندسية / عمرو أبو عمارة» (25). Zero video-ID overlap with the pilot, but holdout grouping must treat them as one content family.

## Pending diagram recovery

No video was fetched. The 421 chosen keyframe hints are recorded as **pending recovery pointers only**; CF-02/CF-07 will name the diagrams actually needed (video ID + timestamp + later captured-byte evidence), using the [capture CLI](KEYFRAME_CAPTURE.md) under its exit-code discipline.

## Blockers that still prevent scope freeze

1. Lecture order unknown — needs CF-02 playlist metadata or explicit unknown slots.
2. 60 postprocessed SRT files await fidelity checks (or an explicit raw-only authoring decision, CF-02A).
3. Keyframe hints are hints only — needed diagrams require capture + reviewer verification.
4. All 83 legacy v2 lessons are audit-only — every transcript needs fresh v1 processing regardless.
5. Sibling optics playlists must be grouped in the CF-06 split manifest before any holdout claim.
6. `SAq013FtOLQ` disposition unresolved.
7. Truncated `entries` metadata — membership completeness rests on sync_github until the live playlist is compared.

Not source blockers, but still required before freeze per [the plan](pilot-opto-2311-plan.md): subject-reviewer recruitment, CF-04 quota observations/allocations, and the protected-family access decision.

## Reproduce

```bash
.venv/bin/python -m pytest tests/unit/test_build_pilot_manifest.py   # 33 focused tests
.venv/bin/python scripts/build_pilot_manifest.py                     # rebuild manifest (offline)
```

The exporter refuses a nonempty WAL, never writes outside its output file, imports nothing from `src/`, and performs no network or model calls. Suite status at implementation: **214 passed** (181 baseline + 33 new).
