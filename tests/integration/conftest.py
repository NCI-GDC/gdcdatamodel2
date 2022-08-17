from typing import List, Optional, Union

import psqlgraph
import pytest
from gdcdictionary import gdcdictionary

from gdcdatamodel2 import models
from tests.helpers import db, hints

SAMPLE_PROGRAM = "GDC"
SAMPLE_PROJECT = "MISC"


@pytest.fixture(scope="session")
def gdc_graph() -> psqlgraph.PsqlGraphDriver:
    graph = db.init_graph(use_gpas=False)
    db.create_ng_tables(graph.engine)

    yield graph

    db.truncate_ng_tables(graph.engine)
    db.tear_down_graph(graph)


@pytest.fixture()
def gdc_graph_mock(gdc_graph: psqlgraph.PsqlGraphDriver) -> db.GraphDataGenerator:
    """
    Provides a more generic entry point to creating mock graph data for testing
    Returns:
        A function for generating list of mocked nodes
    """
    data_cache = db.SampleDataCache(gdc_graph)

    def mock_graph(
        graph_data: hints.GraphData,
        extension: Optional[db.DataLoaderExtension] = None,
    ) -> List[models.Node]:
        extension = extension or db.DataLoaderExtension(g=gdc_graph)
        x_nodes = db.mock_data(
            gdc_graph,
            gdcdictionary,
            graph_data["nodes"],
            graph_data["edges"],
            extension=extension,
        )

        data_cache.nodes.extend(x_nodes)
        return data_cache.nodes

    yield mock_graph

    data_cache.finalize()


@pytest.fixture()
def gdc_sample_data(
    gdc_graph: psqlgraph.PsqlGraphDriver, gdc_graph_mock: db.GraphDataGenerator
) -> db.GraphDataGenerator:
    def mock_from_file(
        resource: Union[str, hints.GraphData],
        extension: Optional[db.DataLoaderExtension] = None,
    ) -> List[models.Node]:
        db.drop_graph_entries(gdc_graph, is_gpas=False)
        _graph_data = db.load_data_file(resource) if isinstance(resource, str) else resource
        return gdc_graph_mock(_graph_data, extension)

    return mock_from_file
