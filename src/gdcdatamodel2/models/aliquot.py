from typing import Any, Dict, List, Optional, Union

import psqlgraph
from sqlalchemy.ext import hybrid

from .helpers import base, datetime_hooks, indexes, related_cases, versioning


class Aliquot(base.Node):
    __tablename__: str = "node_aliquot"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {
        "state": "validated",
        "no_matched_normal_low_pass_wgs": False,
        "no_matched_normal_targeted_sequencing": False,
        "no_matched_normal_wgs": False,
        "no_matched_normal_wxs": False,
        "selected_normal_wxs": False,
        "selected_normal_wgs": False,
        "selected_normal_targeted_sequencing": False,
        "selected_normal_low_pass_wgs": False,
    }
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Aliquot",
        "namespace": "https://gdc.cancer.gov",
        "category": "biospecimen",
        "submittable": True,
        "downloadable": False,
        "description": "Pertaining to a portion of the whole; any one of two or more samples of something, of the same volume or weight.",
        "required": ["submitter_id"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "aliquot"

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
            "annotations": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "files": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("file"),
            },
            "raw_methylation_arrays": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("raw_methylation_array"),
            },
            "read_groups": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("read_group"),
            },
            "submitted_genotyping_arrays": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_genotyping_array"),
            },
            "submitted_methylation_beta_values": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_methylation_beta_value"),
            },
            "submitted_tangent_copy_number": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "analytes": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("analyte"),
            },
            "annotations": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("annotation"),
            },
            "centers": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("center"),
            },
            "files": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("file"),
            },
            "raw_methylation_arrays": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("raw_methylation_array"),
            },
            "read_groups": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("read_group"),
            },
            "samples": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("sample"),
            },
            "submitted_genotyping_arrays": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_genotyping_array"),
            },
            "submitted_methylation_beta_values": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_methylation_beta_value"),
            },
            "submitted_tangent_copy_number": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "analytes": {
                "edge_out": "_AliquotDerivedFromAnalyte_out",
                "dst_type": base.Node.get_subclass("analyte"),
            },
            "centers": {
                "edge_out": "_AliquotShippedToCenter_out",
                "dst_type": base.Node.get_subclass("center"),
            },
            "samples": {
                "edge_out": "_AliquotDerivedFromSample_out",
                "dst_type": base.Node.get_subclass("sample"),
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

    @psqlgraph.pg_property(float, int)
    def aliquot_quantity(self, value):
        self._set_property("aliquot_quantity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def aliquot_volume(self, value):
        self._set_property("aliquot_volume", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def amount(self, value):
        self._set_property("amount", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "cfDNA",
            "DNA",
            "EBV Immortalized Normal",
            "FFPE DNA",
            "FFPE RNA",
            "GenomePlex (Rubicon) Amplified DNA",
            "m6A Enriched RNA",
            "Nuclei RNA",
            "Repli-G (Qiagen) DNA",
            "Repli-G Pooled (Qiagen) DNA",
            "Repli-G X (Qiagen) DNA",
            "RNA",
            "Total RNA",
        ],
    )
    def analyte_type(self, value):
        self._set_property("analyte_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["D", "E", "G", "H", "R", "S", "T", "W", "X", "Y"])
    def analyte_type_id(self, value):
        self._set_property("analyte_type_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def concentration(self, value):
        self._set_property("concentration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_low_pass_wgs(self, value):
        self._set_property("no_matched_normal_low_pass_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_targeted_sequencing(self, value):
        self._set_property("no_matched_normal_targeted_sequencing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_wgs(self, value):
        self._set_property("no_matched_normal_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_wxs(self, value):
        self._set_property("no_matched_normal_wxs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def source_center(self, value):
        self._set_property("source_center", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_wxs(self, value):
        self._set_property("selected_normal_wxs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_wgs(self, value):
        self._set_property("selected_normal_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_targeted_sequencing(self, value):
        self._set_property("selected_normal_targeted_sequencing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_low_pass_wgs(self, value):
        self._set_property("selected_normal_low_pass_wgs", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Aliquot)
datetime_hooks.cls_inject_updated_datetime_hook(Aliquot)
