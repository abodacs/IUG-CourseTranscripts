"""CF-05: the knowledge-graph layer — graph.json schema and validators.

Nodes are stable-ID concepts/lessons/skills; edges are typed (prerequisite,
relates_to, mentions) and every edge and node carries provenance references
that must resolve against the CF-02A evidence index. Prerequisite edges must
stay acyclic. This is the machine-checkable source of truth; any OKF export
is a rendering of it (see docs/research/okf-v02-evaluation.md).
"""
import re

EDGE_TYPES = ("prerequisite", "relates_to", "mentions")
NODE_KINDS = ("concept", "lesson", "skill")
NODE_ID_RE = r"[a-z0-9\-]+:(concept|lesson|skill):[a-z0-9\-]+"


class GraphError(ValueError):
    """graph.json violates the schema, references, or prerequisite rules."""


def _require(condition, message):
    if not condition:
        raise GraphError(message)


def validate_graph(graph, evidence_index):
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    _require(nodes, "graph has no nodes")
    known_segments = {
        segment["segment_id"]
        for video in (evidence_index.get("videos") or {}).values()
        for segment in video.get("segments", [])
    }

    node_ids = set()
    for node in nodes:
        node_id = node.get("node_id")
        _require(node_id and node_id not in node_ids, f"node_id missing or duplicated: {node_id!r}")
        _require(
            re.fullmatch(NODE_ID_RE, node_id),
            f"{node_id}: node IDs must look like <course>:<kind>:<name>",
        )
        kind = node.get("kind")
        _require(kind in NODE_KINDS, f"{node_id}: kind must be one of {NODE_KINDS}")
        _require(bool(node.get("title")), f"{node_id}: a title is required")
        for ref in node.get("evidence_refs") or []:
            _require(ref in known_segments, f"{node_id}: evidence segment unknown to the index: {ref}")
        node_ids.add(node_id)

    edge_ids = set()
    prereq_graph = {}
    for edge in edges:
        edge_id = edge.get("edge_id")
        _require(edge_id and edge_id not in edge_ids, f"edge_id missing or duplicated: {edge_id!r}")
        edge_ids.add(edge_id)
        edge_type = edge.get("edge_type")
        _require(edge_type in EDGE_TYPES, f"{edge_id}: edge_type must be one of {EDGE_TYPES}")
        source, target = edge.get("source"), edge.get("target")
        _require(source in node_ids, f"{edge_id}: source node unknown: {source!r}")
        _require(target in node_ids, f"{edge_id}: target node unknown: {target!r}")
        _require(source != target, f"{edge_id}: self-loop on {source}")
        refs = edge.get("provenance_refs") or []
        for ref in refs:
            _require(ref in known_segments, f"{edge_id}: provenance segment unknown to the index: {ref}")
        if edge_type == "prerequisite":
            _require(refs, f"{edge_id}: a prerequisite edge must cite evidence for the ordering")
            prereq_graph.setdefault(target, set()).add(source)
    _require_acyclic_prerequisites(prereq_graph)
    return graph


def _require_acyclic_prerequisites(prereq_graph):
    resolved, stack = set(), set()

    def visit(node):
        if node in resolved:
            return
        _require(node not in stack, f"prerequisite cycle through {node}")
        stack.add(node)
        for parent in prereq_graph.get(node, ()):
            visit(parent)
        stack.discard(node)
        resolved.add(node)

    for node in list(prereq_graph):
        visit(node)
