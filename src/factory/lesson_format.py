"""CF-05: the constrained lesson Markdown dialect — parser, validators, and
the minimal RTL-first static renderer.

Dialect: CommonMark subset + declared extensions — `$$…$$` math (allowlisted
subset), pipe tables, `quiz` fenced payloads, and explicit teaching-node IDs
(`[course:node:id]` markers) that carry identity across revisions (never
ordinals or content hashes). Prohibited: raw HTML, event handlers, MDX/JS,
non-allowlisted URL schemes, active SVG content, oversized documents.

Answer-leak rule (F14): the renderer emits quiz prompts and choices only.
Answers, rationales, and feedback stay in the private sidecar and never enter
the lesson HTML — not even inside collapsed/accessibility-visible elements.
Static practice therefore cannot promise exam secrecy; that limitation is
recorded, not hidden.
"""
import json
import re

MAX_DOC_BYTES = 2_000_000
NODE_RE = re.compile(r"^\[([a-z0-9\-]+):node:([a-z0-9\-]+)\]$", re.IGNORECASE)
QUIZ_ID_RE = re.compile(r"^[a-z0-9\-]+:quiz:[a-z0-9\-]+$")
MATH_COMMAND_RE = re.compile(r"\\([a-zA-Z]+)")
ALLOWED_MATH_COMMANDS = {
    "frac", "dfrac", "sqrt", "sum", "int", "prod", "lim", "alpha", "beta", "gamma",
    "theta", "lambda", "mu", "nu", "pi", "rho", "sigma", "tau", "phi", "omega",
    "Delta", "nabla", "times", "cdot", "div", "pm", "mp", "leq", "geq", "neq",
    "approx", "equiv", "propto", "rightarrow", "leftarrow", "Rightarrow",
    "infty", "partial", "sin", "cos", "tan", "log", "ln", "exp", "text",
    "begin", "end", "left", "right", "hat", "bar", "vec",
}
ALLOWED_ENVIRONMENTS = {"aligned", "cases", "pmatrix", "bmatrix"}
FORBIDDEN_MARKUP_RE = re.compile(
    r"(<script|<iframe|<object|<embed|<form|<style|</?[a-z]+[> ]|javascript:|data:text/html|\{\{|\{/\*)",
    re.IGNORECASE,
)
ALLOWED_URL_RE = re.compile(r"^(https://|/|assets/|#)", re.IGNORECASE)
SVG_ACTIVE_RE = re.compile(r"(<script|on[a-z]+\s*=|<foreignObject)", re.IGNORECASE)
HTML_ESCAPE = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}


class DialectError(ValueError):
    """The document violates the dialect or a trust boundary."""


def _escape(text):
    for char, replacement in HTML_ESCAPE.items():
        text = text.replace(char, replacement)
    return text


def parse_lesson(source):
    """Parse a lesson document into nodes, quizzes, and math spans."""
    if len(source.encode("utf-8")) > MAX_DOC_BYTES:
        raise DialectError("document exceeds the maximum accepted size")
    if FORBIDDEN_MARKUP_RE.search(source.replace("$$", "")):
        raise DialectError("forbidden markup: raw HTML/JS/event handlers/MDX are not part of the dialect")

    lines = source.splitlines()
    nodes, quizzes, paragraphs = [], [], []
    current_node = None
    buffer = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip().startswith("```quiz"):
            payload_lines = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                payload_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise DialectError("quiz block is not closed")
            quizzes.append(parse_quiz("\n".join(payload_lines), current_node))
            index += 1
            continue
        header = NODE_RE.match(line.strip())
        if header:
            if current_node and buffer:
                paragraphs.append((current_node, "\n".join(buffer).strip()))
            current_node = f"{header.group(1)}:node:{header.group(2)}"
            buffer = []
        elif current_node is not None:
            buffer.append(line)
        index += 1
    if current_node and buffer:
        paragraphs.append((current_node, "\n".join(buffer).strip()))
    if current_node is None:
        raise DialectError("lesson has no teaching nodes; every teaching paragraph needs a node ID")

    for node_id, text in paragraphs:
        validate_math_in(text)
        validate_urls_in(text)
        nodes.append({"node_id": node_id, "text": text})

    ids = [node["node_id"] for node in nodes]
    if len(ids) != len(set(ids)):
        raise DialectError("duplicate teaching-node IDs")
    quiz_ids = [quiz["quiz_id"] for quiz in quizzes]
    if len(quiz_ids) != len(set(quiz_ids)):
        raise DialectError("duplicate quiz IDs")
    return {"nodes": nodes, "quizzes": quizzes}


def parse_quiz(payload_text, owner_node):
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        raise DialectError(f"quiz payload is not valid JSON: {error}") from error
    required = {"quiz_id", "prompt", "choices", "answer", "rationale", "feedback"}
    missing = required - set(payload)
    if missing:
        raise DialectError(f"quiz payload missing fields: {sorted(missing)}")
    if not QUIZ_ID_RE.match(payload["quiz_id"]):
        raise DialectError(f"quiz_id violates the naming rule: {payload['quiz_id']!r}")
    if not isinstance(payload["choices"], list) or len(payload["choices"]) < 2:
        raise DialectError("quiz needs at least two choices")
    if not isinstance(payload["answer"], int) or not 0 <= payload["answer"] < len(payload["choices"]):
        raise DialectError("quiz answer must be a choice index in range")
    for field in ("prompt", "rationale", "feedback"):
        payload[field] = _escape(str(payload[field]))
    payload["choices"] = [_escape(str(choice)) for choice in payload["choices"]]
    payload["owner_node"] = owner_node
    validate_urls_in(payload["prompt"])
    return payload


