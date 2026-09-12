"""Offline outcome-matrix pass CLI (OPTO 2311).

No model calls, no network, no DB, no env vars. Runs on any checkout that
has the repo plus the local corpus (``data/`` and ``GeminiLongContext/``,
both git-ignored), inside or outside zIDE.

Subcommands:
  start-window --window N      archive the current matrix and start a fresh one
  next [--window N]            next unprocessed batch in position order
  dump <video_id>              numbered raw-segment dump + chapter hints + cleaned paths
  segments <video_id> <out>    write the segment text map (json) for drafters
  verify <video_id> <rows>     mechanical checks of drafted rows
  persist <draft> --window N   write rows + lesson to the matrix, append exposure event

Policy grounding:
  - teaching sources = raw whisper JSON (canonical for segmentation and
    timestamps) plus the cleaned counterparts in ``GeminiLongContext/``
    (approved teaching sources 2026-09-07, bound per video), resolved via
    src/etl/cleaned_store.py — never guessed paths
  - teaching evidence = raw whisper segments only
    (src/factory/evidence.py); evidence refs must exist in
    artifacts/opto-2311/evidence-index.json and excerpts are checked
    verbatim against the raw segment text
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.etl import cleaned_store  # noqa: E402

DEFAULT_PLAYLIST = "PL9fwy3NUQKway0xLRTe7OlRxcQic7R2s-"

REQUIRED_FIELDS = ("outcome_id", "task", "cognitive_level", "intended_learner", "sufficiency")
SUFFICIENCY = ("supported", "needs_youtube_diagram", "unsupported")
COGNITIVE_LEVELS = ("remember", "understand", "apply", "analyze", "evaluate", "create")
COMPONENTS = ("explanation", "example", "practice", "transfer_task")

CLEANED_ROLE_NOTES = {
    "chapters": "audit-only hint pointers",
    "v2_content": "approved teaching source (2026-09-07); present for 83/105 pilot videos",
    "lecture_context": "approved teaching source (2026-09-07); usually Python-literal, not strict JSON — read leniently",
    "content": "earlier cleaned variant (superseded by v2_content when present)",
}

HEADER = {
    "schema": 1,
    "kind": "outcome_matrix_draft",
    "policy": (
        "DRAFT for reviewer approval — no row is approved until the operator and "
        "subject reviewer sign the freeze. Teaching sources per video: raw whisper "
        "JSON (data/<playlist>/<video>_raw.json, canonical for segmentation and "
        "timestamps) plus its cleaned GeminiLongContext counterparts "
        "(<video>_chapters.json, <video>_v2_content.json, <video>_lecture_context.json; "
        "approved teaching sources 2026-09-07, bound per video). Teaching evidence: "
        "raw whisper segments only; every evidence ref is hash-verified against "
        "artifacts/opto-2311/evidence-index.json and excerpt-checked verbatim against "
        "the raw segment text; cleaned sources are never segment loads "
        "(src/factory/evidence.py). Schema per src/factory/outcomes.py "
        "(validate_outcome_matrix); extra descriptive fields (component_notes, "
        "asr_note) are review aids, not validator inputs. Chapter hints are audit-only "
        "discovery pointers, never evidence. Sufficiency values: supported | "
        "needs_youtube_diagram | unsupported (blocker_note required)."
    ),
    "source_policy_ref": [
        "docs/NEXT_STEPS.md (Next task)",
        "docs/pilot/opto-2311/opto-2311-scope-freeze.md",
        "docs/README.md (corpus layout)",
        "src/factory/outcomes.py",
        "src/factory/evidence.py",
        "src/etl/cleaned_store.py",
        "wayfinder issue #11 resolution 2026-09-07 (1a/2a/3a/4a)",
    ],
    "position_notes": {
        "skipped": {
            "8": "unavailable source (no raw transcript set)",
            "105": "exam-logistics notice (skipped per authorized work loop)",
            "106": "exam-logistics notice (skipped per authorized work loop)",
        },
        "teaching_positions_total": 103,
    },
}


def today(args):
    return args.date or datetime.date.today().isoformat()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def art_dir(root):
    return Path(root) / "artifacts" / "opto-2311"


def matrix_path(root):
    return art_dir(root) / "outcome-matrix.json"


def exposure_path(root):
    return art_dir(root) / "exposure-log.json"


def fresh_matrix(args):
    return dict(HEADER, created=today(args), outcomes=[], lessons=[])


def load_matrix(args):
    path = matrix_path(args.root)
    if path.exists():
        return load_json(path)
    return fresh_matrix(args)


def lecture_entries(root):
    order_path = art_dir(root) / "lecture-order.json"
    if not order_path.exists():
        raise SystemExit(f"missing {order_path} — build it with scripts/reconcile_lecture_order.py first")
    return load_json(order_path)["order"]


def raw_path(args, video_id):
    return Path(args.root) / "data" / args.playlist / f"{video_id}_raw.json"


def raw_segments(args, video_id):
    path = raw_path(args, video_id)
    if not path.exists():
        raise SystemExit(f"missing raw transcript {path}")
    return load_json(path)["segments"]


def evidence_index(args):
    path = art_dir(args.root) / "evidence-index.json"
    if not path.exists():
        raise SystemExit(f"missing {path} — build it with `python -m src.factory.evidence` first")
    return load_json(path)


def check_hashes(args, video_id, segments):
    idx = evidence_index(args)["videos"][video_id]
    if idx["segment_count"] != len(segments):
        raise SystemExit(f"{video_id}: segment_count mismatch index={idx['segment_count']} raw={len(segments)}")
    for i, (seg, iseg) in enumerate(zip(segments, idx["segments"])):
        h = hashlib.sha256(seg["text"].encode("utf-8")).hexdigest()
        if h != iseg["text_sha256"] or abs(seg["start"] - iseg["start"]) > 1e-6:
            raise SystemExit(f"{video_id} seg {i}: raw does not match evidence index")
    return True


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def cmd_start_window(args):
    current = matrix_path(args.root)
    had_rows = False
    if current.exists():
        existing = load_json(current)
        had_rows = bool(existing.get("outcomes") or existing.get("lessons"))
        if had_rows:
            archive = art_dir(args.root) / f"outcome-matrix-window{args.window - 1}.json"
            if archive.exists() and not args.force:
                raise SystemExit(f"{archive} already exists — pass --force to overwrite")
            write_json(archive, existing)
            print(f"archived current matrix ({len(existing.get('outcomes', []))} rows, "
                  f"{len(existing.get('lessons', []))} lessons) -> {archive}")
    write_json(current, fresh_matrix(args))
    print(f"started window {args.window}: fresh {current} (created {today(args)})")
    if not had_rows:
        print("nothing to archive")


def cmd_next(args):
    matrix = load_matrix(args)
    skipped = matrix.get("position_notes", {}).get("skipped", {})
    done = {lesson["position"] for lesson in matrix.get("lessons", [])}
    todo = []
    for entry in lecture_entries(args.root):
        position = entry["position"]
        if entry.get("unavailable"):
            continue
        if str(position) in skipped:
            continue
        if position in done:
            continue
        todo.append(entry)
    teaching_total = matrix.get("position_notes", {}).get("teaching_positions_total")
    window = f"window {args.window}" if args.window else "current pass"
    print(f"### {window}: {len(done)} position(s) persisted, {len(todo)} remaining"
          + (f" of {teaching_total} teaching positions" if teaching_total else ""))
    if not todo:
        print("all teaching positions persisted — nothing remaining")
        return
    batch = todo[: args.batch_size]
    print(f"### next batch ({len(batch)} of remaining {len(todo)}):")
    for entry in batch:
        video_id = entry["video_id"]
        raw_exists = raw_path(args, video_id).exists()
        cleaned = cleaned_store.existing_cleaned(args.playlist, video_id, Path(args.root) / "GeminiLongContext")
        flags = []
        if not raw_exists:
            flags.append("MISSING RAW")
        if not cleaned:
            flags.append("no cleaned counterparts")
        tail = f"  [{'; '.join(flags)}]" if flags else ""
        print(f"  p{position_fmt(entry['position'])} {video_id}  {entry.get('title', '')}{tail}")


def position_fmt(position):
    return f"{position:03d}"


def cmd_dump(args):
    video_id = args.video_id
    segments = raw_segments(args, video_id)
    check_hashes(args, video_id, segments)
    print(f"### {video_id} raw segments: {len(segments)}")
    for i, seg in enumerate(segments):
        print(f"[{i:04d}] {seg['start']:.2f}-{seg['end']:.2f} {norm(seg['text'])}")
    cleaned_root = Path(args.root) / "GeminiLongContext"
    cleaned = cleaned_store.existing_cleaned(args.playlist, video_id, cleaned_root)
    if cleaned:
        print("### cleaned counterparts (approved teaching sources 2026-09-07; raw stays evidence-canonical)")
        for role, path in cleaned.items():
            print(f"  CLEANED {role}: {path}  ({CLEANED_ROLE_NOTES.get(role, '')})")
    else:
        print("### no cleaned counterparts found for this video (raw only)")
    chapters = cleaned.get("chapters")
    if chapters:
        payload = load_json(chapters)
        print("### chapter hints (audit-only pointers)")
        for c in payload.get("chapters", []):
            print(f"  HINT {c.get('start_timestamp')}-{c.get('end_timestamp')} {c.get('title')}")


def cmd_segments(args, out):
    video_id = args.video_id
    segments = raw_segments(args, video_id)
    check_hashes(args, video_id, segments)
    Path(out).write_text(
        json.dumps(
            {
                "video_id": video_id,
                "segments": [
                    {"i": i, "segment_id": f"{video_id}:seg:{i:04d}", "start": s["start"], "end": s["end"], "text": s["text"]}
                    for i, s in enumerate(segments)
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"wrote {out}")


def cmd_verify(args):
    video_id = args.video_id
    rows = load_json(args.rows_path)
    if isinstance(rows, dict):
        rows = rows.get("outcomes", [])
    segmap = {f"{video_id}:seg:{i:04d}": s for i, s in enumerate(raw_segments(args, video_id))}
    errors = []
    for row in rows:
        oid = row.get("outcome_id", "?")
        for f in REQUIRED_FIELDS:
            if not row.get(f):
                errors.append(f"{oid}: missing {f}")
        if row.get("sufficiency") not in SUFFICIENCY:
            errors.append(f"{oid}: bad sufficiency")
        if row.get("cognitive_level") not in COGNITIVE_LEVELS:
            errors.append(f"{oid}: bad cognitive_level {row.get('cognitive_level')!r}")
        for comp in COMPONENTS:
            if not isinstance((row.get("required_components") or {}).get(comp), list):
                errors.append(f"{oid}: required_components.{comp} not a list")
        ev = row.get("evidence") or []
        if not ev:
            errors.append(f"{oid}: no evidence")
        for ref in ev:
            if isinstance(ref, dict):
                ref, excerpt = ref.get("segment_id"), ref.get("excerpt", "")
            else:
                ref, excerpt = ref, ""
            if ref not in segmap:
                errors.append(f"{oid}: unknown segment {ref}")
                continue
            if excerpt and norm(excerpt) not in norm(segmap[ref]["text"]):
                errors.append(f"{oid}: excerpt not in {ref}: {excerpt[:60]!r}")
        if row.get("sufficiency") == "needs_youtube_diagram":
            d = row.get("diagram") or {}
            if not (d.get("video_id") and d.get("start") is not None):
                errors.append(f"{oid}: diagram video/start required")
        if row.get("sufficiency") == "unsupported" and not row.get("blocker_note"):
            errors.append(f"{oid}: blocker_note required")
        for p in row.get("prerequisites") or []:
            if isinstance(p, str) and not p.startswith(("O-p", "NONE")):
                errors.append(f"{oid}: prerequisite {p!r} not an O-p id")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK {len(rows)} rows for {video_id}")


def sha16(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def dev_family_ids(root):
    path = art_dir(root) / "evaluation-families.json"
    if not path.exists():
        return set()
    families = load_json(path).get("development_families", [])
    ids = set()
    for fam in families:
        if isinstance(fam, str):
            ids.add(fam)
        elif isinstance(fam, dict) and fam.get("family_id"):
            ids.add(fam["family_id"])
    return ids


def append_exposure(args, matrix_text, video_id, position, lesson_id, window):
    log_path = exposure_path(args.root)
    log = load_json(log_path)
    event_id = f"exp-matrix-w{window}-p{position_fmt(position)}"
    appended = not any(e.get("id") == event_id for e in log["events"])
    if appended:
        log["events"].append(
            {
                "id": event_id,
                "date": today(args),
                "access_kind": "transcript_text_read",
                "family_scope": f"fam-{video_id}",
                "video_ids": [video_id],
                "purpose": (
                    f"outcome matrix pass window {window} {today(args)}: raw segments and "
                    f"cleaned counterparts read, outcome rows drafted (position {position})"
                ),
                "evidence_ref": (
                    f"artifacts/opto-2311/outcome-matrix.json sha256:{sha16(matrix_text)} #lesson {lesson_id}"
                ),
                "recorded_by": f"session:outcome-matrix-pass-w{window}",
            }
        )
    read_videos = {
        vid
        for e in log["events"]
        if e.get("access_kind") == "transcript_text_read"
        for vid in e.get("video_ids", [])
    }
    dev = dev_family_ids(args.root)
    candidates = sorted(vid for vid in read_videos if f"fam-{vid}" not in dev)
    counters = log.setdefault("counters", {})
    counters["events_total"] = len(log["events"])
    counters["candidate_videos_touched_by_transcript_text"] = len(candidates)
    counters["candidate_videos_touched_list"] = candidates
    write_json(log_path, log)
    return event_id, appended


def cmd_persist(args):
    draft = load_json(args.draft_path)
    video_id = draft["video_id"]
    position = draft["position"]
    rows = draft["outcomes"]
    window = args.window
    matrix = load_matrix(args)

    by_id = {o["outcome_id"]: o for o in matrix["outcomes"]}
    for row in rows:
        row = dict(row)
        ev = row.get("evidence") or []
        if ev and isinstance(ev[0], dict):
            row["evidence_excerpts"] = [
                {"segment_id": e["segment_id"], "excerpt": e["excerpt"]} for e in ev
            ]
            row["evidence"] = [e["segment_id"] for e in ev]
        row.setdefault("draft_status", "draft_pending_review")
        row.setdefault("drafted_by", f"session:outcome-matrix-pass-w{window}")
        by_id[row["outcome_id"]] = row
    matrix["outcomes"] = sorted(by_id.values(), key=lambda o: (o.get("position", 999), o["outcome_id"]))

    lesson_id = f"L-p{position_fmt(position)}"
    lesson = {
        "lesson_id": lesson_id,
        "position": position,
        "video_id": video_id,
        "title": draft.get("title"),
        "outcome_ids": [r["outcome_id"] for r in rows],
    }
    lessons = {l["lesson_id"]: l for l in matrix["lessons"]}
    lessons[lesson_id] = lesson
    matrix["lessons"] = sorted(lessons.values(), key=lambda l: l["position"])

    lesson_position = {}
    for l in matrix["lessons"]:
        for oid in l["outcome_ids"]:
            lesson_position[oid] = l["position"]
    for row in rows:
        for p in row.get("prerequisites") or []:
            if p == "NONE":
                continue
            if p not in lesson_position:
                raise SystemExit(f"{row['outcome_id']}: unknown prerequisite {p}")
            if lesson_position[p] > position:
                raise SystemExit(f"{row['outcome_id']}: prerequisite {p} is at a later position")

    write_json(matrix_path(args.root), matrix)
    text = matrix_path(args.root).read_text(encoding="utf-8")
    event_id, appended = append_exposure(args, text, video_id, position, lesson_id, window)
    state = "appended" if appended else "already present"
    print(f"persisted {lesson_id} ({len(rows)} rows) -> {matrix_path(args.root)}; exposure event {event_id} {state}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="outcome_matrix.py",
        description="Offline OPTO 2311 outcome-matrix pass (no model calls, no network).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=str(REPO_ROOT), help="repo root (default: this checkout)")
    common.add_argument("--playlist", default=DEFAULT_PLAYLIST, help="pilot playlist id")
    common.add_argument("--date", default=None, help="ISO date stamp (default: today)")

    p = sub.add_parser("start-window", parents=[common], help="archive the current matrix, start fresh")
    p.add_argument("--window", type=int, required=True)
    p.add_argument("--force", action="store_true", help="overwrite an existing archive")
    p.set_defaults(func=cmd_start_window)

    p = sub.add_parser("next", parents=[common], help="next unprocessed batch in position order")
    p.add_argument("--window", type=int, default=None)
    p.add_argument("--batch-size", type=int, default=10)
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("dump", parents=[common], help="raw segments + chapter hints + cleaned paths")
    p.add_argument("video_id")
    p.set_defaults(func=cmd_dump)

    p = sub.add_parser("segments", parents=[common], help="write the segment text map for drafters")
    p.add_argument("video_id")
    p.add_argument("out")
    p.set_defaults(func=lambda a: cmd_segments(a, a.out))

    p = sub.add_parser("verify", parents=[common], help="mechanical checks of drafted rows")
    p.add_argument("video_id")
    p.add_argument("rows_path")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("persist", parents=[common], help="write rows + lesson, append exposure event")
    p.add_argument("draft_path")
    p.add_argument("--window", type=int, required=True)
    p.set_defaults(func=cmd_persist)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # downstream closed the pipe (e.g. `| head`) — exit quietly
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
