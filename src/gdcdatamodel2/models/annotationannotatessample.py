from typing import Callable, List

import psqlgraph

from .helpers import base, related_cases


class AnnotationAnnotatesSample(base.Edge):

    __tablename__: str = "edge_annotationannotatessample"
    __table_args__ = {"extend_existing": True}

    __label__: str = "annotates"
    __dst_class__: str = "Sample"
    __dst_table__: str = "node_sample"
    __src_class__: str = "Annotation"
    __src_table__: str = "node_annotation"

    __dst_src_assoc__: str = "annotations"
    __src_dst_assoc__: str = "samples"

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
