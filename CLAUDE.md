# Agent guide — IUG Course Transcripts

Docs-first repo: a legacy transcript ETL pipeline plus the Content Factory v1 plan.
**Start at [docs/README.md](docs/README.md)** — it maps every document and its authority.
**The current task is always [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md).**

## Commands

```bash
uv sync                                          # setup (Python 3.11+)
.venv/bin/python -m pytest                       # tests (passing ≠ v1 acceptance)
python3 scripts/inventory_content_factory.py --output /tmp/content-factory-inventory.json
```

The inventory scans local sources with no model calls; it needs the local database and corpus and refuses a nonempty WAL. `scripts/capture_keyframes.py` recovers diagrams from chapter JSON (see [docs/KEYFRAME_CAPTURE.md](docs/KEYFRAME_CAPTURE.md)).

## Hard rules

- **Never commit or upload the local corpus.** `data/`, `clarified/`, root `*.srt`, and `artifacts/` are git-ignored private working artifacts; a fresh clone does not have them. `.gitignore` blocks `*.json`/`*.srt` on purpose — do not force-add.
- **Legacy generated lessons (v2 outputs) are audit-only.** Never regenerate content from them.
- **Teaching sources:** transcripts only, plus the matching YouTube lecture solely to recover a diagram that is missing or unclear.
- **Budget:** the pilot runs on the operator's zIDE quota (300M tokens, zero incremental cash). Prefer offline scripts over model calls; route heavy exploration through subagents and keep file dumps out of the main thread (see [docs/context-management-mcp-token-cost.md](docs/context-management-mcp-token-cost.md) for measured per-request overhead).
- **Don't reopen settled decisions.** Authority order is in [docs/README.md](docs/README.md#which-document-wins): goal → resolution → pilot packet; inventory is dated evidence; blindspots and older comparisons are historical context.
