# PR #25 walkthrough diagrams — illustration artifacts, not authority

These images were posted in [PR #25](https://github.com/abodacs/IUG-CourseTranscripts/pull/25)
as a guided tour of the diff. They explain the change; they hold no authority.
[docs/README.md](../../README.md) and the documents it lists remain the only
sources of truth.

| File | What it is |
|---|---|
| `pr25-0{1..4}-*.png` | Hand-drawn concept diagrams (evidence law · outcome-matrix machine · provider valve · document map). |
| `pr25-ontology.tldraw` | Editable tldraw source for all four. Open in [tldraw offline](https://offline.tldraw.com/) or drag onto tldraw.com. |
| `root-architecture-*.svg`, `outcome-matrix-data-flow-*.svg` | pr-lens renders of the committed PR diff (light/dark; the data-flow SVG is animated). |

Regenerate the pr-lens renders from a checkout of this branch:

```bash
npx @coldtea/pr-lens-cli analyze --base origin/main --pr 25   # writes .pr-lens/graph.json (git-ignored)
npx @coldtea/pr-lens-cli render  .pr-lens/graph.json -o .pr-lens/
```
