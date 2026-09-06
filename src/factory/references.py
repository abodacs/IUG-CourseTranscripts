"""CF-06: a blank human-labeling worksheet for locally prepared reference sets.

The worksheet enumerates the rows the reference sets must cover — Arabic-first
good cases, the 12 hard-failure classes, English cases, and mixed-direction
cases. Humans with verified per-domain competence label each excerpt
independently, BEFORE any judge score exists (F13); `expected_class` is sealed
construction metadata rather than human ground truth. Excerpts and evidence
must be prepared locally before labeling; no private corpus is embedded in code.
"""
import datetime
import re

REQUIRED_CLASSES = (
    ["good_ar", "good_en", "mixed_direction"]
    + [f"H{i:02d}" for i in range(1, 13)]
)
CLASS_TITLES = {
    "good_ar": "مثال سليم عربي (جودة مرجعية)",
    "good_en": "English good reference excerpt",
    "mixed_direction": "Arabic/English mixed-direction case (equations inside RTL prose)",
    "H01": "wrong assertion (contradicts source evidence)",
    "H02": "outdated/incorrect version (against the course's own correction)",
    "H03": "transcription ambiguity asserted as fact",
    "H04": "absent visual treated as present",
    "H05": "contamination (legacy v2 / outside source / exposed holdout)",
    "H06": "wrong quiz key",
    "H07": "persuasive wrong solution",
    "H08": "missing prerequisite taught past",
    "H09": "cross-lesson contradiction",
    "H10": "harmful simplification",
    "H11": "invalid repair",
    "H12": "instruction-like text in source",
}


class WorksheetError(ValueError):
    """The worksheet is malformed or a labeling record is incomplete."""


def build_worksheet(playlist_id, rubric_version):
    rows = []
    for position, class_id in enumerate(REQUIRED_CLASSES, start=1):
        rows.append(
            {
                # Opaque public ID: the class name must not reach the labeler.
                "ref_id": f"ref-{position:02d}",
                "expected_class": class_id,
                "class_title": CLASS_TITLES[class_id],
                "language": "ar" if class_id == "good_ar" or class_id.startswith("H") else "en",
                "direction": "rtl" if class_id not in ("good_en",) else "ltr",
                "excerpt": "",
                "excerpt_provenance": "",
                "label": "",
                "labeler": "",
                "labeled_at": "",
                "notes": "",
            }
        )
    return {
        "playlist_id": playlist_id,
        "rubric_version": rubric_version,
        "policy": {
            "order": "labels are recorded BEFORE any judge score exists; judge outputs never touch this file",
            "competence": "each labeler must have verified per-domain competence (optics, English, digital logic per case)",
            "independence": "labelers work independently; disagreements are recorded and resolved explicitly",
            "sealed": "expected_class is construction metadata; it and construction notes are not shown to labelers; it is not human ground truth",
        },
        "rows": rows,
    }


def labeler_view(worksheet):
    """The only version a labeler should see: the sealed fields
    and construction notes are omitted; excerpts need local source preparation."""
    return {
        "playlist_id": worksheet["playlist_id"],
        "instructions": worksheet["policy"],
        "rows": [
            {key: row[key] for key in ("ref_id", "language", "direction", "excerpt", "label", "labeler", "labeled_at", "notes")}
            for row in worksheet["rows"]
        ],
    }


def label_row(worksheet, ref_id, label, labeler, notes=""):
    for row in worksheet["rows"]:
        if row["ref_id"] == ref_id:
            if not re.fullmatch(r"(good|bad)(_[a-z]+)?", label):
                raise WorksheetError(f"{ref_id}: label must be 'good' or 'bad' (optionally suffixed), got {label!r}")
            if not labeler or not str(labeler).strip():
                raise WorksheetError(f"{ref_id}: a named human labeler is required; agents cannot label")
            row["label"] = label
            row["labeler"] = labeler
            row["labeled_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
            row["notes"] = notes
            return row
    raise WorksheetError(f"unknown ref_id: {ref_id}")


def validate_complete(worksheet):
    unlabeled = [row["ref_id"] for row in worksheet["rows"] if not row["label"]]
    if unlabeled:
        raise WorksheetError(f"rows still unlabeled: {unlabeled}")
    for row in worksheet["rows"]:
        if not row["excerpt"]:
            raise WorksheetError(f"{row['ref_id']}: reference rows must carry their excerpt")
    return True
