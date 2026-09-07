# Artifact storage and review — bounded-cost plan

2026-09-07 · Recommendation, not a deployed service. Operator-confirmed maximum: $5/month total for artifact hosting/operations. Existing zIDE model quota remains separate. No files uploaded or subscriptions purchased.

**Recommend:** local factory workspace + fixed-quota private Drive archive + Cloudflare Pages public site and protected reviewer previews. GitHub stores code, schemas, synthetic fixtures and public documentation. JSON format is fine in artifact storage; production artifacts do not belong in this Git repository.

| Data | Working copy | Durable copy / access |
|---|---|---|
| Raw/cleaned local corpus, source excerpts, evidence images, credentials | Existing local private roots | Independent operator-controlled offline backup; existing no-corpus-upload rule remains |
| Intermediate generated drafts and resumable checkpoints | Ignored `artifacts/` tree | Permitted generated-only checkpoints archived privately; exclude copied corpus evidence and secrets |
| Review candidate | Immutable candidate directory | Private archive + protected rendered preview; only named reviewers |
| Findings and approvals | Private append-only records | Back up with candidate IDs/hashes; reviewer identity, role, decision and time |
| Accepted final artifacts | Versioned accepted bundle | Private archive retains editable/generated source and manifests; public allowlist alone goes to Pages |
| Public site | Generated HTML/CSS/JS and approved media | Pages Direct Upload; no GitHub corpus upload needed |

Suggested local layout: `artifacts/factory/<course-id>/runs/<run-id>/`, `candidates/<candidate-id>/`, `releases/<release-id>/`; keep a single local SQLite catalog for state and artifact pointers. Snapshot SQLite consistently before backup. Upload completed bundles, never a live database or an actively written folder.

Each bundle has a manifest: stable course/lesson IDs, schema version, input hashes, stage/tool version, file sizes/checksums and predecessor. Hash the final rendered output too. Never overwrite a reviewed candidate; create a new revision. Stage archives can contain many JSON files without forcing them into Git. Per-lesson/stage archives avoid reuploading the whole course for a small change.

**Review flow**

`draft → automated checks → frozen candidate → subject/editorial review → fixes/new candidate → operator approval → publish exact approved bytes`

1. Reviewers see the actual lesson/quiz/media rendering, candidate ID and a short findings form keyed to lesson/node IDs. Raw evidence needed for source review stays in the operator-controlled local review environment under the existing corpus policy.
2. Reviewer responses contain candidate hash, reviewer identity/role, findings and approve/changes-required decision. A read-only shared sheet or returned review form is enough initially; no review-dashboard application is needed. Archive each submitted response as a private record.
3. Required independent subject/editorial judgments remain distinct from operator publication approval. Any relevant change invalidates affected approval; stale approvals cannot clear a new candidate. All existing curriculum, learner-trial, rights and quality gates still apply.
4. Protect reviewer URLs before uploading real candidates. Pages previews are public by default; its Access preview setting does not protect the production hostname or custom domains. Test every candidate route/asset unauthenticated. Use a dedicated review project with a harmless production page and protected preview deployments. [Preview behavior](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
5. Named reviewers may use email one-time PIN access. This does not introduce learner accounts. Check current Free plan seat allowance before invitation. [OTP](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/), [plans](https://www.cloudflare.com/plans/)

**Cost choice**

| Component | Start | Growth condition |
|---|---|---|
| Private artifact archive | Existing free Drive quota: up to 15 GB shared with Gmail/Photos | Fixed-capacity Google One only after confirming local recurring charge, taxes and other hosting charges total at most $5 |
| Public site and review previews | Pages Free; local build/Direct Upload | Verify file count, largest asset and Access quota before release; no automatic paid upgrade |
| Independent corpus backup | Existing separate operator-controlled storage | Availability/capacity must be confirmed; a second folder on the same disk is not an independent backup |
| SEO tools | Search Console and Bing Webmaster Tools | No paid SEO/citation monitoring subscription |

[Google storage policy](https://support.google.com/drive/answer/6374270/manage-files-in-your-google-drive-storage?hl=en-GB) states uploads stop at quota. Preserve headroom because Gmail also shares the limit. The public [Google One price page](https://one.google.com/about/plans) displays 100 GB at $1.99/month; this is not a verified Egypt checkout price or final tax-inclusive bill. Do not purchase until the actual total meets the ceiling. Drive is an archive, not the public website/media server.

**R2 is not the hard-cap recommendation.** It has metered storage/operations; [budget alerts](https://developers.cloudflare.com/billing/manage/budget-alerts/) explicitly do not pause or cap usage. [R2 prices](https://developers.cloudflare.com/r2/pricing/) can yield low expected costs, but this review found no enforceable $5 account ceiling. An alert or script that reacts later cannot establish the requested maximum.

**Measured now:** read-only logical-byte scan on 2026-09-07 found `artifacts/` at about 6 MB/89 files, `data/` 5.510 GB, and `GeminiLongContext/` 1.738 GB. These are local working sizes, not accepted-course sizes or permission to upload the corpus. The final 325-course footprint is unknown. Available Drive quota and independent-backup capacity were not inspected.

**Retention proposal:** keep resumable active checkpoints; keep latest and previous failed attempts briefly for diagnosis; remove only confirmed disposable caches after a retention decision. Retain accepted editable content, review/provenance records, current eligible releases and recovery history according to an explicit operator policy. Preserve unknown attempts and unresolved incidents. Deduplicate unchanged assets; never delete required evidence merely to fit quota. When capacity is exhausted, retain local work and stop new archive/publish jobs rather than enable metered overages. This stop policy is recommended, not yet confirmed.

**Scale qualification:** [Pages Free](https://developers.cloudflare.com/pages/platform/limits/) supports 20,000 files/site and 25 MiB/asset. A 100 GB archive does not give Pages 100 GB of usable media delivery. Measure realistic final bundles, search/graph assets, history and video first. If a single deployment fails the limit, design a bounded multi-site/media layout with stable canonical URLs and recheck total costs; no promise that all 325 courses fit one project. Keep full-catalog SEO requirements intact.

**Before release:** prove archive restore, checksum verification, reviewer isolation, stale-approval rejection, public/private allowlists, exact preview/live bytes, rollback and withdrawal of old preview/public URLs. Search indexing is separate from privacy: `noindex` is not access control. Full private evidence restore uses the independent local corpus backup plus the generated-artifact archive.

Open setup inputs: available fixed quota and backup device; reviewer emails/roles; chosen public hostname; actual output/media sizes. These are setup facts to resolve before provisioning, not reasons to reopen the north star.
