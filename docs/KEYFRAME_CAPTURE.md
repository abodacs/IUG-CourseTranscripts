# Capture diagrams from existing keyframe hints

**Run one video first, then open its image gallery.** Allow about 3 minutes to read this guide. Capture time depends on video access and the number of timestamps.

**Status:** the CLI works with local videos and YouTube. A live optics trial captured four images, including the conventional/Fresnel prism diagram at 05:26. A fifth hint at 32:31 was rejected because the video lasts 23:00. Captured images still need content review.

## Run it

From the repository root, preview a real video's plan without network or output writes:

```bash
python3 scripts/capture_keyframes.py \
  GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/-AsaJEAav4s_chapters.json \
  --dry-run
```

Capture its YouTube frames using the yt-dlp version verified in this task. FFmpeg must be installed. `uv` caches this separate environment; model APIs are not involved:

```bash
uv run --isolated --no-project --with 'yt-dlp[default]==2026.8.19' \
  python scripts/capture_keyframes.py \
  GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/-AsaJEAav4s_chapters.json
```

Open `artifacts/captures/-AsaJEAav4s/index.html` after the run. This example deliberately retains the original invalid timestamp: expect four captures and one reported failure, with exit status 1. The tool preserves the original JSON.

For an already available matching video, use the same JSON with `--video /absolute/path/to/lecture.mp4`. Local capture needs Python, FFmpeg, and ffprobe; it makes no network calls. The caller must ensure the file is the matching lecture; the tool records its hash but cannot infer that identity from its pixels.

## Useful options

| Option | Effect |
|---|---|
| `--all-candidates` | Include `candidates_keyframes` as well as the chosen frame; duplicate timestamps produce one image with all associated hints. |
| `--offsets=-2,0,2` | Capture neighboring frames when the proposed moment lands during a transition or before a diagram is finished. |
| `--output /path/to/captures` | Keep generated PNGs, manifests, and galleries in a separate location. Default output is Git-ignored. |
| `--refresh` | Recapture existing frames. Otherwise reuse only images whose recorded hashes and source identity match. |
| `--max-frames 500 --timeout 90` | Set the invocation's frame limit and per-command timeout. The default limit is 50; directory input discovers `*_chapters.json` recursively. |

Single-file mode infers the video ID from `_chapters`, `_v2_content`, `_lecture_context`, or `_raw` filename stems. A `_lecture_context.json` holds lecture context metadata, not keyframe hints: planning stops there — and most copies are Python-literal rather than strict JSON, so they fail JSON parsing first.

For a course-wide plan, pass the course's `GeminiLongContext/<playlist_id>` directory with `--dry-run --max-frames 500`. The inspected optics directory has **105 JSON files**, **420 distinct chosen timestamps**, and **897 timestamps when including all candidates**. There are **131 chosen-hint/chapter-range warnings**. These are capture hints, not accepted diagrams or trusted course order.

## What the tool reads and saves

The current corpus uses `chapters[].chosen_keyframe` and `chapters[].candidates_keyframes`, each with `timestamp` and `description`. Numeric timestamps are seconds. The misleading chapter `time_format` label is ignored; actual clock strings are parsed as `MM:SS` or `HH:MM:SS`. A flat `key_moments` list with the same fields and a top-level `video_id` also works.

```json
{
  "video_id": "-AsaJEAav4s",
  "key_moments": [
    {"timestamp": 326, "description": "Review the prism comparison diagram"}
  ]
}
```

Each video's output folder contains full-frame PNGs named by requested milliseconds, `manifest.json`, and `index.html`. The manifest records the input JSON hash, requested timestamps, original hints, source information, PNG hashes, warnings, and failed/captured status. Every frame remains `unreviewed`; the gallery labels descriptions as hints rather than verified captions. The original transcript and old generated prose are never rewritten or sent to a model.

The tool seeks the selected video stream at the requested times and saves one frame per time. It does not save an entire video as an output, but network bytes fetched depend on the stream and seeking support. No claim of frame-exact measured presentation timestamps is made. It uses the best available MP4 video up to 1080p when available, with format fallbacks; it cannot recover detail absent from the source.

## Failure and review behavior

