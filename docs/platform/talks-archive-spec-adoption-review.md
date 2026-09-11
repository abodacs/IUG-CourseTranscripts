# Talks Archive specification: adoption review and platform addendum

2026-09-08 · Comparative input review of the user-supplied **Talks Archive Specification v1 (2026-09-06)**. This document merges compatible improvements into platform planning. It is not implementation evidence, release approval, or a new authority over the factory goal, resolution, pilot packet, or current task.

## Decision

Do **not** merge the Talks Archive specification wholesale. It reconstructs a searchable archive whose primary unit is one recorded session. This repository builds an Arabic-first university learning platform whose source recordings become prerequisite-aware, skill-based learning units with worked examples, practice, assessment, wiki entries, and a typed concept graph. The default mapping is one source video to one learning unit, while reviewed outcome-matrix evidence may justify an explicit split or synthesis exception. Replacing the learning model with session summaries, tag threads, or video packs would weaken the product.

Merge its strongest implementation details: explicit identity and lifecycle rules, pair-complete source caches, validate-before-replace writes, per-item failure isolation, ancillary-work reconciliation, URL-persisted filters, precise search states, derived-asset freshness, no-change automation behavior, safe optional-service contracts, and scenario-based acceptance checks.

The resulting position is:

| Decision | Meaning |
|---|---|
| `MERGED` | This addendum adopts the requirement for the relevant future platform/factory ticket, subject to higher authority and scope gates. |
| `PRESENT+` | The repository already requires the useful behavior and usually does so more rigorously. Preserve the existing rule. |
| `ADAPT-LATER` | Useful after the static learner foundation, but requires a bounded design/authorization decision. |
| `REJECT` | Wrong domain model, conflicts with settled policy, or creates unjustified scope. |
| `OPEN` | Potentially useful, but evidence or an operator choice is missing. |

## Authority and scope guardrails

1. Authority remains [goal](../factory/content-factory-v1-goal.md) → [resolution](../factory/content-factory-v1-resolution.md) → [pilot packet](../pilot/opto-2311/content-factory-v1-pilot.md). [NEXT_STEPS](../NEXT_STEPS.md) remains the execution order. This review cannot certify a ticket, authorize model/network work, or move platform implementation ahead of the current evidence task.
2. The current task remains the all-105-source outcome matrix and reviewable reference packet. Live provider integration, calibrated gates, learner trial, and deployment remain unfinished.
3. Private corpus and production artifacts remain outside Git. `data/`, `GeminiLongContext/`, `artifacts/`, source excerpts, reviewer records, and private evidence must not be committed or exposed through a public build.
4. Source identity and learning-unit identity remain distinct, but current and future course processing MUST default to one source video per learning unit. Splitting one video across units or synthesizing one unit across videos requires an explicit reviewed exception supported by the outcome matrix. Curriculum order comes from reviewed outcomes and prerequisites, not upload order or tags.
5. Before complete prerequisite-closed course acceptance, the only public surface is the approved non-teaching status page. Daily talk-style partial publication is not an alternative release route.
6. The broader platform v1 retains Concepts/wiki/graph as a first-class destination. The subordinate monochrome learner-v0 wireframe prompt deliberately renders concepts only inside lessons while keeping graph-ready records. This is staged scope, not a conflict to resolve by importing Threads or deleting the later concept surface.
7. “Merged” below means incorporated into this platform addendum. It does not mean implemented, tested, provisioned, or accepted.

## Section-by-section crosswalk

Each row below is atomic and has exactly one classification. Qualifiers narrow when or how that classification applies; they do not create a second decision.

