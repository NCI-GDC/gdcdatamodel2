import json
import os
import uuid
import warnings
from typing import List, Optional, Union

import attr
import pkg_resources
import psqlgraph
import yaml
from psqlgraph import create_all, ext, mocks
from psqlgraph.base import ORMBase, VoidedBase
from sqlalchemy import MetaData, engine
from sqlalchemy import exc as sa_exc

from gdcdatamodel2 import models
from tests.helpers import hints, typing_compat

SAMPLE_PROGRAM = "GDC"
SAMPLE_PROJECT = "MISC"
PROJECT_ID = f"{SAMPLE_PROGRAM}-{SAMPLE_PROJECT}"


@attr.s(auto_attribs=True)
class DataLoaderExtension:
    """Extends the mock data loading function to allow for adding custom functionality while generating mocks"""

    g: psqlgraph.PsqlGraphDriver
    gpas: bool = False
    project: models.Node = attr.ib(default=None, init=False)

    def pre(self) -> None:
        """Runs just before creating the mocks"""

        self.project = add_sample_project(self.g, "GDC", "MISC", self.gpas)

    def run(self, node: models.Node) -> None:
        """Runs just before merging the generated node"""

        if hasattr(node, "projects"):
            node.projects.append(self.project)
        if hasattr(node, "state"):
            node.state = "submitted"
        if hasattr(node, "project_id"):
            node.project_id = "GDC-MISC"

    def post(self) -> None:
        ...


@attr.s(auto_attribs=True)
class GpasDataLoaderExtension(DataLoaderExtension):
    """GPAS specific mock extension"""

    gpas: bool = True

    def run(self, node: models.Node) -> None:
        super().run(node)
        if hasattr(node, "gdc_uuid"):
            node.gdc_uuid = None


def init_graph(use_gpas: bool = False) -> psqlgraph.PsqlGraphDriver:
    """
    Initializes a psqlgraph driver for the given namespace
    Args:
        use_gpas: False defaults to GDC, True for biograph
    Returns:
        PsqlGraphDriver: instance of psqlgraph driver
    """
    env = "BIO_" if use_gpas else ""
    ns = "gpas" if use_gpas else None
    graph = psqlgraph.PsqlGraphDriver(
        os.environ[f"{env}PG_HOST"],
        os.environ[f"{env}PG_USER"],
        os.environ[f"{env}PG_PASS"],
        os.environ[f"{env}PG_NAME"],
        package_namespace=ns,
    )

    # Make sure to start with a clean DB
    tear_down_graph(graph)

    base = ext.get_orm_base(ns) if use_gpas else ORMBase
    create_all(graph.engine, base=base)
    return graph


def add_sample_project(
    g: psqlgraph.PsqlGraphDriver,
    program_name: str = SAMPLE_PROGRAM,
    project_code: str = SAMPLE_PROJECT,
    use_gpas: bool = False,
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
    with pkg_resources.resource_stream("tests", "data/{}".format(source)) as js:
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
    active_dictionary: hints.DictionaryType,
    nodes: List[hints.NodeData],
    edges: List[hints.EdgeData],
    extension: DataLoaderExtension,
) -> List[models.Node]:
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
    active_dictionary: hints.DictionaryType,
    program_name: str = SAMPLE_PROGRAM,
    project_code: str = SAMPLE_PROJECT,
) -> mocks.GraphFactory:
    global_props = {
        "properties": {
            "project_id": f"{program_name}-{project_code}",
            "state": "submitted",
        }
    }
    factory = mocks.GraphFactory(
        models=models, dictionary=active_dictionary, graph_globals=global_props
    )
    return factory


def drop_graph_entries(pg_driver: psqlgraph.PsqlGraphDriver, is_gpas: bool = True) -> None:
    base = ext.get_orm_base("gpas") if is_gpas else ORMBase
    with pg_driver.engine.begin() as txn:
        for table in reversed(base.metadata.sorted_tables + VoidedBase.metadata.sorted_tables):
            # do not clear schema versions so each test does not re-trigger migration.
            txn.execute("TRUNCATE {} CASCADE;".format(table.name))


@attr.s
class SampleDataCache(object):
    g = attr.ib(type=psqlgraph.PsqlGraphDriver)
    nodes: List[models.Node] = attr.ib(default=attr.Factory(list))

    def finalize(self):
        tear_down_graph(self.g)


class GraphDataGenerator(typing_compat.Protocol):
    def __call__(
        self,
        resource: Union[str, hints.GraphData],
        extension: Optional[DataLoaderExtension] = None,
    ) -> List[models.Node]:
        ...
