# Documentation map

**Open [NEXT_STEPS.md](NEXT_STEPS.md) to prepare the optics scope-review evidence.** Read this map in about 2 minutes; open the longer references only when the task needs them.

**Teaching sources:** transcripts — raw whisper JSON plus, per video, the cleaned `GeminiLongContext/` counterparts (approved 2026-09-07) — and the matching YouTube lecture only when a needed diagram is missing or unclear. Derived SRT variants stay non-evidence. [Full source policy](factory/content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed).

**Current position:** the source manifest, keyframe capture CLI, and offline preparation helpers exist. The transcript-backed outcome matrix, live runtime, calibrated quality gates, learner trial, and deployment are still unfinished.

## Start here

| File | Purpose |
|---|---|
| [README.md](README.md) | This map and document authority. |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Current task, completion proof, and later milestones. |
| [Outcome-matrix pass](factory/outcome-matrix-pass.md) | Paste-ready prompt and offline CLI for the current preparation pass. |

## Factory contract and tools — `factory/`

| File | Purpose |
|---|---|
| [Goal](factory/content-factory-v1-goal.md) | Binding v1 objective, fixed decisions, and definition of done. |
| [Resolution](factory/content-factory-v1-resolution.md) | Implementation rules for the 13 resolved blindspots. |
| [Inventory](factory/content-factory-v1-inventory.md) | Dated source/output measurements and limitations. |
| [Blindspot review](factory/content-factory-v1-blindspots.md) | Historical rationale; not current authority. |
| [Course rubric](factory/COURSE_RUBRIC.md) | Quality checks, hard failures, and calibration fields. |
| [Keyframe capture](factory/KEYFRAME_CAPTURE.md) | Diagram-recovery CLI, commands, and verification. |

## Optics pilot — `pilot/opto-2311/`

| File | Purpose |
|---|---|
| [Pilot packet](pilot/opto-2311/content-factory-v1-pilot.md) | Selected course, local coverage, challenge cases, and reviewer inputs. |
| [Production plan](pilot/opto-2311/pilot-opto-2311-plan.md) | CF-01…CF-13 dependencies, gates, operations, and session briefs. |
| [Source review](pilot/opto-2311/opto-2311-source-review.md) | CF-01 evidence, gaps, order evidence, and freeze blockers. |
| [First review](pilot/opto-2311/opto-2311-first-review.md) | CF-02 candidate skills, spans, and reviewer decisions. |
| [Scope freeze](pilot/opto-2311/opto-2311-scope-freeze.md) | CF-03 draft checklist and remaining gates. |
| [Learner trial](pilot/opto-2311/opto-2311-learner-trial.md) | CF-10 recruitment, session, transfer, and observation instruments. |
| [Operations](pilot/opto-2311/opto-2311-operations.md) | CF-13 incident, monitoring, repair, backup, and rehearsal skeleton. |

## Platform delivery — `platform/`

| File | Purpose |
|---|---|
| [North star](platform/platform-north-star.md) | Learner purpose, accepted defaults, scale destination, and outcomes. |
| [Platform brief](platform/platform-map-brief.md) | Product scope: reader, RTL, quizzes, wiki, and concept graph. |
| [Course app plan](platform/course-app-plan.md) | Provisional hosting and presentation slice. |
| [Artifact storage review](platform/artifact-storage-review.md) | Private review, exact-bundle approval, storage, and budget. |
| [Search discovery plan](platform/search-discovery-2026-q3.md) | Dated SEO and AI-citation requirements. |
| [Talks Archive adoption review](platform/talks-archive-spec-adoption-review.md) | Section-by-section external-spec crosswalk and compatible platform contract additions; recommendation, not authority or implementation proof. |

## Research and evaluations — `research/`

| File | Purpose |
|---|---|
| [Skills map](research/skills-map.md) | Candidate tools, possible roles, licenses, and costs. |
| [Fanout analysis](research/fanout-feature-analysis.md) | Adopt/adapt/skip benchmark from local screenshots. |
| [OKF evaluation](research/okf-v02-evaluation.md) | Draft graph/export format evaluation. |
| [Context-cost analysis](research/context-management-mcp-token-cost.md) | Measured MCP/skills overhead and context-management fixes. |

