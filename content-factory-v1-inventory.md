# Content Factory v1 — local inventory and pilot evidence

Inspected 2026-09-05. This is a local filesystem/database reconciliation, not evidence of current upstream availability, reuse rights, transcript fidelity, or accepted teaching quality. No pipeline imports, model calls, downloads, remote synchronization, or corpus/state/database edits were performed.

## Reproducible method

Run from the repository root:

```bash
python3 scripts/inventory_content_factory.py --output /tmp/content-factory-inventory.json
```

The [scanner](scripts/inventory_content_factory.py) also accepts `--root /absolute/repository/path`; without `--output`, it prints JSON. It copies `youtube-iug.db` into a temporary directory and queries the copy using SQLite `mode=ro&immutable=1`. It refuses a nonempty WAL and checks database size/mtime and WAL size before/after copying. The inspected WAL was empty or absent across scans. A live database with pending WAL transactions requires a separately obtained consistent snapshot; this scanner does not checkpoint or synchronize it. Snapshots remain under `/tmp` for inspection.

Only explicit playlist metadata and synchronization columns are selected; credentials and `private_meta` are not inspected. `entries` is parsed as JSON or, when applicable, with `ast.literal_eval`; malformed values remain untrusted. Artifact discovery traverses both `data/` and `GeminiLongContext/`, excluding hidden/cache/log directories; it recognizes complete 11-character video IDs by known filename suffixes. It also inventories the separate root-level sample playlist. Folder names are preserved, including a discovered typo; nothing is silently renamed.

## Reconciled counts

| Inventory unit | Count | Meaning |
|---|---:|---|
| Playlist metadata rows / unique playlist IDs | 340 / 340 | Local snapshot, superseding the unverified 321-playlist planning figure for this checkout. |
| Synchronization rows | 8,269 | Includes duplicate membership rows. |
| Unique `(video_id, playlist_id)` memberships | 8,259 | Nine repeated pairs contribute ten excess rows; one pair occurs three times. |
| Unique expected video IDs | 8,129 | Shared lectures occur in multiple playlists. |
| Raw JSON files in `data/` | 8,250 | 8,120 unique video IDs. |
| Raw SRT files in `data/` | 8,250 | Same 8,120 IDs; no JSON-only/SRT-only ID gaps. |
| Raw IDs shared between two playlist memberships | 130 | 260 copies per raw format. |
| Normalized/plain SRT files in `data/` | 8,207 | 8,077 unique IDs; presence alone does not certify transformation quality. |
| Chapter JSON files in `GeminiLongContext/` | 8,200 | 8,070 unique IDs. |
| Existing `_v2_content.json` files | 5,608 | 5,608 unique IDs; historical output format, not Content Factory v1 acceptance. |

There are no raw video IDs outside the synchronization inventory. Raw file coverage is 8,120/8,129 expected unique IDs, but this is file presence relative to the local table, not proof that upstream playlists or all source segments are complete.

### Folder alias: 34 apparent missing sources are present

All 34 videos for **Introduction To English Literature**, expected playlist `PL9fwy3NUQKwYNxhPlUU9pxwfg8zlh4TPZ`, exist under `data/L9fwy3NUQKwYNxhPlUU9pxwfg8zlh4TPZ` — its directory is missing the initial `P`.

Consequently, strict physical-folder matching reports 43 missing expected memberships and 34 unexpected physical memberships. Matching the 34 raw video IDs to their recorded playlist resolves those 34 apparent gaps, leaving nine genuinely absent IDs within the inspected raw roots. A `PL*`-only scan would incorrectly classify the entire English-literature course as missing. Preserve this mapping as an explicit migration alias; do not download or regenerate those 34 sources merely because the expected folder is absent.

### Exact IDs with no raw file in `data/`

| Video ID | Course | Recorded disposition |
|---|---|---|
| `EJ2sWNX0UFM` | حاضر العالم الإسلامي | Video `skip=1`; `downloaded_r2=0`. |
| `JLwtEdN0hmg` | فن الإذاعة والتلفزيون | Video `skip=1`; `downloaded_r2=0`. |
| `L7jciMwEMz0` | مقدمة في المهارات السريرية (2) | Video `skip=1`; `downloaded_r2=0`. |
| `SAq013FtOLQ` | البصريات الهندسية | Video `skip=1`; `downloaded_r2=0`. |
| `xqVsJVzoNU8` | مبادئ الإحصاء | Video `skip=1`; `downloaded_r2=0`. |
| `UO-vjOe-BSM` | التعليم الالكتروني E-learning | Playlist `skip=1`; video skip unset; `downloaded_r2=0`. |
| `IeBKzxIlDnQ` | طب المسنين Geriatric Medicine | Neither skip set; `downloaded_r2=0`. |
| `ShZhBn7Sho4` | علوم الجهاز العصبي الأساسية MEDC 2411 | Neither skip set; `downloaded_r2=0`. |
| `xi0uThM4sAc` | علوم الجهاز العصبي الأساسية MEDC 2411 | Neither skip set; `downloaded_r2=0`. |

