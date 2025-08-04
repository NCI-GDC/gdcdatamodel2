from __future__ import annotations

import os
import typing
from collections.abc import Iterator

import psqlgraph
import pytest
import sqlalchemy
from testcontainers import postgres

from gdcdatamodel2 import models
from gdcdatamodel2.partial_dictionary import utils
from tests.helpers import db, hints

SAMPLE_PROGRAM = "GDC"
SAMPLE_PROJECT = "MISC"


@pytest.fixture(scope="session")
def pg_container() -> typing.Generator[sqlalchemy.engine.Engine | None, None, None]:
    if os.getenv("CI_COMMIT_REF_NAME"):
        # disable test containers in gitlab ci
        yield None
        return
    with postgres.PostgresContainer("postgres:13") as pg:
        engine = sqlalchemy.create_engine(pg.get_connection_url())
        yield engine
        engine.dispose()


@pytest.fixture(scope="session")
def gdc_graph(pg_container: sqlalchemy.engine.Engine) -> Iterator[psqlgraph.PsqlGraphDriver]:
    graph = db.init_graph(pg_container)

    yield graph

    db.tear_down_graph(graph)


@pytest.fixture()
def gdc_graph_mock(
    gdc_graph: psqlgraph.PsqlGraphDriver,
) -> Iterator[db.GraphDataGenerator]:
    """
    Provides a more generic entry point to creating mock graph data for testing
    Returns:
        A function for generating list of mocked nodes
    """
    data_cache = db.SampleDataCache(gdc_graph)

    partial_dictionary = utils.get_partial_dictionary()

    def mock_graph(
        graph_data: str | hints.GraphData,
        extension: db.DataLoaderExtension | None = None,
    ) -> list[models.Node]:
        extension = extension or db.DataLoaderExtension(g=gdc_graph)
        x_nodes = db.mock_data(
            gdc_graph,
            partial_dictionary,
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
        graph_data: str | hints.GraphData,
        extension: db.DataLoaderExtension | None = None,
    ) -> list[models.Node]:
        db.drop_graph_entries(gdc_graph)
        _graph_data = (
            db.load_data_file(graph_data) if isinstance(graph_data, str) else graph_data
        )
        return gdc_graph_mock(_graph_data, extension)

    return mock_from_file