Supporting visual material stays in [wireframes/](wireframes/index.html) and [`inspiring/`](inspiring/). Use `inspiring/` for visual and interaction inspiration and the pilot wireframes as worked examples; neither is an authority document or the scope boundary for the full platform.

The repository's [root README](../README.md) is the short project entrypoint with setup, test, and inventory commands.

## Corpus layout (local only — never commit)

For each video, the raw transcript `data/<playlist_id>/<video_id>_raw.json` has its cleaned counterparts in the mirrored `GeminiLongContext/<playlist_id>/` tree under the same video ID: `…_chapters.json`, `…_v2_content.json` (earlier variant `…_content.json`), and `…_lecture_context.json`.

| Path pattern | Contents |
|---|---|
| `data/<playlist_id>/<video_id>_raw.json` | Raw Whisper output (`segments[]` with start/end/text) — the canonical teaching source for v1: segmentation, timestamps, and evidence spans bind here. Sibling `.srt` variants live beside it and stay non-evidence. |
| `GeminiLongContext/<playlist_id>/<video_id>_chapters.json` | Cleaned, chapter-organized lecture structure: chapter titles + timestamps, pondering introduction, opening/essential questions, main topics, and keyframe hints. |
| `GeminiLongContext/<playlist_id>/<video_id>_v2_content.json` | Cleaned transcript text organized per chapter (`title`, `start`/`end`, `cleaned_transcript_text`, `subtitle_count`). `_content.json` is an earlier variant of the same. |
| `GeminiLongContext/<playlist_id>/<video_id>_lecture_context.json` | Per-lecture context metadata: study language, faculty, course, audience, title, duration. In the pilot course 94 of 105 are Python-literal, not strict JSON. |

In the optics pilot every raw set has its `_chapters` and `_lecture_context` counterpart (105 of 105); 83 of 105 also have a `_v2_content` output.

`GeminiLongContext/` is the cleaned and organized per-video content store the historical long-context processing produced from the raw transcripts. **User-confirmed reversal 2026-09-07:** these cleaned counterparts are approved teaching sources for v1, bound per video alongside the raw transcripts — the earlier audit-only rule is withdrawn ([source policy](factory/content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed)). Raw whisper JSON stays canonical for segmentation and timestamps; derived SRT variants remain non-evidence.

- Both roots are git-ignored (`data`, `GeminiLongContext`, plus the global `*.json` rule): a fresh clone has none of this. Never commit or upload it.
- Playlist IDs end in `-`, so a nested path reads as if the playlist and video IDs were concatenated (`…R2s-/-AsaJEAav4s_chapters.json`); the trees are still nested by playlist.
- Known quirks: legacy flat `PL*` folders at the repo root, the `L9fwy3NUQKwYNxhPlUU9pxwfg8zlh4TPZ/` alias folder in both trees (playlist ID missing its leading `P`), and stray non-conforming files at the `GeminiLongContext/` root. [The inventory](factory/content-factory-v1-inventory.md) holds the measured counts.

## Which document wins?

1. The **goal** owns current v1 scope and fixed decisions: transcript-based reprocessing with YouTube diagrams only as needed; optics; zIDE/ZCode execution through an OpenAI-compatible provider adapter, starting with authorized Gemini free-tier quota; continued free work until every configured authorized quota is confirmed exhausted; the separate $5/month hosting/operations ceiling; and Cloudflare Pages.
2. The **resolution** supplies implementation rules; the **pilot packet** applies them to the selected course.
3. **Inventory** is dated evidence. **Blindspots** and older candidate comparisons retain historical context, not authority to reopen a settled choice.
4. The **platform map** defines broader product scope. The **skills map** supplies candidates, not approved dependencies.
5. **Next steps** describes execution order. Update it when a milestone is proved; a checklist alone cannot certify implementation.

## Already known

The optics pilot has **106 recorded video IDs**, **105 raw/post-processed transcript sets**, **105 chapter files**, and **83 legacy v2 outputs**. One skipped source is absent; 22 available-source videos have no v2 output. All 105 available transcript sets are in scope for fresh v1 processing; old output counts do not reduce that work. Its playlist `entries` field is truncated, so lecture order still needs trustworthy evidence.

**Next action:** open [the scope-review preparation task](NEXT_STEPS.md#next-task-prepare-the-scope-review-evidence).
