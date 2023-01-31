from typing import Any, Dict, List, Optional, Tuple, Union

import psqlgraph
from sqlalchemy.ext import hybrid
from sqlalchemy.orm import Session, query

from .helpers import (
    base,
    datetime_hooks,
    indexes,
    related_cases,
    versioned_nodes,
    versioning,
)


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
    def _secondary_keys(self) -> Tuple[Tuple[Any]]:
        vals = []
        for keys in self.__pg_secondary_keys:
            vals.append(tuple(getattr(self, key) for key in keys))
        return tuple(vals)

    @_secondary_keys.comparator
    def _secondary_keys(cls):
        return indexes.SecondaryKeyComparator(cls)

    # Set this attribute so psqlgraph doesn't treat it as a property
    _secondary_keys._is_pg_property = False

    @property
    def _versions(self) -> query.Query:
        """Return a query to get node versions (node history).

        Returns a query if the node is bound to a session. Raises an
            exception if the node is not bound to a session. This is different
            from node tagging and versioning. This is used by sheepdog to save
            node history when a node is updated. But the data seems never read by
            any repo.

        Args:
            self: Psqlgraph Node

        Returns:
            A SQLAlchemy query for node versions.

        Raises:
            RuntimeError if the node is not bound to a session.
        """
        session = self.get_session()
        if not session:
            raise RuntimeError(
                "{} not bound to a session. Try .get_versions(session).".format(self)
            )
        return self.get_versions(session)

    def get_versions(self, session: Session) -> query.Query:
        """Return a query for node versions given a session."""
        return (
            session.query(versioned_nodes.VersionedNode)
            .filter(versioned_nodes.VersionedNode.node_id == self.node_id)
            .filter(versioned_nodes.VersionedNode.label == self.label)
            .order_by(versioned_nodes.VersionedNode.key.desc())
        )

    @psqlgraph.pg_property(str)
    def submitter_id(self, value):
        self._set_property("submitter_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def batch_id(self, value):
        self._set_property("batch_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "validating",
            "suppressed",
            "live",
            "submitted",
            "error",
            "validated",
            "md5summing",
            "uploaded",
            "uploading",
            "released",
            "md5summed",
            "redacted",
            "invalid",
        },
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

    @psqlgraph.pg_property(
        str,
        enum={
            "Keratinizing dysplasia; mild",
            "Hyperkeratosis",
            "Intestinal metaplasia",
            "Pulmonary interstitial fibrosis",
            "Bone marrow discordant histology",
            "Bilateral ovaries with endometriotic cyst and surface adhesions",
            "Endometriosis",
            "Platinum-resistant",
            "Epithelial hyperplasia",
            "Other",
            "Pleural plaque",
            "Sialadenitis",
            "Sinonasal papilloma",
            "Colonization; bacterial",
            "Nonkeratinizing dysplasia; severe (carcinoma in situ)",
            "Percent follicular component <= 10%",
            "Epithelial dysplasia",
            "Tubular (papillary) adenoma(s)",
            "PD-L1 CPS (223C LDT) - 20%",
            "Squamous papilloma; solitary",
            "Endosalpingiosis",
            "Carcinoma in situ",
            "Cirrhosis",
            "Squamous metaplasia",
            "Leiomyomata w/ degenerative changes",
            "Tumor-associated lymphoid proliferation",
            "Cyst(s)",
            "Squamous papillomatosis",
            "Benign endocervical polyp",
            "Bone marrow concordant histology",
            "Glomerular disease",
            "Diffuse and early nodular diabetic glomerulosclerosis",
            "Leiomyoma",
            "Atypical hyperplasia/Endometrial intraepithelial neoplasia (EIN)",
            "Asbestos bodies",
            "Endometroid carcinoma with local mucinous differentiation",
            "Clostridioides difficile (c. diff)",
            "Atrophic endometrium",
            "Autoimmune atrophic chronic gastritis",
            "Inflammation",
            "Keratinizing dysplasia; moderate",
            "Tumor has rough spikey edges",
            "Dysplasia; high grade",
            "Nonkeratinizing dysplasia; mild",
            "Endometrial polyp",
            "Percent follicular component > 10%",
            "Dysplasia; low grade",
            "Keratinizing dysplasia; severe (carcinoma in situ)",
            "Adenomyosis",
            "Nonkeratinizing dysplasia; moderate",
            "Gallbladder adenomyomatosis",
            "Colonization; fungal",
        },
    )
    def additional_pathology_findings(self, value):
        self._set_property("additional_pathology_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def anaplasia_present(self, value):
        self._set_property("anaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Equivocal",
            "Focal",
            "Absent",
            "Present",
            "Sclerosis",
            "Not Reported",
            "Diffuse",
        },
    )
    def anaplasia_present_type(self, value):
        self._set_property("anaplasia_present_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def bone_marrow_malignant_cells(self, value):
        self._set_property("bone_marrow_malignant_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def breslow_thickness(self, value):
        self._set_property("breslow_thickness", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def circumferential_resection_margin(self, value):
        self._set_property("circumferential_resection_margin", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def columnar_mucosa_present(self, value):
        self._set_property("columnar_mucosa_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def consistent_pathology_review(self, value):
        self._set_property("consistent_pathology_review", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "No Dysplasia",
            "Unknown",
            "Mild",
            "Moderate",
            "Severe",
            "Indefinite",
            "Not Reported",
            "Low Grade",
            "High Grade",
        },
    )
    def dysplasia_degree(self, value):
        self._set_property("dysplasia_degree", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Epithelial",
            "Nonkeratinizing",
            "Not Reported",
            "Other",
            "Keratinizing",
            "Esophageal Mucosa Columnar Dysplasia",
            "Esophageal Columnar Dysplasia",
        },
    )
    def dysplasia_type(self, value):
        self._set_property("dysplasia_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Focal", "Not Reported", "Extensive"})
    def extracapsular_extension(self, value):
        self._set_property("extracapsular_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={"Microscopic Extension", "Gross Extension", "No Extranodal Extension"},
    )
    def extranodal_extension(self, value):
        self._set_property("extranodal_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def extrascleral_extension(self, value):
        self._set_property("extrascleral_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def greatest_tumor_dimension(self, value):
        self._set_property("greatest_tumor_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def gross_tumor_weight(self, value):
        self._set_property("gross_tumor_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Macroscopic (2cm or less)",
            "Not Reported",
            "Microscopic",
            "Macroscopic (greater than 2cm)",
        },
    )
    def largest_extrapelvic_peritoneal_focus(self, value):
        self._set_property("largest_extrapelvic_peritoneal_focus", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Modified Radical Neck Dissection",
            "Functional (Limited) Neck Dissection",
            "Radical Neck Dissection",
        },
    )
    def lymph_node_dissection_method(self, value):
        self._set_property("lymph_node_dissection_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Neck, Left", "Neck, NOS", "Neck, Right"})
    def lymph_node_dissection_site(self, value):
        self._set_property("lymph_node_dissection_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Femoral",
            "None",
            "Iliac-common",
            "Mediastinal",
            "Cervical",
            "Parotid",
            "Aortic",
            "Occipital",
            "Submandibular",
            "Splenic",
            "Iliac, NOS",
            "Unknown",
            "Hilar",
            "Paraaortic",
            "Pelvis, NOS",
            "Iliac-external",
            "Popliteal",
            "Mesenteric",
            "Supraclavicular",
            "Axillary",
            "Epitrochlear",
            "Not Reported",
            "Retroperitoneal",
            "Inguinal",
        },
    )
    def lymph_node_involved_site(self, value):
        self._set_property("lymph_node_involved_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Indeterminant", "Not Reported", "Negative", "Positive"}
    )
    def lymph_node_involvement(self, value):
        self._set_property("lymph_node_involvement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_positive(self, value):
        self._set_property("lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"No", "Yes", "Not Reported"})
    def lymph_nodes_removed(self, value):
        self._set_property("lymph_nodes_removed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_tested(self, value):
        self._set_property("lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def lymphatic_invasion_present(self, value):
        self._set_property("lymphatic_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Uninvolved", "Unknown", "Indeterminant", "Not Reported", "Involved"}
    )
    def margin_status(self, value):
        self._set_property("margin_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def metaplasia_present(self, value):
        self._set_property("metaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Solid",
            "Cribiform",
            "Cohesive",
            "Non-cohesive",
            "Micropapillary",
            "Papillary, NOS",
            "Tubular",
            "Papillary Renal Cell",
        },
    )
    def morphologic_architectural_pattern(self, value):
        self._set_property("morphologic_architectural_pattern", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def necrosis_percent(self, value):
        self._set_property("necrosis_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def necrosis_present(self, value):
        self._set_property("necrosis_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Present", "Indeterminate", "Unknown", "Not Reported", "Absent"}
    )
    def non_nodal_regional_disease(self, value):
        self._set_property("non_nodal_regional_disease", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def non_nodal_tumor_deposits(self, value):
        self._set_property("non_nodal_tumor_deposits", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def number_proliferating_cells(self, value):
        self._set_property("number_proliferating_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def percent_tumor_invasion(self, value):
        self._set_property("percent_tumor_invasion", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def percent_tumor_nuclei(self, value):
        self._set_property("percent_tumor_nuclei", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def perineural_invasion_present(self, value):
        self._set_property("perineural_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"1-3", "Unknown", "Not Reported", "4 or More", "0"})
    def peripancreatic_lymph_nodes_positive(self, value):
        self._set_property("peripancreatic_lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def peripancreatic_lymph_nodes_tested(self, value):
        self._set_property("peripancreatic_lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def prostatic_chips_positive_count(self, value):
        self._set_property("prostatic_chips_positive_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def prostatic_chips_total_count(self, value):
        self._set_property("prostatic_chips_total_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def prostatic_involvement_percent(self, value):
        self._set_property("prostatic_involvement_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"R0", "RX", "R2", "R1"})
    def residual_tumor(self, value):
        self._set_property("residual_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"No macroscopic disease", ">20 mm", "11-20 mm", "1-10 mm"})
    def residual_tumor_measurement(self, value):
        self._set_property("residual_tumor_measurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def rhabdoid_percent(self, value):
        self._set_property("rhabdoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def rhabdoid_present(self, value):
        self._set_property("rhabdoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def sarcomatoid_percent(self, value):
        self._set_property("sarcomatoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def sarcomatoid_present(self, value):
        self._set_property("sarcomatoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def size_extraocular_nodule(self, value):
        self._set_property("size_extraocular_nodule", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Present", "Unknown", "Absent", "Not Reported"})
    def transglottic_extension(self, value):
        self._set_property("transglottic_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def tumor_largest_dimension_diameter(self, value):
        self._set_property("tumor_largest_dimension_diameter", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def tumor_level_prostate(self, value):
        self._set_property("tumor_level_prostate", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def tumor_thickness(self, value):
        self._set_property("tumor_thickness", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def vascular_invasion_present(self, value):
        self._set_property("vascular_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Macro",
            "Extramural",
            "Unknown",
            "Not Reported",
            "No Vascular Invasion",
            "Intramural",
            "Micro",
        },
    )
    def vascular_invasion_type(self, value):
        self._set_property("vascular_invasion_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Transition zone",
            "Central zone",
            "Peripheral zone",
            "Overlapping/multiple zones",
            "Unknown zone",
        },
    )
    def zone_of_origin_prostate(self, value):
        self._set_property("zone_of_origin_prostate", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(PathologyDetail)
datetime_hooks.cls_inject_updated_datetime_hook(PathologyDetail)