def validate_math_in(text):
    for match in re.finditer(r"\$\$(.+?)\$\$", text, re.DOTALL):
        expr = match.group(1)
        for command in MATH_COMMAND_RE.findall(expr):
            if command not in ALLOWED_MATH_COMMANDS:
                raise DialectError(f"math command not in the dialect subset: \\{command}")
        for env in re.findall(r"\\begin\{(\w+)\}", expr):
            if env not in ALLOWED_ENVIRONMENTS:
                raise DialectError(f"math environment not allowed: {env}")


def validate_urls_in(text):
    for url in re.findall(r'(?:src|href)=["\']([^"\']+)["\']|\((assets/[^)\s]+|https?://[^)\s]+)\)', text):
        candidate = url[0] or url[1]
        if not ALLOWED_URL_RE.match(candidate):
            raise DialectError(f"URL scheme/path not allowlisted: {candidate}")
        if SVG_ACTIVE_RE.search(candidate):
            raise DialectError(f"active content in asset reference: {candidate}")


def validate_provenance(document, provenance, evidence_index):
    """Every teaching node maps to transcript spans that exist; every quiz
    belongs to a node. References resolve — counts prove nothing."""
    segments = {
        segment["segment_id"]
        for video in evidence_index.get("videos", {}).values()
        for segment in video.get("segments", [])
    }
    node_ids = {node["node_id"] for node in document["nodes"]}
    for node_id, entry in (provenance.get("nodes") or {}).items():
        if node_id not in node_ids:
            raise DialectError(f"provenance names a node the lesson does not have: {node_id}")
        for ref in entry.get("segments") or []:
            if ref not in segments:
                raise DialectError(f"provenance segment unknown to the evidence index: {ref}")
    unmapped = node_ids - set(provenance.get("nodes") or {})
    if unmapped:
        raise DialectError(f"nodes without provenance: {sorted(unmapped)}")
    for quiz in document["quizzes"]:
        if quiz["owner_node"] not in node_ids:
            raise DialectError(f"{quiz['quiz_id']}: owner node missing in this lesson")
    return True


def render_html(document, *, title, lang="ar", direction="rtl"):
    """Minimal static RTL-first HTML. Quiz answers/rationales/feedback are
    deliberately NOT emitted (F14): the static bundle cannot promise exam
    secrecy, so it ships no answers at all."""
    parts = [
        f"<!doctype html>\n<html lang=\"{_escape(lang)}\" dir=\"{_escape(direction)}\">\n<head>",
        "<meta charset=\"utf-8\">",
        f"<title>{_escape(title)}</title>",
        "</head>\n<body>\n<main>",
        f"<h1>{_escape(title)}</h1>",
    ]
    quiz_by_node = {}
    for quiz in document["quizzes"]:
        quiz_by_node.setdefault(quiz["owner_node"], []).append(quiz)
    for node in document["nodes"]:
        parts.append(f"<section id=\"{_escape(node['node_id'])}\">")
        for paragraph in node["text"].split("\n\n"):
            if paragraph.strip():
                parts.append(f"<p>{_escape(paragraph.strip())}</p>")
        for quiz in quiz_by_node.get(node["node_id"], []):
            parts.append(f"<form class=\"quiz\" data-quiz-id=\"{_escape(quiz['quiz_id'])}\">")
            parts.append(f"<p class=\"quiz-prompt\">{_escape(quiz['prompt'])}</p>")
            for choice_index, choice in enumerate(quiz["choices"]):
                parts.append(
                    f"<label><input type=\"radio\" name=\"{_escape(quiz['quiz_id'])}\""
                    f" value=\"{choice_index}\"> {_escape(choice)}</label>"
                )
            parts.append("</form>")
            parts.append("</section>")
    parts.append("</main>\n</body>\n</html>\n")
    html = "\n".join(parts)
    assert_no_answer_leak(html, document)
    return html


def assert_no_answer_leak(html, document):
    """Deterministic guard: the answer index, rationale, and feedback must
    never appear in the rendered HTML. (The answer choice's text legitimately
    appears as one of the displayed choices; which one is correct must not.)"""
    for quiz in document["quizzes"]:
        if "data-answer" in html or '"answer"' in html or f"value=\"{quiz['answer']}\"></input>" in html:
            raise DialectError(f"{quiz['quiz_id']}: the answer marker leaked into the HTML")
        if quiz["rationale"] and _escape(quiz["rationale"]) in html:
            raise DialectError(f"{quiz['quiz_id']}: the rationale leaked into the HTML")
        if quiz["feedback"] and _escape(quiz["feedback"]) in html:
            raise DialectError(f"{quiz['quiz_id']}: the feedback leaked into the HTML")
    return True