Thus the nine comprise five explicit video skips, one playlist skip, and three unexplained gaps. A skip flag is a recorded disposition, not a verified reason or a complete-course waiver. Eight synchronization rows have `skip=1` in total: the other three IDs already have raw files (`rkdTm8rWz40`, `JMwSbUAxLRk`, `aN_-kh7BptU`). Existing content and skip status must therefore be reconciled separately.

### Duplicate revisions and metadata limits

SHA-256 was computed for the 130 duplicated raw IDs: **520 files**, covering both JSON and SRT copies. Every duplicated ID has one distinct JSON hash and one distinct SRT hash across its examined copies; no conflicting raw revisions were found in this duplicate-membership set. Full hashes and paths are in the scanner's JSON output. This does not certify all 8,120 unique sources, nor justify reusing lesson verdicts across different course contexts.

Of 340 playlist `entries` values, 143 parse as Python literals and 197 do not parse. All 197 malformed values have length **32,767 characters**; checked examples terminate inside a quoted value. This is strong evidence of truncated metadata, although this read-only inspection does not establish where truncation occurred. The synchronization table can support a provisional manifest, but it cannot prove that all original playlist entries were captured. Do not infer course completeness from the malformed lists.

## Historical processing state

The relevant output root is the repository's `GeminiLongContext/`. The historical chapter extractor's `cwd.parent.parent / 'GeminiLongContext'` resolves there when launched from `src/etl`; equivalent paths inferred from repository-root or `src` launch directories do not exist in the inspected workspace.

`src/etl/.transcript_processing_state.json` contains 32,644 completed item IDs, including **5,608 `_processed` markers**, and 145 failed entries. Its processed-video ID set exactly matches the 5,608 existing v2 output IDs: **zero missing-output markers and zero outputs without corresponding processed markers**. This corrects any conclusion based only on searching `data/` for v2 outputs.

However, **139 of the 145 failed entries belong to videos that also have processed markers and output files**. This overlap requires disposition review; a failure entry could be historical or a sign that an output omitted failed material. The inventory does not decide which. Output existence and matching markers cannot certify chapter/segment completeness. No exact item ID appears in both the completed and failed lists.

The separate root and `src/` state files both have empty completion lists. They should not be treated as evidence that no prior work exists. State is currently tied to launch location and video-level IDs; migration needs explicit discovery and validation of the actual artifacts.

## Three concrete pilot/challenge candidates

| Role | Local course and source ID | Raw / chapter / v2 file coverage | Evidence and remaining question |
|---|---|---|---|
| **Recommended bounded Arabic pilot** | **تكنولوجيا التعليم**, د. محمود محمد درويش الرنتيسي — `PL9fwy3NUQKwb5uWX2ICXF3-4qsXBCakIB` | **13 / 13 / 13**, against 13 unique recorded videos | Its 13-entry metadata list parses and matches memberships. Raw sample `-oZOmuChGew` is Arabic teaching prose with visible transcription errors. The course description includes preparing and using teaching aids, giving a concrete candidate skill task. Confirm intended learner/reviewer fit and whether demonstrations need missing visual evidence. |
| **Arabic/English and equation challenge** | **فيزياء عامة أ**, د. بسام السقا — `PL9fwy3NUQKwb6OQhcTn5SkdK0XkcfDNyC` | **12 / 12 / 12**, against 12 unique recorded videos | Its 12-entry metadata list parses and matches memberships. Raw sample `1noCDAkxHwg` mixes Arabic with vectors, scalars, displacement, and coordinate-system terminology. Use a bounded excerpt to probe mathematical transcription, mixed direction, and diagram dependence; it needs a physics reviewer. |
| **English challenge / partial-work recovery** | **اللغة الإنجليزية**, أ. هاني علي رباح الحلو — `PL9fwy3NUQKwZQm1WzCEzA1TRC9joCRwzb` | **30 / 30 / 24**, against 30 unique recorded videos | Metadata identifies Arabic-speaking learners and `study_lang=en`; sample `0mkSe0xrqKk` is English lecture prose. Six recorded videos lack v2 outputs. Its `entries` metadata is truncated, so full source inventory must be resolved before treating it as a complete course. |

Recommendation is based on bounded local source coverage, a plausible observable skill, and inspected language samples, **not** a judgment that the lessons are already good. All candidate raw counts mean both JSON and SRT are present. Only one raw excerpt per candidate was examined; audio/video, rendering, equations, rights, and all existing v2 contents were not validated. Use the two challenge courses for small validation sets, not automatic whole-course processing. A local file count is not a spend estimate.

The remaining choices are target learners, a qualified Arabic/subject reviewer, permission to publish the selected sources, and a numeric pilot budget. The proposed pilot remains conditional on those choices and source-sufficiency review.
