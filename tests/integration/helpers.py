import warnings
from typing import Any, Dict, Iterable, List, Optional

try:
    from typing import Literal, Protocol, TypedDict
except ImportError:
    from typing_extensions import Literal, Protocol, TypedDict

import psqlgraph
from psqlgraph import ext
from psqlgraph.base import ORMBase, VoidedBase
from sqlalchemy import MetaData
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm.attributes import flag_modified

UniqueIdLiteral = Literal["node_id", "submitter_id"]


class EdgeData(TypedDict):
    src: str
    dst: str
    label: str


class NodeData(TypedDict):
    label: str
    node_id: str
    submitter_id: str
    properties: Dict[str, Any]
    system_annotations: Dict[str, Any]


class GraphData(TypedDict):
    nodes: List[NodeData]
    edges: List[EdgeData]


class ExtensibleGraphData(GraphData, total=False):
    extends: Optional[str]


class ResourceLoader(Protocol):
    def __call__(self, source: str, source_type: Optional[str] = "json") -> ExtensibleGraphData:
        ...


class Node(Protocol):
    tag: str
    ver: int
    acl: List[str]
    label: str
    node_id: str
    gdc_uuid: Optional[str]
    submitter_id: str
    sysan: Dict[str, Any]
    system_annotations: Dict[str, Any]
    edges_in: Iterable["Edge"]
    edges_out: Iterable["Edge"]

    gencode_version: str
    props: Dict[str, Any]
    _dictionary: Dict[str, Any]

    def traverse(
        self, edge_pointer: str = "in", mode: Literal["bfs", "dfs"] = "bfs", edge_predicate=None
    ) -> Iterable["Node"]:
        ...

    def to_json(self) -> Dict[str, Any]:
        ...

    def __getitem__(self, item: str) -> Any:
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        ...

    def is_taggable(self) -> bool:
        ...


def update_mocked_system_annotations(
    g: psqlgraph.PsqlGraphDriver,
    unique_key: UniqueIdLiteral,
    nodes: Iterable[Node],
    node_data: Dict[str, "NodeData"],
) -> None:
    """Force sysan values to exactly what was specified in the test data

    sysan values like ver, tag and latest are autogenerate so ignores what was specified in the test data.
    This function resets those values to what was specified in the test data.
    """
    with g.session_scope():
        for n in nodes:
            node = g.nodes().get(n.node_id)
            meta = node_data[node[unique_key]]
            sysans = meta.get("system_annotations")
            if not sysans:
                continue

            node.sysan.update(sysans)
            flag_modified(node, "_sysan")


def tear_down_graph(graph: psqlgraph.PsqlGraphDriver) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        m = MetaData(graph.engine)
        m.reflect()
        for tbl in reversed(m.sorted_tables):
            graph.engine.execute(tbl.delete())

        # close connection to database
        graph.engine.dispose()


def drop_graph_entries(pg_driver):
    base = ext.get_orm_base("gpas") if pg_driver.package_namespace == "gpas" else ORMBase
    with pg_driver.engine.begin() as txn:
        for table in reversed(base.metadata.sorted_tables + VoidedBase.metadata.sorted_tables):
            # do not clear schema versions so each test does not re-trigger migration.
            txn.execute(f"TRUNCATE {table.name} CASCADE;")
