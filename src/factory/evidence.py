"""CF-02A: the evidence boundary for v1 authoring.

Decision recorded 2026-09-06: v1 authors from raw whisper JSON only, because
CF-01 measured real damage in derived SRT variants (zero-duration cues,
malformed blocks, truncation) and the legacy outputs were unvalidated.
Decision reversed 2026-09-07 (operator): the cleaned per-video counterparts
in the mirrored ``GeminiLongContext/<playlist_id>/`` tree —
``_chapters.json``, ``_v2_content.json`` (earlier variant ``_content.json``),
and ``_lecture_context.json`` — are allowed teaching sources alongside the
raw JSON. Raw whisper JSON remains the canonical segmentation: segment IDs,
timestamps, and segment hashes bind to it, while cleaned sources attach per
video. Derived SRT variants stay ineligible; the damage measurements stand.

``eligibility_of`` therefore distinguishes ``teaching_eligible`` (raw JSON,
the only segment source) from ``teaching_eligible_cleaned`` (cleaned
counterparts, video-level sources that are never segment loads).

This module never imports the model/network pipeline and performs no I/O
beyond the files it is given.
"""
from pathlib import Path
import dataclasses
import datetime
import hashlib
import json
import re

PLAYLIST_ID = "PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-"
VIDEO_ID = "0Ca8cjsIysc"
RAW_SUFFIX = "_raw.json"
CLEANED_SUFFIXES = (
    "_chapters.json",
    "_v2_content.json",
    "_lecture_context.json",
    "_content.json",
)
VIDEO_ID_RE = re.compile(r"[A-Za-z0-9_-]{11}")


class EvidencePolicyError(RuntimeError):
    """A requested action violates the evidence policy (ineligible input,
    missing attribution, append-only violation, missing reviewer)."""


class EvidenceIntegrityError(RuntimeError):
    """Recorded evidence does not match reality (hash mismatch, unknown
    reference, mutated capture bytes)."""


def eligibility_of(path_text):
    """Raw whisper JSON is the segment source; cleaned GeminiLongContext
    counterparts are video-level teaching sources; derived SRT variants are
    not evidence at all."""
    name = Path(path_text).name
    if name.endswith(RAW_SUFFIX) and VIDEO_ID_RE.fullmatch(name[: -len(RAW_SUFFIX)]):
        return "teaching_eligible"
    for suffix in CLEANED_SUFFIXES:
        if name.endswith(suffix) and VIDEO_ID_RE.fullmatch(name[: -len(suffix)]):
            return "teaching_eligible_cleaned"
    return "not_eligible"


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _text_sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclasses.dataclass(frozen=True)
class SegmentRef:
    video_id: str
    index: int
    start: float
    end: float
    segment_id: str


@dataclasses.dataclass(frozen=True)
class RawSegment:
    ref: SegmentRef
    text: str
    text_sha256: str


def load_segments_from(path):
    """Load segments from an explicit file, enforcing the eligibility gate."""
    kind = eligibility_of(path)
    if kind == "teaching_eligible_cleaned":
        raise EvidencePolicyError(
            f"{path} is a cleaned source: it binds per video and is never a raw segment load"
        )
    if kind != "teaching_eligible":
        raise EvidencePolicyError(
            f"{path} is not eligible teaching evidence; author from {RAW_SUFFIX} and the "
            "cleaned GeminiLongContext counterparts only"
        )
    path = Path(path)
    video_id = path.name[: -len(RAW_SUFFIX)]
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _segments_from_payload(payload, video_id)


def load_raw_video(root, playlist_id, video_id):
    path = Path(root) / "data" / playlist_id / f"{video_id}{RAW_SUFFIX}"
    if not path.exists():
        raise FileNotFoundError(f"no raw transcript for {video_id}: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _segments_from_payload(payload, video_id)


def _segments_from_payload(payload, video_id):
    segments = payload.get("segments")
    if not isinstance(segments, list) or not segments:
        raise EvidenceIntegrityError(f"{video_id}: raw JSON has no usable segments[]")
    loaded = []
    for index, segment in enumerate(segments):
        start = float(segment["start"])
        end = float(segment["end"])
        text = segment["text"]
        if not isinstance(text, str) or end <= start or start < 0:
            raise EvidenceIntegrityError(f"{video_id} segments[{index}]: unusable raw unit")
        loaded.append(
            RawSegment(
                ref=SegmentRef(
                    video_id=video_id,
                    index=index,
                    start=start,
                    end=end,
                    segment_id=f"{video_id}:seg:{index:04d}",
                ),
                text=text,
                text_sha256=_text_sha256(text),
            )
        )
    return loaded


def verify_segment(segment, text):
    """A same-length altered equation changes the hash exactly like a rewrite."""
    if _text_sha256(text) != segment.text_sha256:
        raise EvidenceIntegrityError(
            f"hash mismatch for {segment.ref.segment_id}: text is not the recorded raw evidence"
        )
    return True


class AppendOnlyJsonLog:
    """Shared shape for append-only record stores: records are never edited,
    dispositions are appended, state is derived by folding."""

    PREFIX = "r"

    def __init__(self, path):
        self.path = Path(path)
        self.records = []
        if self.path.exists():
            self.records = json.loads(self.path.read_text(encoding="utf-8"))["records"]

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"records": self.records}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _next_id(self):
        return f"{self.PREFIX}-{len(self.records) + 1:04d}"


