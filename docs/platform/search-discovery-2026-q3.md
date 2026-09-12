# Search and AI discovery — Q3 2026

Checked 2026-09-07 against primary documentation. Requirements for the planned platform; nothing is configured or indexed yet. Discovery supports the [north star](platform-north-star.md): learners find a useful lesson or concept and can continue into meaningful practice. Citation counts do not measure learning.

**Current findings that affect the plan**

- Google's [generative-AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) emphasizes distinctive useful content and normal SEO. It says Google does not use `llms.txt` for ranking and advises against mass-producing query variations or dividing content into tiny chunks for AI. Our advantage must come from reviewed Arabic teaching, useful explanations and practice.
- A material Q3 change: Google says its [Search generative AI control](https://support.google.com/webmasters/answer/16908024) rolled out worldwide by **2026-08-31**. Verify Search Console Settings → Search generative AI includes the site, including inherited property settings. Search eligibility and AI training controls are separate.
- OpenAI distinguishes [OAI-SearchBot from GPTBot](https://developers.openai.com/api/docs/bots). Permit OAI-SearchBot and its published IPs for ChatGPT search eligibility. GPTBot concerns model training; training permission is not required for search inclusion. Do not blanket-block every AI user agent at the CDN.
- Google's [2026 updates](https://developers.google.com/search/updates) retire practice-problem rich results and FAQ rich results. [Course Info/Learning Video features](https://developers.google.com/search/blog/2025/06/simplifying-search-results?hl=en) were retired in 2025. The remaining [Course List rich result](https://developers.google.com/search/docs/appearance/structured-data/course) is documented as English-only. Do not promise Arabic course rich results or add obsolete markup for an imagined ranking benefit.
- [Bing AI Performance](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) reports citation activity for supported Microsoft/partner surfaces, including page-level citations and sampled grounding queries. It is not a measurement of every chat app or a ranking score.

**Publish pages students can actually find and cite**

| Page | Purpose | Required content |
|---|---|---|
| Subject/catalog | Find an appropriate course | Real subject/level organization and links to released courses |
| Course | Understand the learning path | Arabic title, natural English equivalents, course code where useful, outcomes, prerequisites, scope, ordered lessons |
| Lesson | Learn and practise a specific outcome | Descriptive title/headings, explanation, worked example, accessible diagram text, practice, stable section IDs, source references |
| Concept/wiki | Resolve a term or connection | Definition with context, aliases, typed relationships and links back to teaching; independent value beyond duplicated lesson prose |
| Editorial/about/corrections | Understand who stands behind the content | Actual authors/reviewers and roles where publishable, editorial method, source attribution, limitations, dated material corrections |

Generate useful content and links in initial HTML. Keep graphs, animations and quizzes as enhancements; provide textual concept/relationship pages and media explanations. No requirement that a crawler drag a graph, play a video or attempt a quiz to discover the teaching. This also supports low-bandwidth reading; it is not a claim that Google cannot render JavaScript.

Use a stable canonical public URL per page, independent of storage paths, candidate IDs and deployment hashes. Example shape: `/ar/courses/<course>/lessons/<lesson>/` and `/ar/concepts/<subject>/<concept>/`. Give genuine translations separate URLs with appropriate language metadata/hreflang; English term aliases on an Arabic page are not an English translation. Do not publish shallow duplicate pages for spelling/query variants.

Generate titles, descriptions, canonical links, breadcrumbs, XML sitemaps and accurate changed dates from accepted metadata. Keep preview URLs, internal search/filter combinations, duplicate exports and archived versions out of indexable navigation/sitemaps. Unreleased teaching stays private. Index only eligible canonical pages; choose intentional noindex for thin navigation pages. Verify the actual canonical host before public promotion.

Use structured data only where it truthfully describes visible content; consider Course, BreadcrumbList and relevant article/organization information, without invented credentials, ratings or institutional endorsement. Rich-result eligibility varies; validate the supported type before implementation. Metadata, descriptions and accessible alternatives must not introduce unsupported teaching facts.

**AI citation policy**

Make the visible content precise enough to cite: clear concept scope, natural bilingual terminology, stable headings/anchors, provenance and real review/update information. Students and agents receive the same accepted teaching. Optional Markdown/OKF exports can serve explicit consumers later; `llms.txt`, an MCP server, embeddings and paid GEO services are not launch dependencies. Do not invent an agent-specific content feed as a substitute for useful public pages. Crawl access creates eligibility, never a citation guarantee.

**Publication and measurement**

1. Build: validate canonical URLs, crawlable internal links, sitemap membership, language metadata, visible content/structured-data agreement, no private artifact leaks, readable math/diagrams and performance on a weak phone.
2. Review: keep candidate pages authenticated. Check public `robots.txt`, robots headers/meta and CDN rules separately; public pages must permit relevant search crawlers and useful snippets. Keep answers to formative quizzes out of pre-attempt presentation/search snippets without suppressing the lesson itself.
3. Promote: publish approved stable pages, then update sitemaps. Notify participating engines of changed/deleted URLs with [IndexNow](https://www.indexnow.org/documentation); acceptance is not an indexing guarantee and this does not replace Google's sitemap/Search Console workflow.
4. Observe: Google Search Console indexing/search reports and its available generative-AI reporting; Bing indexing and AI Performance; identifiable referral traffic where available. No comprehensive cross-chat citation metric is assumed. Record missing coverage honestly.
5. Improve: examine real Arabic queries, unsuccessful discovery journeys and learner feedback. Fix content/navigation issues through the normal review process. Track useful discovery separately from observed learning outcomes; avoid publishing unreviewed SEO pages to increase counts.

**Qualification still needed:** real hostname ownership, search-tool verification, per-platform crawler/CDN checks, representative Arabic search intents, catalog-scale crawl/performance tests, and current schema validation. No paid SEO tooling is needed for this proposed workflow. Recheck provider guidance at implementation because this is dated research, not a permanent contract.
