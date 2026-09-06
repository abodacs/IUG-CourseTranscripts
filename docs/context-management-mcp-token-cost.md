# Context management & the "empty prompt" token cost of MCP/tools

## APPLIED 2026-09-06: global MCP slimmed, target hit

The fix below is **implemented**, not just recommended. Global `mcpServers` in `~/.claude.json` now keeps only the five lean servers (context7, deepwiki, web-search-prime, web-reader, zread = **~2,528 measured tool-schema tokens — inside the 1–3k target**, down from ~39.5k across 11 servers).

End-to-end verification on `glm-5.3[1m]`, fresh session, one-word prompt (`claude -p`):

| | input tokens |
|---|---|
| Before (11 global servers) | 41,051 |
| After (5 lean servers) | **31,152** |
| **Saved per request** | **9,899 (−24%)**, before prompt-caching effects on top |

All five kept servers verified ✔ Connected via `claude mcp list`. Disabled: gitnexus, browser-tools, chrome-devtools, playwright, zai-mcp-server (vision tools), expect (was broken). The disabled six' full configs are preserved in `~/.claude/disabled-mcp-servers.json`; restore is a copy-paste back into `mcpServers`, or revert with `cp ~/.claude.json.bak-20260906-mcp-slim ~/.claude.json`. Scope gitnexus/chrome-devtools/browser-tools into specific projects' `.mcp.json` where a project truly needs them (bloowatch projects already do this).

Note: the −24% delta is smaller than the ~35k of disabled schema tokens because `claude -p` startup only includes servers that initialize in time, and several of the disabled ones were failing/slow to start in practice — which is also why removing them costs nothing in practice. The remaining ~31k of the empty prompt is harness system prompt + built-in tools (not MCP-configurable); in interactive sessions add the ~12.5k skills index, which is the next lever (disable unused plugin bundles) if total overhead must shrink further.

---

## ROUND 2 (2026-09-06): skill-index prune, guided by usage data — applied

`~/.claude.json` records per-skill/per-plugin usage across 3,063 startups, so pruning ran on evidence, not vibes:

- **Skills index: ~12,499 → ~10,510 tokens** (204 → 165 indexed `SKILL.md` files). 39 skill dirs with **zero recorded use ever** moved to `~/.agents/skills-disabled/` (manifest + `restore.sh` inside; restore one or all).
- **Cross-reference safety filter:** a first pass flagged 55 candidates, but 16 of them (`polish`, `clarify`, `audit`, `extract`, `critique`, `harden`, …) are referenced by heavily-used kept skills (`impeccable`, `thermo-nuclear-code-quality-review`, …) — those were **spared**. Keep-policy union: ever used, member of a used suite, modified in 30 days, or referenced by a kept skill.
- **Plugins disabled** in `~/.claude/settings.json` (backup `settings.json.bak-round2-20260906`): `mattpocock-skills` (its skills remain available under identical bare names from `~/.agents/skills`/`~/.zcode/skills`) and `marketing-board` (zero uses ever). Heavily-used plugins untouched: typescript-lsp (4,621 uses), pyright-lsp (3,082), caveman (237), pyright (495).
- **Correction to round 1:** `expect` was called "dead weight" — usage data shows 13 calls, the last 3 days ago. Retested after clearing the corrupted npx cache: `expect-cli` fails to launch at `@latest` *and* `0.1.3` even on fresh installs (upstream ESM breakage, `--help` exits 1). It stays disabled until upstream fixes it; restore from `~/.claude/disabled-mcp-servers.json`, or use it from Cursor where it is also configured.

Repo-side round-2 changes (this branch): added a root **`CLAUDE.md`** (with an **`AGENTS.md`** symlink) so agents orient from one ~350-token file instead of re-reading the map each session, and converted two blindspots evidence links that point into the git-ignored local corpus to code spans (they broke for every fresh clone/GitHub reader, verified by link check across all docs).

---

**Question:** what does it cost us, in tokens, to have our MCP servers and tool/skill definitions loaded before any real work starts — and what is the best context-management practice around it?

**Method:** measured on this machine (2026-09-06) by launching the actual MCP servers, calling `tools/list`, and tokenizing the exact JSON schemas with `tiktoken o200k_base` (within ~10% of Claude/GLM tokenizers). Skills index measured from the 204 installed `SKILL.md` frontmatters. Industry benchmarks from the sources at the bottom.

## Measured on this machine, per request, before the first user message

| Component | Size | Notes |
|---|---|---|
| **gitnexus MCP** (global) | **~16,036 tokens** (17 tools) | Biggest single offender; `impact` tool alone ≈ 4,455 |
| **browser-tools MCP** (global) | **~7,409 tokens** (16 tools) | |
| **chrome-devtools MCP** (global) | **~6,817 tokens** (29 tools) | |
| **playwright MCP** (global) | **~4,794 tokens** (24 tools) | |
| **context7 MCP** (global) | **~1,110 tokens** (2 tools) | |
| **deepwiki MCP** (global) | **~442 tokens** (3 tools) | |
| **expect MCP** (global) | broken | npx fails with an ESM resolution error; server never loads |
| **zai-mcp-server, web-search-prime, web-reader, zread** | est. ~1–3k combined | Auth'd remote servers; small tool counts |
| **Skills index** (204 skills, name+description only) | **~12,500 tokens** | Injected into every request; full skill bodies (~247k tokens combined) load only on invoke |
| Global CLAUDE.md | ~47 tokens | Negligible |

