"""CF-06: the human-labeling worksheet for reference sets.

The worksheet enumerates the rows the reference sets must cover — Arabic-first
good cases, the 12 hard-failure classes, English cases, and mixed-direction
cases. Humans with verified per-domain competence label each excerpt
independently, BEFORE any judge score exists (F13); `expected_class` is sealed
construction metadata, shown to no labeler, and is compared only after
labeling closes.
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
    for class_id in REQUIRED_CLASSES:
        rows.append(
            {
                "ref_id": f"ref-{class_id.lower()}",
                "expected_class": class_id,
                "class_title": CLASS_TITLES[class_id],
                "language": "ar" if class_id == "good_ar" or class_id.startswith("H") else "en",
                "direction": "rtl" if class_id not in ("good_en",) else "ltr",
                "excerpt": "",
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
            "sealed": "expected_class is construction metadata; it is not shown to labelers and is compared only after labeling closes",
        },
        "rows": rows,
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


def score_against_expected(worksheet):
    """Only after labeling closes: agreement per class, disagreement listed —
    never averaged away (F13)."""
    disagreements = []
    for row in worksheet["rows"]:
        expected = "good" if row["expected_class"].startswith("good") or row["expected_class"] == "mixed_direction" else "bad"
        labeled = (row["label"] or "").split("_")[0]
        if labeled and labeled != expected:
            disagreements.append({"ref_id": row["ref_id"], "expected_class": row["expected_class"], "labeled": row["label"]})
    total = sum(1 for row in worksheet["rows"] if row["label"])
    return {"labeled": total, "disagreements": disagreements, "agreement_rate": (total - len(disagreements)) / total if total else None}
