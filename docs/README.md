# Documentation map

**Open [NEXT_STEPS.md](NEXT_STEPS.md) to start the optics source-manifest task.** Read this map in about 2 minutes; open the longer references only when the task needs them.

**Teaching sources:** reprocess transcripts into new v1 content; use the matching YouTube lecture only when a needed diagram is missing or unclear. Old generated lessons are audit-only. [Full source policy](content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed).

**Current position:** the keyframe capture CLI works and legacy integrity safeguards are available for pilot preparation. The v1 runtime, calibrated quality gates, learner trial, and deployment are still unfinished.

## Start here

| File | What it contains | Open it when… |
|---|---|---|
| [README.md](README.md) | This map: short recaps, reading order, and document authority. | You need to find the right file. |
| [NEXT_STEPS.md](NEXT_STEPS.md) | The immediate offline task, expected outputs, completion checks, and later milestones. | You are ready to do the next piece of work. |
| [content-factory-v1-goal.md](content-factory-v1-goal.md) | The v1 objective, fixed decisions, quality/cost rules, and definition of done. | You need to decide what v1 must deliver. |
| [KEYFRAME_CAPTURE.md](KEYFRAME_CAPTURE.md) | Working JSON-to-video-frame tool, commands, verification, and evaluation of the Answer.AI workflow. | You need to recover a diagram from a lecture. |
| [content-factory-v1-pilot.md](content-factory-v1-pilot.md) | The selected optics course, verified local counts, challenge cases, and review fields. | You are preparing sources or arranging a reviewer. |
| [pilot-opto-2311-plan.md](pilot-opto-2311-plan.md) | The full production plan: CF-01…CF-13, evidence/qualification subtickets, release gates, operations and repair, 21 control findings, discovery drills, and session briefs. | You are executing, scheduling, or resourcing the pilot. |
| [opto-2311-source-review.md](opto-2311-source-review.md) | CF-01 evidence report: recomputed counts, eligible vs audit-only variants, integrity findings, source gaps, order evidence, and scope-freeze blockers. | You need the current source-truth for the optics pilot. |
| [opto-2311-first-review.md](opto-2311-first-review.md) | CF-02 draft skill sheet for the first/middle/final lectures with candidate skills, evidence spans, and reviewer decisions. | You are the subject reviewer, or preparing their first review. |
| [opto-2311-scope-freeze.md](opto-2311-scope-freeze.md) | CF-03 scope-freeze DRAFT: verified inputs, the nine-item freeze checklist, and remaining OPEN gates. | You are closing or checking the scope freeze. |
| [COURSE_RUBRIC.md](COURSE_RUBRIC.md) | The v1 grading rubric: four checks, the 12 hard-failure classes, teaching-node coverage, judge plan, and OPEN calibration thresholds. | You are calibrating, judging, or reviewing lessons. |

## Reference files

| File | What it contains | Open it when… |
|---|---|---|
| [content-factory-v1-resolution.md](content-factory-v1-resolution.md) | Decisions for all 13 blindspots, including correction authority, evaluations, formats, caching, quota accounting, and withdrawal. | You are implementing a rule or need its required proof. |
| [content-factory-v1-inventory.md](content-factory-v1-inventory.md) | Measured source/output counts, missing IDs, duplicate hashes, folder aliases, and metadata limitations. | You need evidence about transcripts and historical output coverage. |
| [content-factory-v1-blindspots.md](content-factory-v1-blindspots.md) | The historical review: 13 risks, supporting evidence, and discovery experiments. | You need to understand why a control was added. |
| [platform-map-brief.md](platform-map-brief.md) | The broader courses platform: reading experience, RTL, quizzes, graph/wiki, and stack-comparison scope. | You are planning platform features beyond the factory. |
| [skills-map.md](skills-map.md) | Candidate skills/tools, their possible roles, license questions, and operating costs. | You are choosing a tool for a specific stage. |
| [fanout-feature-analysis.md](fanout-feature-analysis.md) | Feature-by-feature disassembly of Fanout (fanout.sh) from the `inspiring/fanout-company/` screenshots, with adopt/adapt/skip verdicts against the platform map. Its adopted patterns are folded into the brief, skills map, and pilot milestones. | You are designing a platform feature and want the benchmark or the reason to skip. |
| [context-management-mcp-token-cost.md](context-management-mcp-token-cost.md) | Measured "empty prompt" token cost of every installed MCP server and the skills index, industry benchmarks, and the ranked context-management fixes for this machine. | You are tuning agent token budgets, quota burn, or fanout per-agent overhead. |

The repository's [root README](../README.md) is the short project entrypoint with setup, test, and inventory commands.

## Which document wins?

1. The **goal** owns current v1 scope and fixed decisions: transcript-based reprocessing with YouTube diagrams only as needed, optics, zIDE quota, zero incremental cash, and Cloudflare Pages.
2. The **resolution** supplies implementation rules; the **pilot packet** applies them to the selected course.
3. **Inventory** is dated evidence. **Blindspots** and older candidate comparisons retain historical context, not authority to reopen a settled choice.
4. The **platform map** defines broader product scope. The **skills map** supplies candidates, not approved dependencies.
5. **Next steps** describes execution order. Update it when a milestone is proved; a checklist alone cannot certify implementation.

## Already known

The optics pilot has **106 recorded video IDs**, **105 raw/post-processed transcript sets**, **105 chapter files**, and **83 legacy v2 outputs**. One skipped source is absent; 22 available-source videos have no v2 output. All 105 available transcript sets are in scope for fresh v1 processing; old output counts do not reduce that work. Its playlist `entries` field is truncated, so lecture order still needs trustworthy evidence.

**Next action — under 2 minutes:** open [Ticket CF-01](NEXT_STEPS.md#ticket-cf-01-build-the-optics-source-manifest).
