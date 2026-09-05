# IUG Course Transcripts

**Start with [the documentation map](docs/README.md).** It explains what each file contains and which one to open next.

The existing Python pipeline collects and processes IUG course transcripts. Content Factory v1 will turn reusable source material into reviewed Arabic-first lessons, assessments, editable diagrams, and wiki/graph artifacts. v1 is not yet implemented or accepted.

The selected pilot is **OPTO 2311 — البصريات الهندسية**. The current contract uses the operator's **zIDE subscription quota of 300 million tokens**, with **zero incremental cash**, and targets **Cloudflare Pages**. Model integration, measured remaining quota, and per-run/pilot token caps still need verification.

## Open the right document

| Need | Open |
|---|---|
| A short recap of every document | [Documentation map](docs/README.md) |
| The next implementation task, in detail | [Next steps](docs/NEXT_STEPS.md) |
| The release requirements and settled decisions | [Goal and acceptance contract](docs/content-factory-v1-goal.md) |
| Pilot sources, reviewer preparation, and open inputs | [Pilot packet](docs/content-factory-v1-pilot.md) |

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

[The tests](tests/) cover the current implementation. Passing them does not certify lesson quality or grant a v1 release. Follow [the next-step guide](docs/NEXT_STEPS.md) for the offline work that comes first.