1. **Inspect the actual image.** A JSON hint can be wrong. Verify labels, equations, framing, and that the intended diagram is present before teaching from it.
2. **Keep gaps visible.** Malformed hints block planning. Chapter-range inconsistencies are warnings; a timestamp beyond the actual video duration fails that capture. Negative neighbor offsets are skipped with a warning. Missing/private/unavailable videos and command timeouts are recorded as failures.
3. **Resume safely.** Each attempted frame checkpoints the manifest. Valid PNGs survive later failures and are reused on reruns. A corrupt PNG is recaptured. Use one process per output video directory. YouTube identity is a video ID, not an immutable media revision; use `--refresh` if the upload has been edited or timing changed.
4. **Correct hints separately.** Save a reviewed `key_moments` JSON when changing timestamps; retain the old JSON for audit. Neither the old description nor a successful image export proves visual correctness.
5. **Read the exit status.** `0` means all requested captures succeeded or were reused; `1` means at least one capture failed; `2` means invalid input, missing prerequisites, or another setup error. The CLI summary includes failure reasons and the gallery path.

## What we adopted from the Answer.AI article

[The article](https://www.answer.ai/posts/2025-10-13-video-to-doc.html) describes preparing transcript evidence before writing, then outlining and reviewing one section at a time. We apply that process within the [transcript-only source policy](content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed).

| Article component | Decision for this project |
|---|---|
| Timestamped images beside transcript sections | Adopt. Existing keyframes guide capture; image evidence must be checked and linked back to the matching lecture. |
| Two stages: prepare evidence, then write | Adopt. Keep immutable raw transcripts plus reviewed visual notes; use a separate writing pass with access to the original evidence. |
| Outline, section-sized requests, edits, and omission checks | Adopt. Account for every transcript segment, preserve a coverage map, and retain whole-lesson/course review after assembly. |
| Runnable examples and clarifying explanations | Adapt. Derive them from allowed evidence and independently check the result. External repositories, papers, web enrichment, and added subject facts remain outside scope. |
| SolveIt-specific capture/message tools | Evaluate as references. Implement file-based equivalents for the existing zIDE/Python workflow. Do not assume SolveIt image tags or message editing APIs work in zIDE. |

The linked `dialoghelper` project contains `capture_tool`, `capture_screen`, `setup_share`, and `start_share`. Its screen-capture path uses SolveIt's browser events and a user-selected display stream; it does not accept a YouTube URL and timestamp or select diagrams. This CLI is an independent implementation of the screenshot workflow, using the project's yt-dlp dependency and FFmpeg for timestamp-directed capture. [Capture implementation](https://github.com/AnswerDotAI/dialoghelper/blob/856b8a423f14c0d36b9d42dfafa9d98c8bb5b928/dialoghelper/capture.py), [browser bridge](https://github.com/AnswerDotAI/dialoghelper/blob/856b8a423f14c0d36b9d42dfafa9d98c8bb5b928/dialoghelper/screenshot.js), [SolveIt context](https://github.com/AnswerDotAI/dialoghelper/blob/856b8a423f14c0d36b9d42dfafa9d98c8bb5b928/dialoghelper/core.py).

Two implementation findings matter before copying article code. Its sample splitter ignores the `dst` argument in favor of `scribe_dst`, and emits chunks only when it reaches images. A local probe confirmed that a transcript without images yields zero chunks, and text after the last image/caption is omitted. Use segment-based splitting with explicit coverage checks. Its `run_cmd` example supplies a timeout but is not an execution sandbox; generated examples still need the existing isolated execution contract. [Article code examples](https://www.answer.ai/posts/2025-10-13-video-to-doc.html#enriching-the-transcript).

The public example labels its initial material as “Scribe,” but the inspected sources do not establish a distributable Scribe ingestion tool or prove which capture backend prepared those initial screenshots. `dialoghelper`'s available capture function is verified separately. Its repository declares Apache-2.0; no upstream code was copied into this CLI. [Public example](https://share.solve.it.com/dlgs/intelligent-frost-ascends-gracefully-2a18c7os), [upstream license](https://github.com/AnswerDotAI/dialoghelper/blob/856b8a423f14c0d36b9d42dfafa9d98c8bb5b928/LICENSE).

## Verification

Focused tests cover timestamp parsing, deduplication, offsets, identity mismatch, missing/malformed hints, dry-run behavior, frame limits, lookup failure, URL redaction, real FFmpeg pixel checks, invalid video positions, input preservation, gallery escaping, and verified cache recovery:

```bash
.venv/bin/python -m pytest tests/unit/test_capture_keyframes.py -q
```

The installed project yt-dlp `2025.09.05` failed the live video lookup. The isolated `2026.08.19` build successfully captured the four in-range frames. No project dependency or lockfile was upgraded during this task. [yt-dlp options](https://github.com/yt-dlp/yt-dlp#usage-and-options), [FFmpeg seeking and frame options](https://ffmpeg.org/ffmpeg.html#Main-options).

**Next action — under 2 minutes:** open the generated gallery and check the 05:26 prism diagram.
