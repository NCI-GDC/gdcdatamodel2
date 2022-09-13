from typing import Callable, List

import psqlgraph

from .helpers import base, related_cases


class CaseProcessedAtTissueSourceSite(base.Edge):

    __tablename__: str = "edge_caseprocessedattissuesourcesite"
    __table_args__ = {"extend_existing": True}

    __label__: str = "processed_at"
    __dst_class__: str = "TissueSourceSite"
    __dst_table__: str = "node_tissuesourcesite"
    __src_class__: str = "Case"
    __src_table__: str = "node_case"

    __dst_src_assoc__: str = "cases"
    __src_dst_assoc__: str = "tissue_source_sites"

    _session_hooks_before_insert: List[Callable] = psqlgraph.Edge._session_hooks_before_insert + [
        related_cases.cache_related_cases_on_insert
    ]

    _session_hooks_before_update: List[Callable] = psqlgraph.Edge._session_hooks_before_update + [
        related_cases.cache_related_cases_on_update
    ]

    _session_hooks_before_delete: List[Callable] = psqlgraph.Edge._session_hooks_before_delete + [
        related_cases.cache_related_cases_on_delete
    ]

    @classmethod
    def post_process(cls) -> None:
        pass