@dataclasses.dataclass(frozen=True)
class Correction:
    video_id: str
    segment_id: str
    original_excerpt: str
    corrected_text: str
    evidence_span: str
    derivation: str
    affected_artifacts: tuple = ()
    uncertain_note: str = ""

    @classmethod
    def new(cls, video_id, segment_id, corrected_text, evidence_span, derivation,
            original_excerpt="", affected_artifacts=None, uncertain_note=""):
        if not evidence_span:
            raise EvidencePolicyError("a correction needs recorded evidence for the change")
        if not derivation:
            raise EvidencePolicyError("a correction needs a source-based derivation, not taste")
        if not isinstance(original_excerpt, str) or not original_excerpt.strip():
            raise EvidencePolicyError("a correction needs a non-empty original excerpt")
        if affected_artifacts is not None and not all(isinstance(a, str) and a for a in affected_artifacts):
            raise EvidencePolicyError("affected artifact IDs must be non-empty strings")
        return cls(
            video_id, segment_id, original_excerpt, corrected_text, evidence_span, derivation,
            tuple(affected_artifacts or ()), uncertain_note,
        )


class CorrectionLedger(AppendOnlyJsonLog):
    """Append-only records: `correction` entries never change; dispositions
    are appended as new records and folded to derive current state."""

    PREFIX = "c"

    def propose(self, video_id, segment_id, original_excerpt, corrected_text, evidence_span,
                derivation, affected_artifacts=None, uncertain_note=""):
        correction = Correction.new(
            video_id, segment_id, corrected_text, evidence_span, derivation, original_excerpt,
            affected_artifacts, uncertain_note,
        )
        record = {
            "kind": "correction",
            "correction_id": self._next_id(),
            "disposition": "proposed",
            "created_at": _now(),
            **dataclasses.asdict(correction),
        }
        record["affected_artifacts"] = list(record["affected_artifacts"])
        self.records.append(record)
        self._save()
        return record

    def rewrite(self, correction_id, changes):
        raise EvidencePolicyError("the correction ledger is append-only; write a new record instead")

    def record_disposition(self, correction_id, reviewer, decision):
        if not reviewer:
            raise EvidencePolicyError("a disposition needs a named reviewer; agents cannot approve")
        self.records.append(
            {
                "kind": "disposition",
                "correction_id": correction_id,
                "reviewer": reviewer,
                "decision": decision,
                "recorded_at": _now(),
            }
        )
        self._save()

    def state(self):
        corrections = {r["correction_id"]: dict(r) for r in self.records if r["kind"] == "correction"}
        for record in self.records:
            if record["kind"] == "disposition" and record["correction_id"] in corrections:
                corrections[record["correction_id"]]["disposition"] = record["decision"]
        return corrections

    def approved_ids(self):
        return {
            cid for cid, record in self.state().items() if record["disposition"] == "approved"
        }


@dataclasses.dataclass
class CorrectionOutcome:
    applied: list
    quarantined: list
    texts: list


def apply_corrections(segments, ledger):
    """Approved corrections are applied to excerpt level; anything else
    quarantines its outcome instead of silently changing teaching text."""
    by_segment = {segment.ref.segment_id: segment for segment in segments}
    applied, quarantined = [], []
    edits = {segment.ref.segment_id: segment.text for segment in segments}
    for cid, record in sorted(ledger.state().items()):
        target = record["segment_id"]
        if record["disposition"] != "approved":
            quarantined.append(cid)
            continue
        if target not in by_segment:
            quarantined.append(cid)
            continue
        text = edits[target]
        if not isinstance(record["original_excerpt"], str) or not record["original_excerpt"].strip():
            raise EvidenceIntegrityError(f"{cid}: recorded original excerpt is empty")
        if record["original_excerpt"] not in text:
            raise EvidenceIntegrityError(
                f"{cid}: recorded excerpt is no longer present in {target}; evidence drifted"
            )
        edits[target] = text.replace(record["original_excerpt"], record["corrected_text"])
        applied.append(cid)
    return CorrectionOutcome(applied=applied, quarantined=quarantined, texts=[edits[s.ref.segment_id] for s in segments])


