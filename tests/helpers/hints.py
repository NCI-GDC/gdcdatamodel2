from typing import Dict, List, Optional

from tests.helpers.typing_compat import TypedDict


class EdgeData(TypedDict):
    src: str
    dst: str


class NodeData(TypedDict, total=False):
    label: str
    state: str
    submitter_id: str


class GraphData(TypedDict, total=False):
    nodes: List[NodeData]
    edges: List[EdgeData]
    extends: Optional[str]
    summary: Dict[str, int]
    description: str
