# Context management & the "empty prompt" token cost of MCP/tools

## CODEX APPLIED 2026-09-08: global MCP duplication removed

The earlier measurements below are for Claude. Codex was audited separately with its own prompt renderer and configuration.

- `codex debug prompt-input x` produced **11,242 message-context tokens** under `tiktoken o200k_base` for a fresh one-character prompt. This covers rendered developer/user messages, not separately supplied tool schemas.
- The rendered skills block was **22,237 characters** before and **22,237 characters** after duplicate-only pruning. Codex expands the remaining descriptions to its catalog budget, so removing duplicate skill entries did not reduce this block. Unique-skill pruning was tested, showed essentially no byte saving, and was rolled back.
- Disabled globally: `gitnexus`, `expect`, `browser-tools`, `chrome-devtools`, `playwright`, and `zai-mcp-server`. Retained: Codex's `node_repl` plus the five lean remote servers `context7`, `deepwiki`, `web-reader`, `web-search-prime`, and `zread`.
- Disabled duplicate plugins: `code-review@claude-plugins-official` and `mattpocock-skills@claude-plugins-official`; their identical bare skills remain available.
- Moved **34 byte-identical** `~/.codex/skills` duplicates to `~/.codex/skills-disabled-context-20260907/`; the retained copies are in `~/.agents/skills/`.
- Recovery: restore `~/.codex/config.toml.bak-codex-context-20260907`, then move the dated disabled-skill directory's children back into `~/.codex/skills/`.

`codex --strict-config doctor --summary` passed after the change: 19 checks OK, no warnings or failures. The useful Codex gain is fewer global server startups and no duplicate capabilities; the measured message-token baseline remains **11.2k**, so this report does not claim a skill-index token saving.

---

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

Repo-side round-2 changes (this branch): added a root **`AGENTS.md`** (with a **`CLAUDE.md`** symlink) so agents orient from one ~350-token file instead of re-reading the map each session, and converted two blindspots evidence links that point into the git-ignored local corpus to code spans (they broke for every fresh clone/GitHub reader, verified by link check across all docs).

---

## Claude current cost after both applied rounds

These numbers describe different measurements and must not be added as if they came from one trace:

| Measurement | Current result | Meaning |
|---|---:|---|
| Fresh `claude -p` request with a one-word prompt | **31,152 input tokens** | End-to-end CLI measurement; includes the prompt and whatever the harness loaded for that request |
| Enabled global MCP schemas | **~2,528 tokens** | `tools/list` schemas for the five retained lean servers, tokenized with `tiktoken o200k_base` |
| Indexed skills | **~10,510 tokens** (165 skills) | Separate interactive-session index measurement; full skill bodies still load only when invoked |

The only observed end-to-end current total is **31,152 input tokens** for the fresh one-word CLI request. If an interactive client adds the measured skill index to an otherwise comparable prefix, **~41.7k** is a planning estimate, not a separately observed total. Prompt caching and client loading behavior change billed/accounted tokens across later requests.

## Historical baseline before the fixes

The following measurements explain why the two pruning rounds were performed. They are retained as dated evidence, not a description of the current global configuration.

**Method (2026-09-06):** launch the then-configured MCP servers, call `tools/list`, and tokenize the exact JSON schemas with `tiktoken o200k_base` (within ~10% of Claude/GLM tokenizers). The old skills index was measured from 204 installed `SKILL.md` frontmatters.

| Component | Size | Notes |
|---|---|---|
| **gitnexus MCP** (formerly global) | **~16,036 tokens** (17 tools) | Biggest single offender; `impact` tool alone ≈ 4,455 |
| **browser-tools MCP** (formerly global) | **~7,409 tokens** (16 tools) | |
| **chrome-devtools MCP** (formerly global) | **~6,817 tokens** (29 tools) | |
| **playwright MCP** (formerly global) | **~4,794 tokens** (24 tools) | |
| **context7 MCP** (retained globally) | **~1,110 tokens** (2 tools) | |
| **deepwiki MCP** (retained globally) | **~442 tokens** (3 tools) | |
| **expect MCP** (formerly global) | broken | npx fails with an ESM resolution error; server never loads |
| **zai-mcp-server, web-search-prime, web-reader, zread** | est. ~1–3k combined | Auth'd remote servers; small tool counts |
| **Skills index** (204 skills, name+description only) | **~12,500 tokens** | Injected into every request; full skill bodies (~247k tokens combined) load only on invoke |
| Global CLAUDE.md | ~47 tokens | Negligible |

