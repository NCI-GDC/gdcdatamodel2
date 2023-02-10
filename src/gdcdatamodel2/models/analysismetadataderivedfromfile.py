from typing import List, Callable

import psqlgraph

from .helpers import base, related_cases


class AnalysisMetadataDerivedFromFile(base.Edge):
    __tablename__: str = "edge_analysismetadataderivedfromfile"

    __label__: str = "derived_from"
    __dst_class__: str = "File"
    __dst_table__: str = "node_file"
    __src_class__: str = "AnalysisMetadata"
    __src_table__: str = "node_analysismetadata"

    __dst_src_assoc__: str = "analysis_metadata_files"
    __src_dst_assoc__: str = "files"

    _session_hooks_before_insert: List[
        Callable
    ] = psqlgraph.Edge._session_hooks_before_insert + [
        related_cases.cache_related_cases_on_insert
    ]

    _session_hooks_before_update: List[
        Callable
    ] = psqlgraph.Edge._session_hooks_before_update + [
        related_cases.cache_related_cases_on_update
    ]

    _session_hooks_before_delete: List[
        Callable
    ] = psqlgraph.Edge._session_hooks_before_delete + [
        related_cases.cache_related_cases_on_delete
    ]

    @classmethod
    def post_process(cls) -> None:
        pass
