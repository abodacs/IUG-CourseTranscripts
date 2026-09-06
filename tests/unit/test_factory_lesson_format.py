"""CF-05 checks: dialect validation, trust boundaries, provenance, renderer."""
import json

import pytest

from src.factory import lesson_format as lf


def lesson_with(quiz_payload=None, body=None):
    body = body or (
        "[opto2311:node:intro]\n"
        "العدسة الرقيقة تُحسب بالعلاقة $$\\frac{1}{f} = \\frac{1}{u} + \\frac{1}{v}$$\n"
    )
    quiz = quiz_payload if quiz_payload is not None else json.dumps(
        {
            "quiz_id": "opto2311:quiz:q1",
            "prompt": "ما وحدة قوة العدسة؟",
            "choices": ["ديوبتر", "متر"],
            "answer": 0,
            "rationale": "قوة العدسة بالمتر المعكوس = ديوبتر",
            "feedback": "راجع تعريف الديوبتر في الدرس",
        },
        ensure_ascii=False,
    )
    return f"{body}\n```quiz\n{quiz}\n```\n"


def provenance():
    return {
        "nodes": {
            "opto2311:node:intro": {"segments": ["AAAAAAAAAAA:seg:0000"]},
        }
    }


def evidence_index():
    return {"videos": {"AAAAAAAAAAA": {"segments": [{"segment_id": "AAAAAAAAAAA:seg:0000"}]}}}


def test_valid_lesson_parses_with_nodes_and_quiz():
    document = lf.parse_lesson(lesson_with())
    assert document["nodes"][0]["node_id"] == "opto2311:node:intro"
    assert document["quizzes"][0]["quiz_id"] == "opto2311:quiz:q1"


@pytest.mark.parametrize("bad", [
    "<script>alert(1)</script>",
    "<div onclick=\"x()\">نص</div>",
    "{{ injected }}",
    "{/* mdx */}",
    "<iframe src=\"https://x\"></iframe>",
])
def test_forbidden_markup_is_rejected(bad):
    with pytest.raises(lf.DialectError, match="forbidden markup"):
        lf.parse_lesson(f"[opto2311:node:a]\nنص\n{bad}\n")


def test_math_subset_is_enforced():
    with pytest.raises(lf.DialectError, match="not in the dialect subset"):
        lf.parse_lesson("[opto2311:node:a]\n$$\\includegraphics{x}$$\n")
    with pytest.raises(lf.DialectError, match="environment not allowed"):
        lf.parse_lesson("[opto2311:node:a]\n$$\\begin{align} x \\end{align}$$\n")
    lf.parse_lesson("[opto2311:node:a]\n$$\\begin{aligned} x &= 1 \\end{aligned}$$\n")


def test_quiz_payload_failures():
    bad = json.dumps({"quiz_id": "x:quiz:q", "prompt": "س", "choices": ["أ", "ب"], "answer": 5,
                      "rationale": "ر", "feedback": "ف"}, ensure_ascii=False)
    with pytest.raises(lf.DialectError, match="in range"):
        lf.parse_lesson(lesson_with(bad))
    missing = {"quiz_id": "x:quiz:q", "prompt": "س", "choices": ["أ", "ب"], "answer": 0}
    with pytest.raises(lf.DialectError, match="missing fields"):
        lf.parse_lesson(lesson_with(json.dumps(missing, ensure_ascii=False)))
    unclosed = "[opto2311:node:a]\nنص\n```quiz\n{}\n"
    with pytest.raises(lf.DialectError, match="not closed"):
        lf.parse_lesson(unclosed)


def test_duplicate_node_ids_rejected():
    doc = "[opto2311:node:a]\nنص أول\n[opto2311:node:a]\nنص ثانٍ\n"
    with pytest.raises(lf.DialectError, match="duplicate teaching-node"):
        lf.parse_lesson(doc)


def test_lesson_without_nodes_rejected():
    with pytest.raises(lf.DialectError, match="no teaching nodes"):
        lf.parse_lesson("نص بلا علامات عقدة\n")


def test_url_allowlist_and_active_svg():
    with pytest.raises(lf.DialectError, match="not allowlisted"):
        lf.parse_lesson("[opto2311:node:a]\nشاهد (http://insecure.example/a.png)\n")
    with pytest.raises(lf.DialectError, match="active content"):
        lf.parse_lesson("[opto2311:node:a]\nرسم (assets/d.svg?onload=1)\n")


def test_provenance_must_resolve_and_cover_every_node():
    document = lf.parse_lesson(lesson_with())
    assert lf.validate_provenance(document, provenance(), evidence_index())
    with pytest.raises(lf.DialectError, match="unknown to the evidence index"):
        lf.validate_provenance(
            document, {"nodes": {"opto2311:node:intro": {"segments": ["B:seg:9"]}}}, evidence_index()
        )
    with pytest.raises(lf.DialectError, match="without provenance"):
        lf.validate_provenance(document, {"nodes": {}}, evidence_index())


def test_renderer_is_rtl_first_and_leaks_no_answers():
    document = lf.parse_lesson(lesson_with())
    html = lf.render_html(document, title="الدرس الأول")
    assert 'dir="rtl"' in html and 'lang="ar"' in html
    assert "ما وحدة قوة العدسة؟" in html and "ديوبتر" in html  # prompt + choices visible
    lf.assert_no_answer_leak(html, document)
    assert "answer" not in html.lower()
    assert "راجع تعريف الديوبتر" not in html  # feedback absent


def test_answer_index_is_undetectable_in_markup():
    document = lf.parse_lesson(lesson_with())
    html = lf.render_html(document, title="t")
    for choice_index in range(2):
        assert f'value="{choice_index}"' in html  # all choices rendered equally
    assert "data-answer" not in html
    assert "correct" not in html.lower()


def test_oversized_document_rejected():
    with pytest.raises(lf.DialectError, match="maximum accepted size"):
        lf.parse_lesson("[opto2311:node:a]\n" + "نص " * (MAX := lf.MAX_DOC_BYTES // 3))
