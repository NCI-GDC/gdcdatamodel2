from __future__ import annotations

from typing import TypedDict


class EdgeData(TypedDict):
    src: str
    dst: str


class NodeData(TypedDict, total=False):
    label: str
    state: str
    submitter_id: str


class GraphData(TypedDict, total=False):
    nodes: list[NodeData]
    edges: list[EdgeData]
    extends: str | None
    summary: dict[str, int]
    description: str
