# Course platform — product blueprint and delivery plan

2026-09-07 · Provisional implementation recommendation; not release approval. The operator accepted the learner-purpose, independent-study and low-bandwidth defaults in [the north star](platform-north-star.md). See [artifact storage/review](artifact-storage-review.md) and [Q3 search/AI discovery](search-discovery-2026-q3.md) for the expanded delivery requirements.

**Confirmed scope:** no learner accounts for now. The destination covers roughly 325 higher-education courses and thousands of lessons across specializations, including approved output families from [skills-map.md](../research/skills-map.md). This is a planning scale, not a reconciled count of accepted courses. Optics remains the factory pilot. The small-reader proposal below is a first delivery slice, not the full product north star.

**Learner-platform v0 boundary:** the public product is generated static pages plus browser-side enhancement. It provides no server-side application functions: no application server, runtime database, custom API, authentication, server-synced progress, server-processed forms, or runtime model calls. Search indexes and concept graphs are produced at build time; progress and quiz attempts stay in the browser. Reporting uses a static link to an explicitly chosen external channel until a later version authorizes a backend. Private artifact storage, protected candidate review, and release operations are delivery infrastructure outside the public v0 learner runtime, not learner-facing server features.

**Goal:** A learner can open an accepted course on their phone, understand the learning path, read an Arabic-first lesson, practise, and return to their place. Adding another accepted course should require content, not new application code.

**The finished product — recommended shape**

One public learning site with three primary entry points: **Courses / المساقات**, **Concepts / المفاهيم**, and **Search / البحث**. A learner can follow a course in order or enter at a useful concept from Google or a chat app. Every entry leads into the same reviewed learning material. A returning learner sees a small Continue action based on this browser's history. About, editorial policy, blog, updates and problem reporting belong in supporting navigation.

| Screen | What the student sees and does |
|---|---|
| Home / course catalog | Search by subject, course or concept; browse specializations and level; open a released course. Show real available content rather than 325 empty cards. |
| Subject page | Relevant courses, prerequisites/levels and reviewed learning paths. Filters narrow the catalog without creating duplicate indexable pages. |
| Course home | What the learner will be able to do, required knowledge, course scope, ordered units, stage deliverables, estimated effort where established, and Start/Continue. Outline and roadmap are two views of the same order. |
| Lesson reader | Course outline on the right on desktop; reading column in the center; optional section navigation. On phones, one reading column with course/section drawers. Practice, assessment states, submission, and feedback are embedded components inside the lesson; there is no separate quiz or assessment destination. |
| Concept/wiki page | Context-specific definition, Arabic/English aliases, relevant examples, prerequisites and links to lessons. A compact neighbor graph explains relationships; the full graph remains available through Concepts. |
| Concept explorer | Search concepts/aliases/lessons; filter by course/subject; full and neighbor views, drag interaction and progress indicators. Provide an equivalent navigable list. Load useful subsets instead of putting every node on a phone at once. |
| Search results | Clearly distinguish courses, lessons and concepts. Prefer current course context when relevant; allow search across the catalog. A result explains where it belongs, not just a matching title. |
| Blog / updates / about / report | Useful editorial posts, the stack-comparison post, release/correction history, actual provenance/review process and specific problem reporting. Shared editorial templates keep these small. |

**A concrete student journey:** a student searches for an optics concept, lands on its Arabic lesson, sees the required prior knowledge, studies the explanation and diagram, attempts a task, reads feedback, opens an unfamiliar term's concept page, and returns to continue the course. Another student starts from a specialization and follows the course outline. Neither needs an account.

**One reader, several teaching components.** Each lesson starts with its outcome and prerequisites. Its reviewed teaching then uses the components it needs: prose, math, code, table, worked example, Excalidraw-derived diagram, simplified explanation, formative question, open task, interactive figure or captioned video. Practice can use a choice, numeric answer or self-check rubric as appropriate; the exact schema follows the content contract. Do not force proofs, essays and practical tasks into four-choice questions. Media belongs inside lessons and concept pages; each skill does not get its own disconnected mini-site. Use approved exports/adapters, accessible alternatives and lazy loading.

