"""Locate each video's cleaned sources in the GeminiLongContext/ tree.

For every raw transcript ``data/<playlist_id>/<video_id>_raw.json`` the
mirrored ``GeminiLongContext/<playlist_id>/`` tree holds the cleaned
counterparts under the same video ID: ``<video_id>_chapters.json``,
``<video_id>_v2_content.json`` (earlier variant ``_content.json``), and
``<video_id>_lecture_context.json``.

Policy reversal recorded 2026-09-07: these cleaned counterparts are approved
teaching sources for v1, bound per video; the raw whisper JSON stays
canonical for segmentation and timestamps. This module resolves paths and
coverage only — it reads no file contents.
"""
from pathlib import Path

CLEANED_ROOT = Path("GeminiLongContext")
RAW_ROOT = Path("data")
RAW_SUFFIX = "_raw.json"
SUPPORT_DIRS = {"raw", "processed", "final"}

# role -> filename suffix. ``_v2_content.json`` and the earlier
# ``_content.json`` variant are separate entries; exact-suffix matching
# keeps them distinct.
CLEANED_SUFFIXES = (
    ("chapters", "_chapters.json"),
    ("v2_content", "_v2_content.json"),
    ("lecture_context", "_lecture_context.json"),
    ("content", "_content.json"),
)


def cleaned_path(playlist_id, video_id, role, root=CLEANED_ROOT):
    """Path of one cleaned counterpart (which may not exist on disk)."""
    suffix = dict(CLEANED_SUFFIXES)[role]
    return Path(root) / playlist_id / f"{video_id}{suffix}"


def existing_cleaned(playlist_id, video_id, root=CLEANED_ROOT):
    """{role: path} for the cleaned counterparts present on disk."""
    found = {}
    for role, suffix in CLEANED_SUFFIXES:
        path = Path(root) / playlist_id / f"{video_id}{suffix}"
        if path.exists():
            found[role] = path
    return found


def iter_raw_videos(raw_root=RAW_ROOT):
    """Yield (playlist_id, video_id, raw_path) for every *_raw.json.

    Playlist folders sit directly under data/; the raw/processed/final
    support directories are not playlists. A missing raw root yields
    nothing, so a fresh clone reports zero coverage instead of crashing.
    """
    root = Path(raw_root)
    if not root.is_dir():
        return
    for playlist_dir in sorted(root.iterdir()):
        if not playlist_dir.is_dir() or playlist_dir.name in SUPPORT_DIRS:
            continue
        for raw_file in sorted(playlist_dir.glob(f"*{RAW_SUFFIX}")):
            yield playlist_dir.name, raw_file.name[: -len(RAW_SUFFIX)], raw_file


def source_coverage(raw_root=RAW_ROOT, cleaned_root=CLEANED_ROOT):
    """Per-video view of the cleaned sources: for each raw transcript, which
    cleaned counterparts exist in the mirrored tree."""
    videos = []
    counts = {role: 0 for role, _ in CLEANED_SUFFIXES}
    without_cleaned = []
    for playlist_id, video_id, raw_path in iter_raw_videos(raw_root):
        found = existing_cleaned(playlist_id, video_id, cleaned_root)
        for role in found:
            counts[role] += 1
        if not found:
            without_cleaned.append(f"{playlist_id}/{video_id}")
        videos.append(
            {
                "playlist_id": playlist_id,
                "video_id": video_id,
                "raw_path": str(raw_path),
                "cleaned": {role: str(path) for role, path in found.items()},
            }
        )
    return {
        "videos": videos,
        "counts": counts,
        "videos_without_cleaned": without_cleaned,
    }
