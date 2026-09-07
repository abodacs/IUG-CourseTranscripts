# IUG Course Transcripts

**Start with [the documentation map](docs/README.md).** It explains what each file contains and which one to open next.

The existing Python pipeline collects and processes IUG course transcripts. Content Factory v1 will reprocess course transcripts into reviewed Arabic-first lessons, assessments, editable diagrams, and wiki/graph artifacts. Teaching sources are the transcripts — raw whisper JSON plus, per video, the cleaned `GeminiLongContext/` counterparts (approved 2026-09-07) — plus the matching YouTube lecture only when needed to recover diagrams; derived SRT variants and external teaching supplements are excluded. v1 is not yet implemented or accepted.

The selected pilot is **OPTO 2311 — البصريات الهندسية**. The current contract uses the operator's **zIDE subscription quota of 300 million tokens**, with **zero incremental cash**, and targets **Cloudflare Pages**. Model integration, measured remaining quota, and per-run/pilot token caps still need verification.

## Open the right document

| Need | Open |
|---|---|
| A short recap of every document | [Documentation map](docs/README.md) |
| The next implementation task, in detail | [Next steps](docs/NEXT_STEPS.md) |
| The release requirements and settled decisions | [Goal and acceptance contract](docs/factory/content-factory-v1-goal.md) |
| Pilot sources, reviewer preparation, and open inputs | [Pilot packet](docs/pilot/opto-2311/content-factory-v1-pilot.md) |

For diagrams already identified in chapter JSON, use the [keyframe capture tool](docs/factory/KEYFRAME_CAPTURE.md). It saves timestamped PNGs, a manifest, and a review gallery from local or matching YouTube videos.

## Local commands

Run these from the repository root. Setup uses Python 3.11+ and uv:

```bash
uv sync
```

Run the existing automated tests:

```bash
.venv/bin/python -m pytest
```

Inspect local source metadata and artifacts without model calls or remote synchronization:

```bash
python3 scripts/inventory_content_factory.py --output /tmp/content-factory-inventory.json
```

The inventory needs the local database and corpus; these large/private working artifacts are excluded from Git. A fresh clone does not include them. The scanner refuses a nonempty database WAL instead of reporting a potentially stale snapshot.

## Existing implementation

[main.py](main.py) is the legacy ETL entrypoint; its raw-JSON-to-SRT step still contains a placeholder. [The chapter extractor](src/etl/transcript_chapter_extractor.py) includes migration integrity safeguards and saved-result recovery. Legacy scripts can call Gemini directly and do not enforce the v1 zIDE token-budget contract.

[The tests](tests) cover the current implementation. Passing them does not certify lesson quality or grant a v1 release. Follow [the next-step guide](docs/NEXT_STEPS.md) for the offline work that comes first.