**The private side:** the operator produces versioned artifacts, reviewers inspect a frozen candidate and submit findings, the operator approves the eligible corrected version, and publication promotes those exact bytes. Start with a protected preview plus review form; a custom admin/CMS is not required. Reviewer access is separate from learner accounts. The archive stores source/editable derivatives, JSON checkpoints and approval records outside GitHub, subject to the existing private-corpus boundary.

**Behavior we should design, not leave to chance**

| State | Required behavior |
|---|---|
| First visit / no local history | Offer Start and browse/search; no empty dashboard or login prompt. |
| Search has no result | Explain the active scope, offer broader search and subjects; do not manufacture content. |
| Slow connection / unavailable media | Keep the lesson readable; show the reviewed static/text alternative and an explicit media retry. |
| Wrong answer / open-ended work | Useful feedback after an attempt; retry or rubric/model response. No unsupported mastery claim. |
| Progress saved / storage unavailable | Distinguish read, attempted and self-reported completion; keep reading usable and explain when progress cannot be saved. |
| Lesson revised or withdrawn | Preserve stable identity and show a meaningful correction/review-needed state; remove unsafe content and point only to eligible replacements. |
| Very large course or graph | Search/filter and load sections/subgraphs as needed; retain keyboard/list navigation. |

**Design direction:** reading-led and calm, with strong Arabic typography, clear hierarchy, restrained course accents and purposeful diagrams. Existing monochrome wireframes express layout only. Preserve Thmanyah as the intended house font and Fanout's useful navigation patterns. Actual visual compositions still need a design pass; this blueprint does not certify the UI's finish.

Use the captures in [`docs/inspiring/`](../inspiring/) as visual and interaction inspiration for hierarchy, course overviews, long ordered curricula, graph controls, and release-note rhythm. They are references, not authority, templates to copy, or a requirement to reproduce Fanout's colors, branding, accounts, commerce, community, or server-backed behavior. Translate useful patterns into the Arabic-first, monochrome-wireframe, static v0 constraints above.

**What “built” means**

| Milestone | Concrete deliverable | Completion evidence |
|---|---|---|
| 1. Product walkthrough | Connected catalog → subject → course → lesson → practice → concept/search flow, desktop and phone, with clearly synthetic fixtures | The entire learner journey is reviewable; all controls have defined behavior. This is a prototype, not a teaching release. |
| 2. Working platform foundation | Manifest-driven reader, approved format adapters, search, wiki/graph, local progress and editorial templates | Representative disciplines/media work; keyboard, mixed-direction text, weak-phone and catalog-scale checks pass. Covers #23. |
| 3. Real review and release | Private archive, authenticated candidate preview, reviewer records and operator promotion to stable public URLs | Recovery, approval invalidation, privacy and $5/month qualification; SEO/AI crawl eligibility verified. Covers #22 and #24. |
| 4. Full platform v1 | All screen families above, populated from eligible bundles; course/global graph and blog included | New courses publish through the same contract. Capacity for the target catalog is measured; accepted course coverage is reported separately. |

Optics is the first accepted-content milestone when factory gates clear. It does not define the maximum platform feature set. Full platform v1 need not wait for all 325 courses to finish production, but must prove their intended catalog/format scale. Supporting a video format does not yet prove affordable delivery of every future video.

The next app-workstream build artifact is milestone 1: a connected product walkthrough, not another disconnected wireframe or new planning document. It begins only when authorized alongside or after the factory task in [NEXT_STEPS.md](../NEXT_STEPS.md). The remaining product choice is whether this screen/flow blueprint matches the intended platform; the remaining engineering qualifications are formats, capacity and controlled publication.

**Provisional implementation recommendation:** Astro, constrained Markdown, browser-side interaction, Cloudflare Pages. No learner accounts. Phone-first, low-bandwidth online delivery is accepted; offline downloads are not a launch promise. Reassess the full delivery architecture against catalog size and approved interactive HTML, animation, video, wiki and graph outputs before final framework selection.