**Six measured servers alone carry ~36,600 tokens (91 tools). All 11 global servers ≈ 38–40k tokens.**

### The full "empty prompt" stack

Adding the harness system prompt (~2–3k), built-in tool definitions (~15–20k), the MCP tools above (~38–40k), the skills index (~12.5k), and per-session environment/git context (~1–2k):

> **≈ 70–80k tokens are consumed in this setup before the user types anything.** On a ~200k-token model that is over a third of the context window spent before work starts.

## Industry benchmarks (sanity check)

- Anthropic's internal test: a heavy tool library cost **134k tokens before the first prompt**; tool search cut it to **~5k (−85%)** with *accuracy gains* ([Anthropic, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).
- Claude Code A/B test on runs that called at least one MCP tool: **51k → 8.5k tokens (−46.9%)** with tool search enabled ([summary](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)).
- Multi-server setups commonly burn **30k–100k+ tokens before the agent starts**: 200–500 tokens per tool definition, so 5 servers × 30 tools ≈ 30–60k ([Albato](https://albato.com/blog/publications/embedded-mcp-context-bloat-hallucinations)); "55k+ tokens before a single user message" ([Apideck](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)); "100k tokens before a single question" for SQL/GitHub/Slack-scale servers ([Solo.io](https://www.solo.io/blog/keeping-context-and-tokens-low-with-progressive-disclosure-in-agentgateway)).

Our measured ~38–40k of MCP + ~12.5k of skills sits right in the published range.

## What it actually costs us

1. **Money/quota:** the prefix is sent with *every* API request in the session. With prompt caching, repeats are cheap cache reads — but cache misses (new session, after compaction, prefix changed) re-pay full input price. At ~75k overhead, a few hundred requests/day is 15–20M input tokens of pure overhead, a real share of a subscription quota like the zIDE/GLM plan this project depends on.
2. **Context window:** overhead directly shrinks the working window. `CLAUDE_CODE_AUTO_COMPACT_WINDOW=150000` minus ~75k of prefix leaves ~75k of real work room; trimming overhead extends it one-for-one.
3. **Quality:** accuracy measurably *drops* with too many always-loaded tools (49% → 74% on Opus 4 when deferring tool loading — [claude-code#12836](https://github.com/anthropics/claude-code/issues/12836)). Tools also compete for attention.
4. **Fanout multiplies it:** in the subagent/fanout architecture this repo is planning, **every spawned agent pays its own prefix**. 40k of avoidable MCP overhead × N agents is the single largest lever on pilot token budgets.

## Best-practice ranking for this setup (by tokens saved per request)

1. **Move global MCP servers to per-project `.mcp.json`.** Only context7/web-reader/web-search-prime earn global status. Moving gitnexus, chrome-devtools, browser-tools, playwright into the projects that need them saves ~30k+ tokens in every other project. Note: the gitnexus *skills* are already disabled via `skillOverrides`, but the gitnexus *MCP server* (16k) is still global — the expensive half is still on.
2. **Keep exactly one browser-automation server.** Playwright + chrome-devtools + browser-tools overlap ≈ **19k tokens**; keep one (playwright is the leanest per capability).
3. **Delete `expect`** — it is broken at launch and pure dead weight.
4. **Prune skills/plugins.** 204 skills cost ~12.5k of index on every request. Disabling unused plugin bundles (marketing-board, i-have-adhd, caveman, mattpocock-skills, refactoring-ui, …) can cut ~8–9k. Progressive disclosure already keeps skill *bodies* off the prompt — only the index is the fixed cost.
5. **Prefer CLIs over MCP where a good CLI exists** (`gh`, `gcloud`, atlassian CLI): zero tool-schema tokens, results stay out of context until called ([Apideck argument](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)).
6. **Use tool search / deferred tool loading where the client supports it** (−85%, with accuracy gains — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)); the skill-index pattern is the same idea and already works here.
7. **Cache-friendly hygiene:** keep the prefix byte-stable within a session (don't edit CLAUDE.md/settings mid-session), stable-before-volatile ordering, and remember compaction re-pays the full prefix write.
8. **Subagent isolation for heavy exploration** — already the plan in [fanout-feature-analysis.md](fanout-feature-analysis.md): fan out readers, return summaries, keep tool-result floods out of the main thread. Tool *results* (file dumps, HTML) typically dwarf schema costs; truncation/pagination discipline matters as much as schema trimming.

## Sources

- [Anthropic — Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic — Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [claude-code#12836 — tool search accuracy/token results](https://github.com/anthropics/claude-code/issues/12836)
- [Joe Njenga — Claude Code cut MCP context bloat 46.9%](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)
- [Apideck — Your MCP Server Is Eating Your Context Window](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)
- [Solo.io — Progressive disclosure in agentgateway](https://www.solo.io/blog/keeping-context-and-tokens-low-with-progressive-disclosure-in-agentgateway)
- [Albato — How too many MCPs break your AI agent](https://albato.com/blog/publications/embedded-mcp-context-bloat-hallucinations)
- [Anthropic — Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
