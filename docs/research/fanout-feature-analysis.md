# Fanout feature analysis — the reference product in `inspiring/fanout-company/`

**Quick read:** A feature-by-feature disassembly of [Fanout](https://fanout.sh) (beta) from the 15 screenshots stored in [inspiring/fanout-company/](../inspiring/fanout-company), plus a mapping of every feature onto this platform's fixed constraints. Use it when a platform feature needs a benchmark, a pattern, or a reason to skip. Fanout is the closest public analogue to what [platform-map-brief.md](../platform/platform-map-brief.md) describes: sequenced MD-style lessons, a per-course roadmap graph, a cross-course knowledge graph, labs, and a blog — executed to a very high polish bar.

Research date: 2026-09-05. Verdicts (same scale as [skills-map.md](skills-map.md)): ✅ adopt · 🔧 adapt · 📐 pattern only, don't depend · ❌ skip for v1.

**Evidence basis.** Primary evidence is the screenshot set (captured 2026-09-05, ~7 PM), referenced below as **(S1)–(S15)** with the file list in [Sources](#7-sources). Web checks against fanout.sh are marked **(web)**. The live site is a JS-rendered app, so most page bodies do not survive plain fetching — where a claim rests on a screenshot transcription of small text, it is marked "≈" and should not be quoted without re-checking the PNG. Details the screenshots do not cover are listed in [section 6](#6-what-the-screenshots-do-not-cover) rather than guessed.

---

## 1. Product snapshot

| Aspect | What Fanout shows |
|---|---|
| Product | "Technical learning through guided study, practical instruments, daily papers, and sequenced courses." (footer, all pages) |
| Domain / status | fanout.sh, public **BETA** (logo badge) (S1, S3) |
| Positioning | Hero: "Everything a ~~Stripe L7~~ knows. Mapped." — senior-engineer competence as the promise (S1) |
| Audience | Working/studying engineers: AI research, system design, ML math, inference engineering, robotics |
| Founders | Ashutosh Lath and Suraj Gaud (per the launch tweets wall and LinkedIn coverage) (S4, web) |
| Courses at capture | AI Research, System Design, ML Math; **Inference Engineering** launching "this week" (announcement bar, S1–S15); Open Robotics in "sneak peek" preview (S1) |
| Monetization | Subscription in **EGP with purchasing-power pricing** (monthly / quarterly / annual) + one-time lifetime tier; launch code LAUNCH50 + "20% off applied automatically at checkout" (S4) |
| Scale claims | "24k+ developers, students, and researchers learn with Fanout"; ~40-organization learner logo wall; live "N online" badge (e.g. 236 online on the homepage) (S1, S4) |
| Free surface | Blog (81 posts), Daily papers explainers, Labs, roadmaps, tools directory, 14-lesson free ML Math preview, public working notes for unfinished courses (S1–S15, web) |

Two structural facts matter for this repo:

1. **Fanout is a content business with a product shell, not a video platform.** Every course is text + custom diagrams + interactive instruments. There is no lecture video anywhere in the captured surface. This is the same bet as the platform brief: transcripts are raw material, the lesson is the product.
2. **The free tier is the marketing.** Roadmaps, labs, daily explainers, the blog, and even unfinished-course working notes are public. Paid access buys the sequenced courses ("every lesson note, exercise, and learning path") (S4). The blog's 81 posts are category-mapped 1:1 onto the paid tracks, with "(Pro)" tags marking gated posts (web).

## 2. Product surface map

The homepage states the surface explicitly as a numbered grid, "Everything else on Fanout" (S1):

| # | Surface | One-line sublabel on the tile | Captured in |
|---|---|---|---|
| 01 | **Labs** | "Interactive lessons" | S5, S10 |
| 02 | **Daily** | "A new paper explained daily" | S8 |
| 03 | **Companies** | "Real systems, disassembled" | S2 (release note) |
| 04 | **Study With Me** | "See what others learn daily" | S13 |
| 05 | **Roadmap** | "Every course on one map" | S3 |
| 06 | **Papers** | "Foundational, in reading order" | S9 |
| 07 | **Tools** | "Curated instruments" | S12 |
| 08 | **Blog** | "Field notes, weekly" | web |

Around that grid: five sequenced courses (S1, S7, S13, S15), a global knowledge graph ("Knowledge Topography", S6), release notes (S2), pricing (S4), community (Discord + suggestion board + public study wall, S1/S13), and a deep footer with 18 "Use Fanout" links including surfaces the main nav hides: Math Decoder, Topography, Startups, Ideas, Jobs, Updates, Resources (S1).

## 3. Feature deep-dives

### 3.1 Courses

Five course destinations, each with its own accent color and card-deck cover art (S1):

- **AI Research** — the flagship: "12 modules · 108 lessons" (roadmap hub, S3). Module names visible on the map: Math, AI Intuitions, PyTorch, TensorFlow (27 lessons), Fine-Tuning, Neural Nets, Transformers, LLMs from Scratch, RL, MLOps (25 lessons), Research, Bonus.
- **System Design** — "Learn system design, end to end." Two parts (S13): *Part 1 · Start Here* — fundamentals plus a long run of "Build and design real systems" lessons (Build Bitly-style URL shortener, timelines, and ≈20 named builds, each a table row with duration); *Part 2* — ≈15 topic modules (Fundamentals; APIs, parameters & contracts; DNS, networking & TLS; caching & CDNs; routing, partitioning & sharding; distributed consensus; storage engines; async work & queues; search & retrieval; analytics & counting; and more), each a dense lesson table. The lesson page has a **left sidebar tree with per-lesson checkmarks** — progress is per-lesson and visible at a glance.
- **ML Math** — "Build the models a prediction depends on." ≈15 module tables (matrix algebra, decompositions, tensors, gradients, probability, distributions…). Per the release notes, the free surface was recently reshaped into "a focused 14-lesson preview … one coherent path through vectors, matrices, products, bundles, and optimization basics" (S2, S7).
- **Inference Engineering** — launching at capture; see 3.12 for its build-in-public page (S15).
- **Open Robotics** — "sneak peek" card; "frames raw physics, kinematics, and control to vision-language-action models around a critical simulation before physical hardware" (S1, S2).

Observable lesson anatomy from the captured pages: lesson titles are skill- or build-shaped ("Build …", "ML Pipeline with DVC & AWS S3", "Code, Write & Publish AI Research Paper") (web, /ai related links); every lesson row carries a duration; subscriptions include "every lesson note, exercise, and learning path" (S4). No quiz UI is visible anywhere in the captured set — assessment is the one anatomy element Fanout does not show.

**Pattern:** one course = one accent color + one cover motif, carried through roadmaps, graph nodes, calendar chips, and index sidebars. The color is the course's identity key across every surface.

### 3.2 Info Roadmaps — the per-course map

The "Info Roadmap" page (S3) renders each course as an **interactive prerequisite graph**:

- A central hub node ("AI Research — 12 modules · 108 lessons") with spokes to module nodes; each node carries a distinct **shape + color + lesson count** (diamond, pentagon, hexagon, triangle…), so the map reads without a legend.
- **Two edge types:** solid and dashed lines, plus tiny numbered badges on edges — reading order is encoded in the graph, not in a list.
- A collapsible **INDEX sidebar** groups modules into named phases: FOUNDATIONS → BUILD → FRONTIER → PUBLISH & SHIP, each with expandable module rows and lesson counts.
- A closing card hands off to the paid product: "Continue from the map into the full AI Research course, with sequenced lessons, notes, and practice." + Go Pro.

Tabs switch the same rendering between AI Research / System Design / ML Math. The roadmap is free, public, and linked from the pricing teaser ("Check out the roadmaps.") — it is the top-of-funnel artifact: you can study the whole map before paying.

### 3.3 Knowledge Topography — the cross-course concept graph

The flagship feature for this repo (S6):

- A full-viewport force-directed graph spanning all courses: header reads **"256 NODES · 591 RELATIONS"** and "AI Research ↔ System Design ↔ ML Math".
- Nodes are **colored by course** (blue AI, green systems, orange math) with large labeled hub nodes per course.
- Toolbar: **search over "concepts, aliases, and lessons"**, a course filter, a **progress filter** ("All progress" — the graph knows what you have completed), and two view modes, **Full** vs **Neighbors**.
- Interaction hint: "DRAG A NODE · ITS NEIGHBORHOOD FOLLOWS" — dragging a concept pulls its local subgraph, the natural way to answer "what do I need before X?". Minimap bottom-right, zoom/fullscreen controls, per-course legend chips.
- It has its own route (`/knowledge-graph`, web) and a footer link ("Topography") — the graph is a first-class destination page, not a course sidebar.

This is a working implementation of exactly what platform-map-brief constraint 6 specifies (concept nodes + typed edges across the whole corpus), with two additions worth stealing: **alias search** (one concept, many names — indispensable for Arabic ↔ English term mapping) and **progress-tinted nodes** (the graph doubles as a "what's left" dashboard).

### 3.4 Daily papers + Papers library — two layers of paper content

**Daily ("Academic papers made simple to understand", S8):**

- One paper per day, rendered as a typographically faithful card: authors line, venue + year (example: Consistent Hashing and Random Trees, STOC 1997), the original abstract simplified into plain prose, and a **custom diagram** built for the explanation (three caches → cache 5 joins).
- Calls to action are ordered: "Read the original paper ↗" before "Read the complete explanation →" — the explainer claims to sit *under* the source, not replace it.
- Archive is a **month calendar** with per-day chips color-coded by track (blue/purple/lavender/yellow), month picker, prev/next.

**Papers library ("Foundational papers by track in reading order", S9):**

- A separate destination (fanout.sh/papers, header art "papers.sh") listing **≈37 foundational papers** grouped by track and era dividers.
- Each card: original venue + year (NeurIPS 1986, STOC 1997, NeurIPS 2017…), a one-line takeaway, a small custom diagram, and "Read the original paper ↗".
- The sequence for the AI track runs the canonical chain: Perceptron → back-propagation/dropout/optimizers → batch norm → GANs/VAEs → AlexNet → seq2seq → attention → BERT → scaling laws → LoRA → RLHF/DPO → retrieval and prompting eras.
- The Sep 5 release note ties it together: the four tracks "span TLA systems, reinforcement learning, and inference papers by prerequisite depth, with connected illustrations and **progress that carries as you move from one paper to the next**" (S2) — reading order + carried progress is the product.

**Pattern:** the same paper asset serves three surfaces (daily digest, track-ordered library, blog posts), each with a different entry intent. One explanation, three funnels.

### 3.5 Labs — "Technical systems you can touch"

A directory of **15 interactive instruments** (S5), each a standalone page:

Math Decoder · Agent Control Room · Latency Numbers · Tokenizer and Context · RAG Chunking and Retrieval · Inference Memory and KV Cache · Fanout Scale · Eval Confidence · Gradient Descent · Sampling Playground · Timeout Architect · How AI remembers · Daily Planner · Model Router and Pareto Explorer · PDF-to-RAG Readiness Scan.

Directory mechanics: a search box ("Search tokens, latency, RAG, agents, models, PDF…", **"PRESS / TO FOCUS"**), filter chips with live counts (All 15 · On device 13 · Live data 2), and a match counter. Note the filter taxonomy: 13 of 15 labs run **on device** — they are client-side artifacts, not services.

**Math Decoder** is the one to study (S2, S15): "a notation-first lab — unfamiliar and polluted worked examples now connect unfamiliar notation to the underlying operation instead of teaching via a solved problem" (≈ release-note transcription). It attacks the exact failure mode of reading math without manipulating it, and it doubles as a course (it has its own nav route and footer slot).

### 3.6 Daily Planner — the lab done right (case study)

Two near-identical screenshots (S10, S11) capture a complete feature spec:

- **Circular 24-hour dial** ("24 HOURS · QUARTER-HOUR SNAP"): time blocks are donut segments (Sleep, Deep work, Project work, Exercise, Lunch, Morning routine) with drag handles on segment edges; the center shows the date, plan name, and "17H 15M SCHEDULED".
- **Conflict detection is the headline:** "If two blocks compete for the same minutes, the dial says so." Stats row: SCHEDULED / FREE / OVERLAP; a red conflict marker appears on the rim; status line "✓ No overlap. The day currently has no hard edges."
- A **second synchronized view**, "The circle, unfolded" — a proportional 00:00–24:00 linear timeline of the same blocks, "for truth at a glance" vs "exposing the exact gaps between them".
- Per-block editor: label, start/end pickers, live duration, six color swatches, remove; an "＋ Add block" list; "Download PNG" export ("The PNG is created when you ask for it").
- **The privacy model is explicit UI**, not a policy page: "Anonymous plans stay in this browser. If you sign in, your current plan syncs privately to your Fanout account. Planner content is not sent to an AI model, and RAG outputs are generated on this device only when you ask." Drafts never enter the page URL; guest drafts stay on the device.

**Pattern:** a genuinely useful utility (no signup), on-device computation, a privacy promise stated in the product's own voice, and dual representations of one data structure. This is the quality bar the brief means by "Apple-grade": the feature is small, and nothing about it is careless.

### 3.7 Tools directory — 21 curated external instruments

"Research, learn, and build." / "Make the invisible parts visible." (S12): a two-section catalog of **external** tools, each card = tag pill + index number (№ 01–21) + one-line job description + screenshot + domain link.

- **AI & ML (9):** Connected Papers, Dataset Search, DrivenData, Distill.pub, Seeing Theory, TensorTonic, Image Kernels, ML Knowledge Graph, Scrollscope.
- **System design (12):** System Design Simulator, Database of Databases, DB Fiddle, Postgres Explain Visualizer, Raft Consensus Visualization, Bloom Filters by Sam Who, Compactionary, Flink Watermarks WTF, Consistent Hash Ring Visualizer, Geohashes, VisuAlgo Trees, HyperLogLog Playground.

The curation principle is visible in the card copy: every entry visualizes or lets you manipulate the exact concept a course lesson teaches (Raft → consensus module; bloom filters → probabilistic structures; hash ring → sharding module). The directory converts the course syllabus into a trust-building free resource — and the Study With Me feed shows learners posting screenshots of these same tools (S13), closing the loop.

### 3.8 Companies — real systems, disassembled

"Eleven real-world System Design walkthroughs are live. Notifications, feeds, ads, limits, safety, search, availability, migration, e-commerce, recommendations, payments. **Each one disassembles a real company stack into raw fundamentals.**" (S2, release note; homepage tile "Real systems, disassembled", S1). This is the "skills, not explanations" thesis applied to case studies: the lesson unit is a production system stripped to the primitives it proves.

### 3.9 Study With Me — the public learning wall

A devlog-style feed, "See what people learned today." (S13):

- Masonry wall of embedded X posts — learners showing what they studied or built today (a Go concurrency deep-dive, RL simulator runs, TLA+ specs, KV-cache notes, a mini-SQL engine, day-count project logs), mixed languages (English, Japanese), each embed with the original like/reply/copy-link actions and "Read more ↗".
- Header avatars + a nudge CTA ("Get a personal nudge when…"), a "Load more" pagination, and a hero collage (CRT TV wall with one blue screen: "What I Learned Today").
- The release notes treat it as a content pipeline of its own: "Nine new public study logs landed in Study With Me — …open the original post, and jump into congruent breakdowns" (S2) — i.e., logs get cross-linked to the relevant lesson.

**Pattern:** the testimonial wall and the community feed are the same object. Learner proof is harvested where it happens (X) and republished with attribution, feeding both trust and the "people doing the work" section on the homepage (S1: "Keep company with people doing the work" + Discord CTA).

### 3.10 Blog — the SEO and trust engine (web)

The blog index lists **81 posts in four categories that mirror the paid tracks**: Inference engineering (37), System design (15), ML mathematics (11), AI research (18). Title grammar is instructive: number-first explainers ("AI inference engineering, explained with numbers"), head-to-head comparisons ("FlashAttention vs PagedAttention: what each fixes", "FP8 vs INT8 vs AWQ vs GPTQ"), interview-prep and roadmap posts ("ML engineer roadmap for career switchers"), and career/study guides. A minority carry a **"(Pro)"** tag — gated teasers for the paid catalog. Every post is a free search-entry point that terminates in a course, a lab, or the pricing page.

### 3.11 Community and trust machinery

- **Discord** ("Join our Discord"), homepage section "Keep company with people doing the work." (S1).
- **A public suggestion board**: "Help shape what Fanout builds next … suggest a feature, vote on planned work" — linked directly from the release-notes page under "WHAT'S NEXT" (S2).
- **Liveness**: a persistent "N online" badge (236/158/152 across captures) — cheap, effective aliveness proof (S1–S15).
- **Trust wall**: "24k+ developers, students, and researchers" + ~40 university/org logos (Amazon, Harvard, IIT Bombay, Cornell, Dropbox, Northwestern, MIT…, including several IITs — a signal of the target demographic) (S1, S4).
- **Tweet wall**: "Engineers love fanout" — founder-led launch tweets + organic reactions, embedded with engagement counts (S1, S4).
- **Weekly newsletter**: "One short email a week — papers, systems notes, and course drops worth your time." in every footer (S1–S15).

### 3.12 Release notes and build-in-public

The changelog (S2) ships ~14 dated entries across three weeks (Aug 18 – Sep 5), one feature per entry, each with a custom illustration and a deep link. Cadence matters more than any single entry: surface area grows visibly every few days, and the changelog doubles as the roadmap ("WHAT'S NEXT" → suggestion board).

The Inference Engineering page (S15) is the build-in-public pattern at course granularity:

- STATUS: "roadmap and drop notes (work in progress)"; a "New course dropping this week" bar sits on every page.
- "**Start with the working notes.** The complete course is still being assembled. These public lab and sourced explanations are available while the course is pointed to early access." — four finished notes ship now ("Calculate KV-cache memory", "Derive the KV-cache formula", "Separate prefill from decode", "Understand continuous batching").
- A 7-stage roadmap, each stage ending in a **deliverable** ("A reproducible spreadsheet…", "A written decision memo…", "A deployment topology that meets the latency target…") — the course is specified as a sequence of artifacts you produce, which is the "skills, not explanations" thesis in syllabus form.
- "The useful pieces arrive first": a print-packet of worksheets (latency numbers, KV-cache sizing worksheet, quantization tradeoff demo, token-per-task glossary, capacity planning template).
- "Compare the released alternatives" — a page inviting comparison against **open** resources, including their own roadmap: confidence as a feature.

### 3.13 Pricing and access

Captured fully (S4):

| Plan | Price (EGP) | Billing | Notes |
|---|---|---|---|
| Monthly | 768.29 /mo | monthly | "Full access with the shortest commitment" |
| Quarterly | 618.17 /mo | 1,854.51 per quarter | "Three months of full access in one payment" |
| Annual *(Recommended)* | 501.15 /mo | 6,013.80 per year | "Best value for staying for ongoing access" |
| Lifetime | ~~higher~~ 6,782.14 one-time | once | "Get every Fanout course forever, including future releases and updates"; framed as paying for itself "once you finish more than two to three courses" |

- **Purchasing-power pricing is a first-class mechanism**: a region toggle ("Purchasing-power pricing for Egypt updated" | Local | USD), a note that non-Egyptian users pay the standard international price through a two-step verification + redirect at checkout, and "Regional pricing — 20% off applied automatically at checkout". The launch discount code **LAUNCH50** has its own FAQ entry; several FAQs reference a countdown timer ("What happens when the timer reaches zero?").
- "Every subscription includes": every current course; new content and course updates while the plan is active; **every lesson note, exercise, and learning path**; cancel from the billing portal.
- Plan-equality reassurance: "Do Monthly, Quarterly, and Annual unlock different content? — No. All three subscriptions unlock the complete current Fanout catalog." Lifetime and refund handling each get FAQ entries; invoices for employer learning budgets are pre-answered ("The invoice and receipt from checkout are all you need to submit").
- A concierge hook: "Tell us what you are trying to learn — we can help with a guaranteed plan of action, identify blind spots, or tailor the standard curriculum order." + Send a question.

**The signal for this repo:** Fanout sells to Egypt in **Egyptian pounds at Egyptian purchasing power**. The platform's own audience (Gaza/Levant universities, Arabic-first) is the adjacent market mainstream products price out — and Fanout's pricing page is proof the regional-pricing playbook works for technical education.

### 3.14 Global UX patterns

- **Cmd+K global search** (shipped Sep 3, S2): "one shortcut searches lessons, daily papers, blogs, tools, and notes, with keyboard navigation, recent queries, and **course-aware scopes when you're in labs**". Search scopes follow context.
- **Course context switcher** in the nav ("Learning ⇅") — the whole site re-voices itself around the active course (S1–S15).
- **Announcement bar** on every page with the launch deadline; dismissible (S1–S15).
- **"New in September" pill** next to Sign in — freshness is permanently advertised (S1–S15).
- **Keyboard affordances surfaced in the UI** ("/ to focus" on lab search, Cmd+K hints).
- **Deep footer** with 18 links, including surfaces the nav omits (Math Decoder, Topography, Startups, Ideas, Jobs, Updates, Resources) — the footer is the real sitemap (S1).
- **Labs/course interactivity is client-side**: privacy notes state computation happens on the device (S10); the "On device 13 / Live data 2" filter confirms it (S5). This is what keeps a highly interactive site shoppable at low infra cost.

### 3.15 Design language

- **Hand-drawn illustration system**: spot illustrations on every release-note card, cover art per course (stacked card decks), a manila-folder storyboard on the homepage, pink hand-drawn architecture diagram on the Inference page. Nothing looks like stock.
- **Typography pairs a monospace/pixel voice** (headings like "Info Roadmap", body accents) **with a serious serif** for paper titles (S8) — playful shell, rigorous content.
- **One accent color per course**, carried across course cards, roadmap nodes, graph nodes, calendar chips, and block colors.
- **Card grammar is identical everywhere**: eyebrow label → title → one-line description → single CTA with "→". Same rhythm on labs, tools, papers, release notes, pricing.
- Light theme, generous whitespace, dot-matrix/ASCII texture bands on lab cards, live-status chip in the corner. The overall effect is "engineered artifact", which is the brand.

## 4. Patterns worth stealing

*Adopted patterns are propagated into the [platform brief](../platform/platform-map-brief.md) (constraints 4 and 6 and the benchmarks paragraph), the [skills map](skills-map.md) (graphify UX bar, client-side search, taste-skill brief), and the pilot release work in [NEXT_STEPS.md](../NEXT_STEPS.md) (milestone 4).*

1. **Ship one non-teaching status page before the course.** It may describe high-level progress, but roadmap detail, working notes, release notes, and all teaching stay private until the complete prerequisite-closed course is accepted (S3, S15).
2. **Progress is a graph property.** Progress filters into the knowledge graph (S6) and carries across papers (S2) — completion is visible on every structural view, not just a course checklist.
3. **Alias search in the concept graph.** "Search concepts, aliases, and lessons" (S6) is the exact hook Arabic/English terminology needs.
4. **One asset, three funnels.** A paper explanation surfaces as daily digest, track library entry, and blog post (S8, S9, web).
5. **Explain under the source.** Every explainer links the original paper first (S8, S9) — the same grounding instinct as the brief's paragraph-level source checks.
6. **Deliverable-ended stages.** Inference Engineering stages end in artifacts you produce, not chapters you read (S15).
7. **Privacy as product voice.** On-device computation stated in the UI, in the product's own words (S10).
8. **Small-batch shipping, publicly logged.** ~14 changelog entries in 3 weeks, each with an illustration and deep link, feeding a public suggestion board (S2).
9. **Free coherent module — defer.** ML Math's "focused 14-lesson preview … one coherent path" (S2) is a possible post-pilot product pattern, not an authorized pre-acceptance release.
10. **Regional pricing as strategy.** EGP purchasing-power pricing for the exact region this platform serves (S4).
11. **Identical card grammar everywhere.** One rhythm for labs, tools, papers, plans, and changelog entries (all screenshots) — the cheapest possible way to look Apple-grade.
12. **Liveness as proof.** A persistent online counter and a public learner wall (S1, S13).

## 5. Mapping to the IUG platform

Against [platform-map-brief.md](../platform/platform-map-brief.md) constraints. v1 = Content Factory v1 (optics pilot, static-first, no paid model API, hosting/operations capped at $5/month); "platform" = the broader destination in the brief.

| Fanout feature | Brief constraint it touches | Verdict | Notes |
|---|---|---|---|
| Knowledge Topography graph | 6 (knowledge graph + openwiki) | 🔧 | The existence proof for constraint 6: cross-course, searchable, progress-aware, own destination page. `graphify` (skills-map §2) already outputs `graph.json` + interactive `graph.html`; the gap to Fanout's bar is UX (neighbors view, drag interaction, minimap) + Arabic aliases + RTL text in nodes. Alias search is the must-copy detail. |
| Per-course roadmap graph + INDEX sidebar | 6, pedagogy thesis | 🔧 | Same substrate as above, filtered per course, with phase groupings (FOUNDATIONS → BUILD → …) matching skill-track organization. Ship the optics-pilot roadmap publicly when the pilot's graph exists. |
| Custom diagram per concept/paper | 3 (aha diagrams via Excalidraw) | ✅ pattern | Fanout's "one idea, one diagram" discipline is exactly constraint 3; the brief's deterministic SVG/HTML preference (constraint 9) matches Fanout's diagram style. Excalidraw source + render stays the plan. |
| Lesson = sidebar tree + per-lesson checkmarks + durations | 4 (reading experience) | ✅ pattern | Cheap, high-value reader chrome for MD lessons; progress state is client-side/static-friendly. |
| Lesson anatomy (notes, exercises, learning paths) | 5 (inline assessment) | 📐 | Fanout shows exercises in marketing copy but **no quiz UI anywhere in the captured surface** — assessment remains this platform's differentiator (mdbook-quiz line), not a copy job. |
| Build-in-public working notes for an unfinished course | 10 (release communication), pilot | 📐 | Before acceptance, publish only a non-teaching status page. Keep working notes, roadmap detail, release notes, and all teaching private until the complete prerequisite-closed course is accepted. |
| Release notes / changelog page | platform (blog) | ✅ | A blog category plus one illustrated page. Cheap, on-brand for an audit-trail culture. |
| Free focused module (14-lesson preview) | pilot | 📐 | Deferred until after full-course acceptance; it is not an approved pre-acceptance release. |
| Blog: category-mapped SEO posts, some gated "(Pro)" | 7 (platform includes blog) | ✅ pattern | The stack-comparison post is already mandated as blog post #1; Fanout shows the long game (81 posts mapped to tracks). Gating is a future monetization decision, out of v1 scope. |
| Cmd+K global search with scopes | 4, 7 | 🔧 | Static-site analogue exists (client-side search indexes, e.g. Pagefind-style) — fits static-first. "Course-aware scopes" = filter by course context. |
| Interactive labs (13 of 15 on-device) | 9 (static-first, bounded operations) | 📐 | V2+ surface, not v1. The transferable rule: interactivity must be a client-side artifact with a privacy statement, never a metered paid service in the critical path. Math Decoder's notation-first idea is directly relevant to math-heavy courses like optics. |
| Daily Planner (dual views, conflict detection, PNG export) | 9 | 📐 | A masterclass in small-feature polish; not education-core. Mine it when building any v2 tool. |
| Daily papers / Papers library | — | ❌ for v1 | A daily editorial commitment with no pilot budget. The *format* (original link → simplified abstract → one diagram → full explanation) is a reusable lesson template for later. |
| Tools directory (curated external) | — | 📐 | Nearly free to build, high trust yield. Post-v1; must respect the teaching-source policy (linking out is fine; importing others' content is not). |
| Study With Me public wall | — | ❌ for v1 | Needs community + moderation + embeds (dynamic). Revisit after platform v1; the git-backed "learner evidence" idea in the brief is a calmer v1-compatible cousin. |
| Purchasing-power EGP pricing | — | 📐 | Validates the market and the playbook for a future paid tier; v1 permits only the narrow $5/month hosting/operations ceiling and no paid model APIs, so this is a platform-era decision, not now. |
| Discord + suggestion board + online counter | — | ❌/📐 | Dynamic services; the suggestion board could later be a static issues-based board (GitHub-backed). Online counter conflicts with static-first — skip. |
| Tweet/logo trust walls | — | 📐 | For launch, not build. Note their logo wall includes IITs — the demographic proof for regional technical education. |
| Design language (hand-drawn system, course accent colors, card grammar, pixel+serif type) | 1 (Apple-grade), 2 (RTL) | ✅ pattern | Adopt the *system* (one accent per course, one card grammar, illustrated changelog), not the fonts — Thmanyah stays the house typeface. All of it must be rebuilt RTL-first; Fanout has zero Arabic surface, which is this platform's opening. |

**Where Fanout cannot lead.** Everything Fanout ships is LTR English, inside a JS app, monetized from day one. The brief's three sharpest constraints — RTL-first excellence, transcript-provenance grounding with LLM-judged gates, and tightly bounded static delivery (no paid model APIs; hosting/operations at most $5/month) — have no counterpart in Fanout's captured surface. Fanout is the benchmark for **finish and product thinking**; the differentiators stay exactly where the brief puts them.

## 6. What the screenshots do not cover

Marked so nobody treats this report as complete: the lesson-reading interior beyond the system-design sidebar (typography, figure treatment, exercise blocks) (S13 shows only the shell); the account/dashboard; the Discord itself; checkout; the actual Cmd+K palette open state; Open Robotics and Math Decoder interior pages; the Companies walkthrough layout. The live site renders these client-side, so plain fetches return only navigation (web). If any of these matter for a feature decision, capture them in `inspiring/fanout-company/` and extend section 3.

## 7. Sources

Screenshots (all in [inspiring/fanout-company/](../inspiring/fanout-company), captured 2026-09-05):

- **S1** `Fanout-AI-Research-System-Design-ML-Math…07_05_PM.png` — homepage
- **S2** `What's-new-in-Fanout…07_02_PM.png` — release notes
- **S3** `AI-system-design-ML-math-roadmaps…07_04_PM.png` — Info Roadmap (AI Research tab)
- **S4** `Fanout-Course-Pricing-AI-Systems-and-ML-Math…07_03_PM.png` — pricing
- **S5** `Interactive-AI-and-System-Design-Labs…07_05_PM.png` — labs directory
- **S6** `Knowledge-Topography…07_13_PM.png` — knowledge graph
- **S7** `ML-math-course-overview…07_06_PM.png` — ML Math course
- **S8** `AI-Research-Papers-Explained-Daily…07_05_PM.png` — daily papers
- **S9** `Foundational-papers-by-track-in-reading-order…07_04_PM.png` — papers library
- **S10** `Daily-Planner-…07_14_PM.png` and **S11** `…07_15_PM.png` — daily planner (near-duplicates)
- **S12** `Tools-for-technical-work…07_08_PM.png` — tools directory
- **S13** `System-design-overview…07_07_PM.png` — system design course shell
- **S14** `Study-With-Me…07_04_PM.png` — study wall
- **S15** `LLM-Inference-Engineering-Roadmap-2026…07_05_PM.png` — inference roadmap page

Web (checked 2026-09-05): [fanout.sh](https://fanout.sh) (routes/sitemap), [fanout.sh/blog](https://fanout.sh/blog) (81-post index), [fanout.sh/pricing](https://fanout.sh/pricing) (JS-rendered; body not retrievable — pricing evidence is S4), [/ai related-lesson links](https://fanout.sh/ai), plus the LinkedIn launch post identifying the founders.

Companion docs: [platform-map-brief.md](../platform/platform-map-brief.md) (constraints referenced above), [skills-map.md](skills-map.md) (tool candidates the mapping leans on, esp. graphify).