Authority remains [goal](../factory/content-factory-v1-goal.md) → [resolution](../factory/content-factory-v1-resolution.md) → [pilot plan](../pilot/opto-2311/pilot-opto-2311-plan.md). This is the app workstream; the factory's immediate task remains [NEXT_STEPS.md](../NEXT_STEPS.md). App fixtures may be synthetic; public teaching requires accepted content.

**The learner path**

`Courses → Course outline → Lesson → Attempt practice → Feedback → Next lesson`

Return visits offer “Continue”. Related concepts and search help learners recover when stuck.

| Surface | Smallest useful version |
|---|---|
| Courses | Accepted courses only. Start with optics; simple cards, no elaborate marketing homepage. |
| Course home | Outcomes, prerequisites, ordered units, stage deliverables, start/continue. The roadmap lives here. |
| Lesson reader | RTL sidebar/drawer, skill, explanation, worked example, diagram, inline practice, transfer task, next/previous. Desktop and mobile share one template. |
| Concepts | Reviewed definitions, Arabic/English aliases, related lessons and typed relationships. Accessible links/list first; simple course graph from the same data. |
| Updates | One template for release notes and accepted working notes; blog uses the same layout later. |

Use [existing wireframes](../wireframes/index.html), especially 01, 02, 03 and 09, as starting material. Their placeholders and staged-publication banners are not acceptance evidence.

**Borrow from Fanout**

Borrow its visible learning path, consistent course cards, lesson navigation and concept aliases. Rebuild in Arabic-first Thmanyah, subject to publishing rights. Keep the course reader central. Daily papers, labs directories, pricing, social walls and live counters each add a separate product obligation.

