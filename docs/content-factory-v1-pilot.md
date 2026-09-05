# Content Factory v1 — optics pilot packet

**Quick read:** The selected course, actual local coverage, challenge cases, and reviewer inputs. Open [the first task](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest) to prepare the sources.

**Source rule:** reprocess the optics course from transcripts. Use its matching YouTube lectures only to recover needed diagrams. Legacy generated chapters/lessons remain inventory artifacts; their presence does not skip v1 work. See the [binding policy](content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed).

Status: optics is selected in [the goal](content-factory-v1-goal.md). Source completeness/order, subject approval, learner evidence, and per-run/pilot token allocations remain unverified. The earlier Educational Technology recommendation is historical.

## Fixed scope

| Decision | Value |
|---|---|
| Course | **OPTO 2311 — البصريات الهندسية**, كلية العلوم الصحية. |
| Playlist | `PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-`. |
| Execution | This repository; zIDE-only model work; zero incremental cash. |
| Budget / hosting | Operator-stated 300M-token subscription quota; Cloudflare Pages. Numeric run/pilot allocations and actual remaining quota still need recording. |

Working learner assumption: Arabic-speaking undergraduates with the actual optics-course prerequisites. Confirm those prerequisites from transcript evidence before defining the baseline skill task. An optics subject reviewer must establish whether the explanations, equations, sign conventions, diagrams, and answers are correct.

The goal's runner-up is **جبر حديث 1**, playlist `PL9fwy3NUQKwZKOpj354PRgwYPWWgxchnI`. Its local coverage is 59 raw/post-processed transcript sets, 59 chapter files, and 49 legacy outputs. It is an alternative only if the selected pilot proves unsuitable; no automatic scope switch is authorized by a missing source or failed lesson.

## Local evidence — checked 2026-09-05

| Item | Count / finding |
|---|---|
| Recorded videos | 106 distinct IDs. |
| Raw JSON, raw SRT, post-processed SRT | 105 of each. |
| Chapter files / older v2 outputs | 105 / 83. |
| Source gap | `SAq013FtOLQ` has `skip=1` and no raw file; the reason and effect on promised outcomes remain unresolved. |
| Legacy output / order gaps | 22 available-source videos have no v2 output. The 32,767-character playlist `entries` field is truncated; it cannot establish lecture order. |

Paths are relative to the repository root: `data/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/` and `GeminiLongContext/PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-/`. [The inventory](content-factory-v1-inventory.md#selected-optics-pilot--follow-up-inspection) records the method and limits. Legacy file counts describe historical work, not how many v1 lessons can be skipped. Every selected transcript still needs the new processing path.

## First source review

1. Build a per-video manifest covering all 106 recorded IDs, including the skipped one. Preserve each source and processed variant with its path/hash and current evidence status.
2. Establish lecture order from trustworthy metadata. Record unknown positions if the evidence is incomplete; filenames or database row order are not a substitute.
3. Once order is verified, choose first, middle, and final lectures. For each, identify a tangible candidate skill and its original evidence spans.
4. Classify each skill as supported, needing a diagram from the matching YouTube lecture, or unsupported. Record the missing visual, its lecture timestamp, and recovery effort. No external teaching supplements are allowed.
5. Have the subject reviewer check a worked example and an unseen task independently. Freeze full-course outcome coverage after this discovery and before authoring.

## Bounded challenge cases

| Case | Source | Purpose |
|---|---|---|
| Mathematics and mixed language | فيزياء عامة أ — `PL9fwy3NUQKwb6OQhcTn5SkdK0XkcfDNyC`, video `1noCDAkxHwg` | Arabic/English notation, equations, diagrams, and mixed-direction rendering. |
| English and incomplete legacy work | اللغة الإنجليزية — `PL9fwy3NUQKwZQm1WzCEzA1TRC9joCRwzb`, video `0mkSe0xrqKk` | English prose and recovery behavior; this course has 30 raw/chapter files and 24 legacy outputs. |
| Unseen visual referred to in text | Digital-logic sample `Kzxd5D8ZgnQ`, 13:37 | Recover the referenced diagram from this same YouTube video at the relevant timestamp; if it is unavailable or unreadable, block teaching its contents. |

These are small validation excerpts, not additional whole-course launches. Reading or analyzing an excerpt makes its source family development data; reserve different unseen families for the final holdout.

## Inputs for the reviewer and operator

| Input | Status / action |
|---|---|
| Subject and Arabic editorial review | Names/roles pending. The same person may cover both if qualified; reference decisions precede model scores. |
| Learners and prerequisites | Pending. Proposed 5–8 learners for formative discovery; define the final-task criterion before testing. |
| Source/font/asset permission | Pending for transcripts, needed YouTube diagram captures, fonts/assets, and the skipped video's disposition. |
| zIDE observability | Verify work submission, model identity, usage reporting, quota period/reset, and interruption recovery. Capabilities are not assumed. |
| Run / pilot token allocations | Pending after measuring input volumes and remaining quota. The 300M figure is the total stated allowance, not permission to consume it all in one run. |

Per-outcome records must capture the learner/task/prerequisites; original evidence IDs/timecodes/revisions; sufficiency and correction decisions; worked example/practice/unaided transfer task with independent answers; required lesson/quiz/diagram/wiki/graph IDs. The detailed rules live in [the resolution](content-factory-v1-resolution.md).

**Next action — under 2 minutes:** open [Ticket CF-01](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest). Offline preparation can proceed while reviewer availability is being arranged.
