import uuid

from gdcdatamodel2 import models, validators
from tests import MockSubmissionEntity


def create_node(gdc_graph, doc, session):
    cls = models.Node.get_subclass(doc["type"])
    node = cls(str(uuid.uuid4()))
    node.props = doc["props"]
    for key, value in doc["edges"].items():
        for target_id in value:
            edge = gdc_graph.nodes().ids(target_id).first()
            node[key].append(edge)
    session.add(node)
    return node


def update_schema(graph_validator, entity, key, schema):
    graph_validator.schemas.schema[entity][key] = schema


def test_graph_validator_without_required_link(gdc_graph):
    graph_validator = validators.GDCGraphValidator()
    entities = [MockSubmissionEntity()]

    with gdc_graph.session_scope() as session:
        node = create_node(
            gdc_graph,
            {"type": "aliquot", "props": {"submitter_id": "test"}, "edges": {}},
            session,
        )
        entities[0].node = node
        update_schema(
            graph_validator,
            "aliquot",
            "links",
            [
                {
                    "name": "analytes",
                    "backref": "aliquots",
                    "label": "derived_from",
                    "multiplicity": "many_to_one",
                    "target_type": "analyte",
                    "required": True,
                }
            ],
        )
        graph_validator.record_errors(gdc_graph, entities)
        assert entities[0].errors[0]["keys"] == ["analytes"]


def test_graph_validator_with_exclusive_link(gdc_graph):
    graph_validator = validators.GDCGraphValidator()
    entities = [MockSubmissionEntity()]

    with gdc_graph.session_scope() as session:
        analyte = create_node(
            gdc_graph,
            {
                "type": "analyte",
                "props": {"submitter_id": "test", "analyte_type_id": "D", "analyte_type": "DNA"},
                "edges": {},
            },
            session,
        )
        sample = create_node(
            gdc_graph,
            {
                "type": "sample",
                "props": {"submitter_id": "test", "sample_type": "DNA", "sample_type_id": "01"},
                "edges": {},
            },
            session,
        )

        node = create_node(
            gdc_graph,
            {
                "type": "aliquot",
                "props": {"submitter_id": "test"},
                "edges": {"analytes": [analyte.node_id], "samples": [sample.node_id]},
            },
            session,
        )
        entities[0].node = node
        update_schema(
            graph_validator,
            "aliquot",
            "links",
            [
                {
                    "exclusive": True,
                    "required": True,
                    "subgroup": [
                        {
                            "name": "analytes",
                            "backref": "aliquots",
                            "label": "derived_from",
                            "multiplicity": "many_to_one",
                            "target_type": "analyte",
                        },
                        {
                            "name": "samples",
                            "backref": "aliquots",
                            "label": "derived_from",
                            "multiplicity": "many_to_one",
                            "target_type": "sample",
                        },
                    ],
                }
            ],
        )
        graph_validator.record_errors(gdc_graph, entities)
        assert entities[0].errors[0]["keys"] == ["analytes", "samples"]
