from typing import Any, Dict, List, Optional, Union

import psqlgraph
from sqlalchemy.ext import hybrid

from .helpers import base, datetime_hooks, indexes, related_cases, versioning


class PathologyDetail(base.Node):
    __tablename__: str = "node_pathologydetail"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Pathology Detail",
        "namespace": "https://gdc.cancer.gov",
        "category": "clinical",
        "submittable": True,
        "downloadable": False,
        "description": "Information derived from a pathologic review of a specific sample or slide that was not known to be submitted to the GDC.",
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
        return "pathology_detail"

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
                "name": "pathology_details",
                "src_type": base.Node.get_subclass("annotation"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "pathology_details",
                "type": base.Node.get_subclass("annotation"),
            },
            "diagnoses": {
                "backref": "pathology_details",
                "type": base.Node.get_subclass("diagnosis"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "diagnoses": {
                "edge_out": "_PathologyDetailDescribesDiagnosis_out",
                "dst_type": base.Node.get_subclass("diagnosis"),
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
    def additional_pathology_findings(self, value):
        self._set_property("additional_pathology_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def anaplasia_present(self, value):
        self._set_property("anaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Absent",
            "Diffuse",
            "Equivocal",
            "Focal",
            "Present",
            "Sclerosis",
            "Unknown",
            "Not Reported",
        ],
    )
    def anaplasia_present_type(self, value):
        self._set_property("anaplasia_present_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def bone_marrow_malignant_cells(self, value):
        self._set_property("bone_marrow_malignant_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def breslow_thickness(self, value):
        self._set_property("breslow_thickness", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def circumferential_resection_margin(self, value):
        self._set_property("circumferential_resection_margin", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def columnar_mucosa_present(self, value):
        self._set_property("columnar_mucosa_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "High Grade",
            "Indefinite",
            "Low Grade",
            "Mild",
            "Moderate",
            "No Dysplasia",
            "Severe",
            "Unknown",
            "Not Reported",
        ],
    )
    def dysplasia_degree(self, value):
        self._set_property("dysplasia_degree", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Epithelial",
            "Esophageal Columnar Dysplasia",
            "Keratinizing",
            "Nonkeratinizing",
            "Other",
            "Unknown",
            "Not Reported",
        ],
    )
    def dysplasia_type(self, value):
        self._set_property("dysplasia_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def greatest_tumor_dimension(self, value):
        self._set_property("greatest_tumor_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def gross_tumor_weight(self, value):
        self._set_property("gross_tumor_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Macroscopic (2cm or less)",
            "Macroscopic (greater than 2cm)",
            "Microscopic",
            "Unknown",
            "Not Reported",
        ],
    )
    def largest_extrapelvic_peritoneal_focus(self, value):
        self._set_property("largest_extrapelvic_peritoneal_focus", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Axillary",
            "Cervical",
            "Epitrochlear",
            "Femoral",
            "Hilar",
            "Iliac-common",
            "Iliac-external",
            "Iliac, NOS",
            "Inguinal",
            "Mediastinal",
            "Mesenteric",
            "None",
            "Occipital",
            "Paraaortic",
            "Parotid",
            "Popliteal",
            "Retroperitoneal",
            "Splenic",
            "Submandibular",
            "Supraclavicular",
            "Unknown",
            "Not Reported",
        ],
    )
    def lymph_node_involved_site(self, value):
        self._set_property("lymph_node_involved_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Indeterminant", "Negative", "Positive", "Unknown", "Not Reported"]
    )
    def lymph_node_involvement(self, value):
        self._set_property("lymph_node_involvement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_positive(self, value):
        self._set_property("lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_tested(self, value):
        self._set_property("lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def lymphatic_invasion_present(self, value):
        self._set_property("lymphatic_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Involved", "Uninvolved", "Indeterminant", "Unknown", "Not Reported"]
    )
    def margin_status(self, value):
        self._set_property("margin_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def metaplasia_present(self, value):
        self._set_property("metaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Cohesive",
            "Cribiform",
            "Micropapillary",
            "Non-cohesive",
            "Papillary Renal Cell",
            "Papillary, NOS",
            "Solid",
            "Tubular",
        ],
    )
    def morphologic_architectural_pattern(self, value):
        self._set_property("morphologic_architectural_pattern", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def necrosis_percent(self, value):
        self._set_property("necrosis_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Not Reported"])
    def necrosis_present(self, value):
        self._set_property("necrosis_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Absent", "Indeterminate", "Present", "Unknown", "Not Reported"]
    )
    def non_nodal_regional_disease(self, value):
        self._set_property("non_nodal_regional_disease", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def non_nodal_tumor_deposits(self, value):
        self._set_property("non_nodal_tumor_deposits", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def number_proliferating_cells(self, value):
        self._set_property("number_proliferating_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_tumor_invasion(self, value):
        self._set_property("percent_tumor_invasion", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def perineural_invasion_present(self, value):
        self._set_property("perineural_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["0", "1-3", "4 or More", "Unknown", "Not Reported"])
    def peripancreatic_lymph_nodes_positive(self, value):
        self._set_property("peripancreatic_lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def peripancreatic_lymph_nodes_tested(self, value):
        self._set_property("peripancreatic_lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_positive_count(self, value):
        self._set_property("prostatic_chips_positive_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_total_count(self, value):
        self._set_property("prostatic_chips_total_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_involvement_percent(self, value):
        self._set_property("prostatic_involvement_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def rhabdoid_percent(self, value):
        self._set_property("rhabdoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Not Reported"])
    def rhabdoid_present(self, value):
        self._set_property("rhabdoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def sarcomatoid_percent(self, value):
        self._set_property("sarcomatoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Not Reported"])
    def sarcomatoid_present(self, value):
        self._set_property("sarcomatoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Absent", "Present", "Unknown", "Not Reported"])
    def transglottic_extension(self, value):
        self._set_property("transglottic_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_largest_dimension_diameter(self, value):
        self._set_property("tumor_largest_dimension_diameter", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Yes", "No", "Unknown", "Not Reported"])
    def vascular_invasion_present(self, value):
        self._set_property("vascular_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Extramural",
            "Intramural",
            "Macro",
            "Micro",
            "No Vascular Invasion",
            "Unknown",
            "Not Reported",
        ],
    )
    def vascular_invasion_type(self, value):
        self._set_property("vascular_invasion_type", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(PathologyDetail)
datetime_hooks.cls_inject_updated_datetime_hook(PathologyDetail)
