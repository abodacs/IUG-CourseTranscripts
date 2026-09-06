"""CF-05 checks: graph.json schema, typed edges, provenance, acyclicity."""
import pytest

from src.factory.graph import GraphError, validate_graph


def evidence_index():
    return {"videos": {"AAAAAAAAAAA": {"segments": [
        {"segment_id": "AAAAAAAAAAA:seg:0000"},
        {"segment_id": "AAAAAAAAAAA:seg:0001"},
    ]}}}


def graph(nodes=None, edges=None, **edge_overrides):
    edge = {
        "edge_id": "e-1",
        "edge_type": "prerequisite",
        "source": "opto2311:concept:thin-lens-equation",
        "target": "opto2311:concept:lens-combination",
        "provenance_refs": ["AAAAAAAAAAA:seg:0000"],
    }
    edge.update(edge_overrides)
    return {
        "nodes": nodes if nodes is not None else [
            {"node_id": "opto2311:concept:thin-lens-equation", "kind": "concept",
             "title": "معادلة العدسة الرقيقة", "evidence_refs": ["AAAAAAAAAAA:seg:0000"]},
            {"node_id": "opto2311:concept:lens-combination", "kind": "concept",
             "title": "تجميع العدسات", "evidence_refs": ["AAAAAAAAAAA:seg:0001"]},
        ],
        "edges": edges if edges is not None else [edge],
    }


def test_valid_graph_passes():
    assert validate_graph(graph(), evidence_index()) == graph()


def test_bad_node_ids_and_kinds_rejected():
    with pytest.raises(GraphError, match="must look like"):
        validate_graph(graph(nodes=[{"node_id": "lens", "kind": "concept", "title": "t"}]), evidence_index())
    with pytest.raises(GraphError, match="kind must be"):
        validate_graph(graph(nodes=[{"node_id": "opto2311:concept:lens", "kind": "widget", "title": "t"}]),
                       evidence_index())
    with pytest.raises(GraphError, match="duplicated"):
        validate_graph(graph(nodes=[
            {"node_id": "opto2311:concept:lens", "kind": "concept", "title": "t"},
            {"node_id": "opto2311:concept:lens", "kind": "concept", "title": "t2"},
        ]), evidence_index())


def test_edges_must_reference_known_nodes_and_types():
    with pytest.raises(GraphError, match="edge_type must be"):
        validate_graph(graph(edge_type="causes"), evidence_index())
    with pytest.raises(GraphError, match="source node unknown"):
        validate_graph(graph(source="opto2311:concept:ghost"), evidence_index())
    with pytest.raises(GraphError, match="self-loop"):
        validate_graph(graph(source="opto2311:concept:thin-lens-equation",
                             target="opto2311:concept:thin-lens-equation"), evidence_index())


def test_provenance_must_resolve():
    with pytest.raises(GraphError, match="unknown to the index"):
        validate_graph(graph(provenance_refs=["ZZZZZZZZZZZ:seg:0000"]), evidence_index())


def test_prerequisite_edges_must_cite_evidence():
    with pytest.raises(GraphError, match="must cite evidence"):
        validate_graph(graph(provenance_refs=[]), evidence_index())


def test_relates_to_needs_no_evidence_but_still_validates_nodes():
    g = graph(edge_type="relates_to", provenance_refs=[])
    assert validate_graph(g, evidence_index()) == g


def test_prerequisite_cycles_are_rejected():
    g = graph()
    g["nodes"].append({"node_id": "opto2311:concept:third", "kind": "concept", "title": "ثالث"})
    g["edges"] = [
        {"edge_id": "e-1", "edge_type": "prerequisite",
         "source": "opto2311:concept:thin-lens-equation",
         "target": "opto2311:concept:lens-combination", "provenance_refs": ["AAAAAAAAAAA:seg:0000"]},
        {"edge_id": "e-2", "edge_type": "prerequisite",
         "source": "opto2311:concept:lens-combination",
         "target": "opto2311:concept:third", "provenance_refs": ["AAAAAAAAAAA:seg:0001"]},
        {"edge_id": "e-3", "edge_type": "prerequisite",
         "source": "opto2311:concept:third",
         "target": "opto2311:concept:thin-lens-equation", "provenance_refs": ["AAAAAAAAAAA:seg:0001"]},
    ]
    with pytest.raises(GraphError, match="cycle"):
        validate_graph(g, evidence_index())
