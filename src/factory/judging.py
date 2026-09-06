"""CF-06: the judge harness — batched verdicts with a strict output contract.

Coverage judging runs in batches over stable per-node IDs, with whole-lesson
context in every call. The judge's output contract is deterministic: every
expected ID must come back exactly once with a valid verdict — a missing ID,
an unknown ID, unparseable output, or an invalid verdict value fails the whole
batch (never silently passes).

This is a dry harness using FakeJudge only. A live adapter with durable
reservations, output persistence, and usage reconciliation is not implemented.

Verdict cache keys follow the CF-05 identity rules: content hash + evidence
refs + lesson context + rubric version + prompt version + model + schema
version. Identical inputs reuse cached verdicts and never re-dispatch.
"""
import hashlib
import json

RUBRIC_VERSION = "1.0-draft"
PROMPT_VERSION = "1"
SCHEMA_VERSION = "1"
VALID_VERDICTS = {"pass", "fail"}


class JudgeContractError(ValueError):
    """The judge output violated the contract (missing/unknown ID, malformed
    payload, invalid verdict). The batch fails; nothing is silently accepted."""


class DispatchBlocked(RuntimeError):
    """A provider was passed to the dry-only harness."""


class FakeJudge:
    """Scripted dry-mode judge. `replies` maps item_id -> verdict; items
    without a scripted reply default to `default_verdict`."""

    model = "fake-judge-v0"

    def __init__(self, replies=None, default_verdict="pass", raw_response=None):
        self.replies = dict(replies or {})
        self.default_verdict = default_verdict
        self.raw_response = raw_response
        self.calls = 0

    def call(self, batch_items, lesson_context):
        self.calls += 1
        if self.raw_response is not None:
            return self.raw_response
        return {
            verdict_id: self.replies.get(verdict_id, self.default_verdict)
            for verdict_id, _kind, _refs in batch_items
        }


def batch_items_for_lesson(lesson_document, provenance):
    """One stable ID per teaching-bearing unit: every node, and every quiz's
    choices/answer/rationale as its own judged unit (rubric §coverage)."""
    items = []
    for node in lesson_document["nodes"]:
        evidence_refs = (provenance.get("nodes", {}).get(node["node_id"]) or {}).get("segments", [])
        items.append((node["node_id"], "node", evidence_refs))
    for quiz in lesson_document["quizzes"]:
        for part in ("choices", "answer", "rationale"):
            items.append((f"{quiz['quiz_id']}#{part}", f"quiz_{part}", []))
    return items


def verdict_cache_key(item_id, kind, evidence_refs, lesson_context, model="unset"):
    """Deterministic per the CF-05 key rules; a rubric/prompt/model change
    changes every key, an unchanged rerun changes nothing."""
    payload = json.dumps(
        {
            "item": item_id,
            "kind": kind,
            "evidence_refs": list(evidence_refs),
            "lesson_context_sha256": hashlib.sha256(lesson_context.encode("utf-8")).hexdigest(),
            "rubric_version": RUBRIC_VERSION,
            "prompt_version": PROMPT_VERSION,
            "schema_version": SCHEMA_VERSION,
            "model": model,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_judge_response(response, expected_ids):
    """Enforce the contract: JSON object; every expected ID exactly once;
    no unknown IDs; verdicts in the allowed set."""
    if not isinstance(response, dict):
        raise JudgeContractError("judge response must be a JSON object of id -> verdict")
    returned = set(response)
    missing = sorted(set(expected_ids) - returned)
    if missing:
        raise JudgeContractError(f"missing verdict IDs: {missing}")
    unknown = sorted(returned - set(expected_ids))
    if unknown:
        raise JudgeContractError(f"unknown verdict IDs: {unknown}")
    verdicts = {}
    for verdict_id, verdict in response.items():
        if verdict not in VALID_VERDICTS:
            raise JudgeContractError(f"invalid verdict for {verdict_id}: {verdict!r}")
        verdicts[verdict_id] = verdict
    return verdicts


def run_judging(lesson_document, provenance, judge, *, lesson_context, batch_size=8,
                cache=None):
    """Judge every teaching-bearing unit of one lesson in batches, with
    whole-lesson context per call. Fails on any contract violation; caches
    per the CF-05 key rules. Only the local scripted FakeJudge is supported."""
    if type(judge) is not FakeJudge:
        raise DispatchBlocked("dry-only harness: live judge integration is not implemented")
    items = batch_items_for_lesson(lesson_document, provenance)
    context_hash = hashlib.sha256(lesson_context.encode("utf-8")).hexdigest()
    verdicts = {}
    cache_hits = []
    pending = []
    for item in items:
        item_id, kind, evidence_refs = item
        key = verdict_cache_key(item_id, kind, evidence_refs, lesson_context, judge.model)
        if cache is not None and key in cache:
            verdicts[item_id] = cache[key]
            cache_hits.append(item_id)
        else:
            pending.append(item)
    for start in range(0, len(pending), batch_size):
        batch = pending[start:start + batch_size]
        response = judge.call(batch, lesson_context)
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as error:
                raise JudgeContractError(f"malformed judge output: {error}") from error
        verdicts.update(
            parse_judge_response(response, [item_id for item_id, _kind, _refs in batch])
        )
        if cache is not None:
            for item_id, kind, evidence_refs in batch:
                key = verdict_cache_key(item_id, kind, evidence_refs, lesson_context, judge.model)
                cache[key] = verdicts[item_id]
    return {
        "verdicts": verdicts,
        "cache_hits": cache_hits,
        "cache_keys": {
            item_id: verdict_cache_key(item_id, kind, evidence_refs, lesson_context, judge.model)
            for item_id, kind, evidence_refs in items
        },
        "model": judge.model,
        "lesson_context_sha256": context_hash,
        "rubric_version": RUBRIC_VERSION,
    }


def summarize_verdicts(report, known_bad_ids=(), known_good_ids=()):
    """Named denominators for the CF-09 report: nothing is reported as a
    bare ratio without the sets that define it."""
    verdicts = report["verdicts"]
    known_bad = set(known_bad_ids)
    known_good = set(known_good_ids)
    judged = set(verdicts)
    return {
        "judged_items": len(judged),
        "failed_items": sorted(item_id for item_id, verdict in verdicts.items() if verdict == "fail"),
        "bad_accepted": sorted(known_bad & judged & {i for i, v in verdicts.items() if v == "pass"}),
        "known_bad_total": len(known_bad),
        "good_rejected": sorted(known_good & judged & {i for i, v in verdicts.items() if v == "fail"}),
        "known_good_total": len(known_good),
        "cache_hits": len(report["cache_hits"]),
    }
