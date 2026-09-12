#!/usr/bin/env python3
"""CF-01: offline source manifest for the OPTO 2311 pilot playlist.

Reads a consistent local snapshot of youtube-iug.db and the transcript corpus,
then writes one manifest record per expected video with variant hashes, source
roles, integrity findings, and unresolved evidence. Never edits the corpus,
state, or database; imports nothing from src/; performs no network or model
calls.

Wall-clock inspection data (generation time) is kept in a separate "inspection"
block outside the hashed semantic payload, so unchanged reruns produce the same
manifest hash.
"""
from pathlib import Path
import argparse
import ast
import collections
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import sys
import tempfile

MANIFEST_VERSION = 1
TOOL_NAME = "build_pilot_manifest.py"
DEFAULT_PLAYLIST = "PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-"
DEFAULT_OUTPUT = Path("artifacts/opto-2311/source-manifest.json")
VIDEO_ID_RE = r"[A-Za-z0-9_-]{11}"
PLAYLIST_DIR_RE = re.compile(r"^(?:PL|L9)[A-Za-z0-9_-]{30,33}$")

# Known variant suffixes -> role. Order matters: longer suffixes must be tried
# before bare ".srt" so `_raw.srt` is not read as the normalized variant.
VARIANT_SUFFIXES = [
    ("_raw.json", "raw_transcript_json"),
    ("_raw.srt", "raw_transcript_srt"),
    ("_postprocess.srt", "postprocess_srt"),
    ("_chapters.json", "chapter_hints"),
    ("_v2_content.json", "legacy_v2_lesson"),
    ("_lecture_context.json", "legacy_lecture_context"),
    ("_content.json", "legacy_generated_context"),
    (".srt", "normalized_srt"),
]
# Eligibility per the source policy. Reversal recorded 2026-09-07 (operator):
# the cleaned GeminiLongContext counterparts (chapter hints, v2 lessons,
# lecture context) are teaching sources bound per video; raw whisper JSON
# stays the canonical segmentation, and derived SRT variants stay excluded.
ROLE_ELIGIBILITY = {
    "raw_transcript_json": "teaching_eligible",
    "raw_transcript_srt": "teaching_eligible",
    "postprocess_srt": "conditional_fidelity_check",
    "normalized_srt": "classify_only_not_trusted",
    "chapter_hints": "teaching_eligible_cleaned",
    "legacy_v2_lesson": "teaching_eligible_cleaned",
    "legacy_lecture_context": "teaching_eligible_cleaned",
    "legacy_generated_context": "teaching_eligible_cleaned",
}
UNCLASSIFIED_RE = re.compile(rf"^(?P<vid>{VIDEO_ID_RE})_(?P<rest>.+)$")

# Near-duplicate content families for the CF-06 split manifest (recorded as
# metadata only; no processing of these playlists happens here).
FAMILY_WATCHLIST = [
    {
        "playlist_id": "PL9fwy3NUQKwb_KOrEPbVXCHcPMZKR0uEY",
        "title": "بصريات هندسية",
        "note": "same course name; zero video-ID overlap with the pilot; candidate near-duplicate family for the CF-06 split manifest",
    },
    {
        "playlist_id": "PL9fwy3NUQKwZZYWdO8xTBLJBmEjaQDzzb",
        "title": "البصريات الهندسية / عمرو أبو عمارة",
        "note": "same course name; zero video-ID overlap with the pilot; candidate near-duplicate family for the CF-06 split manifest",
    },
]

SRT_TIMESTAMP_RE = re.compile(
    r"^(?P<start>\d{1,3}:\d{1,2}:\d{1,2}[,.]\d{1,3})\s*-->\s*(?P<end>\d{1,3}:\d{1,2}:\d{1,2}[,.]\d{1,3})\s*$"
)

# Screening thresholds for faster-whisper quality flags. These are hints to
# prioritize human/CF-02A review, never verdicts about correctness.
SCREENING_THRESHOLDS = {
    "no_speech_prob_gt": 0.6,
    "avg_logprob_lt": -1.0,
    "compression_ratio_gt": 2.5,
}


class ManifestError(RuntimeError):
    """Refusal condition (unsafe database state, unusable inputs)."""


