# Platform north star

2026-09-07. Operator accepted the recommended learner-purpose, independent-study and connectivity defaults. Implementation choices and numeric measures below remain recommendations; release gates still apply.

**North star:** Help Arabic-speaking university learners discover, understand and independently apply their subjects through clear courses, meaningful practice and connected concepts—without needing an account.

**Accepted defaults:** understand and apply university subjects is the primary job; independent study within explicitly stated outcomes and prerequisites; phone-first, low-bandwidth online delivery. Offline course downloads are not a launch promise. Lab/supervision limits must be visible where relevant.

**Additional operator priorities:** public pages discoverable through search and citable by AI agents/chat apps; private intermediate/final artifact storage outside GitHub; other people can review a candidate before final operator approval; artifact hosting/operations may cost at most $5/month (operator-confirmed). See [storage and review](artifact-storage-review.md) and [Q3 2026 discovery plan](search-discovery-2026-q3.md). The new cash allowance is for hosting/artifacts, not paid model APIs.

**Confirmed by the operator:** no learner accounts for now; roughly 325 higher-education courses and thousands of lessons across specializations; support the platform requirements and approved outputs described in [skills-map.md](../research/skills-map.md). This scale is a destination, not a claim that those courses are accepted or that playlist counts equal course counts.

**Existing constraints:** Arabic-first with strong English/mixed-direction support; canonical Markdown; reviewed teaching and diagrams; inline assessment; course/lesson wiki and cross-course typed concept graph; excellent reading and accessibility; open-source, simple tooling; static-first economics. [Platform brief](platform-map-brief.md) defines this destination. [Factory goal](../factory/content-factory-v1-goal.md) governs the optics pilot and release quality. [App plan](course-app-plan.md) is a provisional implementation slice.

**How the requirements serve the promise**

| Learner need | Required product capability | Evidence that it helps |
|---|---|---|
| Find the right starting point | Catalog by subject/level, course outcomes, prerequisites, search | Learner selects an appropriate course or prerequisite without assistance |
| Understand a difficult idea | Reader, worked examples, editable-source diagrams, reviewed simplifications, accessible visual/media outputs | Learner explains or uses the idea on a new task |
| Practise the actual subject | Inline questions and discipline-appropriate tasks with useful feedback | Learner produces work aligned with the stated outcome |
| Connect ideas and recover missing knowledge | Wiki, bilingual aliases, typed relationships, course/global graph exploration | Learner finds the correct concept sense and a valid prerequisite or related lesson |
| Continue studying | Navigation and clearly described local progress; low-bandwidth online baseline | Learner resumes after interruption and understands any revision or storage loss |
| Trust the material | Visible scope, source references, correction/report route and current release | Learner can identify what is covered and report a specific problem |

**Success: proposed measurement, not an implemented analytics system**

Primary learning evidence: the proportion of eligible, observed learner–outcome attempts that meet a predeclared criterion on a fresh unaided task after study. Record baseline ability and report by discipline/outcome; disclose sample size and exclusions. This is a formative measure, not proof of causal improvement or whole-catalog mastery. Retention claims need delayed checks.

No accounts does not prevent voluntary learner trials, but it does prevent assuming a reliable global count of distinct learners from local progress. Do not silently turn this measurement proposal into tracking. Downloads, reading time, quiz attempts and checkmarks are diagnostic signals, not the north star. Course count measures coverage.

Supporting constraints: correctness, accessible task completion, time to find a useful lesson, bytes needed to study, review effort and maintenance cost per accepted course. Numeric targets require evidence and operator choices.

**Skills-output promise**

The platform should preserve the teaching purpose of approved outputs through consistent presentation. The skills map is a candidate tool map, not a requirement to install everything or a guarantee of compatibility.

| Output family | Delivery requirement to resolve |
|---|---|
| Markdown, math, code, tables, quizzes | Shared versioned parser; stable teaching IDs; appropriate assessment types |
| Excalidraw/static SVG or recovered images | Approved export, editable-source linkage, readable labels and accessible explanation |
| Interactive HTML/SVG and motion | Approved renderer/isolated asset contract, reviewed states, keyboard/touch behavior, reduced-motion/static alternative |
| Rendered video | Captions/transcript, poster, size budget and delivery path; do not assume the HTML authoring runtime belongs in the learner app |
| Wiki, graph, glossary, simplifications | Reviewed identities/aliases, typed edges, source links and invalidation on corrections |
| Obsidian/OKF, slide or other downloadable exports | Decide whether learner-facing; version, accessibility, rights and withdrawal/update expectations |

The authored-content ban on arbitrary HTML/JavaScript remains binding. Interactive-output support needs an explicit adapter or isolated asset design; neither blanket rejection nor unrestricted embedding is an adequate product contract.

**Blindspots to test before committing to the full platform design**

| Unproven assumption | Small discovery test | Decision it informs |
|---|---|---|
| One lesson/quiz template fits higher education | Compare examples of a proof, interpretation/essay, numerical problem and practical task from available disciplines | Shared anatomy versus specialized practice components; boundaries of independent study |
| A tool's export is ready to publish | Render one representative artifact per family on a phone, keyboard-only, reduced-motion and with external requests disabled | Supported formats, adapters and fallbacks |
| Cross-course links are useful and correct | Inspect ambiguous Arabic/English terms and course-specific conventions with reviewers | Concept identity, alias rules and prerequisite equivalence |
| The destination fits pilot hosting assumptions | Synthetic catalog at roughly 325 courses with declared lesson/asset scenarios; measure build/update time, files, bytes and device loading | Deployment partitioning and media delivery; no performance claims before measurement |
| A correction stays local | Trace a shared concept correction through lessons, wiki, graph, exports and local progress | Course release boundaries, invalidation and learner notices |
| The current navigation matches how students look for help | Observe target learners choosing a course, finding a concept and recovering a prerequisite | Main entry point and search ranking |

These are proposed experiments, not completed evidence. Known source-rights, review, recovery and budget controls already have binding policies; their implementation is still required.

**Remaining implementation questions**

- Actual available archive quota; paid plans require a verified monthly total including fees/taxes within the $5/month ceiling.
- Named reviewers, operator/backup owner, and real discipline-specific task criteria before their release gates.
- Representative output sizes and catalog-scale build measurements before choosing full-catalog deployment/media layout.

These do not change the agreed learner promise. Framework selection and delivery capacity require the experiments above; no capacity or learning-quality claim is established by this planning document.
