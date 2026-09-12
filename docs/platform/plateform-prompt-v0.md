You are an expert UI/UX designer specializing in clean, low-to-mid fidelity wireframes and large educational platforms.

  Design the complete learner-facing v0 of an Arabic-first university course platform. The platform must support approximately 325 higher-education courses and thousands of lessons across faculties, subjects, and academic levels.

  This is a platform-level design—not a wireframe for one pilot course.

  ## SOURCE MATERIAL

  Before designing:

  1. Inspect `@docs/inspiring/` for visual and interaction inspiration.
  2. Inspect `@docs/wireframes/` and reuse its course-specific wireframes as the v0 baseline.
  3. Follow the platform requirements in:
     - `@docs/platform/platform-north-star.md`
     - `@docs/platform/platform-map-brief.md`
     - `@docs/platform/course-app-plan.md`

  Use `@docs/inspiring/` to study:

  - Information hierarchy
  - Course overview composition
  - Long curriculum organization
  - Course-card consistency
  - Roadmap presentation
  - Search placement
  - Use of whitespace and content density

  Do not copy Fanout’s branding, colors, pricing, accounts, community features, or server-backed functionality.

  The pilot wireframes do not define the full platform scope, but their course-specific screens must be reused
  rather than redesigned. Build the missing platform-level experience around them.

  ## PRODUCT PURPOSE

  Help Arabic-speaking university learners discover, understand, and independently apply their subjects through:

  - Structured courses
  - Skill-based lessons
  - Clear explanations
  - Worked examples
  - Diagrams and media
  - Inline practice
  - Formative assessments
  - Bilingual concept context and relationships inside lessons

  Learners must not need an account.

  ## PLATFORM SCALE

  Design for:

  - Approximately 325 courses
  - Thousands of lessons
  - Multiple faculties
  - Multiple academic levels
  - Arabic and English terminology
  - Cross-course prerequisites
  - Cross-course concepts and aliases
  - Gradual publication of reviewed courses

  Do not render all courses or lessons simultaneously. Demonstrate scalable navigation through search, filters, categories, pagination, collapsible units, and progressive disclosure.

  Do not imply that all 325 courses are already reviewed or published.

  ## V0 TECHNICAL BOUNDARY

  Learner-platform v0 is a static website with browser-side enhancement only.

  It provides no server-side application functions.

  Do not design or assume:

  - An application server
  - A runtime database
  - Custom server APIs
  - Authentication
  - Learner accounts
  - Server-synced progress
  - Server-processed forms
  - Cloud grading
  - Runtime model calls
  - Payments
  - Certificates
  - Community features
  - Social features
  - A custom CMS

  Allowed browser-side behavior:

  - Static page navigation
  - Client-side search over a build-generated index
  - Client-side catalog filters
  - Local progress stored in the browser
  - Local quiz and practice state
  - Collapsible navigation
  - Accessible drawers and dialogs

  Search data, course manifests, lesson navigation, and knowledge-graph-ready concept data are generated at build time.

  If browser storage is unavailable, reading must continue to work.

  Problem reporting must use a static link to an explicitly configured external channel, such as email. Do not create a server-submitted report form.

  ## PLATFORM

  - Responsive public website
  - Mobile-first
  - Arabic-first
  - RTL by default
  - Strong mixed-direction support
  - Static-first
  - Low-bandwidth friendly
  - Accessible without JavaScript for core reading
  - Stable public URLs
  - No login required

  ## STRICT WIREFRAME STYLE

  These rules are mandatory:

  - Black outlines and black text only
  - White backgrounds
  - Very light gray fills only when required for state distinction
  - No accent colors
  - No shadows
  - No gradients
  - No textures
  - No decorative effects
  - No production branding
  - No polished illustrations
  - Square corners or minimal 2–4px radius
  - Simple system typography
  - Consistent spacing and border weights
  - Crossed boxes for image, diagram, and video placeholders
  - Dashed borders for unavailable, empty, withdrawn, or placeholder content
  - Double outlines for keyboard focus
  - Use layout, spacing, labels, and type size to express hierarchy
  - Keep everything unmistakably low-to-mid fidelity

  Do not reproduce the colors or decorative styling found in the inspiration screenshots.

  ## GLOBAL INFORMATION ARCHITECTURE

  Create a scalable information architecture with these primary destinations:

  - `الرئيسية`
  - `المساقات`
  - `البحث`

  Persistent utilities:

  - Global search
  - Continue learning
  - Course-aware search
  - Local-progress status
  - Mobile navigation menu

  Do not place hundreds of links in the global navigation.

  ## REQUIRED PLATFORM-LEVEL SCREENS

  ### 1. Platform Home — الصفحة الرئيسية

  Include:

  - Concise platform purpose
  - Global search
  - Continue-learning section when local history exists
  - Browse by faculty
  - Browse by subject
  - Recently released courses
  - Foundational courses
  - No-account-required message
  - Local-progress explanation

  Avoid a generic promotional landing page.

  ### 2. Course Catalog — دليل المساقات

  Design a catalog capable of supporting approximately 325 courses.

  Include:

  - Search input
  - Results count
  - Faculty filter
  - Subject filter
  - Academic-level filter
  - Language filter
  - Availability filter
  - Sort control
  - Active filters
  - Clear-filters action
  - Reusable course cards
  - Pagination or progressive loading
  - Loading state
  - No-results state

  Course cards should show:

  - Course code
  - Arabic title
  - English equivalent where available
  - Faculty and subject
  - Academic level
  - Availability
  - Prerequisites summary
  - Local progress when present

  Show released courses as available. Clearly label unreleased or planned content without manufacturing
  course pages.

  ### 3. Faculty Page — صفحة الكلية

  Include:

  - Faculty name
  - Short description
  - Subject groups
  - Available courses
  - Suggested starting points
  - Course levels
  - Search within the faculty
  - Partially populated state

  ### 4. Subject Page — صفحة الموضوع

  Include:

  - Subject title
  - Subject description
  - Related faculties
  - Foundational courses
  - Advanced courses
  - Suggested learning order
  - Important lesson topics
  - Related lessons
  - Course availability

  ### 5. Global Search — البحث

  Search across:

  - Courses
  - Lessons
  - Subjects
  - Arabic terms
  - English terms
  - Alternative spellings and aliases

  Include:

  - Search input
  - Search scope
  - Filters
  - Grouped result types
  - Result type label
  - Result location and context
  - Matching term
  - Current-course priority where relevant
  - Suggested broader search
  - No-results state

  Clearly distinguish courses, lessons, and subjects. Concept names and aliases may match lesson results,
  but v0 does not expose concepts as a separate result type or destination.

  Search runs locally against a build-generated static index.

  ## REUSED COURSE-SPECIFIC WIREFRAMES

  Reuse these existing structures from `@docs/wireframes/` inside the final review canvas; do not invent
  replacement layouts:

  - `01-course-home.html` — course home
  - `05-roadmap.html` — course roadmap
  - `02-lesson-reader-desktop.html` — desktop lesson reader
  - `09-lesson-reader-mobile.html` — mobile lesson reader
  - `03-quiz-states.html` — embedded practice states

  Adapt only what is necessary to connect them to the v0 global navigation, the static data model, and the
  scope changes in this prompt. Remove or replace any link to a standalone concept graph with an in-lesson
  concept section or lesson anchor. Do not reuse `06-knowledge-graph.html`; v0 remains knowledge-graph ready
  in its data, without a graph interface.

  The requirements below are compatibility checks for the reused screens, not requests to redesign them.

  ### 6. Course Home — صفحة المساق

  Include:

  - Course code
  - Arabic title
  - English equivalent
  - Faculty
  - Academic level
  - Publication status
  - Course description
  - Skill-based learning outcomes
  - Required prior knowledge
  - Scope and limitations
  - Ordered units
  - Ordered lessons
  - Stage deliverables
  - Estimated effort where available
  - Start or Continue action
  - Local progress
  - Outline view
  - Roadmap view
  - Key concepts linked to their relevant lessons
  - Review and source information
  - Static problem-report link

  The outline and roadmap must represent the same canonical lesson order.

  ### 7. Course Roadmap — خارطة المساق

  Include:

  - Ordered learning stages
  - Prerequisite relationships
  - Completed stage
  - Current stage
  - Upcoming stage
  - Named deliverable for every stage
  - Links to relevant lessons
  - Prerequisite concept labels linked to their relevant lessons
  - Accessible linear-list alternative

  Use the roadmap patterns in `@docs/inspiring/` as inspiration, but rebuild them for Arabic RTL use.

  ### 8. Lesson Reader: Desktop — قارئ الدرس

  Include:

  - Breadcrumbs
  - Course outline on the right
  - Central reading column
  - Optional section navigation
  - Lesson title
  - Skill outcome
  - Prerequisites
  - Estimated duration
  - Source and review information
  - Explanation sections
  - “Aha moment”
  - Worked example
  - Math, code, or table content
  - Diagram or media
  - Arabic accessible description
  - Simplified explanation
  - Embedded practice
  - Embedded assessment
  - Transfer task
  - Concept definitions and related-concept links within the lesson
  - Previous lesson
  - Next lesson
  - Mark-complete action
  - Static problem-report link

  ### 9. Lesson Reader: Mobile — قارئ الدرس على الجوال

  Include:

  - Single reading column
  - Collapsible course-outline drawer
  - Collapsible section-navigation drawer
  - Large touch targets
  - Correct RTL navigation
  - Correct Arabic and English wrapping
  - Correct math and code direction
  - No horizontal clipping
  - Low-bandwidth media alternative
  - Previous and next lesson actions
  - Embedded practice and feedback
  - Local progress

  The desktop and mobile readers are two responsive versions of the same lesson route.

  ## EMBEDDED PRACTICE AND ASSESSMENT

  Practice and assessment are built directly into the lesson reader.

  They are not standalone pages, routes, or primary navigation destinations.

  Place them at pedagogically appropriate points within the lesson.

  Support representative forms:

  - Multiple choice
  - Numeric response
  - Short written response
  - Self-check rubric
  - Open practical task

  Show embedded states:

  - Unanswered
  - Answer selected
  - Submitted
  - Correct
  - Incorrect
  - Partially complete
  - Retry available
  - Disabled
  - Feedback displayed
  - Rationale displayed
  - Model response or self-check rubric

  Rules:

  - Never reveal an answer before the learner attempts the task.
  - Show useful feedback beside the question.
  - Keep attempts and results in the browser.
  - Do not submit answers to a server.
  - Do not design a quiz dashboard.
  - Do not design a grading API.
  - Do not claim mastery from one answer.
  - Do not force every discipline into multiple-choice questions.

  A separate component-state board may be included for design review, but it must be labeled:

  `Component reference only — embedded inside the lesson, not a standalone product screen.`

  ## KNOWLEDGE-GRAPH READINESS — NO STANDALONE V0 GRAPH UI

  Concepts appear only in lesson content in v0. Do not create a concept/wiki route, concept explorer,
  concept directory, concept card, or top-level concept navigation.

  Keep the build-generated content model ready for a later knowledge graph. Each concept occurrence must support:

  - Stable concept ID
  - Arabic preferred label
  - English equivalent where available
  - Alternative spellings and aliases
  - Context-specific definition
  - Source lesson and section anchor
  - Prerequisite and related concept IDs
  - Typed, directed relationships
  - Related course and lesson IDs
  - Source and review metadata

  In v0, render only the relevant definition and a compact, accessible list of related concepts inside the
  lesson. Links must resolve to lesson anchors, not standalone concept pages. Search may use concept labels and
  aliases to find lessons without exposing concepts as a separate result type. Do not design graph controls.

  ### 10. Continue Learning — تابع التعلّم

  This is a lightweight local component or home-page section, not an account dashboard.

  Include:

  - Recently opened course
  - Last lesson
  - Last reading position
  - Read state
  - Attempted state
  - Self-reported completion
  - Continue action
  - Reset-progress action
  - Local-storage explanation
  - Storage-unavailable warning
  - Revised-lesson state
  - Withdrawn-lesson state

  ### 11. Essential System States

  Show representative states for:

  - First visit
  - No local history
  - Empty catalog category
  - No search results
  - Loading
  - Slow connection
  - Media unavailable
  - Browser storage unavailable
  - Lesson revised
  - Lesson withdrawn
  - Course under review
  - Course unavailable
  - Broken link
  - 404 page
  - General error

  Reading must remain available when optional browser functionality fails.

  ## SAMPLE CONTENT

  Use the optics pilot as one realistic example—not as the whole platform:

  - Course code: `OPTO 2311`
  - Arabic title: `البصريات الهندسية`
  - English title: `Geometric Optics`
  - Faculty: `كلية العلوم الصحية`
  - Example concept: `قانون الانعكاس`
  - Alias: `Law of Reflection`
  - Equation: `θᵢ = θᵣ`
  - Equation: `n₁ sin θ₁ = n₂ sin θ₂`

  Also include a small set of clearly marked synthetic examples to prove that the platform supports different
  disciplines:

  - Mathematics
  - Programming
  - Engineering
  - Health sciences
  - Humanities

  Label synthetic content:

  `[بيانات توضيحية]`

  Do not imply that synthetic or planned courses are reviewed and published.

  ## SHARED ARABIC LABELS

  Use these labels where appropriate:

  - `ابدأ التعلّم`
  - `تابع التعلّم`
  - `استعرض المساقات`
  - `ابحث في المنصة`
  - `صفِّ النتائج`
  - `امسح الفلاتر`
  - `المتطلبات السابقة`
  - `نواتج التعلّم`
  - `خطة المساق`
  - `خارطة المساق`
  - `المهارة`
  - `لحظة الفهم`
  - `مثال محلول`
  - `تدريب`
  - `اختبر نفسك`
  - `تحقق من الإجابة`
  - `حاول مرة أخرى`
  - `مهمة نقل`
  - `الدرس السابق`
  - `الدرس التالي`
  - `اشرح أبسط`
  - `الإبلاغ عن مشكلة`

  Local-progress notice:

  `يُحفظ تقدّمك في هذا المتصفح فقط. لا تحتاج إلى إنشاء حساب، وقد تفقد تقدّمك عند حذف بيانات المتصفح.`

  ## PRIMARY USER FLOWS

  ### Flow A: Browse by faculty and subject

  Home → Faculty → Subject → Course → Lesson → Embedded Practice → Feedback → Next Lesson

  ### Flow B: Search for a topic or concept term

  Search → Matching Lesson → Concept Section → Prerequisite Lesson Anchor → Return

  ### Flow C: Returning learner

  Home → Continue Learning → Previous Reading Position → Embedded Practice → Next Lesson

  ### Flow D: Follow related knowledge

  Lesson → Related Concept Link → Relevant Lesson Anchor → Return

  ### Flow E: Report a problem

  Lesson → Static External Reporting Link

  Show the flows using simple numbered arrows.

  ## RESPONSIVE REQUIREMENTS

  Provide new desktop and mobile frames for the platform-level screens, and include the reused course-specific
  frames listed above:

  - Home
  - Catalog
  - Search
  - Course home
  - Lesson reader

  Demonstrate:

  - 360px mobile viewport
  - RTL navigation
  - Collapsible filters
  - Collapsible course outline
  - Large touch targets
  - Mixed-direction content
  - Math and code without clipping
  - Behavior at 200% zoom

  ## ACCESSIBILITY

  - Apply `dir="rtl"` to Arabic pages.
  - Isolate English, code, and equations correctly.
  - Never mirror mathematical notation.
  - Use visible form labels.
  - Show keyboard-focus states.
  - Provide Arabic alternative text for diagrams and media.
  - Do not use color as the only state indicator.
  - Keep core reading usable without JavaScript.
  - Provide text alternatives for interactive media.
  - Nothing may require animation.
  - Avoid horizontal page scrolling at mobile width or 200% zoom.

  ## OUTPUT FORMAT

  Create one self-contained HTML document with embedded basic CSS.

  The document must include:

  1. Platform sitemap
  2. Global navigation model
  3. Reusable component inventory
  4. Primary user-flow map
  5. Desktop wireframes
  6. Mobile wireframes
  7. Embedded practice states
  8. Empty, error, loading, and unavailable states
  9. Scalability annotations

  Implementation restrictions:

  - Semantic HTML where practical
  - Basic CSS only
  - No UI frameworks
  - No external fonts
  - No external images
  - No external assets
  - No server code
  - No API calls
  - No database
  - No authentication
  - No server-submitted forms
  - No animation
  - No production visual styling

  Display all wireframes on one review canvas and clearly label every frame.

  ## FINAL VALIDATION

  Before returning the result, verify that:

  - The design covers the complete platform, not only OPTO 2311.
  - The catalog structure can support approximately 325 courses.
  - Thousands of lessons do not appear in one flat navigation structure.
  - Courses, subjects, and lessons are discoverable; concept labels and aliases lead to lesson results.
  - Concepts appear only inside lessons; there are no standalone concept pages or graph controls.
  - Build-generated concept records include stable IDs, aliases, typed relationships, and lesson anchors for a future knowledge graph.
  - Practice and assessment are embedded inside lesson pages.
  - There is no standalone quiz destination.
  - No server-side functionality was introduced.
  - Search, filtering, and progress interactions are browser-side.
  - Course-specific layouts reuse the named pilot wireframes rather than replacing them.
  - Learners never encounter a login prompt.
  - Optics is used only as a sample course.
  - Unreleased content is not represented as accepted.
  - Inspiration was adapted rather than copied.
  - Every screen remains a strict monochrome wireframe.