Evidence: [local feature analysis](../research/fanout-feature-analysis.md), plus [Fanout's live surface index](https://fanout.sh/) checked 2026-09-07. Live text retrieval exposed navigation, not the full reader; detailed visual claims remain based on the local analysis, not a fresh visual audit.

**Delivery scope**

| Classification | Scope |
|---|---|
| Pilot required | Accepted course rendering; inline assessments embedded in the lesson reader; diagrams/math; course/lesson wiki and graph artifacts; Arabic/mobile/accessibility checks; source references; static reporting route; versioned releases and recovery. |
| CF-11 supporting surfaces | Before course acceptance: one non-teaching public status page only. Working notes, roadmap details, release notes, and teaching surfaces remain private until the complete prerequisite-closed course is accepted. |
| Recommended first-app additions | Catalog, continue/reset, device progress, course-scoped search. Small browser features; do not redefine factory acceptance. |
| Full platform v1, beyond the factory pilot | Cross-course interactive graph, drag/neighbors/progress filters, blog and published stack-comparison post. These remain required platform capabilities, even though the pilot reader can precede them. |
| Separate future decisions | Accounts, synced progress, payments, certificates, community, live tutoring, CMS. No need to build their infrastructure speculatively. |

**Framework decision**

This is a bounded selection, not the finished comparison blog. Fit judgments below are engineering recommendations; costs exclude existing operator time and equipment.

| Option | License / community evidence | Fit and running cost | Decision |
|---|---|---|---|
| Astro | [MIT](https://github.com/withastro/astro/blob/main/LICENSE); public ecosystem and framework docs | Build-time pages, small interactive components; static Pages hosting within limits. Direct control over course UX. | Recommend. |
| Astro + Starlight | [MIT, public project/support](https://github.com/withastro/starlight); [built-in RTL](https://starlight.astro.build/guides/i18n/) | Faster documentation shell; same static hosting. Course progress and assessment still need custom work. | Good fallback if a docs-style shell is acceptable. |
| Next.js | [MIT, public community](https://github.com/vercel/next.js/); [static export](https://nextjs.org/docs/app/guides/static-exports) | Can also run statically on Pages. More framework concepts than this reading app needs; useful if server-backed product needs become concrete. | Capable, unnecessary here. |
| Mintlify | Full-platform open-source license not verified in this review | [Self-hosting is Enterprise](https://www.mintlify.com/pricing); no verified free Pages deployment path. | Exclude from this plan. |

Astro supports [static routing](https://docs.astro.build/en/guides/routing/) and [interactive islands](https://docs.astro.build/en/concepts/islands/). Start with Astro templates, CSS and small TypeScript components; add a UI framework only for a component that benefits from it. Custom layout carries accessibility maintenance work: prove it in the reader slice.

**Architecture and content boundary**

`Private factory → accepted release bundle → validate/build → preview → promote same bytes → Pages`

- Keep app code in `web/` in this repository. Use synthetic fixtures in Git. Import final public content through an explicit bundle allowlist; never copy the corpus or private evidence directories into the site.
- Bundle: release/schema IDs, course order, stable course/lesson/node IDs, constrained Markdown, quiz payloads, approved visual exports, derived concept data and public source references. Keep full evidence, verdicts, reviewer/learner records and operational state private.
- Use the resolution's Markdown contract: math/tables and schema-validated fenced quizzes; no authored MDX, arbitrary HTML or JavaScript. One parser/conformance suite serves preview and final rendering. The app does not regenerate teaching.
- Stable lesson URLs and one manifest drive navigation, prerequisites and concept links. Learner-platform v0 permits no runtime database, custom API, server-side application function, authentication, server-processed form, or model call.
- Progress records lesson ID, content revision, completion and last location. “Completed” is self-reported, not mastery. Preserve unchanged lessons; mark materially revised lessons for review; ignore withdrawn IDs. Provide reset; keep reading usable when storage is unavailable. State that progress stays in this browser and can be lost when storage is cleared.
- Quizzes provide formative feedback after an attempt. Exclude solutions from pre-attempt display, accessibility output, print and search snippets. Browser-delivered answers are inspectable; independent trial answer keys stay private.
- Search candidate: [Pagefind](https://pagefind.app/docs/multilingual/) documents Arabic UI and stemming. Verify pinned dependency licensing during implementation. Test real Arabic spelling and English aliases; multilingual support alone does not prove alias matching.
- Build graphs from accepted concepts; do not run extraction in the app. [OKF evaluation](../research/okf-v02-evaluation.md) remains a draft export decision, not a reason to add a graph database.

**Build order and proof**

1. **Reader slice:** synthetic Arabic/mixed-language lesson, diagram, equation, quiz, mobile drawer. Prove Markdown conformance, keyboard flow, readable math and no clipping at 360px/200% zoom.
2. **Course shell:** manifest-driven outline, navigation, continue/reset, search, concepts. Prove stable links, alias queries, revision handling and storage failure. Reading works without JavaScript.
3. **Release path:** integrate one accepted bundle when available. Reject malformed, unapproved or private files; verify preview/live identity. Prove failed-update isolation, rollback, withdrawal including historic URLs, and independent-backup restore under CF-11A.
4. **Public launch:** complete accepted optics course and required supporting surfaces after factory/reviewer/learner gates. Name report owner and backup cadence. Then add courses through bundles.

Current [Pages limits](https://developers.cloudflare.com/pages/platform/limits/): Free allows 20,000 files; maximum asset size 25 MiB; hosted builds 500/month with 20-minute timeout. Measure the complete generated site before expanding. The operator now allows at most $5/month total for hosting/artifact operations (operator-confirmed); the recommended free baseline and conditional fixed-price archive are in [storage/review](artifact-storage-review.md). Record build, storage, review and operating effort; a free host does not remove that work.

**Unresolved questions**

- North star defaults are accepted. The $5/month ceiling is confirmed; quota-stop behavior remains to be specified; no paid services have been provisioned.
- Skills-output contract: which interactive asset forms are approved, how they retain provenance and accessibility, and how generated HTML is adapted to the constrained-content policy. Supporting a tool's useful outputs does not imply executing its raw output unchanged.
- Catalog scale: course identity versus source playlist, cross-specialization prerequisites, representative assessment types, generated file/media totals, and release boundaries across courses.
- Before implementation freeze: confirm quiz schema and public bundle contract with CF-03/C5; accept the framework recommendation.
- Before publication: resolve existing source/font rights, reviewer/learner gates and operating ownership. These are existing release prerequisites, not reasons to delay a synthetic reader prototype.
