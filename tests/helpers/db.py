from __future__ import annotations

import dataclasses
import json
import os
import uuid
import warnings
from importlib import resources
from typing import Protocol

import psqlgraph
import yaml
from psqlgraph import ext, hydrator, voided
from sqlalchemy import MetaData
from sqlalchemy import exc as sa_exc

from gdcdatamodel2 import models
from gdcdatamodel2.partial_dictionary import utils
from tests.helpers import hints

SAMPLE_PROGRAM = "GDC"
SAMPLE_PROJECT = "MISC"
PROJECT_ID = f"{SAMPLE_PROGRAM}-{SAMPLE_PROJECT}"


@dataclasses.dataclass()
class DataLoaderExtension:
    """Extends the mock data loading function to allow for adding custom functionality while generating mocks"""

    g: psqlgraph.PsqlGraphDriver
    project: models.Node | None = dataclasses.field(default=None)

    def pre(self) -> None:
        """Runs just before creating the mocks"""

        self.project = add_sample_project(self.g, "GDC", "MISC")

    def run(self, node: models.Node) -> None:
        """Runs just before merging the generated node"""

        if hasattr(node, "projects"):
            node.projects.append(self.project)
        if hasattr(node, "state"):
            node.state = "submitted"
        if hasattr(node, "project_id"):
            node.project_id = "GDC-MISC"

    def post(self) -> None: ...


def init_graph() -> psqlgraph.PsqlGraphDriver:
    """
    Initializes a psqlgraph driver for the given namespace

    Returns:
        PsqlGraphDriver: instance of psqlgraph driver
    """
    graph = psqlgraph.PsqlGraphDriver(
        os.getenv("PG_HOST", "localhost"),
        os.getenv("PG_USER", "test"),
        os.getenv("PG_PASS", "test"),
        os.getenv("PG_NAME", "gdcdatamodel2"),
    )

    # Make sure to start with a clean DB
    tear_down_graph(graph)

    psqlgraph.create_all(graph.engine)

    return graph


def add_sample_project(
    g: psqlgraph.PsqlGraphDriver,
    program_name: str = SAMPLE_PROGRAM,
    project_code: str = SAMPLE_PROJECT,
    phs_id: str = "phs000335",
) -> models.Node:
    """Adds a sample project"""

    with g.session_scope():
        project = g.nodes(models.Project).props(code=project_code).one_or_none()
        if project:
            return project

        # create program
        program = models.Program(node_id=str(uuid.uuid4()))
        program.dbgap_accession_number = phs_id
        program.name = program_name

        project = models.Project(node_id=str(uuid.uuid4()))
        project.code = project_code
        project.dbgap_accession_number = phs_id
        program.projects.append(project)
        g.node_insert(program)

        return project


def tear_down_graph(graph: psqlgraph.PsqlGraphDriver) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        m = MetaData(graph.engine)
        m.reflect()
        for tbl in reversed(m.sorted_tables):
            graph.engine.execute(tbl.delete())

        # close connection to database
        graph.engine.dispose()


def load_data_file(source: str, source_type: str = "json") -> hints.GraphData:
    source_type = source_type if source.endswith(".json") else "yaml"
    with (resources.files("tests") / f"data/{source}").open() as js:
        payload: hints.GraphData = (
            yaml.safe_load(js) if source_type == "yaml" else json.loads(js.read())
        )
    extended_path = payload.pop("extends", None)
    if extended_path:
        extended = load_data_file(source=extended_path)
        payload["nodes"].extend(extended["nodes"])
        payload["edges"].extend(extended["edges"])

    return payload


def mock_data(
    pg_driver: psqlgraph.PsqlGraphDriver,
    active_dictionary: utils.PartialDictionary,
    nodes: list[hints.NodeData],
    edges: list[hints.EdgeData],
    extension: DataLoaderExtension,
) -> list[models.Node]:
    gdc_factory = graph_factory(active_dictionary)

    extension.pre()
    with pg_driver.session_scope(can_inherit=False) as s:
        s.autoflush = False
        x_nodes = gdc_factory.create_from_nodes_and_edges(
            nodes=nodes, edges=edges, unique_key="submitter_id", all_props=True
        )
        for n in x_nodes:
            extension.run(node=n)
            s.add(n)
    extension.post()
    return x_nodes


def graph_factory(
    active_dictionary: utils.PartialDictionary,
    program_name: str = SAMPLE_PROGRAM,
    project_code: str = SAMPLE_PROJECT,
) -> hydrator.GraphFactory:
    global_props = {
        "properties": {
            "project_id": f"{program_name}-{project_code}",
            "state": "submitted",
        }
    }
    factory = hydrator.GraphFactory(
        models=models, dictionary=active_dictionary, graph_globals=global_props
    )
    return factory


def drop_graph_entries(pg_driver: psqlgraph.PsqlGraphDriver) -> None:
    base = ext.get_orm_base(None)

    with pg_driver.engine.begin() as txn:
        for table in reversed(
            base.metadata.sorted_tables + voided.Base.metadata.sorted_tables
        ):
            # do not clear schema versions so each test does not re-trigger migration.
            txn.execute(f"TRUNCATE {table.name} CASCADE;")


@dataclasses.dataclass()
class SampleDataCache:
    g: psqlgraph.PsqlGraphDriver
    nodes: list[models.Node] = dataclasses.field(default_factory=list)

    def finalize(self):
        tear_down_graph(self.g)


class GraphDataGenerator(Protocol):
    def __call__(
        self,
        graph_data: str | hints.GraphData,
        extension: DataLoaderExtension | None = None,
    ) -> list[models.Node]: ...
