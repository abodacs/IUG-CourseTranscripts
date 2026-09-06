#!/usr/bin/env python3
"""CF-02: turn a pinned yt-dlp flat-playlist dump into lecture-order.json.

Parses the `--flat-playlist --print` TSV output, records the fetch metadata,
and reconciles the ordered playlist entries against the CF-01 source
manifest: which entries lack local raw transcripts, which local videos are
absent from the playlist, and which entries look like re-uploads (same title
and duration). Titles/durations are metadata for ordering and capture hints —
never teaching facts.
"""
from pathlib import Path
import argparse
import collections
import datetime
import json
import re
import sys

TOOL = "yt-dlp[default]==2026.8.19 (uv run --isolated --no-project)"
NA = "NA"

# Absolute Arabic ordinals/digits that can appear after "المحاضرة". Relative
# references (السابقة/القادمة = previous/next) carry no absolute number and
# are never treated as evidence.
ORDINAL_WORDS = {
    "الأولى": 1, "الأول": 1, "الثانية": 2, "الثاني": 2, "الثالثة": 3, "الثالث": 3,
    "الرابعة": 4, "الرابع": 4, "الخامسة": 5, "الخامس": 5, "السادسة": 6, "السادس": 6,
    "السابعة": 7, "السابع": 7, "الثامنة": 8, "الثامن": 8, "التاسعة": 9, "التاسع": 9,
    "العاشرة": 10, "العاشر": 10, "الحادية عشرة": 11, "الثانية عشرة": 12,
    "الثالثة عشرة": 13, "الرابعة عشرة": 14, "الخامسة عشرة": 15,
    "السادسة عشرة": 16, "السابعة عشرة": 17, "الثامنة عشرة": 18, "التاسعة عشرة": 19,
}
LECTURE_WORD_RE = re.compile(r"[مم]حاضرة\s+([0-9]+|[^\s،.!?]+(?:\s+[^\s،.!?]+)?)")


def parse_order_tsv(text):
    """Parse yt-dlp TSV lines into ordered entry dicts (position preserved)."""
    order = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 4:
            raise ValueError(f"unexpected line format: {line!r}")
        position, video_id, title, duration = parts
        order.append(
            {
                "position": int(position),
                "video_id": video_id,
                "title": None if title == NA else title,
                "duration_seconds": None if duration == NA else int(duration),
                "unavailable": title == NA and duration == NA,
            }
        )
    if not order:
        raise ValueError("empty playlist dump")
    positions = [entry["position"] for entry in order]
    if positions != list(range(1, len(order) + 1)):
        raise ValueError(f"non-contiguous positions: {positions[:5]}…")
    return order


def duplicate_title_groups(order):
    """Entries sharing title and duration — candidate re-upload duplicates."""
    groups = collections.defaultdict(list)
    for entry in order:
        if entry["title"] is not None and entry["duration_seconds"] is not None:
            groups[(entry["title"], entry["duration_seconds"])].append(entry["video_id"])
    return [
        {"title": title, "duration_seconds": duration, "video_ids": sorted(ids)}
        for (title, duration), ids in sorted(groups.items())
        if len(ids) > 1
    ]


def reconcile(order, manifest):
    """Compare the ordered playlist against the CF-01 manifest video set."""
    manifest_ids = {video["video_id"] for video in manifest["videos"]}
    order_ids = {entry["video_id"] for entry in order}
    local_missing_playlist = [
        entry for entry in order if entry["video_id"] not in manifest_ids
    ]
    playlist_missing_local = sorted(manifest_ids - order_ids)
    skipped_visible = [
        {
            "video_id": entry["video_id"],
            "position": entry["position"],
            "unavailable_at_fetch": entry["unavailable"],
        }
        for entry in order
        if entry["video_id"] in {
            video["video_id"]
            for video in manifest["videos"]
            if video.get("source_gap")
        }
    ]
    return {
        "playlist_entries": len(order),
        "local_manifest_videos": len(manifest_ids),
        "playlist_entries_without_local_raw": local_missing_playlist,
        "local_videos_absent_from_playlist": playlist_missing_local,
        "skipped_or_gapped_entries": skipped_visible,
        "duplicate_title_groups": duplicate_title_groups(order),
    }


def numbered_title_count(order):
    """How many titles carry an explicit sequence number (المحاضرة/التمرين N)."""
    markers = ("المحاضرة", "التمرين", "محاضرة", "تمرين")
    return sum(1 for entry in order if entry["title"] and any(m in entry["title"] for m in markers))


