# Skills map — where each candidate skill plugs in

**Quick read:** Candidate skills/tools, their proposed roles, and license/cost checks. These are options to verify, not a list to install wholesale.

**Available locally:** [keyframe capture CLI and Answer.AI evaluation](../factory/KEYFRAME_CAPTURE.md). It reads the existing chapter JSON hints and saves actual video frames; no model calls or SolveIt dependency.

**Teaching-source constraint:** tools may transform raw whisper JSON and its matched cleaned `GeminiLongContext/` counterparts, and recover needed diagrams from the matching YouTube lectures. Tool recommendations do not authorize external course material, broad video ingestion, or unmatched/unbound generated lessons as authoring inputs. Read the [source policy](../factory/content-factory-v1-goal.md#allowed-teaching-sources--user-confirmed).


Companion to [platform-map-brief.md](../platform/platform-map-brief.md). Research date: 2026-09-05. Verdicts: ✅ adopt · 📦 already installed locally · 🔧 adapt/re-vendor · 📐 pattern only, don't depend · ❌ skip.

**Delivery contract:** the existing pipeline is Content Factory v0; the next version is defined in [content-factory-v1-goal.md](../factory/content-factory-v1-goal.md). Apple-grade quality control covers every stage. Candidate verdicts below are research recommendations, not proof of license clearance, Arabic quality, integration, or zero operating cost. Verify the selected revision before adoption; install only what the current stage needs. The [blindspot resolutions](../factory/content-factory-v1-resolution.md) define required source sufficiency, independent correctness review, learner evidence, and runtime contracts; a skill cannot substitute for those proofs.

**Headline finding:** across everything checked, only **two** items touch Arabic/RTL at all (`rtl-web-development-skill` for UI, `Arab-Writer` for prose) — and one high-quality one is redundant with skills already installed. RTL remains the platform's own differentiating work.

---

## 1. Content pipeline (transcript → lesson MD)

### education-agent-skills (GarethManning) ✅
165 evidence-grounded pedagogy skills in 20 domains (retrieval practice, spacing, cognitive load, curriculum design & assessment, scope & sequence, hint ladders, teach-back evaluators). 731★, CC BY-SA 4.0, ships a registry + tests.
- **Use for:** brief constraints 3 & 8 — the course rubric, lesson anatomy, quiz authoring guidance, and the "latest pedagogy standards" research ticket. Its Curriculum Design & Assessment + Student-Facing Learning Skills domains map almost 1:1 onto the lesson format.
- **Watch out:** English-only (no RTL); CC BY-SA is share-alike — fine to consult, check before embedding its text verbatim in shipped content.

### dair-academy-plugins (dair-ai) — 3 of 8 plugins relevant, MIT, 611★
- `youtube-notetaker` 🔧 — YouTube → markdown study file with timestamped transcript + extracted slide images (uses existing VTT captions, yt-dlp + ffmpeg). Potential use is limited to recovering a needed diagram from the matching lecture at a recorded timestamp; do not adopt its generated study notes as teaching evidence. Slide extraction is something the current pipeline does not do. Arabic auto-captions quality is a known risk.
- `wiki-builder` 🔧 — reusable research wikis with per-wiki structure/flavors. Compare against our openwiki design (OKF v0.2) before building.
- `lesson-generator` / `learn` 📐 — patterns only: lesson-generator outputs HTML, not MD; `learn` is an interactive tutoring pattern worth mining for the reader experience.
- `llm-council` 📐 — multi-model deliberation pattern (parallel answers → cross-ranking → chair synthesis; needs Fireworks key). Good shape for the LLM-judged gates, but it has **no rubric** — we supply ours.

## 2. Knowledge graph & openwiki

### graphify (Graphify-Labs) ✅ — the direct hit
`/graphify` turns any folder into a queryable knowledge graph. Ingests **markdown/docs** (plus code via AST, PDFs via citation mining, images via vision). Outputs `graph.json`, interactive `graph.html`, an **Obsidian vault**, a **Wikipedia-style `wiki/` per community**, and a report (god nodes, surprising connections). Every edge tagged EXTRACTED / INFERRED / AMBIGUOUS. Apache-2.0, 114k★, pushed today.
- **Use for:** brief constraint 6 — concept nodes + typed edges across the corpus, and a strong candidate substrate for the per-course/lesson openwiki layer (evaluate its wiki output vs. OKF v0.2 representation). The UX bar on top of this output is Fanout's Knowledge Topography ([fanout-feature-analysis.md](fanout-feature-analysis.md) §3.3): a first-class destination page, search over concepts/aliases/lessons (the Arabic ↔ English term hook), a course filter, progress-tinted nodes, and a drag-to-neighbors view — none ship with graphify; treat them as our layer.
- **Watch out:** Arabic NLP quality rides on the underlying model, not graphify; edges need our pedagogy-aware ontology typing. Markdown/docs semantic extraction also uses a model; budget it alongside wiki generation, not just image ingestion. Verify outputs against the chosen revision. [Upstream runtime distinction](https://github.com/Graphify-Labs/graphify#readme).

## 3. Lesson visuals (Excalidraw + motion)

### glowmotion (SylphAI) ✅
Animated technical diagrams as **self-contained HTML+SVG** with glowing flow trails; accepts Mermaid input; pure-stdlib Python layout + mandatory `check_diagram.py` verification; dark/light themes; optional GIF/MP4 export. MIT, 110★.
- **Use for:** brief constraint 3 — the animated "aha moment" diagrams. Confirmed pairing with Excalidraw MCP: **Excalidraw = authored, editable static source; glowmotion = the animated HTML render** (feed it the semantic graph JSON / Mermaid derived from the Excalidraw file).
- **Watch out:** no RTL in SVG text — needs our `dir` handling layered on.

### visual-explainer (nicobailon) ✅
Self-contained HTML visual explanations with smart representation routing (Mermaid / CSS-grid cards / tables / Chart.js), design rules baked in, slide mode with PPTX export, optional MCP server. MIT, 9.6k★, very active.
- **Use for:** lesson figures beyond hand-drawn diagrams — architecture/flow explainers, comparison tables; `/generate-web-diagram` and `/generate-slides` in the authoring pipeline.
- **Watch out:** zero RTL/Arabic awareness — same treatment as glowmotion.

### hyperframes official family 📦 (already installed: 8 skills in `~/.agents/skills/`)
Video-from-HTML runtime (HTML composition + `data-*` timing + seekable runtime + CLI). `/faceless-explainer` explains a topic/article with invented visuals — the natural "animated lesson intro / course trailer" path.
- **Use for:** course promo videos, animated explainers, motion titles inside or alongside lessons.

### hyperframes-motion-director (geekjourneyx) ❌ skip
Third-party director layer over the same runtime. Substantive (two-phase gated production, scene schemas), **but**: AGPL-3.0 (copyleft risk if it touches the served product), Chinese-first defaults (9:16 promo orientation), ~6 weeks stale, and redundant — the official family already installed covers this ground. If its brief/storyboard structure appeals, mine it as a pattern, don't install.

## 4. Reader features

### eli5 (dzhng) 🔧 — template, not the tool
Very well-crafted skill ("simplify the telling, never the claims", standalone-readability self-test, strict Problem/Solution/Changes shape) — but it explains **engineering diffs to technical teammates**, and is `disable-model-invocation: true`.
- **Use for:** the user-selected-passage → floating "ELI5" button is a **platform feature + a new passage-scoped skill** we write, using this one as a template after checking reuse rights. Our variant must be Arabic-capable and graded by the same quality gates. For v1, prefer precomputed, reviewed explanations; live model invocation needs a separate bounded service and quality design and is not a zero-cost static feature.

### term-radar (SidKH) 📐 — mismatch with intended use
16 lines: it surfaces the canonical term of art with a Google Images link, appended to a response. **No tracking, no vocabulary store** — the "growing vocabulary" tagline overstates it. No license file.
- **Use for:** the vocabulary/concepts section needs an independently authored **custom glossary skill** wired to the knowledge graph (terms + Arabic equivalents + lesson back-references). Do not copy unlicensed skill text.

### i-have-adhd (ayghri) 📦 applied to documentation
Installed skill version 0.2.0 was read for this documentation pass. Reported MIT. Its output rules include: action first, numbered steps, ≤5-item lists, visible progress, time estimates, no preamble/filler.
- **Use for:** (a) output style for our own build agents; (b) more importantly, the rules translate directly into **lesson formatting for attention** — chunking, progress indicators, next-step cues in the reader UI. Rules are trivially translatable to Arabic; the repo has no Arabic translation.

### Client-side search index (Pagefind-style) 📐 pattern
Fanout's Cmd+K searches lessons, papers, tools, and notes with course-aware scopes ([fanout-feature-analysis.md](fanout-feature-analysis.md) §3.14). The static-first analogue is a prebuilt client-side search index (Pagefind-style; MIT reported — verify the chosen revision before adoption) with course context as the scope filter.
- **Use for:** the platform search surface, post-v1. The pattern to keep: one index, scopes that follow the active course.

## 5. Writing style — Arabic & English

### Arab-Writer (turky015-oss) 📐 reference candidate — reuse permission unresolved
Genuinely good, concrete rules: AI-marker phrase lists in Arabic ("في عالم اليوم…", English calques, empty intensifiers), orthography checklist (hamzat qaṭʿ/waṣl, tāʾ marbūṭa, alif maqṣūra, tanwīn, Arabic punctuation), register rules (fuṣḥá vs dialect), self-scoring /60.
- **Watch out:** the research notes report **no license file**, and the skill ships inside a zip. Verify permission before copying or adapting its lists. Otherwise author an independent `arabic-style` skill using appropriately licensed references; attribution alone does not grant reuse rights.
- **Use for:** brief constraint on Arabic content quality — the de-AI-fication + proofreading pass on generated Arabic lesson prose, and as the Arabic counterpart judged by the same paragraph gates.

### govuk-style (fofr gist) ✅ for English docs
Applies the GOV.UK style guide: front-load everything, one idea per sentence (~15–20 words), active voice, plain-English substitutions, no jargon, **no bold/italics for emphasis**, sentence case. Fresh (updated 2026-09-02), single SKILL.md.
- **Use for:** exactly what you said — English docs, the blog, and research-agent reports. British-English flavoured; pair it with the independently authored or properly licensed Arabic skill as the two prose styles of the platform.

## 6. Platform UI — landing pages, reader UI, polish

### taste-skill (Leonxlnx) 📦 already installed
84k★ anti-slop frontend framework (13 skills: design dials, GSAP skeletons, pre-flight checks). Already on this machine as `design-taste-frontend` (+ `-v1`, `gpt-taste`, `minimalist-ui`, `brandkit`, `image-to-code`, …).
- **Use for:** the Apple-grade bar on course landing pages and the reader UI. Brief it with the adopted Fanout design system ([fanout-feature-analysis.md](fanout-feature-analysis.md) §3.15, §4.11): one accent color per course carried across every surface, one identical card grammar everywhere — rebuilt RTL-first, Thmanyah stays the house typeface. Zero RTL awareness — always run alongside the RTL skill below.

### ui-skills.com (ibelick — not shadcn; shadcn contributes) ✅
Curated hub + `npx ui-skills` CLI + registry (~120 skills). First-party: `ui-skills-root` (router), **`improve-ui`** (audits UI against its own design evidence → implementation plan), `baseline-ui`, **`fixing-accessibility`**, `fixing-motion-performance`, `create-design-md`.
- **Use for:** the polish/audit pass per page, and `fixing-accessibility` for the WCAG constraint. The third-party catalog includes skills we already have (impeccable, web-design-guidelines, improve-animations).

### shadcn `/improve` ❌ for design — it's a code audit
`github.com/shadcn/improve` is a senior-advisor **codebase audit** (bugs, security, perf, tests, tech debt) — nothing to do with visual design. Useful for repo health generally; for UI use `improve-ui` + `web-design-guidelines` (already installed).

### elayadesign/ai-design-skills 🔧 template
Contains exactly one skill: `landing-page-design` — intake questions, page structure, conversion copy, editable visual system. 1.7k★ but 3 commits, untouched since 2026-07.
- **Use for:** the per-course landing page skeleton (its intake + conversion-copy structure is right). Adapt into our own skill with RTL/Arabic-first typography baked in; don't treat as maintained upstream.

### rtl-web-development-skill (AmmarCodes) 📐 reference candidate — reuse permission unresolved
Concrete, correct content derived from Ahmad Shadeed's RTL Styling 101: physical→logical property mappings (Tailwind `ml-4→ms-4`, CSS `margin-left→margin-inline-start`), `dir`/`bdi` handling, what flips and what doesn't, Arabic typography notes, icon-mirroring exceptions. Companion `eslint-plugin-tailwind-rtl` catches regressions in CI.
- **Watch out:** the research notes report **no LICENSE file**. Verify permission before vendoring; otherwise write an independent `rtl-first` skill from appropriately licensed references. Check the ESLint plugin license and behavior separately before adoption.
- **Use for:** brief constraint 2 — mandatory companion to every UI skill above, which all assume LTR.

## 7. Quality gates & rubric

### quality.md (qualitymd) 📐 pattern
`QUALITY.md` declarative criteria file + `/quality evaluate` / `improve` loops + a deterministic CLI runner. Exactly the shape of our gates (declare criteria → evaluate → improve), **but 32★ early-alpha** ("format will change"). Mine the pattern for our `COURSE_RUBRIC.md` + eval harness; don't take the dependency.

---

## What nothing here covers (still ours to build)

1. **Paragraph-level grounding + aha-moment judging** — no off-the-shelf skill; this is the custom eval harness from brief constraint 8 (patterns available: llm-council, quality.md).
2. **Inline MD quizzes** — nothing here changes the mdbook-quiz plan; dair's `learn` is the only adjacent pattern.
3. **Arabic plain-language style guide** — govuk-style has no Arabic counterpart; author one independently using appropriately licensed references and validate it with Arabic reviewers.
4. **RTL theming for visual-explainer / glowmotion output** — both assume LTR.
5. **Quality control across the entire pipeline** — source integrity, complete chunk accounting, resumability, versioned verdict caches, spend limits, failure recovery, and release promotion. Skills provide guidance; the factory must enforce and test these controls.

## License watchouts

| Item | License | Note |
|---|---|---|
| hyperframes-motion-director | AGPL-3.0 | Copyleft; reason to skip |
| education-agent-skills | CC BY-SA 4.0 | Share-alike if content embedded |
| AmmarCodes RTL skill, Arab-Writer, term-radar | **none reported** | Verify permission; otherwise use independently authored alternatives |
| graphify, visual-explainer, taste-skill, i-have-adhd, dair plugins, glowmotion, ui-skills | MIT/Apache-2.0 reported | Verify selected revision, dependencies, and applicable notices |

Public availability and attribution do not establish permission to copy or adapt unlicensed material. [GitHub no-license guidance](https://choosealicense.com/no-permission/).

---

## Cost picture (cost-effective by design)

**Free tool access does not imply zero operating cost or an open-source license.** Prompt-driven skills consume model tokens or subscription quota; local rendering consumes compute. The earlier blanket claim that every candidate is free/open source conflicts with the unresolved licenses above. Count authoring, evaluation, extraction, retries, and discarded work in the cost of accepted lessons.

| Item | Software/access consideration | Operating cost to budget |
|---|---|---|
| education-agent-skills | Local files; check CC BY-SA obligations | Model usage when applied by an agent; avoid introducing a hosted service without need |
| dair plugins | MIT reported; inspect chosen plugin dependencies | Authoring/model calls; council and image APIs where configured; download/slide-extraction compute and storage |
| Prose, UI, glossary, and quality skills | License varies; some unresolved | Agent model usage; deterministic local checks consume compute |
| graphify | Open-source local tooling; verify chosen revision | Markdown/docs/media semantic extraction uses a model; graph computation and storage also count |
| visual-explainer, glowmotion | MIT reported | Model-assisted authoring, local rendering, optional export compute; verify chosen dependencies |
| Excalidraw + MCP | Verify chosen implementation and export support | Agent authoring calls plus local rendering/storage |
| hyperframes family | Local rendering path; verify chosen runtime | Model-assisted authoring if used, local render compute and media storage; optional remote services are separate |
| elayadesign landing-page skill | MIT reported | Model usage during design/authoring |

**Current execution constraint:** v1 model work may use zIDE or ZCode through an OpenAI-compatible provider adapter, beginning with authorized Gemini free-tier quota and allowing other explicitly approved compatible providers. The recorded 300M-token Z.ai allowance is one possible quota source. Paid model APIs need a separate cash cap; artifact hosting/operations has a separate $5/month ceiling. Verify provider terms, key authorization, integration, aggregate limits, and usage reporting before adoption.

**Cost policy for Content Factory v1:**

1. **Preserve complete quality coverage.** Judge every released paragraph and quiz, reused or regenerated, or reuse its valid cached verdict. Use calibrated inexpensive judges for baseline coverage and premium models for generation, escalations, and sampled deep audits. Sampling can estimate inventory quality; it cannot clear unjudged content for release.
2. **Reprocess first; cache subsequent v1 work.** Matched cleaned `GeminiLongContext/` counterparts are approved teaching sources, but neither they nor any other legacy generated lesson can skip the initial transcript-based pass. Key v1 verdicts on content, source evidence, relevant lesson context, rubric, prompt, model/settings, and schema/tool versions. After that first pass, rerun only changed units and affected dependants. Expand transcript reprocessing in measured course batches.
3. **Enforce measurable free-quota exhaustion.** Configure only operator-authorized provider/account/key routes; record quota/reset evidence and disable each route on confirmed exhaustion. Stop when all routes are exhausted or remaining state is uncertain. Cap per-request output, concurrency, retries, and repair cycles. Report all model usage per accepted lesson, including graph/wiki extraction and failed attempts, plus human review time and infrastructure costs. Model selection follows measured Arabic quality and unit cost.
4. **Keep delivery static-first.** Validate projected build size, storage, and service limits before claiming free hosting. Precompute reviewed explanations and SVG/HTML visuals; use local video rendering where needed. Local compute and media storage still count.
5. **Evaluate dependencies individually.** Verify current licenses, optional paid services, and hosted product pricing for the exact candidate selected, including Mintlify. Eliminate candidates that fail the brief's requirements; do not assume only one candidate can introduce charges.
6. **Prove economics on a pilot.** Measure actual source/token volume, authorized free-quota consumption, accepted yield, reuse, repair rate, and quality before forecasting the wider corpus. See [content-factory-v1-goal.md](../factory/content-factory-v1-goal.md) for the acceptance and quota-exhaustion contract.
