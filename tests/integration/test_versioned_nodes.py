import psqlgraph
import pytest

from gdcdatamodel2 import models, versioned_nodes


@pytest.fixture
def portion():
    portion = models.Portion(
        **{
            "node_id": "case1",
            "is_ffpe": False,
            "portion_number": "01",
            "project_id": "CGCI-BLGSP",
            "state": "validated",
            "submitter_id": "PORTION-1",
            "weight": 54.0,
        }
    )
    portion.acl = ["acl1"]
    portion.sysan.update({"key1": "val1"})
    return portion


@pytest.fixture
def analyte():
    return models.Analyte(
        **{
            "node_id": "analyte1",
            "analyte_type": "Repli-G (Qiagen) DNA",
            "analyte_type_id": "W",
            "project_id": "CGCI-BLGSP",
            "state": "validated",
            "submitter_id": "TCGA-AR-A1AR-01A-31W",
        }
    )


def test_round_trip(
    gdc_graph: psqlgraph.PsqlGraphDriver, portion: psqlgraph.Node, analyte: psqlgraph.Node
):
    with gdc_graph.session_scope() as session:
        portion.analytes = [analyte]
        session.add(portion)

    with gdc_graph.session_scope() as session:
        portion = gdc_graph.nodes(models.Portion).one()
        v_node = versioned_nodes.VersionedNode.clone(portion)
        session.add(v_node)

    with gdc_graph.session_scope():
        v_node = gdc_graph.nodes(versioned_nodes.VersionedNode).one()

    assert v_node.properties["is_ffpe"] is False
    assert v_node.properties["state"] == "validated"
    assert v_node.system_annotations == {"key1": "val1"}
    assert v_node.acl == ["acl1"]
    assert v_node.neighbors == ["analyte1"]
    assert v_node.versioned is not None
    assert v_node.key is not None