def canonical_playlist_id(playlist_id, known_ids):
    """Resolve the known folder/membership alias: a playlist id missing its
    leading 'P' (e.g. L9fwy3NUQKw…) maps to the canonical PL… id."""
    if playlist_id in known_ids:
        return playlist_id, "canonical"
    if playlist_id.startswith("L") and "P" + playlist_id in known_ids:
        return "P" + playlist_id, "alias_missing_leading_p"
    return playlist_id, "unknown_playlist_id"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_db_snapshot(root):
    """Copy youtube-iug.db to a temp dir and open that copy read-only.

    Refuses a nonempty WAL (the local database is only safe to read when all
    writes are checkpointed) and verifies the file did not change during the
    copy. Returns (connection, temp_dir, db_sha256); the caller closes the
    connection and removes temp_dir.
    """
    db = root / "youtube-iug.db"
    if not db.exists():
        raise ManifestError(f"database not found: {db}")
    wal = Path(str(db) + "-wal")
    before = (db.stat().st_size, db.stat().st_mtime_ns, wal.stat().st_size if wal.exists() else None)
    if before[2]:
        raise ManifestError("nonempty WAL needs a WAL-aware copied snapshot; refusing to read")
    temp_dir = Path(tempfile.mkdtemp(prefix="cf01-manifest-"))
    snapshot = temp_dir / db.name
    shutil.copy2(db, snapshot)
    after = (db.stat().st_size, db.stat().st_mtime_ns, wal.stat().st_size if wal.exists() else None)
    if before != after:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise ManifestError("database changed during copy; refusing inconsistent snapshot")
    conn = sqlite3.connect(f"file:{snapshot}?mode=ro&immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn, temp_dir, sha256_file(snapshot)


def load_playlist_context(conn, playlist_id):
    """Playlist row, alias-normalized memberships, and shared-video metadata."""
    known_ids = {row[0] for row in conn.execute("SELECT source_id FROM playlists")}
    canonical, id_form = canonical_playlist_id(playlist_id, known_ids)
    playlist_row = conn.execute(
        "SELECT id, source_id, title, skip, entries FROM playlists WHERE source_id=?",
        (canonical,),
    ).fetchone()
    if playlist_row is None:
        raise ManifestError(f"playlist {playlist_id} (canonical {canonical}) not found in playlists")
    memberships = []
    for row in conn.execute(
        "SELECT video_id, playlist_id, downloaded_r2, synced, upload_srt_r2, skip, created_at, modified_at"
        " FROM sync_github ORDER BY id"
    ):
        row_canonical, row_form = canonical_playlist_id(row["playlist_id"], known_ids)
        if row_canonical == canonical:
            memberships.append(
                {
                    "video_id": row["video_id"],
                    "recorded_playlist_id": row["playlist_id"],
                    "id_form": row_form,
                    "downloaded_r2": row["downloaded_r2"],
                    "synced": row["synced"],
                    "upload_srt_r2": row["upload_srt_r2"],
                    "skip": row["skip"],
                    "created_at": row["created_at"],
                    "modified_at": row["modified_at"],
                }
            )
    if not memberships:
        raise ManifestError(f"no sync_github memberships resolve to playlist {canonical}")
    video_ids = sorted({m["video_id"] for m in memberships})
    all_other = collections.defaultdict(set)
    for row in conn.execute("SELECT video_id, playlist_id FROM sync_github"):
        row_canonical, _ = canonical_playlist_id(row["playlist_id"], known_ids)
        if row_canonical != canonical:
            all_other[row["video_id"]].add(row_canonical)
    family_counts = {}
    for family in FAMILY_WATCHLIST:
        family_counts[family["playlist_id"]] = conn.execute(
            "SELECT COUNT(*) FROM sync_github WHERE playlist_id=?", (family["playlist_id"],)
        ).fetchone()[0]
    return {
        "canonical": canonical,
        "requested": playlist_id,
        "requested_id_form": id_form,
        "playlist_row": playlist_row,
        "memberships": memberships,
        "video_ids": video_ids,
        "other_memberships": all_other,
        "family_counts": family_counts,
    }


def discover_variants(root, video_ids):
    """Map video_id -> role -> [paths] across the known corpus roots.

    Discovery is by exact video ID, never by folder membership, so the known
    folder alias (a directory missing the leading 'P') still resolves.
    """
    wanted = set(video_ids)
    found = collections.defaultdict(lambda: collections.defaultdict(list))
    bases = [root / "data", root / "GeminiLongContext"]
    bases += [p for p in sorted(root.iterdir()) if p.is_dir() and PLAYLIST_DIR_RE.fullmatch(p.name)]
    for base in bases:
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(
                d for d in dirnames if not d.startswith(".") and d not in ("gemini_logs", "__pycache__")
            )
            for name in sorted(filenames):
                suffix_role = None
                for suffix, role in VARIANT_SUFFIXES:
                    if name.endswith(suffix):
                        vid = name[: -len(suffix)]
                        if re.fullmatch(VIDEO_ID_RE, vid):
                            suffix_role = (vid, role)
                        break
                if suffix_role is None:
                    unclassified = UNCLASSIFIED_RE.fullmatch(name)
                    if unclassified and unclassified.group("vid") in wanted:
                        found[unclassified.group("vid")]["unclassified"].append(Path(dirpath) / name)
                    continue
                vid, role = suffix_role
                if vid in wanted:
                    found[vid][role].append(Path(dirpath) / name)
    return found


def relative_posix(path, root):
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def file_record(path, root):
    return {
        "path": relative_posix(path, root),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def timestamp_seconds(value):
    """SRT 'HH:MM:SS,mmm', chapter 'MM:SS'/'HH:MM:SS', or a whisper float, as
    finite float seconds."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        if not math.isfinite(number) or number < 0:
            raise ValueError(f"invalid timestamp {value!r}")
        return number
    text = str(value).strip()
    match = re.fullmatch(
        r"(?:(?P<hours>\d{1,3}):)?(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2})(?:[,.](?P<millis>\d{1,3}))?",
        text,
    )
    if not match:
        raise ValueError(f"unparseable timestamp {value!r}")
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis = int(match.group("millis") or 0)
    if minutes > 59 or seconds > 59:
        raise ValueError(f"out-of-range timestamp {value!r}")
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def finding(code, detail, severity="warning"):
    return {"severity": severity, "code": code, "detail": detail}


def probe_whisper_json(path):
    """Integrity observations from a faster-whisper raw JSON."""
    problems = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return {
            "segment_count": None,
            "coverage": None,
            "screening": None,
            "findings": [finding("malformed_json", f"unreadable JSON: {error}", "critical")],
        }
    segments = payload.get("segments")
    if not isinstance(segments, list):
        return {
            "segment_count": None,
            "coverage": None,
            "screening": None,
            "findings": [finding("malformed_json", "missing or non-list segments[]", "critical")],
        }
    observations = {"segment_count": len(segments), "coverage": None, "screening": None, "findings": []}
    previous_start = None
    seen_units = set()
    duplicates = 0
    zero_duration = 0
    screening = collections.Counter()
    valid = 0
    first_start = last_end = None
    for index, segment in enumerate(segments):
        try:
            start = timestamp_seconds(segment.get("start"))
            end = timestamp_seconds(segment.get("end"))
        except (ValueError, TypeError, AttributeError):
            problems.append(f"segments[{index}] invalid timestamps")
            continue
        text = segment.get("text")
        if not isinstance(text, str):
            problems.append(f"segments[{index}] text is not a string")
            continue
        if start < 0:
            problems.append(f"segments[{index}] negative start")
            continue
        if end < start:
            problems.append(f"segments[{index}] end<start ({start}-{end})")
            continue
        if end == start:
            zero_duration += 1
            continue
        valid += 1
        first_start = start if first_start is None else min(first_start, start)
        last_end = end if last_end is None else max(last_end, end)
        if previous_start is not None and start < previous_start:
            problems.append(f"segments[{index}] starts before previous segment (out of order)")
        previous_start = start
        unit = (round(start, 3), round(end, 3), text)
        if unit in seen_units:
            duplicates += 1
        seen_units.add(unit)
        no_speech = segment.get("no_speech_prob")
        logprob = segment.get("avg_logprob")
        compression = segment.get("compression_ratio")
        if isinstance(no_speech, (int, float)) and no_speech > SCREENING_THRESHOLDS["no_speech_prob_gt"]:
            screening["no_speech_prob_gt_0.6"] += 1
        if isinstance(logprob, (int, float)) and logprob < SCREENING_THRESHOLDS["avg_logprob_lt"]:
            screening["avg_logprob_lt_-1.0"] += 1
        if isinstance(compression, (int, float)) and compression > SCREENING_THRESHOLDS["compression_ratio_gt"]:
            screening["compression_ratio_gt_2.5"] += 1
    if valid:
        observations["coverage"] = {"first_start": first_start, "last_end": last_end}
    observations["screening"] = {
        "thresholds": SCREENING_THRESHOLDS,
        "counts": dict(sorted(screening.items())),
        "note": "screening hints only, not verdicts",
    }
    for problem in problems[:20]:
        observations["findings"].append(finding("invalid_segment", problem))
    if len(problems) > 20:
        observations["findings"].append(finding("invalid_segment", f"+{len(problems) - 20} more segment problems"))
    if duplicates:
        observations["findings"].append(finding("duplicate_segment", f"{duplicates} duplicate segment unit(s)"))
    if zero_duration:
        observations["findings"].append(
            finding("zero_duration_segment", f"{zero_duration} segment(s) with start==end")
        )
    return observations


def probe_srt(path):
    """Structural observations from an SRT variant, without trusting it."""
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return {"cue_count": None, "coverage": None, "findings": [
            finding("malformed_srt", f"undecodable text: {error}", "critical")
        ]}
    blocks = [block for block in re.split(r"\n\s*\n", raw_text.strip()) if block.strip()]
    observations = {"cue_count": 0, "coverage": None, "findings": []}
    problems = []
    duplicates = 0
    zero_duration = 0
    range_counts = collections.Counter()
    index_gaps = 0
    expected_index = 1
    previous_start = None
    seen_units = set()
    first_start = last_end = None
    for block_index, block in enumerate(blocks):
        lines = block.splitlines()
        if not lines:
            continue
        cursor = 0
        if re.fullmatch(r"\d+", lines[0].strip()):
            number = int(lines[0].strip())
            if number != expected_index:
                index_gaps += 1
            expected_index = number + 1
            cursor = 1
        match = SRT_TIMESTAMP_RE.fullmatch(lines[cursor].strip()) if cursor < len(lines) else None
        if match is None:
            problems.append(f"block {block_index + 1}: missing/unparseable timestamp line")
            continue
        try:
            start = timestamp_seconds(match.group("start"))
            end = timestamp_seconds(match.group("end"))
        except ValueError as error:
            problems.append(f"block {block_index + 1}: {error}")
            continue
        text = "\n".join(lines[cursor + 1:]).strip()
        if not text:
            problems.append(f"block {block_index + 1}: empty cue text")
        if end < start:
            problems.append(f"block {block_index + 1}: end<start ({start}-{end})")
            continue
        if end == start:
            zero_duration += 1
            continue
        observations["cue_count"] += 1
        range_counts[(round(start, 3), round(end, 3))] += 1
        first_start = start if first_start is None else min(first_start, start)
        last_end = end if last_end is None else max(last_end, end)
        if previous_start is not None and start < previous_start:
            problems.append(f"block {block_index + 1}: starts before previous cue (out of order)")
        previous_start = start
        unit = (round(start, 3), round(end, 3), text)
        if unit in seen_units:
            duplicates += 1
        seen_units.add(unit)
    if observations["cue_count"]:
        observations["coverage"] = {"first_start": first_start, "last_end": last_end}
    for problem in problems[:20]:
        observations["findings"].append(finding("invalid_cue", problem))
    if len(problems) > 20:
        observations["findings"].append(finding("invalid_cue", f"+{len(problems) - 20} more cue problems"))
    if duplicates:
        observations["findings"].append(finding("duplicate_cue", f"{duplicates} duplicate cue unit(s)"))
    repeated_ranges = sum(count - 1 for count in range_counts.values() if count > 1)
    if repeated_ranges:
        observations["findings"].append(
            finding("duplicate_timestamp_range", f"{repeated_ranges} repeated (start,end) cue range(s)")
        )
    if zero_duration:
        observations["findings"].append(
            finding("zero_duration_cue", f"{zero_duration} cue(s) with start==end")
        )
    if index_gaps:
        observations["findings"].append(finding("cue_index_gap", f"{index_gaps} non-sequential cue index(es)"))
    return observations


def probe_keyframe_hints(path):
    """Audit-only statistics from a legacy chapter JSON (hint source)."""
    stats = {"chapters": 0, "chosen_keyframes": 0, "candidate_timestamps": 0, "range_warnings": 0}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return stats, [finding("malformed_chapters_json", f"unreadable: {error}")]
    chapters = payload.get("chapters") if isinstance(payload, dict) else None
    if not isinstance(chapters, list):
        return stats, [finding("malformed_chapters_json", "missing or non-list chapters[]")]
    findings = []
    previous_end = None
    stats["chapters"] = len(chapters)
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            findings.append(finding("malformed_chapter", f"chapters[{index}] is not an object"))
            continue
        if chapter.get("chosen_keyframe") is not None:
            stats["chosen_keyframes"] += 1
        candidates = chapter.get("candidates_keyframes")
        if isinstance(candidates, list):
            stats["candidate_timestamps"] += len(candidates)
        try:
            start = timestamp_seconds(chapter.get("start_timestamp"))
            end = timestamp_seconds(chapter.get("end_timestamp"))
        except (ValueError, TypeError):
            stats["range_warnings"] += 1
            findings.append(finding("chapter_range_warning", f"chapters[{index}]: unparseable range"))
            previous_end = None
            continue
        if end <= start or (previous_end is not None and start < previous_end):
            stats["range_warnings"] += 1
            findings.append(
                finding("chapter_range_warning", f"chapters[{index}]: reversed or overlapping range")
            )
        previous_end = end
    return stats, findings


def coverage_delta(coverage_a, coverage_b):
    if not coverage_a or not coverage_b:
        return None
    return {
        "first_start_delta": round(coverage_a["first_start"] - coverage_b["first_start"], 3),
        "last_end_delta": round(coverage_a["last_end"] - coverage_b["last_end"], 3),
    }


def count_delta(label, count_a, count_b, findings, severity="warning"):
    """Record a count comparison; a delta questions alignment, it never proves
    equal meaning. Returns the delta, or None when a side is missing."""
    if count_a is None or count_b is None:
        findings.append(finding("cross_check_incomplete", f"{label}: missing count on one side", severity))
        return None
    delta = count_a - count_b
    if delta:
        findings.append(finding("count_mismatch", f"{label}: {count_a} vs {count_b} (delta {delta:+d})", severity))
    return delta


def build_video_record(video_id, context, variant_paths, root):
    membership_rows = sorted(
        (m for m in context["memberships"] if m["video_id"] == video_id),
        key=lambda m: (m["recorded_playlist_id"],),
    )
    primary = membership_rows[0]
    others = sorted(context["other_memberships"].get(video_id, set()))
    variants = {}
    findings = []
    for role, paths in sorted(variant_paths.items()):
        records = [file_record(path, root) for path in paths]
        variants[role] = records
        if len(records) > 1:
            distinct = {r["sha256"] for r in records}
            findings.append(
                finding(
                    "conflicting_variants",
                    f"{role}: {len(records)} copies, {len(distinct)} distinct hash(es)",
                    severity="warning" if len(distinct) == 1 else "critical",
                )
            )
    raw_json_records = variants.get("raw_transcript_json", [])
    raw_srt_records = variants.get("raw_transcript_srt", [])
    integrity = {"findings": findings, "cross_checks": {}}
    raw_json_probe = None
    raw_srt_probe = None
    if raw_json_records:
        raw_json_probe = probe_whisper_json(root / raw_json_records[0]["path"])
        integrity["raw_json"] = {
            "segment_count": raw_json_probe["segment_count"],
            "coverage": raw_json_probe["coverage"],
            "screening": raw_json_probe["screening"],
        }
        findings.extend(dict(item, variant="raw_transcript_json") for item in raw_json_probe["findings"])
    if raw_srt_records:
        raw_srt_probe = probe_srt(root / raw_srt_records[0]["path"])
        integrity["raw_srt"] = {
            "cue_count": raw_srt_probe["cue_count"],
            "coverage": raw_srt_probe["coverage"],
        }
        findings.extend(dict(item, variant="raw_transcript_srt") for item in raw_srt_probe["findings"])
    if raw_json_probe and raw_srt_probe:
        integrity["cross_checks"]["raw_json_vs_raw_srt"] = {
            "segment_count_delta": count_delta(
                "raw json segments vs raw srt cues",
                raw_json_probe["segment_count"],
                raw_srt_probe["cue_count"],
                findings,
            ),
            "coverage_delta": coverage_delta(raw_json_probe["coverage"], raw_srt_probe["coverage"]),
        }
    for role in ("postprocess_srt", "normalized_srt"):
        records = variants.get(role, [])
        if not records:
            continue
        probe = probe_srt(root / records[0]["path"])
        integrity[role] = {
            "cue_count": probe["cue_count"],
            "coverage": probe["coverage"],
        }
        findings.extend(dict(item, variant=role) for item in probe["findings"])
        if raw_json_probe:
            integrity["cross_checks"][f"{role}_vs_raw_json"] = {
                "cue_count_delta": count_delta(
                    f"{role} cues vs raw json segments",
                    probe["cue_count"],
                    raw_json_probe["segment_count"],
                    findings,
                ),
                "coverage_delta": coverage_delta(probe["coverage"], raw_json_probe["coverage"]),
            }
        if role == "postprocess_srt":
            identical = bool(raw_srt_records and records[0]["sha256"] == raw_srt_records[0]["sha256"])
            integrity[role]["fidelity_status"] = (
                "identical_to_raw_srt" if identical else "needs_fidelity_check"
            )
    keyframe_hints = None
    chapters_records = variants.get("chapter_hints", [])
    if chapters_records:
        keyframe_hints, hint_findings = probe_keyframe_hints(root / chapters_records[0]["path"])
        findings.extend(dict(item, variant="chapter_hints") for item in hint_findings)
    if variants.get("unclassified"):
        findings.append(
            finding(
                "unclassified_variant",
                "; ".join(p.name for p in variants["unclassified"][:5]),
            )
        )
    eligibility = collections.defaultdict(list)
    for role in variants:
        eligibility[ROLE_ELIGIBILITY.get(role, "unclassified")].append(role)
    has_raw = bool(raw_json_records or raw_srt_records)
    skip_flag = primary["skip"]
    record = {
        "video_id": video_id,
        "membership": {
            "recorded_playlist_id": primary["recorded_playlist_id"],
            "id_form": primary["id_form"],
            "membership_rows": len(membership_rows),
            "downloaded_r2": primary["downloaded_r2"],
            "synced": primary["synced"],
            "upload_srt_r2": primary["upload_srt_r2"],
            "skip": skip_flag,
            "created_at": primary["created_at"],
            "modified_at": primary["modified_at"],
            "other_playlist_memberships": others,
        },
        "shared_video_id": bool(others),
        "lecture_order": {
            "position": "unknown",
            "reason": "sync_github.created_at is a single batch import (download order, not lecture order)",
        },
        "variants": {role: variants[role] for role in sorted(variants)},
        "eligibility": {name: sorted(roles) for name, roles in sorted(eligibility.items())},
        "integrity": integrity,
        "keyframe_hints": keyframe_hints,
    }
    if skip_flag == 1 or not has_raw:
        record["source_gap"] = {
            "skip_flag": skip_flag,
            "has_raw_transcript": has_raw,
            "disposition": "unresolved" if skip_flag == 1 else "missing_source",
        }
    return record


def parse_entries_field(entries):
    """Classify the playlist entries metadata without inventing its content."""
    if entries is None:
        return {"format": "null", "stored_length": 0, "truncated": False}
    if not isinstance(entries, str):
        return {"format": type(entries).__name__, "stored_length": None, "truncated": False}
    try:
        parsed = json.loads(entries)
        return {
            "format": "json",
            "stored_length": len(entries),
            "truncated": False,
            "entry_count": len(parsed) if isinstance(parsed, list) else None,
        }
    except json.JSONDecodeError:
        pass
    try:
        parsed = ast.literal_eval(entries)
        return {
            "format": "python_literal",
            "stored_length": len(entries),
            "truncated": False,
            "entry_count": len(parsed) if isinstance(parsed, list) else None,
        }
    except (ValueError, SyntaxError):
        return {
            "format": "unparseable",
            "stored_length": len(entries),
            "truncated": True,
            "note": (
                "entries likely truncated by the 32,767-char storage limit; "
                "membership comes from sync_github rows, not entries"
            ),
        }


def build_semantic_manifest(root, playlist_id):
    """Build the deterministic semantic payload plus database lineage."""
    conn, temp_dir, db_sha256 = read_db_snapshot(root)
    try:
        context = load_playlist_context(conn, playlist_id)
        variant_paths = discover_variants(root, context["video_ids"])
        playlist_row = context["playlist_row"]
        videos = [
            build_video_record(video_id, context, variant_paths.get(video_id, {}), root)
            for video_id in context["video_ids"]
        ]
        created = sorted(m["created_at"] for m in context["memberships"] if m["created_at"])
        span_seconds = None
        if created:
            parsed = [datetime.datetime.fromisoformat(value) for value in created]
            span_seconds = (parsed[-1] - parsed[0]).total_seconds()
        semantic = {
            "manifest_version": MANIFEST_VERSION,
            "tool": TOOL_NAME,
            "playlist": {
                "playlist_id": context["canonical"],
                "requested_playlist_id": context["requested"],
                "requested_id_form": context["requested_id_form"],
                "db_row_id": playlist_row["id"],
                "title": playlist_row["title"],
                "skip": playlist_row["skip"],
                "entries_metadata": parse_entries_field(playlist_row["entries"]),
                "membership_count": len(context["memberships"]),
                "distinct_video_ids": len(context["video_ids"]),
                "order_evidence": {
                    "lecture_order": "unknown",
                    "created_at_min": created[0] if created else None,
                    "created_at_max": created[-1] if created else None,
                    "created_at_span_seconds": span_seconds,
                    "reason": (
                        "all memberships were created in one batch import; "
                        "sync_github timestamps are download order, not lecture order"
                    ),
                    "resolution_paths": [
                        "CF-02: YouTube playlist metadata via pinned yt-dlp (identity/order only)",
                        "transcript verbal sequence references",
                        "legacy chapter hints (audit-only)",
                    ],
                },
            },
            "evidence_lineage": {"database_sha256": db_sha256},
            "videos": videos,
            "family_watchlist": [
                dict(family, local_sync_memberships=context["family_counts"][family["playlist_id"]])
                for family in FAMILY_WATCHLIST
            ],
        }
        semantic["summary"] = summarize_manifest(semantic)
        semantic["blockers"] = derive_blockers(semantic)
        return semantic
    finally:
        conn.close()
        shutil.rmtree(temp_dir, ignore_errors=True)


def summarize_manifest(semantic):
    videos = semantic["videos"]

    def count(predicate):
        return sum(1 for video in videos if predicate(video))

    role_counts = collections.Counter()
    for video in videos:
        for role, records in video["variants"].items():
            role_counts[role] += len(records)
    findings_by_severity = collections.Counter()
    findings_by_code = collections.Counter()
    for video in videos:
        for item in video["integrity"]["findings"]:
            findings_by_severity[item["severity"]] += 1
            findings_by_code[item["code"]] += 1
    screening_totals = collections.Counter()
    for video in videos:
        screening = ((video["integrity"].get("raw_json") or {}).get("screening") or {}).get("counts") or {}
        for key, value in screening.items():
            screening_totals[key] += value
    return {
        "expected_videos": len(videos),
        "with_raw_transcript_json": count(lambda v: "raw_transcript_json" in v["variants"]),
        "with_raw_transcript_srt": count(lambda v: "raw_transcript_srt" in v["variants"]),
        "with_any_raw_transcript": count(
            lambda v: "raw_transcript_json" in v["variants"] or "raw_transcript_srt" in v["variants"]
        ),
        "with_postprocess_srt": count(lambda v: "postprocess_srt" in v["variants"]),
        "with_normalized_srt": count(lambda v: "normalized_srt" in v["variants"]),
        "with_chapter_hints": count(lambda v: "chapter_hints" in v["variants"]),
        "with_legacy_v2_lesson": count(lambda v: "legacy_v2_lesson" in v["variants"]),
        "with_source_gap": count(lambda v: "source_gap" in v),
        "skipped_flagged": count(lambda v: v["membership"]["skip"] == 1),
        "shared_video_ids": count(lambda v: v["shared_video_id"]),
        "videos_with_findings": count(lambda v: bool(v["integrity"]["findings"])),
        "variant_file_counts": dict(sorted(role_counts.items())),
        "finding_counts_by_severity": dict(sorted(findings_by_severity.items())),
        "finding_counts_by_code": dict(sorted(findings_by_code.items())),
        "whisper_screening_totals": dict(sorted(screening_totals.items())),
        "keyframe_hint_totals": {
            "chapters": sum((v["keyframe_hints"] or {}).get("chapters", 0) for v in videos),
            "chosen_keyframes": sum((v["keyframe_hints"] or {}).get("chosen_keyframes", 0) for v in videos),
            "candidate_timestamps": sum((v["keyframe_hints"] or {}).get("candidate_timestamps", 0) for v in videos),
            "range_warnings": sum((v["keyframe_hints"] or {}).get("range_warnings", 0) for v in videos),
        },
        "postprocess_fidelity": {
            "identical_to_raw_srt": count(
                lambda v: (v["integrity"].get("postprocess_srt") or {}).get("fidelity_status")
                == "identical_to_raw_srt"
            ),
            "needs_fidelity_check": count(
                lambda v: (v["integrity"].get("postprocess_srt") or {}).get("fidelity_status")
                == "needs_fidelity_check"
            ),
        },
    }


def derive_blockers(semantic):
    summary = semantic["summary"]
    blockers = [
        {
            "id": "lecture-order-unknown",
            "description": (
                "lecture order is unknown from local evidence; CF-02 must fetch playlist "
                "metadata or record explicit unknown slots"
            ),
        },
        {
            "id": "postprocess-fidelity",
            "description": (
                f"{summary['postprocess_fidelity']['needs_fidelity_check']} postprocessed SRT "
                "file(s) still need a fidelity check before any use beyond raw text"
            ),
        },
        {
            "id": "keyframe-hints-are-hints",
            "description": (
                f"{summary['keyframe_hint_totals']['chosen_keyframes']} chosen keyframe hints are "
                "audit-only; a hint is not proof of what the frame shows"
            ),
        },
        {
            "id": "legacy-outputs-audit-only",
            "description": (
                f"{summary['with_legacy_v2_lesson']} legacy v2 lessons and all generated contexts "
                "are audit-only; every available transcript still needs fresh v1 processing"
            ),
        },
        {
            "id": "sibling-near-duplicate-families",
            "description": (
                "two sibling optics playlists share the course name and must be grouped in the "
                "CF-06 split manifest"
            ),
        },
    ]
    skipped = sorted(
        v["video_id"]
        for v in semantic["videos"]
        if v.get("source_gap", {}).get("disposition") == "unresolved"
    )
    if skipped:
        blockers.append(
            {
                "id": "skipped-source-disposition",
                "description": (
                    f"skipped video(s) {', '.join(skipped)} remain unresolved (skip=1, no raw file)"
                ),
            }
        )
    if semantic["playlist"]["entries_metadata"].get("truncated"):
        blockers.append(
            {
                "id": "truncated-entries-metadata",
                "description": (
                    "playlist entries metadata is truncated; local membership completeness "
                    "relies on sync_github rows only"
                ),
            }
        )
    return blockers


def manifest_hash(semantic):
    canonical = json.dumps(semantic, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def write_manifest(semantic, db_sha256, output_path):
    document = {
        "manifest_sha256": manifest_hash(semantic),
        "inspection": {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "tool": TOOL_NAME,
            "database_sha256": db_sha256,
        },
        "manifest": semantic,
    }
    payload = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    return document


def print_summary(document):
    manifest = document["manifest"]
    summary = manifest["summary"]
    print(f"Playlist {manifest['playlist']['playlist_id']} — {manifest['playlist']['title']}")
    print(f"Manifest sha256: {document['manifest_sha256']}")
    for key in (
        "expected_videos",
        "with_raw_transcript_json",
        "with_raw_transcript_srt",
        "with_postprocess_srt",
        "with_normalized_srt",
        "with_chapter_hints",
        "with_legacy_v2_lesson",
        "with_source_gap",
        "skipped_flagged",
        "shared_video_ids",
        "videos_with_findings",
    ):
        print(f"  {key}: {summary[key]}")
    print(f"  findings by severity: {summary['finding_counts_by_severity']}")
    print(f"  findings by code: {summary['finding_counts_by_code']}")
    print(f"  whisper screening totals: {summary['whisper_screening_totals']}")
    print(f"  keyframe hints: {summary['keyframe_hint_totals']}")
    print(f"  postprocess fidelity: {summary['postprocess_fidelity']}")
    print("Blockers:")
    for blocker in manifest["blockers"]:
        print(f"  - [{blocker['id']}] {blocker['description']}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Offline OPTO 2311 source manifest; read-only, no network or model calls."
    )
    parser.add_argument(
        "--playlist", default=DEFAULT_PLAYLIST, help="playlist id (canonical or alias form)"
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="manifest JSON output path (kept local)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        semantic = build_semantic_manifest(root, args.playlist)
    except ManifestError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    document = write_manifest(semantic, semantic["evidence_lineage"]["database_sha256"], output)
    print_summary(document)
    print(f"Manifest written to {output} (stays local; JSON is git-ignored)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