@dataclasses.dataclass
class CoverageResult:
    covered: set
    uncovered: list
    total_references: int


def validate_coverage(segments, references):
    """Coverage is proven through references that resolve — never through
    equal counts. Every reference must name a real segment; segments no
    reference covers are reported as uncovered."""
    known = {segment.ref.segment_id for segment in segments}
    for reference in references:
        if reference not in known:
            raise EvidenceIntegrityError(f"unknown segment reference: {reference}")
    covered = {reference for reference in references}
    uncovered = [segment.ref.segment_id for segment in segments if segment.ref.segment_id not in covered]
    return CoverageResult(covered=covered, uncovered=uncovered, total_references=len(references))


class DiagramStore(AppendOnlyJsonLog):
    """Captured diagrams are immutable byte-revisions; replacing a capture
    creates a new revision and approvals bind to the exact revision."""

    PREFIX = "d"

    def bind(self, video_id, timestamp, capture_sha256, captured_at, revision_id=None, replaces=None):
        if revision_id is not None:
            existing = self.get(revision_id)
            if existing["capture_sha256"] != capture_sha256:
                raise EvidenceIntegrityError(
                    f"{revision_id}: capture bytes are immutable; bind a new revision instead"
                )
            return existing
        revision = {
            "kind": "diagram_revision",
            "revision_id": self._next_id(),
            "video_id": video_id,
            "timestamp": timestamp,
            "capture_sha256": capture_sha256,
            "captured_at": captured_at,
            "replaces": replaces,
            "status": "pending_review",
            "created_at": _now(),
        }
        self.records.append(revision)
        self._save()
        return revision

    def approve(self, revision_id, reviewer):
        if not reviewer:
            raise EvidencePolicyError("a diagram revision needs a named reviewer for pixel verification")
        record = self.get(revision_id)
        record["status"] = "approved"
        self.records.append(
            {
                "kind": "diagram_disposition",
                "revision_id": revision_id,
                "reviewer": reviewer,
                "decision": "approved",
                "recorded_at": _now(),
            }
        )
        self._save()

    def get(self, revision_id):
        for record in self.records:
            if record.get("revision_id") == revision_id and record["kind"] == "diagram_revision":
                derived = dict(record)
                for entry in self.records:
                    if (
                        entry["kind"] == "diagram_disposition"
                        and entry["revision_id"] == revision_id
                        and entry["decision"] == "approved"
                    ):
                        derived["status"] = "approved"
                return derived
        raise KeyError(revision_id)


def build_evidence_index(root, playlist_id=PLAYLIST_ID):
    """Index every available raw set (all pilot videos, not just samples) so
    authoring always binds to stable segment identities."""
    folder = Path(root) / "data" / playlist_id
    if not folder.exists():
        raise FileNotFoundError(folder)
    videos = {}
    non_raw_skipped = []
    for path in sorted(folder.iterdir()):
        if eligibility_of(path) == "teaching_eligible":
            video_id = path.name[: -len(RAW_SUFFIX)]
            segments = load_segments_from(path)
            videos[video_id] = {
                "segment_count": len(segments),
                "segments": [
                    {
                        "segment_id": s.ref.segment_id,
                        "start": s.ref.start,
                        "end": s.ref.end,
                        "text_sha256": s.text_sha256,
                    }
                    for s in segments
                ],
            }
        elif "_" in path.name or path.name.endswith(".srt"):
            non_raw_skipped.append(path.name)
    return {
        "playlist_id": playlist_id,
        "policy": "raw whisper JSON is the segment source; cleaned GeminiLongContext counterparts are video-level teaching sources; derived SRT variants are never authoring inputs",
        "videos": videos,
        "non_raw_skipped": sorted(non_raw_skipped),
    }


def main(argv=None):
    """Rebuild the local evidence index for the pilot playlist."""
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild artifacts/opto-2311/evidence-index.json (offline).")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--playlist", default=PLAYLIST_ID)
    parser.add_argument("--output", type=Path, default=Path("artifacts/opto-2311/evidence-index.json"))
    args = parser.parse_args(argv)
    root = args.root.resolve()
    index = build_evidence_index(root, args.playlist)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"generated_at": _now(), **index}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"indexed {len(index['videos'])} raw sets; skipped {len(index['non_raw_skipped'])} non-raw files")
    return 0


if __name__ == "__main__":
    main()
