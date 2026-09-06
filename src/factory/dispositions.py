"""CF-05: the segment-disposition recorder.

Per lecture, every source segment ends in exactly one of four states:
`included` (used in teaching), `duplicate_of` (a repeat of another segment),
`excluded_with_reason` (unused, reason recorded), or `unresolved` (drafting
not finished). A record is complete only when nothing is unresolved — equal
counts prove nothing; the dispositions are the accounting (plan §8/F04).
"""
import re

DISPOSITIONS = ("included", "duplicate_of", "excluded_with_reason", "unresolved")


class DispositionError(ValueError):
    """The disposition record is incomplete or internally inconsistent."""


class DispositionRecord:
    def __init__(self, video_id):
        self.video_id = video_id
        self.entries = {}

    def set_included(self, segment_id):
        self._set(segment_id, "included")

    def set_duplicate_of(self, segment_id, canonical_segment_id):
        if canonical_segment_id == segment_id:
            raise DispositionError(f"{segment_id}: a segment cannot duplicate itself")
        self._set(segment_id, "duplicate_of", canonical=canonical_segment_id)

    def set_excluded(self, segment_id, reason):
        if not reason or not str(reason).strip():
            raise DispositionError(f"{segment_id}: excluded_with_reason needs a recorded reason")
        self._set(segment_id, "excluded_with_reason", reason=str(reason))

    def set_unresolved(self, segment_id):
        self._set(segment_id, "unresolved")

    def _set(self, segment_id, disposition, **extra):
        if not re.fullmatch(r"[A-Za-z0-9_-]+:seg:\d{4,}", segment_id):
            raise DispositionError(f"segment id must reference the raw index namespace: {segment_id}")
        if segment_id in self.entries:
            raise DispositionError(f"{segment_id}: already disposed as {self.entries[segment_id]['disposition']}")
        if not segment_id.startswith(self.video_id + ":"):
            raise DispositionError(f"{segment_id}: belongs to another video, not {self.video_id}")
        self.entries[segment_id] = {"segment_id": segment_id, "disposition": disposition, **extra}

    def included_ids(self):
        return sorted(k for k, v in self.entries.items() if v["disposition"] == "included")

    def unresolved_ids(self):
        return sorted(k for k, v in self.entries.items() if v["disposition"] == "unresolved")

    def to_dict(self):
        return {"video_id": self.video_id, "dispositions": list(self.entries.values())}

    @classmethod
    def from_dict(cls, payload):
        record = cls(payload["video_id"])
        for entry in payload["dispositions"]:
            record.entries[entry["segment_id"]] = entry
        return record


def validate_completed(record, evidence_index):
    """A completed record accounts for every raw segment of the video, and
    every duplicate_of target is an included segment of the same video."""
    known = {
        segment["segment_id"]
        for segment in (evidence_index.get("videos", {}).get(record.video_id) or {}).get("segments", [])
    }
    if not known:
        raise DispositionError(f"{record.video_id}: no raw segments in the evidence index")
    disposed = set(record.entries)
    missing = sorted(known - disposed)
    if missing:
        raise DispositionError(f"{record.video_id}: {len(missing)} segment(s) without disposition: {missing[:3]}…")
    extra = sorted(disposed - known)
    if extra:
        raise DispositionError(f"{record.video_id}: dispositions for unknown segments: {extra[:3]}…")
    if record.unresolved_ids():
        raise DispositionError(f"{record.video_id}: drafting unresolved for {record.unresolved_ids()}")
    included = set(record.included_ids())
    for entry in record.entries.values():
        if entry["disposition"] == "duplicate_of" and entry["canonical"] not in included:
            raise DispositionError(
                f"{entry['segment_id']}: duplicate_of {entry['canonical']} which is not an included segment"
            )
    return True


def coverage_against(record, referenced_segment_ids):
    """Dispositions cannot hide an uncovered skill: every included segment
    must be referenced by the lesson's provenance (F04)."""
    included = set(record.included_ids())
    referenced = set(referenced_segment_ids)
    unreferenced = sorted(included - referenced)
    return {"included": sorted(included), "referenced": sorted(referenced), "included_but_never_referenced": unreferenced}
