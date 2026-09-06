"""CF-05/CF-06 checks: dispositions, node split/merge history, reference
labeling worksheet."""
import pytest

from src.factory import references
from src.factory.dispositions import (
    DispositionError,
    DispositionRecord,
    coverage_against,
    validate_completed,
)
from src.factory.node_history import NodeHistory, NodeHistoryError, validate_lesson_nodes


def evidence_index():
    return {"videos": {"AAAAAAAAAAA": {"segments": [
        {"segment_id": "AAAAAAAAAAA:seg:0000"},
        {"segment_id": "AAAAAAAAAAA:seg:0001"},
        {"segment_id": "AAAAAAAAAAA:seg:0002"},
    ]}}}


def full_record():
    record = DispositionRecord("AAAAAAAAAAA")
    record.set_included("AAAAAAAAAAA:seg:0000")
    record.set_included("AAAAAAAAAAA:seg:0001")
    record.set_duplicate_of("AAAAAAAAAAA:seg:0002", "AAAAAAAAAAA:seg:0001")
    return record


def test_completed_record_accepts_full_accounting():
    assert validate_completed(full_record(), evidence_index()) is True


def test_missing_segment_fails_completion():
    record = DispositionRecord("AAAAAAAAAAA")
    record.set_included("AAAAAAAAAAA:seg:0000")
    with pytest.raises(DispositionError, match="without disposition"):
        validate_completed(record, evidence_index())


def test_duplicate_must_target_an_included_segment():
    record = full_record()
    record.entries["AAAAAAAAAAA:seg:0001"]["disposition"] = "excluded_with_reason"
    with pytest.raises(DispositionError, match="not an included segment"):
        validate_completed(record, evidence_index())


def test_exclusion_requires_reason_and_self_duplicate_rejected():
    record = DispositionRecord("AAAAAAAAAAA")
    with pytest.raises(DispositionError, match="reason"):
        record.set_excluded("AAAAAAAAAAA:seg:0000", "   ")
    with pytest.raises(DispositionError, match="duplicate itself"):
        record.set_duplicate_of("AAAAAAAAAAA:seg:0000", "AAAAAAAAAAA:seg:0000")


def test_unresolved_blocks_completion_and_double_disposition_rejected():
    record = full_record()
    record.set_unresolved  # method exists
    with pytest.raises(DispositionError, match="another video"):
        record.set_included("BBBBBBBBBBB:seg:0000")
    with pytest.raises(DispositionError, match="already disposed"):
        record.set_included("AAAAAAAAAAA:seg:0000")


def test_dispositions_cannot_hide_uncovered_evidence():
    coverage = coverage_against(full_record(), ["AAAAAAAAAAA:seg:0000"])
    assert coverage["included_but_never_referenced"] == ["AAAAAAAAAAA:seg:0001"]


def test_node_split_history_resolves_old_references(tmp_path):
    history = NodeHistory(tmp_path / "nodes.json")
    history.split("opto2311:node:lens", ["opto2311:node:lens-thin", "opto2311:node:lens-power"],
                  "المفهومان مستقلان", revision="r2")
    assert history.descendants("opto2311:node:lens") == [
        "opto2311:node:lens-power", "opto2311:node:lens-thin",
    ]
    assert "opto2311:node:lens" in history.consumed_ids()


def test_node_merge_and_chain(tmp_path):
    history = NodeHistory(tmp_path / "nodes.json")
    history.split("opto2311:node:a", ["opto2311:node:a1", "opto2311:node:a2"], "تفريق", revision="r2")
    history.merge(["opto2311:node:a1", "opto2311:node:a2"], "opto2311:node:a-full", "إعادة دمج", revision="r3")
    assert history.descendants("opto2311:node:a") == ["opto2311:node:a-full"]


