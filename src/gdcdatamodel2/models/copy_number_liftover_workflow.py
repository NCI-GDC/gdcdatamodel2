from typing import Any, Dict, List, Optional, Union

import psqlgraph
from sqlalchemy.ext import hybrid

from .helpers import base, datetime_hooks, indexes, related_cases, versioning


class CopyNumberLiftoverWorkflow(base.Node):
    __tablename__: str = "node_copynumberliftoverworkflow"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Copy Number Liftover Workflow",
        "namespace": "https://gdc.cancer.gov",
        "category": "analysis",
        "submittable": False,
        "downloadable": False,
        "description": "Metadata for the copy number liftover workflow used to harmonize TCGA copy number data.",
        "required": ["submitter_id", "workflow_link", "workflow_type"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "copy_number_liftover_workflow"

    @property
    def id(self):
        return self.node_id

    @id.setter
    def id(self, value):
        self.node_id = value

    @classmethod
    def post_process(cls) -> None:
        cls.add_secondary_key_indexes()
        cls.populate_pg_backrefs()
        cls.populate_pg_links()
        cls.populate_pg_edges()

    @classmethod
    def add_secondary_key_indexes(cls) -> None:
        secondary_key_indexes = indexes.get_secondary_key_indexes(cls)
        for index in secondary_key_indexes:
            cls.__table__.append_constraint(index)

    @classmethod
    def populate_pg_backrefs(cls) -> None:
        """_pg_backrefs are in_edges, links FROM other types."""
        cls._pg_backrefs = {
            "copy_number_segments": {
                "name": "copy_number_liftover_workflows",
                "src_type": base.Node.get_subclass("copy_number_segment"),
            },
            "filtered_copy_number_segments": {
                "name": "copy_number_liftover_workflows",
                "src_type": base.Node.get_subclass("filtered_copy_number_segment"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "copy_number_segments": {
                "backref": "copy_number_liftover_workflows",
                "type": base.Node.get_subclass("copy_number_segment"),
            },
            "filtered_copy_number_segments": {
                "backref": "copy_number_liftover_workflows",
                "type": base.Node.get_subclass("filtered_copy_number_segment"),
            },
            "submitted_tangent_copy_numbers": {
                "backref": "copy_number_liftover_workflows",
                "type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "submitted_tangent_copy_numbers": {
                "edge_out": "_CopyNumberLiftoverWorkflowPerformedOnSubmittedTangentCopyNumber_out",
                "dst_type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @property
    def _related_cases_from_cache(self) -> List[psqlgraph.Node]:
        return related_cases.get_related_cases_from_cache(self)

    @property
    def _related_cases_from_parents(self) -> List[psqlgraph.Node]:
        return related_cases.get_related_cases_from_parents(self)

    @property
    def _secondary_keys_dicts(self) -> List[Dict[str, Any]]:
        vals = []
        secondary_keys = self.__pg_secondary_keys
        for keys in secondary_keys:
            if "id" in keys:
                continue
            vals.append({key: getattr(self, key, None) for key in keys})
        return vals

    @hybrid.hybrid_property
    def _secondary_keys(self):
        vals = []
        for keys in self.__pg_secondary_keys:
            vals.append(tuple(getattr(self, key) for key in keys))
        return tuple(vals)

    @_secondary_keys.comparator
    def _secondary_keys(cls):
        return indexes.SecondaryKeyComparator(cls)

    # Set this attribute so psqlgraph doesn't treat it as a property
    _secondary_keys._is_pg_property = False

    @psqlgraph.pg_property(str)
    def submitter_id(self, value):
        self._set_property("submitter_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def batch_id(self, value):
        self._set_property("batch_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        str,
        enum=[
            "uploading",
            "uploaded",
            "md5summing",
            "md5summed",
            "validating",
            "error",
            "invalid",
            "suppressed",
            "redacted",
            "live",
            "validated",
            "submitted",
            "released",
        ],
    )
    def state(self, value):
        self._set_property("state", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def project_id(self, value):
        self._set_property("project_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, type(None))
    def created_datetime(self, value):
        self._set_property("created_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, type(None))
    def updated_datetime(self, value):
        self._set_property("updated_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def workflow_link(self, value):
        self._set_property("workflow_link", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def workflow_version(self, value):
        self._set_property("workflow_version", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, type(None))
    def workflow_start_datetime(self, value):
        self._set_property("workflow_start_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, type(None))
    def workflow_end_datetime(self, value):
        self._set_property("workflow_end_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["DNAcopy"])
    def workflow_type(self, value):
        self._set_property("workflow_type", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(CopyNumberLiftoverWorkflow)
datetime_hooks.cls_inject_updated_datetime_hook(CopyNumberLiftoverWorkflow)
