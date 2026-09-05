"""Offline integrity checks shared by legacy transcript migration paths."""

import hashlib
import json
import math
import os
import tempfile
from pathlib import Path


def content_hash(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def atomic_json_write(path, value):
    """Replace a JSON file only after the new file is flushed successfully."""
    path = Path(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def assign_subtitles(subtitles, intervals):
    """Assign each subtitle once by greatest overlap; ties go to the earlier chapter.

    Original text and timestamps remain intact. Gaps containing unassigned
    subtitles, invalid intervals, and duplicate subtitle IDs block processing.
    """
    if not intervals:
        raise ValueError("No chapter intervals")
    previous_end = -1
    for start, end in intervals:
        if not all(math.isfinite(v) for v in (start, end)) or start < 0 or start >= end:
            raise ValueError("Invalid chapter interval")
        if start < previous_end:
            raise ValueError("Chapter intervals overlap or are out of order")
        previous_end = end
    assigned = [[] for _ in intervals]
    seen = set()
    previous_start = -1
    for subtitle in subtitles:
        start, end, identifier = subtitle["start"], subtitle["end"], subtitle["index"]
        if identifier in seen:
            raise ValueError(f"Duplicate subtitle ID: {identifier}")
        seen.add(identifier)
        if not all(math.isfinite(v) for v in (start, end)) or start < 0 or start >= end:
            raise ValueError(f"Invalid subtitle timing: {identifier}")
        if start < previous_start:
            raise ValueError(f"Subtitles are out of source order: {identifier}")
        previous_start = start
        if not isinstance(subtitle.get("text"), str) or not subtitle["text"].strip():
            raise ValueError(f"Empty subtitle: {identifier}")
        overlaps = [max(0, min(end, right) - max(start, left)) for left, right in intervals]
        owner = max(range(len(intervals)), key=lambda i: overlaps[i])
        if overlaps[owner] <= 0:
            raise ValueError(f"Subtitle outside all chapters: {identifier}")
        assigned[owner].append(subtitle)
    return assigned