def test_stale_and_reused_ids_are_rejected(tmp_path):
    history = NodeHistory(tmp_path / "nodes.json")
    history.split("opto2311:node:a", ["opto2311:node:a1"], "سبب", revision="r2")
    with pytest.raises(NodeHistoryError, match="consumed"):
        history.split("opto2311:node:a", ["opto2311:node:b"], "مرة أخرى", revision="r3")
    with pytest.raises(NodeHistoryError, match="never reused"):
        history.merge(["opto2311:node:a1", "opto2311:node:z"], "opto2311:node:a", "دوران", revision="r3")


def test_lesson_may_not_use_stale_node_ids(tmp_path):
    history = NodeHistory(tmp_path / "nodes.json")
    history.split("opto2311:node:a", ["opto2311:node:a1", "opto2311:node:a2"], "سبب", revision="r2")
    document = {"nodes": [{"node_id": "opto2311:node:a1"}, {"node_id": "opto2311:node:a"}]}
    with pytest.raises(NodeHistoryError, match="stale node ID"):
        validate_lesson_nodes(document, history)
    fresh = {"nodes": [{"node_id": "opto2311:node:a1"}, {"node_id": "opto2311:node:a2"}, {"node_id": "opto2311:node:new"}]}
    assert validate_lesson_nodes(fresh, history) is True


def test_reference_worksheet_covers_all_required_classes():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    classes = {row["expected_class"] for row in worksheet["rows"]}
    assert classes == set(references.REQUIRED_CLASSES)
    assert len(references.REQUIRED_CLASSES) == 15  # 3 good/mixed + 12 hard-failure classes
    assert "Arabic" in references.CLASS_TITLES["good_ar"] or "عربي" in references.CLASS_TITLES["good_ar"]
    assert "labels are recorded BEFORE any judge score" in worksheet["policy"]["order"]



def row_id(worksheet, class_id):
    return next(r["ref_id"] for r in worksheet["rows"] if r["expected_class"] == class_id)


def test_reference_template_is_blank_and_incomplete():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    assert all(row["excerpt"] == row["excerpt_provenance"] == "" for row in worksheet["rows"])
    with pytest.raises(references.WorksheetError, match="unlabeled"):
        references.validate_complete(worksheet)
    for row in worksheet["rows"]:
        references.label_row(worksheet, row["ref_id"], "good", "Reviewer")
    with pytest.raises(references.WorksheetError, match="must carry their excerpt"):
        references.validate_complete(worksheet)


def test_labeler_view_preserves_local_excerpt_without_construction_notes():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    row = worksheet["rows"][0]
    row["excerpt"] = "Synthetic excerpt mentioning H06 as ordinary text."
    row["excerpt_provenance"] = "Constructed to contain a wrong quiz key."
    view = references.labeler_view(worksheet)
    assert len(view["rows"]) == len(worksheet["rows"])
    assert view["rows"][0]["excerpt"] == row["excerpt"]
    assert all(
        not {"expected_class", "class_title", "excerpt_provenance"}.intersection(item)
        for item in view["rows"]
    )


def test_labeling_requires_named_human_and_valid_label():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    with pytest.raises(references.WorksheetError, match="named human labeler"):
        references.label_row(worksheet, row_id(worksheet, "H06"), "bad", "")
    with pytest.raises(references.WorksheetError, match="'good' or 'bad'"):
        references.label_row(worksheet, row_id(worksheet, "H06"), "correct", "د. المراجع")
    with pytest.raises(references.WorksheetError, match="unknown ref_id"):
        references.label_row(worksheet, "ref-nope", "bad", "د. المراجع")


def test_prepared_and_labeled_worksheet_is_complete():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    for row in worksheet["rows"]:
        row["excerpt"] = "Synthetic local reference excerpt."
        references.label_row(worksheet, row["ref_id"], "bad", "Reviewer", notes="Human assessment")
    assert references.validate_complete(worksheet) is True
    assert all(row["notes"] == "Human assessment" for row in worksheet["rows"])
