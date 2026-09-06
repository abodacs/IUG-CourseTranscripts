# OKF v0.2 evaluation for the wiki layer (CF-05, bounded)

**Status:** DRAFT evaluation, 2026-09-06. Spec source: `GoogleCloudPlatform/knowledge-catalog`, `okf/SPEC.md` (v0.2), fetched 2026-09-06. This evaluation informs the CF-05 wiki/graph design; the adopt/adapt decision itself is ratified with the reviewer/operator at scope freeze — an evaluation is not an approval.

## What OKF v0.2 is

"An open, human- and agent-friendly format for representing knowledge": a directory of markdown files (concepts) with YAML frontmatter, distributed as a Knowledge Bundle. `type` is the only required key; links between concepts are plain markdown links whose *prose* conveys the relationship; provenance uses `sources[]` with keyed footnotes (`human:<id>` actor prefixes drive trust tiers: unverified → machine-confirmed → human-reviewed). Consumers MUST tolerate unknown types/fields.

## Fit against this project's wiki layer

| Need (plan/resolution) | OKF v0.2 answer | Verdict |
|---|---|---|
| Concept nodes as durable identities | One file per concept; identity = stable file path; `index.md`/`log.md` reserved for listing/history | **fits** |
| Human- and agent-writable | Markdown + YAML, git-diffable, no tooling required | **fits** |
| Provenance per claim | `sources[]` with keyed footnotes; `human:` actor convention matches our reviewer-trust tiers (F13) | **fits, adapt** — we require footnotes keyed to our segment refs, which OKF permits as content |
| Reviewer trust lifecycle | `generated`/`verified`/`status`/`stale_after` fields | **fits** |
| **Typed edges** (prerequisite / relates-to / mentions) | Links are untyped — kind lives in prose only | **gap** — we need machine-checkable typed edges (acyclicity, coverage) |
| **Arabic content / RTL** | UTF-8 only; no language tag, no direction, no translation-link convention | **gap** — needs producer extensions |
| Strict validation (reject undeclared) | OKF forbids rejecting unknown fields — deliberately permissive | **tension** — our validators are stricter by design |

## Recommendation (DRAFT — ratification open)

**Adapt, as an export/rendering layer — not as the source of truth.**

1. The machine-checkable knowledge layer stays our own `graph.json`: nodes with stable IDs, **typed** edges, and provenance refs that resolve against the CF-02A evidence index; prerequisite edges validated acyclic (validator ships with CF-05, see `src/factory/graph.py`).
2. The human-facing wiki is **rendered to OKF v0.2**: each graph node becomes a concept file; typed edges become both prose links and a declared frontmatter extension (`x-links:` with `type:` fields); provenance footnotes key to `sources[]` entries whose ids are our segment IDs; reviewer state maps to `human:<id>` actors and `verified`/`generated`.
3. Declared extensions for the Arabic gap: `x-language: ar`, `x-direction: rtl`, and `x-translation-of:` for cross-language concept linking — all conformant, since OKF consumers must tolerate unknown fields.
4. OKF's permissiveness stays at the export boundary: our build pipeline validates strictly *before* export; the OKF bundle never feeds back into authoring (legacy-prose rule, F04/F05).

## Bounded cost/decision note

No new dependency is introduced by the evaluation; the export path is a small deterministic renderer to be built with the wiki layer (CF-07 trial lesson first). If ratification rejects OKF, the fallback is plain HTML wiki pages from the same graph.json — no rework of the knowledge layer either way.
