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


def test_reference_excerpts_are_filled_with_provenance():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    for row in worksheet["rows"]:
        assert row["excerpt"], f"{row['ref_id']} has no excerpt"
        assert row["excerpt_provenance"], f"{row['ref_id']} has no provenance"
    verbatim = [r for r in worksheet["rows"] if "verbatim" in r["excerpt_provenance"]]
    assert len(verbatim) == 3  # good_ar, good_en, mixed_direction from dev families
    h06 = next(r for r in worksheet["rows"] if r["expected_class"] == "H06")
    assert '"answer": 1' in h06["excerpt"]  # the wrong key is the point


def test_labeler_view_strips_sealed_fields():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    view = references.labeler_view(worksheet)
    assert len(view["rows"]) == len(worksheet["rows"])
    assert all("expected_class" not in row and "class_title" not in row for row in view["rows"])
    assert all(row["excerpt"] for row in view["rows"])
    # the seal check inside labeler_view would have raised if anything leaked


def test_labeler_view_refuses_to_leak_classes():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    for row in worksheet["rows"]:
        row["excerpt"] = row["excerpt"] + f" [{row['expected_class']}]"
    with pytest.raises(references.WorksheetError, match="leaked"):
        references.labeler_view(worksheet)


def test_labeling_requires_named_human_and_valid_label():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    with pytest.raises(references.WorksheetError, match="named human labeler"):
        references.label_row(worksheet, row_id(worksheet, "H06"), "bad", "")
    with pytest.raises(references.WorksheetError, match="'good' or 'bad'"):
        references.label_row(worksheet, row_id(worksheet, "H06"), "correct", "د. المراجع")
    with pytest.raises(references.WorksheetError, match="unknown ref_id"):
        references.label_row(worksheet, "ref-nope", "bad", "د. المراجع")


def test_scoring_compares_labels_against_sealed_classes_only_after_labeling():
    worksheet = references.build_worksheet("PLX", "1.0-draft")
    with pytest.raises(references.WorksheetError, match="unlabeled"):
        references.validate_complete(worksheet)
    references.label_row(worksheet, row_id(worksheet, "H06"), "bad", "د. فيزياء")     # agrees (bad)
    references.label_row(worksheet, row_id(worksheet, "good_en"), "bad", "د. لغة")     # disagrees (good)
    score = references.score_against_expected(worksheet)
    assert score["labeled"] == 2
    assert score["disagreements"] == [
        {"ref_id": row_id(worksheet, "good_en"), "expected_class": "good_en", "labeled": "bad"}
    ]
    assert score["agreement_rate"] == pytest.approx(0.5)
