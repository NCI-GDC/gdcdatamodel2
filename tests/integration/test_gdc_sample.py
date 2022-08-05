import psqlgraph
import pytest
from _pytest import fixtures
from sqlalchemy.orm.attributes import flag_modified

from gdcdatamodel2 import models


@pytest.fixture()
def sample_data(gdc_sample_data: fixtures.FixtureFunction) -> None:
    gdc_sample_data("gdc_sample.json")


def test_query_by_node_type(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        demographic = gdc_graph.nodes(models.Demographic).one()
        assert demographic.submitter_id == "demographic_x1"


def test_query_by_property(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        sample_y1 = gdc_graph.nodes().props(submitter_id="sample_y1").one()
        assert sample_y1.sample_type == "Additional Metastatic"


def test_traverse(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        case_x1 = gdc_graph.nodes(models.Case).props(submitter_id="case_x1").one()
        assert len(list(case_x1.traverse())) == 35


# def test_counts(
#     sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
# ) -> None:
#     with gdc_graph.session_scope():
#         assert gdc_graph.nodes().count() == 18
#         assert gdc_graph.nodes().props(project_id="GDC-MISC").count() == 16
#         assert gdc_graph.nodes(models.Project).count() == 1
#         assert gdc_graph.nodes(models.AlignedReads).count() == 4
#
#
# def test_path(
#     sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
# ) -> None:
#     with gdc_graph.session_scope():
#         aligned_reads = (
#             gdc_graph.nodes(models.AlignedReads)
#             .path("harmonization_workflows")
#             .props(workflow_type="miRNA Harmonization and Quantification")
#             .one()
#         )
#         assert aligned_reads.submitter_id == "ar_3"
#         aligned_reads = (
#             gdc_graph.nodes(models.AlignedReads)
#             .path("bamqc_extraction_workflows.bamqc_metrics")
#             .one()
#         )
#         assert aligned_reads.submitter_id == "ar_2"
#
#
# def test_create_and_read(
#     sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
# ) -> None:
#     with gdc_graph.session_scope() as s:
#         aliquot = models.Aliquot("aliquot_1", submitter_id="aliquot_submitter_1")
#         read_group = gdc_graph.nodes(models.ReadGroup).one()
#         aliquot.read_groups = [read_group]
#         s.add(aliquot)
#
#         read_group = gdc_graph.nodes(models.ReadGroup).one()
#         assert len(read_group.aliquots) == 1
#         assert read_group.aliquots[0].node_id == "aliquot_1"
#
#
# def test_update(
#     sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
# ) -> None:
#     with gdc_graph.session_scope():
#         ar0 = gdc_graph.nodes(models.AlignedReads).props(submitter_id="ar_0").one()
#         assert ar0.experimental_strategy == "WGS"
#
#         ar0.experimental_strategy = "WXS"
#         flag_modified(ar0, "_props")
#
#         ar0 = gdc_graph.nodes(models.AlignedReads).props(submitter_id="ar_0").one()
#         assert ar0.experimental_strategy == "WXS"
#
#
# def test_delete(
#     sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
# ) -> None:
#     with gdc_graph.session_scope() as s:
#         ar0 = gdc_graph.nodes(models.AlignedReads).props(submitter_id="ar_0").one()
#         s.delete(ar0)
#         s.commit()
#
#         ar0 = gdc_graph.nodes(models.AlignedReads).props(submitter_id="ar_0").one_or_none()
#         assert ar0 is None
