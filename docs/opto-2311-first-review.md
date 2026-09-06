# OPTO 2311 — first review sheet (CF-02)

**Status:** DRAFT prepared by the agent on 2026-09-06. **Subject reviewer: OPEN — nothing here is approved.** This sheet is the reviewer's first-review input (30–45 min): work one worked example and one unseen task per lecture independently, before any judge exists. Candidate skills are drafts with recorded evidence spans; verdicts and corrections belong to the reviewer.

## Verified lecture order

Fetched with the pinned toolchain (`yt-dlp[default]==2026.8.19`, flat-playlist, metadata only) on 2026-09-06 → `artifacts/opto-2311/lecture-order.json` (local):

- **106 playlist entries ↔ 106 manifest videos; zero missing in either direction.** The local corpus and the live playlist correspond exactly.
- **`SAq013FtOLQ` sits at position 8 and was unavailable at fetch (title/duration NA)** — first real disposition evidence: it contributes no teaching content *now*; curriculum impact still needs the reviewer's judgment (CF-03).
- **One re-upload pair:** «التمرين الثالث بصريات هندسية» (114 s) exists twice — `3LETQng8kTU` and `E4SfMpVuLYk`. Recorded as one content family for CF-06.
- **Positions 105–106 are exam-logistics notices** («التنبيه… تعليمات بخصوص الامتحان النهائي»), not lectures; excluded from the teaching sequence with this recorded reason.
- Titles carry explicit sequence numbers (المحاضرة 1…28, التمرين 2…41) — ordering metadata only, never teaching facts.
- The order table with all 106 positions is in the artifact; every earlier "position unknown" from CF-01 is now resolvable from this evidence.

## Selected lectures (first / middle / final teaching content)

| Slot | Position | Video | Title | Length |
|---|---|---|---|---|
| First | 1 | `3U8quwM9QDg` | بصريات هندسية: المحاضرة 1 | 23:46 |
| Middle | 53 | `N-78zzBlTYU` | التمرين 20 — lens combination | 15:05 |
| Final | 104 | `hQH1Hf6_hEE` | التمرين 41 — spherocylindrical lenses | 06:00 |

## Candidate tangible skills (drafts — reviewer decides)

Evidence refs are `segment[i] @seconds` in the raw whisper JSON plus legacy chapter hints (hints are pointers, not facts).

### Lecture 1 — `3U8quwM9QDg` (foundations)

1. **Explain the chain جسم → نظام بصري → صورة and distinguish luminous vs reflecting bodies.** Evidence: ch1/ch3 hints; segments 0–63 (esp. seg[0] @2 s, seg[48] @1042 s). Classification: `supported`.
2. **Describe the pinhole experiment and predict the image's properties from the hole/screen geometry.** Evidence: ch2 hint; seg[16] @394 s, seg[32] @699 s (aluminum foil, candle, two-feet distance). Classification: `needs_youtube_diagram` — the live experiment frames (hint chosen @300 s, candidates 200/500 s) carry the visual; the transcript alone does not show what the setup looked like.
3. **Argue why the point-source approximation matters for studying optical systems.** Evidence: ch4 hint; seg[48] @1042 s through seg[63] @1406 s. Classification: `supported`.

- **Worked example for review:** walk through the pinhole image formation and state image orientation with reasoning.
- **Unseen transfer task:** predict what happens to the pinhole image when the hole is enlarged and when the screen is moved back, with justification.

### Lecture 53 — `N-78zzBlTYU` (lens combination, worked exercise)

1. **Compute the combined power/effective focal length and image position for two thin lenses in contact using 1/F = 1/u + 1/v with correct sign conventions.** Evidence: seg[8] @208 s (+7 D then +8 D, "in air"), ch1–ch2 hints. Classification: `supported`.
2. **Compute total lateral magnification for a lens system and interpret orientation and size.** Evidence: seg[33] @883 s (final image upright, 0.4× object height), ch3 hint. Classification: `supported`.
3. **Handle mixed units (cm ↔ m, diopter = m⁻¹) in a fresh problem.** Evidence: seg[17] @435 s (object at 25 cm from +8 D lens), seg[25] @647 s. Classification: `supported`.
- Diagram note: the ray-trace visual for the combination is board work — `needs_youtube_diagram` if the reviewer deems the ray diagram load-bearing. **Hint reliability warning:** the ch3 chosen keyframe @1400 s exceeds the video's 905 s duration — a concrete proof that hints require pixel verification before any capture.

- **Worked example for review:** reproduce the in-lecture +7/+8 D combination end to end.
- **Unseen transfer task:** lenses +5 D and −2 D in contact, object at 40 cm — find final image position, magnification, orientation.

### Lecture 104 — `hQH1Hf6_hEE` (spherocylindrical derivation, worked exercise)

1. **Construct a power cross for the cornea/lens and read off meridian powers.** Evidence: seg[7] @160 s, seg[11] @266 s; ch2 hint. Classification: `needs_youtube_diagram` — the power-cross drawing is the teaching visual (hint @146 s, candidates 146/336 s).
2. **Derive the spherical + cylindrical correction (with axis) that normalizes a given corneal refractive error.** Evidence: seg[3] @77 s, seg[14] @348 s (41 + 3 = 44; 44 − 1 = 43 result). Classification: `supported` once the power-cross visual is recovered; without it `unsupported` for the derivation step.

- **Worked example for review:** reproduce the in-lecture derivation.
- **Unseen transfer task:** a cornea measuring 42 D horizontally / 45 D vertically — derive the correcting spherical-cylindrical lens and state the axis.

## Evaluation-family reservation (F03) — recorded before deeper discovery

`artifacts/opto-2311/evaluation-families.json` (local): **5 development families** already exposed (the three lectures above; `0Ca8cjsIysc` — CF-01 probe excerpts; `-AsaJEAav4s` — historical capture inspection), **100 candidate families** covering the remaining 101 videos (the re-upload pair counts as one family), sibling optics playlists on the watchlist. Access rule: semantic exposure before threshold freeze makes a family development data; structural/manifest access does not. Holdout selection is deferred to CF-03/CF-06 with frozen prompts/rubric/thresholds; if eligible families run short, the evaluation design must be resolved — never relabel exposed families as unseen.

## What the reviewer must decide (first review)

1. Work each lecture's worked example and unseen task independently; note prerequisite gaps observed while working (feeds the learner-assumption record).
2. Confirm or correct each candidate skill's classification, especially the `needs_youtube_diagram` calls and whether ray diagrams / power crosses are load-bearing.
3. Judge whether position 8's missing lecture (`SAq013FtOLQ`, unavailable at fetch) leaves any promised outcome unsupported (with CF-03).
4. Approve the teaching sequence derived from the verified order, or flag unknowns.

**Reviewer: OPEN.** Until the first review is recorded, scope freeze (CF-03) and all downstream gates stay blocked.