**At baseline, six measured servers carried ~36,600 tokens (91 tools); all 11 configured global servers were estimated at ~38–40k.**

### Historical full-prefix estimate

Adding the harness system prompt (~2–3k), built-in tool definitions (~15–20k), the then-global MCP tools (~38–40k), the old skills index (~12.5k), and per-session environment/git context (~1–2k) produced this pre-fix estimate:

> **Historical estimate: ≈70–80k prefix tokens before useful task content.** This was not an end-to-end empty-prompt measurement and is not the current cost.

## Industry benchmarks (sanity check)

- Anthropic's internal test: a heavy tool library cost **134k tokens before the first prompt**; tool search cut it to **~5k (−85%)** with *accuracy gains* ([Anthropic, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).
- Claude Code A/B test on runs that called at least one MCP tool: **51k → 8.5k tokens (−46.9%)** with tool search enabled ([summary](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)).
- Multi-server setups commonly burn **30k–100k+ tokens before the agent starts**: 200–500 tokens per tool definition, so 5 servers × 30 tools ≈ 30–60k ([Albato](https://albato.com/blog/publications/embedded-mcp-context-bloat-hallucinations)); "55k+ tokens before a single user message" ([Apideck](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)); "100k tokens before a single question" for SQL/GitHub/Slack-scale servers ([Solo.io](https://www.solo.io/blog/keeping-context-and-tokens-low-with-progressive-disclosure-in-agentgateway)).

The historical ~38–40k MCP estimate plus ~12.5k skills index sat in the published range. The applied pruning reduced those components to ~2,528 and ~10,510 tokens respectively.

## What it actually costs us

1. **Money/quota:** prefix tokens still count as input. Prompt caching can make repeats cheaper, while a new session, compaction, or changed prefix can require another full write. Use the runtime's reported input/cache accounting; do not project spend from the obsolete ~75k estimate.
2. **Context window:** any definitions loaded into a request reduce room for task content one-for-one. The measured current CLI request was 31,152 input tokens; interactive sessions may additionally carry the separately measured ~10,510-token skill index.
3. **Quality:** accuracy measurably *drops* with too many always-loaded tools (49% → 74% on Opus 4 when deferring tool loading — [claude-code#12836](https://github.com/anthropics/claude-code/issues/12836)). Tools also compete for attention.
4. **Fanout multiplies it:** every spawned agent has its own context cost. The old ~40k avoidable-MCP multiplier has been removed; future budgets must use observed per-agent usage from the actual harness.

## Current best practices

1. **Preserve the slim global set.** Keep heavyweight MCPs disabled globally; enable a browser or GitNexus only in a project that needs it. Avoid restoring overlapping browser servers together.
2. **Keep `expect` disabled until it launches reliably.** It has recorded use, so it is not dead weight, but the tested package is currently broken. The preserved configuration makes restoration reversible.
3. **Prune skills only from evidence.** The current 165-skill index is ~10,510 tokens. Retain used skills, suite dependencies, recently modified skills, and cross-references; do not remove retained bundles such as `caveman` merely to chase an unmeasured target.
4. **Prefer CLIs where a good CLI exists** (`gh`, `gcloud`, Atlassian CLI): no always-loaded MCP schema, and results enter context only when called ([Apideck argument](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)).
5. **Use tool search or deferred loading where the client supports it** (−85% in Anthropic's cited test, with accuracy gains — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)).
6. **Keep prefixes cache-friendly:** avoid changing instructions/settings mid-session, keep stable material before volatile material, and re-measure after compaction or configuration changes.
7. **Isolate heavy exploration** as described in [fanout-feature-analysis.md](fanout-feature-analysis.md): return compact summaries and paginate large file/HTML results. Tool results can outweigh schema cost.

## Sources

- [Anthropic — Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic — Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [claude-code#12836 — tool search accuracy/token results](https://github.com/anthropics/claude-code/issues/12836)
- [Joe Njenga — Claude Code cut MCP context bloat 46.9%](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)
- [Apideck — Your MCP Server Is Eating Your Context Window](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)
- [Solo.io — Progressive disclosure in agentgateway](https://www.solo.io/blog/keeping-context-and-tokens-low-with-progressive-disclosure-in-agentgateway)
- [Albato — How too many MCPs break your AI agent](https://albato.com/blog/publications/embedded-mcp-context-bloat-hallucinations)
- [Anthropic — Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