### 1. Product and scope

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Help readers decide what to watch and jump to a source moment. | `MERGED` as a secondary journey | Preserve visible source attribution and time-linked evidence where publishing rights permit, but lead learners into the relevant lesson, explanation, example, and practice. |
| A summary should stand alone without watching. | `REJECT` as product goal | A reviewed lesson must stand alone enough to teach its declared outcome; a summary without meaningful practice fails the [pedagogical thesis](platform-map-brief.md#platform-map-brief). |
| One video equals one learning unit by default. | `MERGED` | Apply the one-video/one-learning-unit default now and in future course processing. Source and learning-unit identities remain separate; a split or synthesis requires an explicit reviewed exception supported by the outcome matrix. |
| Threads derive membership from tags. | `REJECT` as knowledge model | Use namespaced concepts, bilingual aliases, typed edges, reviewed merge/split decisions, and separate prerequisite/build dependency graphs. |
| Packs are authored ordered video lists. | `ADAPT-LATER` | A later problem-oriented learning path may use explicit authored lesson/course membership and reasons. It must not override canonical course order, prerequisites, or acceptance state. |
| Accounts, comments, payments, CMS, live chat are out of scope. | `PRESENT+` | Learner v0 already excludes server runtime, accounts, authentication, synced progress, payments, community, and custom CMS. |
| Public identity and canonical origin are configurable. | `MERGED` | Keep public identity and canonical-origin configuration explicit and consistent across generated surfaces. |
| Sponsorship is configurable. | `REJECT` | Sponsorship is not requested or governed and must never enter teaching claims. |

**Why ours is stronger:** the [north star](platform-north-star.md) measures whether a learner can independently apply an outcome, not whether a page summarizes a recording. The [course blueprint](course-app-plan.md) joins discovery to prerequisites, worked examples, inline practice, feedback, progress, wiki, and graph recovery paths.

### 2. System and durable state

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Python batch pipeline → static build. | `PRESENT+` | The batch factory and static build already fit the platform contract. |
| Optional edge service. | `ADAPT-LATER` | An edge service remains post-v0; ordinary reading, navigation, search baseline, progress, and quizzes cannot depend on it. |
| Canonical lesson Markdown and editable diagrams are durable truth. | `PRESENT+` | These remain authoritative artifacts with versioned provenance and review state. |
| Git stores generated content or private evidence. | `REJECT` | Private production bundles and evidence stay in the private archive. Git stores code, schemas, synthetic fixtures, and public docs, not the corpus. |
| Separate authored and generated write paths. | `MERGED` | A generator MUST NOT overwrite authored scope, course order, learning-path definitions, correction decisions, reviewer findings, or operator approvals. Derived wiki/graph/search/card output must have separate destinations and provenance. |
| Stable video identity and canonical slug; redirects after slug changes. | `MERGED` | Preserve stable course, lesson, teaching-node, concept, and source IDs. Public slug changes MUST retain a redirect or an explicit withdrawn/replacement response and repair all internal references. IDs, never display titles, drive relationships. |
| Temporary write then validate and replace. | `MERGED` | Every generated artifact MUST be written to a staging path, validated, durably recorded, and only then promoted. Invalid regeneration MUST leave the previously accepted artifact and release usable. |
| Cache/generated/authored data survive restart. | `PRESENT+` | Existing immutable candidates, manifests, checksums, SQLite state, attempt states, and exact-byte promotion are stronger. Restart MUST resume from durable state without resetting attempts or acceptance. |
| Secrets split between batch and edge; redact proxy URLs. | `MERGED` generically | Separate generation, review/deploy, and optional runtime credentials. Never place secrets in content, logs, browser bundles, reports, preview URLs, or manifests. |

**Why ours is stronger:** [artifact storage](artifact-storage-review.md) already defines immutable candidate hashes, distinct reviewer/operator approval, public allowlists, exact-byte promotion, protected previews, rollback, withdrawal, and independent restore. The factory [execution contract](../factory/content-factory-v1-resolution.md#durable-spending-and-execution-contract) additionally preserves ambiguous request outcomes and cross-worker attempt limits.

### 3. Content contracts

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Fixed session fields and `TL;DR / Summary / Key ideas / Quotes / References / Who should watch`. | `REJECT` as lesson anatomy | It is archive copy, not a teaching contract. Lesson anatomy remains outcome, prerequisites, explanation/aha, example, visual where needed, practice, assessment, transfer, and concept links. |
| Stable source ID/URL, title, duration, timestamp, provenance, version, and eligibility metadata. | `PRESENT+` | Preserve the repository's more rigorous identity, provenance, evidence, and lifecycle contracts. |
| Typed JSON generation before Markdown; writer and parser share a contract. | `MERGED` | Model-facing intermediates SHOULD be typed and locally validated. Final learner prose remains constrained canonical Markdown with versioned provenance/verdict sidecars. Writer fixtures MUST pass through the production parser and renderer. |
| Store timestamps as integer seconds and validate bounds. | `MERGED` | Source evidence and published deep links MUST retain integer time values until rendering. Require `0 <= t < source_duration`; format only for display; bind each link to its own source ID. |
| Drafts excluded from every public derivative. | `MERGED`, adapted | Use the richer lifecycle: generated, valid candidate, quarantined, reviewed, accepted, published, withdrawn, superseded. Only eligible published artifacts may enter public pages, counts, feeds, search, sitemap, graph/wiki exports, recommendations, or machine interfaces. |
| Complete metadata+caption cache pair; corrupt/partial pairs are repairable errors. | `MERGED`, adapted | Define completeness for the repository’s source bundle: canonical raw transcript plus every declared matched cleaned counterpart and metadata role. Partial, corrupt, hash-mismatched, or ambiguous variants MUST be explicit states, never empty evidence. Cached operation must not require refetching. |
| Facets extract claims/disagreements for threads. | `REJECT` as release evidence | Node-level evidence refs, separate evidence-support and subject-correctness verdicts, outcome coverage, and human review are stronger. Non-authoritative discovery facets MAY be explored later but cannot supply teaching facts or acceptance. |
| Controlled presentation-facet vocabulary. | `ADAPT-LATER` | It may improve later browsing, but requires a bounded vocabulary and learner evidence. |
| Presentation tags replace the concept ontology. | `REJECT` | Tags cannot replace namespaced concepts, bilingual aliases, typed relationships, or reviewed merge/split decisions. |
| Append-only correction records and dependency invalidation. | `PRESENT+` | Preserve evidence-backed corrections and invalidation; do not merge people or concepts from similar spelling alone. |

**Why ours is stronger:** the resolution requires stable teaching nodes, namespaced concept senses, bilingual aliases, typed relationships, append-only correction evidence, and transitive invalidation. Every teaching-bearing node - including equations, quiz keys, visuals, alternatives, wiki entries, and simplifications - needs applicable verdict coverage.

### 4. Discovery and ingestion

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Recent-feed discovery for the fixed pilot. | `REJECT` | The pilot corpus and missing source are already fixed evidence. A provider feed cannot redefine its scope. |
| Provider-listing reconciliation for later course expansion. | `ADAPT-LATER` | Future reconciliation MAY compare provider listings with the local manifest, but cannot silently replace source policy or infer accepted courses from playlists. |
| YouTube Data API plus `youtube-transcript-api` captions. | `REJECT` as canonical ingestion | Raw Whisper JSON plus matched cleaned counterparts are approved teaching sources; raw stays canonical for segmentation/timestamps. Matching YouTube is used only for a specifically needed diagram. |
| Exclude duplicates/short items before model calls. | `PRESENT+` | Deduplicate by source revision/family and apply eligibility/scope rules before dispatch. Do not add a generic ten-minute threshold; short teaching evidence may be essential. |
| Per-item failure isolation and persistence. | `MERGED` | One source/unit failure MUST NOT discard successful durable work. It MUST block only the affected dependency closure and any course release that needs it. |
| Reconcile stale/missing ancillary artifacts without regenerating valid prose. | `MERGED` | Each run MUST detect missing/stale cards, indexes, graph/wiki exports, render proofs, verdicts, and embeddings when enabled. Repair only invalidated outputs. A deliberate decline or inapplicable derivative is a terminal recorded state, not pending work. |
| Recent/full/selected/fetch-only/reprocess/retag/repair/evidence/cards/embeddings commands. | `MERGED` as CLI semantics, renamed | Provide bounded operations for manifest reconciliation, source verification, selected-unit processing, validate-only, explicit regeneration, correction application, verdict refresh, derived-only rebuild, and release verification. Reject incompatible flags. Default no-change execution MUST be safe and zero-call. |
| Network timeouts, bounded retries/concurrency, resumability. | `PRESENT+` | Existing quota/attempt ledger is stricter. Network/model work must remain explicitly authorized and uncertainty must stop dependent dispatch. |

### 5. Generation and editorial standards

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Separate prose, tagging, evidence, and note calls. | `MERGED` as stage isolation | Separate independently invalidatable tasks: course design, lesson authoring, assessment, diagram spec/export, concept/wiki/graph extraction, and evaluation. A correction to one derivative must not force unrelated regeneration. |
| Schema-constrained output plus local validation; explicit refusal/truncation states. | `MERGED` | Provider success is not content validity. Persist refusal, truncation, malformed output, missing IDs, invalid schema, and unsupported evidence as distinct outcomes. |
| Word/count targets for summaries, ideas, quotes. | `REJECT` | Outcome/source sufficiency determines lesson size and components. Quotas cannot justify filler or fabrication. |
| Transcript is evidence, not instructions. | `PRESENT+` | Existing policy is broader: source/generated text cannot issue tools; arbitrary HTML/JS is forbidden; paths/URLs/components are allowlisted; executable examples are isolated. |
| One retry after validation errors; preserve prior page. | `PRESENT+` | Keep bounded retries, targeted repair, durable lineage limits, quarantine, and prior accepted output. Do not hard-code the Talks retry count over the factory budget contract. |
| Faithfulness reviewer is advisory; unresolved grounding blocks. | `PRESENT+` | Ours requires more: evidence support and subject correctness are separate; every applicable node gets a verdict; calibrated evaluation plus named subject/Arabic editorial review and zero unresolved critical defects gate release. |
| Prompt/evidence versions and derived invalidation. | `PRESENT+` | Cache keys already include source/content/context/rubric/prompt/model/settings/schema/tool versions, with a conservative whole-lesson context boundary. |
| Sponsor notes. | `REJECT` | No learner need or operator request establishes sponsorship. It would add commercial, editorial, review, privacy, and product obligations. |

### 6. Threads

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Authored subject definition, derived membership, selected evidence line. | `ADAPT-LATER` | Preserve the separation pattern if editorial topic trails are later justified: definition is authored; membership is reproducibly derived; excerpts stay source-linked and labeled as paraphrase. |
| Any-tag membership, substring term matching, four rows/year, upload-year narrative. | `REJECT` | These rules are shallow and archive-specific. They cannot express concept sense, prerequisite direction, course context, equivalence, or learning order. Counts cannot establish intellectual history. |
| Threads as initial discovery destination. | `REJECT` | Concepts/wiki and the typed graph already provide a stronger learning-recovery destination, with an accessible list fallback. |

### 7. Packs

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Authored membership/order; explain each transition; verify timestamp chips. | `ADAPT-LATER` | Strong pattern for an optional problem-oriented learning path. Use accepted lesson/course IDs, explicit reader problem, prerequisites, reason per transition, source-linked evidence where relevant, and deterministic order. |
| Five-to-twelve video membership and video thumbnail cover. | `REJECT` | Arbitrary archive limits do not define sound curriculum. Length follows learner outcome, prerequisites, cognitive load, and review evidence. |
| Automatic member links from a session page. | `ADAPT-LATER` | A lesson may show one canonical next step and secondary containing paths without competing controls, after usability evidence supports the interaction. |

**Why ours is stronger:** course outline and roadmap are two views of one reviewed sequence. Every stage ends in a deliverable; every outcome records prerequisites and required explanation/example/practice/transfer IDs. Packs cannot substitute for that curriculum contract.

### 8. Website and visual design

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Course-focused homepage search and browsing. | `PRESENT+` | Retain purpose, global search, continue learning, faculties, subjects, foundations, and recent accepted courses. |
| Speaker, company, format, and archive-year browsing. | `OPEN` | Do not add these archive facets without learner evidence and an operator choice. |
| Year archive with URL-persisted validated filters, AND semantics, removable chips, clear-all, back/forward, empty recovery. | `MERGED`, adapted | Catalog filters MUST use faculty, subject, academic level, language, availability, and approved future facets. State MUST be serializable in the URL, validated, reloadable, keyboard usable, and restored through history navigation. Invalid values fail safely. |
| Alphabetical entity indexes. | `ADAPT-LATER` | Potentially useful for large concept/subject/faculty indexes. Arabic collation, aliases, and bilingual sort behavior require explicit tests. |
| Restrained serif/sans/mono palette. | `REJECT` as visual prescription | Preserve Arabic-first Thmanyah, course accents, calm reading, strong mixed direction, and the explicit design pass. The Talks fonts/colors are reference-product styling, not ours. |
| Light/dark/system theme with pre-paint preference. | `OPEN` | Theme support is not yet a settled requirement. If enabled, use one state mechanism, apply before paint, tolerate unavailable storage, and preserve contrast/focus. |
| No horizontal scroll at 360px; accessible focus/reduced motion. | `PRESENT+` | Ours additionally requires correct RTL navigation, math/code direction, Arabic alternatives, 200% zoom, touch targets, weak-phone/low-bandwidth behavior, and useful content when storage/media/JS fails. |
| HTML generated at build time; essential content works without JS. | `PRESENT+` | Already a learner-v0 boundary. Quizzes, graph interactions, filters, and progress are enhancements; reading and core links remain in initial HTML. |
| Canonical/OG/sitemap URL agreement. | `MERGED` | Public routes MUST share one canonical URL/trailing-slash policy across HTML, metadata, sitemap, search, redirects, and machine outputs. |
| Deterministic 1200×630 share cards. | `MERGED`, capacity-gated | Course/lesson cards MAY be implemented only after the catalog file-count/size experiment; displayed metadata changes MUST invalidate them. |
| Sitemap, About page, and useful 404 recovery. | `MERGED` | These routes support existing discovery and recovery needs and must expose only eligible public content. |
| Static release/correction RSS feed. | `ADAPT-LATER` | Consider it after the static foundation; it cannot become a partial-teaching publication route. |
| `llms.txt`. | `ADAPT-LATER` | It remains optional and cannot substitute for useful crawlable teaching. |
| Talks-style content feed. | `REJECT` | The course platform does not require a feed organized around individual talks. |
| Real 404 and clean routes. | `MERGED` | Unknown routes MUST return a real 404 with search/browse recovery. Candidate IDs, hashes, storage paths, and `.html` extensions must not leak into canonical public URLs. |

### 9. Search and agent access

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Pagefind after render; one entry per detail page; exclude aggregate/nav/footer duplication. | `MERGED` | Keep Pagefind as the current candidate. Build the index only from eligible rendered course, lesson, concept/wiki, subject, and approved editorial detail pages. Exclude private/draft/withdrawn content, answer keys, duplicate exports, navigation/footer, and thin aggregates. |
| Result kind, title, excerpt, context, filters, stable heading fragments. | `MERGED` | Both global and course-aware search MUST distinguish result kind and location, show the matched Arabic/English term or alias where useful, and link to stable section IDs. Test against a completed build, not only a dev server. |
| Query at `/search?q=...`; modal focus/Escape/return-focus; loading/no-results/index-error. | `MERGED` | Preserve the query in the URL. Any dialog MUST be keyboard complete. Loading, empty result, invalid scope, and index-load failure are distinct; failure preserves the query and browse recovery. |
| Optional embedding endpoint and related sessions. | `ADAPT-LATER` | No runtime model calls in learner v0. Future semantic retrieval must only retrieve accepted documents, remain optional, preserve keyword fallback, avoid mastery/certainty language, and fit privacy/cost authorization. |
| Canonical embedding text/hash/model/dimensions/order; stale enabled index fails build. | `MERGED` conditionally | If embeddings are enabled later, define canonical input serialization and content hash; record model identity/dimensions; reject missing, stale, duplicate, non-finite, zero, or dimension-mismatched vectors; never make paid calls implicitly during static build. |
| Bound request body/rate/time; stale response cannot beat new request. | `MERGED` conditionally | Any future endpoint MUST validate method/content/input/body size, bound concurrency/time, redact provider failures, preserve the query on error, and prevent out-of-order responses from overwriting newer UI state. |
| Markdown routes, `llms.txt`, content negotiation. | `ADAPT-LATER` | Useful only for accepted public content. HTML remains canonical for browsers; Markdown must retain substantive teaching, provenance, source links, and navigation. `llms.txt` is not a ranking dependency. |
| Full or reduced read-only MCP. | `ADAPT-LATER` | MCP is not a launch dependency and must not expose private corpus, evidence, filesystem, publishing, or credentials. Register only functional tools; `fetch` resolves allowlisted public documents on the configured origin, never arbitrary URLs. Measure context/operations cost first. |

**Why ours is stronger:** [search discovery](search-discovery-2026-q3.md) already separates useful public content from crawler theater, distinguishes search eligibility from training permission, rejects obsolete/unsupported rich-result promises, requires bilingual stable anchors and real provenance, and keeps quiz answers out of snippets.

### 10. Daily operation and maintenance skills

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Daily bounded import, generated PR, no change = no PR. | `ADAPT-LATER` | Appropriate only for post-acceptance maintenance or future source reconciliation. It cannot publish partial courses or bypass the release predicate. A no-change run MUST create no content proposal and consume no model quota. |
| One concurrency group; actionable report with per-item outcomes and usage. | `MERGED` | Serialize publication for a release target. Reports MUST distinguish discovered, cached, generated, valid, reviewed, accepted, published, skipped, failed, quarantined, stale ancillary, and withdrawn states, with stable artifact links and usage. |
| Fix generator/prompt/correction rule, then regenerate; do not permanently hand-patch generated prose. | `MERGED`, qualified | Durable repairs belong in source-backed authored Markdown, generator/prompt/schema, or append-only correction records according to artifact authority. Never alter generated output in a way the next run silently loses. |
| Short maintenance procedures state input, allowed edits, evidence, checks, report. | `MERGED` | Future procedures for daily review, learning paths, concept/taxonomy changes, and identity correction MUST declare those fields plus authorization, privacy boundary, invalidation closure, and publication gate. |
| Backfill starts small and measures coverage. | `PRESENT+` | The optics engineering trial and bounded batches already do more: they require difficult cases, accepted outcome coverage, reviewer time, cost, failure recovery, and learner evidence before expansion. |
| Automated merge may follow passing checks. | `REJECT` for current release | Checks alone cannot supply subject/editorial review, learner evidence, rights, prerequisite closure, or operator approval. Automation may propose; current promotion remains explicitly gated. |

### 11. Reference stack and implementation sequence

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Keep Python 3.11+ with `uv`. | `PRESENT+` | Preserve the repository's current supported runtime and package workflow. |
| Upgrade to Python 3.14 because the reference uses it. | `REJECT` | Change the Python floor only for demonstrated repository value and verified compatibility. |
| Astro and Pagefind as platform choices. | `OPEN` | They remain provisional candidates pending compatibility and prototype evidence. |
| Provider-agnostic OpenAI-compatible adapter. | `PRESENT+` | Preserve the authorized provider-neutral integration contract. |
| Vendor-specific paid SDK as the required integration. | `REJECT` | A named vendor SDK cannot override the provider-neutral adapter, quota authorization, or cash controls. |
| Exact Node/runtime versions. | `OPEN` | Pin them only after compatibility verification. |
| Workers and MCP. | `ADAPT-LATER` | They remain optional post-static-foundation capabilities, not learner-v0 dependencies. |
| Avoid framework/CMS/vector DB/queue without concrete need. | `PRESENT+` | Matches static-first simplicity and the $5/month ceiling. Browser-local enhancement remains the baseline. |
| Fixtures → one complete source → repeatable pipeline → static archive → collections → daily review → optional services → fresh-checkout acceptance. | `MERGED`, reordered to ours | Preserve CF-01…CF-13 and current NEXT_STEPS. Within relevant tickets, keep the useful progression: deterministic fixtures/contracts; one complete engineering trial; no-op/restart proof; static reader; controlled release; optional services last; clean restore/build verification. |

### 12. Acceptance criteria

| Talks Archive proposal | Decision | Course-platform treatment |
|---|---|---|
| Scenario-based acceptance checks instead of vague feature-completion claims. | `MERGED` | Use observable scenarios and expected outcomes in the adapted matrix below. |
| Curriculum sufficiency, teaching quality, independent review, learner transfer, Arabic/RTL behavior, quota uncertainty, exact-byte promotion, and private restore. | `PRESENT+` | Preserve the repository's broader evidence requirements; the Talks Archive scenarios do not replace them. |

## Merged implementation contract

The clauses below are the net-new or newly explicit requirements adopted from the comparison. They apply when their owning ticket/surface is authorized.

### A. Identity, lifecycle, and writes

1. Relationships MUST use stable IDs, never mutable titles/slugs.
2. Source identity, source revision, course membership, teaching-node identity, public slug, candidate revision, and release identity MUST remain distinct.
3. Current and future course processing MUST default to one source video per learning unit. Splitting one video across learning units or synthesizing one learning unit across videos requires an explicit reviewed exception supported by the outcome matrix; stable source and learning-unit identities remain distinct.
4. A public slug change MUST produce a tested redirect or explicit withdrawn/replacement behavior; dependent navigation, canonical metadata, sitemap, search, cards, exports, and local-progress migration MUST be updated or invalidated.
5. Every artifact state transition MUST be explicit. At minimum distinguish source available/incomplete/corrupt; work pending/running/failed/unknown/succeeded; candidate invalid/quarantined/reviewed/accepted; release published/superseded/withdrawn.
6. Only eligible published content may enter public derivatives. The build MUST fail or omit the entire affected derivative according to a declared policy; it must never silently include a draft/quarantined/withdrawn node.
7. Generation MUST use staged writes and validation before atomic replacement/promotion. Failure preserves the last valid candidate and last accepted release.
8. Authored, generated, reviewer, approval, and derived-asset destinations MUST be write-separated. Tools MUST declare which classes they may edit.

### B. Cache completeness and targeted reconciliation

1. Each source manifest record MUST declare the required artifact set and role of each member. “Metadata exists” cannot imply “teaching evidence is complete.”
2. Partial, corrupt, hash-mismatched, missing, or ambiguous source bundles MUST produce typed repairable outcomes. They MUST NOT degrade to an empty transcript or title-only generation.
3. A valid cached source bundle MUST support authorized regeneration and validation with source networking disabled.
4. Each run MUST reconcile required derivatives against dependency hashes/versions. Missing or stale outputs remain pending even when the primary lesson file exists.
5. Reconciliation MUST repair only affected derivatives. Valid prose is not regenerated to redraw a card, rebuild search, rerender HTML, or refresh a stale vector/verdict.
6. “Not applicable” and deliberate decline are durable terminal states distinct from “not attempted.”
7. Unchanged reruns MUST propose no content changes and make zero generation/judging calls unless an explicitly authorized audit is due.

### C. Generation and validation boundary

1. Model-facing outputs SHOULD use typed schemas. Every provider response MUST receive local schema, identity, reference, timestamp, and allowed-content validation.
2. Provider transport success, schema validity, evidence support, subject correctness, editorial/pedagogical acceptance, human approval, and publication MUST remain separate states.
3. Writer → parser → renderer conformance MUST be tested with the writer’s real output shapes plus adversarial fixtures.
4. Persist timestamps numerically and validate against their own source duration. Generated text cannot supply new timestamps detached from source evidence.
5. Refusals, truncation, missing parsed output, missing stable IDs, duplicate identities, and validation errors MUST be categorized and reported.
6. Stage prompts/schemas/models/tools MUST be independently versioned so a change invalidates only its justified dependency closure.

### D. Static build, URLs, and derived assets

1. Essential reading, outcome/prerequisite context, source attribution, and navigation MUST exist in initial HTML. Optional JavaScript or service failure cannot erase them.
2. One canonical-origin and trailing-slash policy MUST govern renderer output, canonical tags, Open Graph URLs, hreflang, breadcrumbs, sitemap, search records, redirects, Markdown representations, and optional machine interfaces.
3. Preview/candidate URLs, hashes, storage paths, duplicate exports, internal filter combinations, and archived versions MUST remain outside public canonical/sitemap surfaces.
4. Unknown routes MUST return an actual 404 plus useful course/subject/search recovery.
5. Derived visual assets MUST record the input identity/hash and renderer/font/template version. Relevant metadata/theme/font/template changes invalidate them.
6. Social-card generation remains capacity-gated; it MUST be deterministic, handle Arabic/mixed-direction long titles and missing images, and avoid model/image-generation calls.

### E. Catalog and keyword search behavior

1. Catalog/filter state MUST serialize to a shareable validated URL and survive reload plus browser back/forward.
2. Selected filters combine according to documented semantics, show removable chips and clear-all, and expose a useful no-match recovery. Unknown filter values cannot crash, leak hidden content, or generate indexable duplicates.
3. Search indexing MUST happen after the production render and contain one intentional record per eligible detail page.
4. Indexable bodies MUST exclude navigation/footer repetition, private/draft/withdrawn content, answer keys/rationales before attempt, and duplicate aggregate/export text.
5. Results MUST expose kind, title, useful context/location, matched term where available, and canonical link. Arabic, English, mixed-script, aliases, common variants, and course-aware ranking require explicit fixtures.
6. Search UI MUST distinguish loading, no results, invalid scope, and index-load failure. It preserves the query and offers broader catalog navigation when recovery is needed.
7. Any search dialog MUST open with sensible focus, close by Escape, restore focus to its opener, and remain keyboard-operable at 360px and 200% zoom.

### F. Optional semantic, Markdown, and MCP profile

These capabilities remain disabled by default and post-v0. Enabling one requires explicit product value, privacy/retention policy, cost authorization, threat model, local-runtime tests, and graceful fallback.

1. Semantic retrieval MAY rank existing accepted content; it MUST NOT generate teaching answers, claims, citations, prerequisites, or mastery judgments.
2. Embedding input serialization, whitespace/separators, hash, model identity, dimensions, normalization, and document order MUST be canonical. Enabled builds reject missing, stale, duplicate, zero, non-finite, or inconsistent vectors.
3. Static builds MUST NOT initiate paid or network embedding work implicitly.
4. Runtime queries MUST be length/body bounded, rate/concurrency/time bounded, and excluded from logs by default unless a reviewed retention policy says otherwise.
5. A failed/low-confidence semantic result preserves the query and routes to keyword search/catalog. Similarity MUST NOT be labeled accuracy, certainty, correctness, or learning fit.
6. A later response cannot overwrite a newer submitted query.
7. Markdown representations expose only accepted public content and preserve useful teaching, provenance, source links, and navigation.
8. MCP registers only working read-only tools. Tool schemas define limits and filters. Unknown IDs return explicit not-found responses. `fetch` resolves only allowlisted documents on the configured canonical origin and never arbitrary URLs.
9. No optional interface may expose local files, corpus text beyond approved public excerpts, evidence packets, review records, unpublished answers, credentials, publishing operations, or filesystem access.

### G. Automation and maintenance

1. A scheduled job MUST use one concurrency group per publication target; overlapping promotion cannot race.
2. No-change runs create no proposal/PR and consume no generation quota.
3. Changed runs report stable IDs and counts by lifecycle state, validation warnings, incomplete ancillary work, quota usage/unknown usage, and exact checks required before review.
4. Automation may prepare a candidate; it cannot replace the machine-readable release predicate, independent review, learner evidence, rights checks, prerequisite closure, or operator approval.
5. Maintenance procedures MUST state: input; authorization; allowed edits; forbidden/private data; evidence to inspect; deterministic/model checks; invalidation closure; preview requirement; completion report; publication boundary.
6. Durable fixes MUST live at the correct authority layer. Do not patch a derivative that regeneration will erase; do not rewrite immutable source evidence; do not use a correction table to smuggle in outside teaching facts.

## Adapted acceptance matrix

These are observable checks, not claims that they currently pass.

| Area | Required scenario and observation |
|---|---|
| Identity | Importing the same source revision twice creates one source identity. Separate course memberships remain associations, not duplicate source/lesson identities. |
| Source coverage | The frozen manifest accounts for every expected pilot ID and every segment disposition. A recent/provider listing alone cannot claim full coverage. |
| Cache | A complete local source bundle supports the permitted offline stage. Partial/corrupt/hash-mismatched bundles fail visibly and are repairable without title-only generation. |
| Failure isolation | One source/unit failure preserves unrelated durable work and the previous accepted release; affected prerequisite closure remains blocked. |
| Atomic replacement | Kill the process before validation, after staging, and before promotion. No mixed/partial candidate or release becomes visible. |
| No-op | A second unchanged run produces no semantic content diff, no model/judge call, no new proposal, and no reset attempt budget. |
| Grounding | Unsupported facts, numbers, equations, names, examples, quotes, and diagram labels are blocked even when schema-valid. External/source-instruction contamination is blocked. |
| Correctness | A faithfully transcribed false or ambiguous claim does not pass subject correctness merely because it is source-grounded. |
| Timestamps | Zero is valid; duration itself is invalid; every public deep link uses the correct source ID and second. |
| Corrections | An approved evidence-backed correction survives regeneration and invalidates every affected lesson, quiz, wiki/graph node, search record, card/export, and contextual verdict. |
| Curriculum | Every accepted outcome has task, prerequisites, eligible evidence, explanation, example, practice, transfer task, and sufficiency. No tag/thread/pack can bypass this matrix. |
| Visibility | Candidate, quarantined, draft, unreviewed, superseded, and withdrawn teaching is absent from public routes, counts, sitemap, search, graph exports, feeds, and machine retrieval. |
| Authored order | Ingestion or retagging cannot silently reorder course units, alter prerequisites, or overwrite authored learning paths. |
| Catalog filters | Faculty + subject + level + language + availability filters serialize correctly, survive reload/back, show truthful counts, and recover from empty/invalid combinations. |
| Keyword search | Known Arabic, English, mixed-script, alias, course, lesson, and concept queries return the correct eligible detail pages; aggregate/navigation text does not dominate. |
| Static delivery | With JavaScript disabled, lesson teaching and core links remain readable. Canonical, hreflang, sitemap, served routes, redirects, and machine representations agree. |
| Responsive/RTL | At 360px and 200% zoom, no unintended page overflow; RTL navigation, Arabic/English wrapping, math/code direction, drawers, quizzes, focus, and touch targets remain usable. |
| Failure UX | Missing media, unavailable storage, broken search index, revised lesson, withdrawn lesson, and 404 states preserve useful reading/recovery and do not invent content. |
| Derived freshness | Changing relevant metadata/content/theme/font/template makes affected cards/search/graph/wiki/exports stale; clean build cannot silently publish stale enabled artifacts. |
| Semantic routing | If enabled, it retrieves only accepted content, passes calibrated Arabic/English intent fixtures, treats unrelated queries cautiously, and falls back without losing the query. |
| Optional service | If enabled, malformed/oversize input, unsupported method, timeout, throttling, unavailable index/provider, stale response, and secret-redaction cases behave according to the documented contract. |
| MCP | If enabled, a real SDK client can list/search/fetch only accepted allowlisted public documents; unknown IDs, unpublished IDs, local paths, and external URLs are rejected. |
| Review/release | Stale reviewer approval, missing learner evidence, unresolved rights, unsupported prerequisite, failed render proof, or private-file leak blocks promotion. Preview and live bytes match. |
| Recovery | Interrupted generation resumes from durable state; previous accepted release, private artifact archive, and independent corpus backup can be restored without regenerating teaching or spending model quota. |
| Automation | Unchanged scheduled run opens nothing. Changed run creates a bounded candidate/report but cannot self-authorize publication. Concurrent publication attempts serialize. |

## Explicit non-adoptions

Do not import the following without a new, evidence-backed scope decision:

- session-as-product architecture or fixed session summary headings;
- speaker/company/host/episode/view-count archive taxonomy;
- `talk`, `podcast`, `meetup`, and `reading_group` formats as core course metadata;
- tag-OR threads, substring evidence selection, upload-year trend narratives, or arbitrary per-year caps;
- five-to-twelve-video packs or automatic tag-driven curriculum membership;
- YouTube API captions as replacement for the approved local source policy;
- duration-based source exclusion without outcome/sufficiency review;
- sponsor notes, sponsor eligibility, advertising, or branded editorial insertions;
- daily partial teaching publication or check-only automatic merge;
- a runtime edge service, embeddings, recommendations, analytics, Markdown negotiation, or MCP as a learner-v0 dependency;
- Talks Archive fonts, palette, LTR information architecture, or MLOps topic vocabulary;
- Python 3.14, a vendor-specific paid SDK/service, or any unverified “latest” runtime merely because the reference used it.

## Where this repository is materially better

| Area | Stronger repository contract |
|---|---|
| Learner value | Independent application of explicit outcomes with practice and transfer evidence, not watch-selection or summary consumption. |
| Source discipline | Bound raw+cleaned per-video evidence; raw canonical for spans/timestamps; matching video only for needed diagrams; no outside subject facts; unsupported gaps block. |
| Curriculum completeness | Outcome matrix plus source-segment dispositions, prerequisites, examples, practice, transfer tasks, and complete prerequisite closure. |
| Quality model | Separate grounding, subject correctness, pedagogy, and coherence judgments for every teaching-bearing node; calibrated challenge/holdout protocol and named human review. |
| Corrections | Append-only source-backed record with original span, replacement, reason, reviewer, disposition, affected IDs, and quarantine when unsupported. |
| Dependency safety | Explicit semantic graph versus build DAG and a transitive invalidation matrix across lessons, quizzes, concepts, diagrams, exports, and verdicts. |
| Cost/recovery | Cross-provider SQLite reservations, persistent attempt lineage, `outcome_unknown`, uncertain-quota stop, crash/concurrency probes, and full accepted-yield accounting. |
| Release integrity | Frozen candidate hashes, distinct reviewer/operator authority, exact-byte promotion, private allowlists, rollback, withdrawal, and independent restore. |
| Arabic/accessibility | Arabic-first RTL, bilingual aliases, mixed-direction text, Thmanyah, math/code isolation, 360px plus 200% zoom, keyboard/touch, low-bandwidth and static alternatives. |
| Knowledge model | Namespaced concept senses, reviewed bilingual aliases/merges, typed edges, acyclic prerequisites, course/global graph, and accessible list representations. |
| Claims discipline | Search/citation/activity metrics are not learning; local completion is not mastery; graph/year counts are not historical causation; a plausible page is not acceptance. |

## Sequencing impact

No current milestone moves. Apply the merged clauses only inside the existing order:

1. **Now:** finish the transcript-backed outcome matrix, diagram needs, and independently prepared reference packet in [NEXT_STEPS](../NEXT_STEPS.md).
2. **CF-04/05/07:** implement typed lifecycle states, staged replacement, cache completeness, targeted reconciliation, conformance, and no-op/restart proofs.
3. **CF-08…13:** use richer reports, derived freshness, immutable review/release behavior, maintenance procedures, and recovery scenarios.
4. **Authorized app milestone 1/2:** implement URL-state catalog filters, Pagefind build contract, search/dialog failure states, canonical/404 rules, and responsive checks with synthetic fixtures.
5. **After measured static foundation:** decide social-card capacity, themes, problem-oriented learning paths, Markdown representations, embeddings, edge routing, analytics, and MCP independently. None is bundled by implication.

## Unresolved questions

- Should deterministic course/lesson social cards enter the first static platform release, or wait for the catalog file-count/size experiment?
- Should light/dark/system themes be a v0 requirement or a later polish feature?
- What learner evidence, if any, would justify speaker, company, format, or archive-year browsing?
- Do the platform prototypes validate Astro and Pagefind, or should either candidate be replaced?
- Which exact Node/runtime versions pass the chosen toolchain's compatibility checks?
- Which exact public slug/trailing-slash and redirect policy should the Astro prototype prove?
- Which typed source-bundle completeness schema should CF-05 use for raw plus optional/required cleaned counterparts?
- Which later learner problem would justify authored cross-course learning paths beyond canonical course roadmaps?
- Are Markdown representations desired before MCP, or should both remain deferred until public-search evidence shows value?
