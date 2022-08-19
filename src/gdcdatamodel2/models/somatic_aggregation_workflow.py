from typing import Any, Dict, List, Optional, Union

import psqlgraph
from sqlalchemy.ext import hybrid

from .helpers import base, datetime_hooks, indexes, related_cases, versioning


class SomaticAggregationWorkflow(base.Node):
    __tablename__: str = "node_somaticaggregationworkflow"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Somatic Aggregation Workflow",
        "namespace": "https://gdc.cancer.gov",
        "category": "analysis",
        "submittable": False,
        "downloadable": False,
        "description": "Metadata for the somatic mutation aggregation workflow used to generate both the public and protected MAFs in the GDC DNA-Seq pipelines.",
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
        return "somatic_aggregation_workflow"

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
            "aggregated_somatic_mutations": {
                "name": "somatic_aggregation_workflows",
                "src_type": base.Node.get_subclass("aggregated_somatic_mutation"),
            },
            "masked_somatic_mutations": {
                "name": "somatic_aggregation_workflows",
                "src_type": base.Node.get_subclass("masked_somatic_mutation"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "aggregated_somatic_mutations": {
                "backref": "somatic_aggregation_workflows",
                "type": base.Node.get_subclass("aggregated_somatic_mutation"),
            },
            "annotated_somatic_mutations": {
                "backref": "somatic_aggregation_workflows",
                "type": base.Node.get_subclass("annotated_somatic_mutation"),
            },
            "masked_somatic_mutations": {
                "backref": "somatic_aggregation_workflows",
                "type": base.Node.get_subclass("masked_somatic_mutation"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "annotated_somatic_mutations": {
                "edge_out": "_SomaticAggregationWorkflowPerformedOnAnnotatedSomaticMutation_out",
                "dst_type": base.Node.get_subclass("annotated_somatic_mutation"),
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

    @psqlgraph.pg_property(
        str,
        enum=[
            "Aliquot Ensemble Somatic Variant Merging and Masking",
            "FoundationOne Variant Aggregation and Masking",
            "GENIE Variant Aggregation and Masking",
            "MuSE Variant Aggregation and Masking",
            "MuTect2 Variant Aggregation and Masking",
            "Pindel Variant Aggregation and Masking",
            "SomaticSniper Variant Aggregation and Masking",
            "VarScan2 Variant Aggregation and Masking",
        ],
    )
    def workflow_type(self, value):
        self._set_property("workflow_type", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(SomaticAggregationWorkflow)
datetime_hooks.cls_inject_updated_datetime_hook(SomaticAggregationWorkflow)