def lecture_number_in(text):
    """Absolute lecture numbers referenced in a title or transcript
    ('المحاضرة 5', 'المحاضرة السادسة'). Relative references (السابقة/القادمة)
    are ignored: they carry no absolute number."""
    numbers = set()
    for match in LECTURE_WORD_RE.finditer(text or ""):
        token = match.group(1).strip()
        if token.isdigit():
            numbers.add(int(token))
            continue
        for word, number in ORDINAL_WORDS.items():
            if token == word or token.startswith(word + " "):
                numbers.add(number)
                break
    return numbers


def title_lecture_number(title):
    return next(iter(lecture_number_in(title)), None) if title else None


def cross_check_transcript_references(order, data_dir):
    """Compare each entry's title number against absolute 'المحاضرة N'
    references in its transcript. A conflict downgrades the position to
    unknown; missing references leave the playlist evidence unverified."""
    data_dir = Path(data_dir) if data_dir else None
    for entry in order:
        entry["order_evidence"] = {"source": "playlist_metadata", "quality": "playlist_title_only"}
        if entry["unavailable"]:
            entry["order_evidence"]["quality"] = "unavailable_entry"
            continue
        title_number = title_lecture_number(entry["title"])
        entry["order_evidence"]["title_lecture_number"] = title_number
        if title_number is None or data_dir is None:
            continue
        raw_path = data_dir / f"{entry['video_id']}_raw.json"
        if not raw_path.exists():
            continue
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
        transcript_text = " ".join(
            segment.get("text", "") for segment in payload.get("segments", [])
        )
        references = lecture_number_in(transcript_text)
        entry["order_evidence"]["transcript_lecture_references"] = sorted(references)
        if references and title_number not in references:
            entry["order_evidence"]["quality"] = "unknown_transcript_conflict"
            entry["order_evidence"]["conflict"] = (
                f"title says المحاضرة {title_number} but transcript references {sorted(references)}"
            )
        elif references:
            entry["order_evidence"]["quality"] = "verified_playlist_and_transcript"


def build_document(tsv_text, manifest, playlist_id, fetched_at, data_dir=None):
    order = parse_order_tsv(tsv_text)
    cross_check_transcript_references(order, data_dir)
    return {
        "playlist_id": playlist_id,
        "fetch": {
            "fetched_at": fetched_at,
            "tool": TOOL,
            "invocation": (
                "uv run --isolated --no-project --with 'yt-dlp[default]==2026.8.19' "
                "yt-dlp --flat-playlist --print "
                "'%(playlist_index)s\\t%(id)s\\t%(title)s\\t%(duration)s' "
                f"'https://www.youtube.com/playlist?list={playlist_id}'"
            ),
        },
        "order": order,
        "reconciliation": reconcile(order, manifest),
        "sequence_hints": {
            "numbered_titles": numbered_title_count(order),
            "note": (
                "titles/durations are playlist metadata for ordering and capture "
                "hints only, never teaching facts; unavailable entries keep their "
                "position visible"
            ),
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build lecture-order.json from a yt-dlp TSV dump.")
    parser.add_argument("--tsv", type=Path, required=True, help="raw yt-dlp --flat-playlist output")
    parser.add_argument("--manifest", type=Path, default=Path("artifacts/opto-2311/source-manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/opto-2311/lecture-order.json"))
    parser.add_argument("--playlist", default="PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-")
    parser.add_argument("--fetched-at", default=None, help="ISO fetch timestamp; defaults to now (UTC)")
    parser.add_argument(
        "--data-dir", type=Path, default=None,
        help="data/<playlist> dir for the transcript cross-check; omit to skip it",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))["manifest"]
    fetched_at = args.fetched_at or datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    data_dir = args.data_dir if args.data_dir is None else (
        args.data_dir if args.data_dir.is_absolute() else root / args.data_dir
    )
    if data_dir is None:
        data_dir = root / "data" / args.playlist
    document = build_document(
        args.tsv.read_text(encoding="utf-8"), manifest, args.playlist, fetched_at, data_dir
    )
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    recon = document["reconciliation"]
    quality = collections.Counter(entry["order_evidence"]["quality"] for entry in document["order"])
    print(f"order evidence quality: {dict(quality)}")
    print(f"order entries: {recon['playlist_entries']}; local manifest videos: {recon['local_manifest_videos']}")
    print(f"playlist entries without local raw: {len(recon['playlist_entries_without_local_raw'])}")
    print(f"local videos absent from playlist: {len(recon['local_videos_absent_from_playlist'])}")
    print(f"duplicate title groups: {len(recon['duplicate_title_groups'])}")
    for group in recon["duplicate_title_groups"]:
        print(f"  - {group['title']} ({group['duration_seconds']}s): {', '.join(group['video_ids'])}")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
