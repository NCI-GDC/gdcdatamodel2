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
        assert len(list(case_x1.traverse())) == 38


def test_counts(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        assert gdc_graph.nodes().count() == 44
        assert gdc_graph.nodes().props(project_id="GDC-MISC").count() == 42
        assert gdc_graph.nodes(models.Project).count() == 1
        assert gdc_graph.nodes(models.AlignedReads).count() == 4


def test_path(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        aliquot = (
            gdc_graph.nodes(models.Aliquot)
            .path("samples")
            .props(sample_type="Additional Metastatic")
            .one()
        )
        assert aliquot.submitter_id == "aliquot_y1"

        case = (
            gdc_graph.nodes(models.Case).path("samples.aliquots").ids("aliquot_y1-node_id").one()
        )
        assert case.submitter_id == "case_y1"


def test_create_and_read(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope() as s:
        aliquot = models.Aliquot("aliquot_x4", submitter_id="aliquot_submitter_x4")
        sample = gdc_graph.nodes(models.Sample).props(submitter_id="sample_x4").one()
        aliquot.samples = [sample]
        s.add(aliquot)

        sample = gdc_graph.nodes(models.Sample).props(submitter_id="sample_x4").one()
        assert len(sample.aliquots) == 1
        assert sample.aliquots[0].node_id == "aliquot_x4"


def test_update(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope():
        aliquot = gdc_graph.nodes(models.Aliquot).props(submitter_id="aliquot_x2").one()
        assert aliquot.no_matched_normal_wgs is False

        aliquot.no_matched_normal_wgs = True
        flag_modified(aliquot, "_props")

        aliquot = gdc_graph.nodes(models.Aliquot).props(submitter_id="aliquot_x2").one()
        assert aliquot.no_matched_normal_wgs is True


def test_delete(
    sample_data: fixtures.FixtureFunction, gdc_graph: psqlgraph.PsqlGraphDriver
) -> None:
    with gdc_graph.session_scope() as s:
        ari_x3 = (
            gdc_graph.nodes(models.AlignedReadsIndex)
            .props(submitter_id="aligned_reads_index_x3")
            .one()
        )
        ar_x3 = (
            gdc_graph.nodes(models.AlignedReads)
            .props(submitter_id="aligned_reads_x3")
            .one_or_none()
        )
        assert len(ar_x3.aligned_reads_indexes) == 1
        s.delete(ari_x3)
        s.commit()

        ari_x3 = (
            gdc_graph.nodes(models.AlignedReadsIndex)
            .props(submitter_id="aligned_reads_index_x3")
            .one_or_none()
        )
        assert ari_x3 is None
        ar_x3 = (
            gdc_graph.nodes(models.AlignedReads)
            .props(submitter_id="aligned_reads_x3")
            .one_or_none()
        )
        assert len(ar_x3.aligned_reads_indexes) == 0
