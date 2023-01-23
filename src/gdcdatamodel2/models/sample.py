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


class Sample(base.Node):
    __tablename__: str = "node_sample"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Sample",
        "namespace": "https://gdc.cancer.gov",
        "category": "biospecimen",
        "submittable": True,
        "downloadable": False,
        "description": "Any material sample taken from a biological entity for testing, diagnostic, propagation, treatment or research purposes, including a sample obtained from a living organism or taken from the biological object after halting of all its life functions. Biospecimen can contain one or more components including but not limited to cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory products.",
        "required": [
            "preservation_method",
            "specimen_type",
            "submitter_id",
            "tissue_type",
            "tumor_descriptor",
        ],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "sample"

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
            "aliquots": {
                "name": "samples",
                "src_type": base.Node.get_subclass("aliquot"),
            },
            "analytes": {
                "name": "samples",
                "src_type": base.Node.get_subclass("analyte"),
            },
            "annotations": {
                "name": "samples",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "child_samples": {
                "name": "parent_samples",
                "src_type": base.Node.get_subclass("sample"),
            },
            "files": {
                "name": "samples",
                "src_type": base.Node.get_subclass("file"),
            },
            "pathology_reports": {
                "name": "samples",
                "src_type": base.Node.get_subclass("pathology_report"),
            },
            "portions": {
                "name": "samples",
                "src_type": base.Node.get_subclass("portion"),
            },
            "protein_expressions": {
                "name": "samples",
                "src_type": base.Node.get_subclass("protein_expression"),
            },
            "slides": {
                "name": "samples",
                "src_type": base.Node.get_subclass("slide"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "aliquots": {
                "backref": "samples",
                "type": base.Node.get_subclass("aliquot"),
            },
            "analytes": {
                "backref": "samples",
                "type": base.Node.get_subclass("analyte"),
            },
            "annotations": {
                "backref": "samples",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "samples",
                "type": base.Node.get_subclass("case"),
            },
            "child_samples": {
                "backref": "parent_samples",
                "type": base.Node.get_subclass("sample"),
            },
            "diagnoses": {
                "backref": "samples",
                "type": base.Node.get_subclass("diagnosis"),
            },
            "files": {
                "backref": "samples",
                "type": base.Node.get_subclass("file"),
            },
            "parent_samples": {
                "backref": "child_samples",
                "type": base.Node.get_subclass("sample"),
            },
            "pathology_reports": {
                "backref": "samples",
                "type": base.Node.get_subclass("pathology_report"),
            },
            "portions": {
                "backref": "samples",
                "type": base.Node.get_subclass("portion"),
            },
            "protein_expressions": {
                "backref": "samples",
                "type": base.Node.get_subclass("protein_expression"),
            },
            "slides": {
                "backref": "samples",
                "type": base.Node.get_subclass("slide"),
            },
            "tissue_source_sites": {
                "backref": "samples",
                "type": base.Node.get_subclass("tissue_source_site"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "cases": {
                "edge_out": "_SampleDerivedFromCase_out",
                "dst_type": base.Node.get_subclass("case"),
            },
            "diagnoses": {
                "edge_out": "_SampleRelatedToDiagnosis_out",
                "dst_type": base.Node.get_subclass("diagnosis"),
            },
            "parent_samples": {
                "edge_out": "_SampleDerivedFromSample_out",
                "dst_type": base.Node.get_subclass("sample"),
            },
            "tissue_source_sites": {
                "edge_out": "_SampleProcessedAtTissueSourceSite_out",
                "dst_type": base.Node.get_subclass("tissue_source_site"),
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
            "validated",
            "md5summing",
            "redacted",
            "invalid",
            "submitted",
            "uploading",
            "released",
            "error",
            "uploaded",
            "md5summed",
        },
    )
    def state(self, value):
        self._set_property("state", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def project_id(self, value):
        self._set_property("project_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), str)
    def created_datetime(self, value):
        self._set_property("created_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), str)
    def updated_datetime(self, value):
        self._set_property("updated_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Gastrointestinal Tract",
            "Mesothelium",
            "Groin",
            "Esophagus - Mucosa Only",
            "Middle Finger",
            "Blood",
            "Hypopharynx",
            "Mitochondria",
            "Ligament",
            "Thoracic Spine",
            "Breast",
            "Salivary Gland",
            "Tonsil (Pharyngeal)",
            "Ampulla Of Vater",
            "Islet Cells",
            "Nasopharynx",
            "Calf",
            "Conjunctiva",
            "Brow",
            "Cervical Spine",
            "Uvula",
            "Clavicle",
            "Bone Marrow",
            "Ascending Colon",
            "Stomach - Mucosa Only",
            "Transverse Colon",
            "Throat",
            "Lymph Node(s) Occipital",
            "Soft Tissue",
            "Pleura",
            "Frontal Cortex",
            "Paranasal Sinuses",
            "Vagina",
            "Effusion",
            "Buccal Mucosa",
            "Colon",
            "Trachea / Major Bronchi",
            "Vertebra",
            "Thigh",
            "Thymus",
            "Liver",
            "Auditory Canal",
            "Cervix",
            "Hard Palate",
            "Cerebrospinal Fluid",
            "Stomach",
            "Fallopian Tube",
            "Lymph Node(s) Regional",
            "Oropharynx",
            "Ileum",
            "Shoulder",
            "Spinal Column",
            "Lymph Node(s) Hilar",
            "Sublingual Gland",
            "Chest",
            "Sacrum",
            "Synovium",
            "Lymph Node(s) Distant",
            "Uterus",
            "Forehead",
            "Pituitary Gland",
            "Oral Cavity - Mucosa Only",
            "Autonomic Nervous System",
            "Maxilla",
            "Esophagus",
            "Gallbladder",
            "Large Bowel",
            "Ascending Colon Hepatic Flexure",
            "Pancreas",
            "Unknown",
            "Small Bowel",
            "Lymph Node(s) Iliac-External",
            "Pineal",
            "Penis",
            "Antrum",
            "Vas Deferens",
            "Occipital Cortex",
            "Lymph Node(s) Submandibular",
            "Connective Tissue",
            "Abdomen",
            "Hepatic Vein",
            "Leptomeninges",
            "Skeletal Muscle",
            "Not Allowed To Collect",
            "Scalp",
            "Foreskin",
            "Anorectum",
            "Lumbar Spine",
            "Ear Canal",
            "Lymph Node(s) Popliteal",
            "Carotid Artery",
            "Lacrimal Gland",
            "Gum",
            "Back",
            "Lymph Node(s) Paraaortic",
            "Cell-Line",
            "Testis",
            "Buccal Cavity",
            "Scrotum",
            "Kidney",
            "Nerve(s) Cranial",
            "Lymph Node(s) Cervical",
            "Abdominal Wall",
            "Ovary",
            "Vulva",
            "Lymph Node(s) Supraclavicular",
            "Anal Sphincter",
            "Spinal Cord",
            "Epididymis",
            "Pharynx",
            "Urethra",
            "Axilla",
            "Leg",
            "Pylorus",
            "Small Finger",
            "Brain Stem",
            "Hip",
            "Round Ligament",
            "Esophageal; Proximal",
            "Not Reported",
            "Omentum",
            "Lung",
            "Bronchus",
            "Finger",
            "Periorbital Soft Tissue",
            "Chest Wall",
            "Parathyroid",
            "Bile Duct",
            "Larynx",
            "Ischium",
            "Cerebral Cortex",
            "Aqueous Fluid",
            "Fundus Of Stomach",
            "Lymph Node(s) Inguinal",
            "Fluid",
            "Colon - Mucosa Only",
            "White Blood Cells",
            "Clitoris",
            "Lymph Node(s) Axilla",
            "Femur",
            "Brain",
            "Venous",
            "Peritoneal Cavity",
            "Pericardium",
            "Prostate",
            "Lymph Node(s) Splenic",
            "Hepatic Flexure",
            "Mesentery",
            "Nerve",
            "Ureter",
            "Arm",
            "Oral Cavity",
            "Tonsil",
            "Sinus(es), Maxillary",
            "Peritoneum",
            "Seminal Vesicle",
            "Retina",
            "Popliteal Fossa",
            "Cerebellum",
            "Lymph Node(s) Retroperitoneal",
            "Ocular Orbits",
            "Epidural Space",
            "Paraspinal Ganglion",
            "Sternum",
            "Cartilage",
            "Lymph Node(s) Iliac-Common",
            "Tongue",
            "Esophagogastric Junction",
            "Buttock",
            "Scapula",
            "Palate",
            "Laryngopharynx",
            "Nails",
            "Parotid Gland",
            "Tibia",
            "Dermal",
            "Fibroblasts",
            "Fibula",
            "Sinus",
            "Ilium",
            "Adipose",
            "Thyroid",
            "Common Duct",
            "Lymph Nodes(s) Mediastinal",
            "Head - Face Or Neck, Nos",
            "Cerebrum",
            "Femoral Vein",
            "Small Bowel - Mucosa Only",
            "Artery",
            "Capillary",
            "Descending Colon",
            "Anus",
            "Rectum",
            "Wrist",
            "Ring Finger",
            "Humerus",
            "Vein",
            "Retro-Orbital Region",
            "Hippocampus",
            "Skull",
            "Head & Neck",
            "Knee",
            "Joint",
            "Adrenal",
            "Aortic Body",
            "Pelvis",
            "Rectosigmoid Junction",
            "Lip",
            "Mandible",
            "Lymph Node(s) Internal Mammary",
            "Esophageal; Distal",
            "Eye",
            "Patella",
            "Cardia",
            "Thorax",
            "Femoral Artery",
            "Forearm",
            "Ear",
            "Lymph Node(s) Subclavicular",
            "Umbilical Cord",
            "Aorta",
            "Elbow",
            "Bowel",
            "Hepatic Duct",
            "Bone",
            "Lymph Node(s) Femoral",
            "Lymph Node(s) Mesenteric",
            "Thumb",
            "Temporal Cortex",
            "Lymph Node(s) Epitrochlear",
            "Urinary Tract",
            "Spleen",
            "Jejunum",
            "Glottis",
            "Neck",
            "Alveolar Ridge",
            "Carina",
            "Submandibular Gland",
            "Carotid Body",
            "Adenoid",
            "Lymph Node(s) Parotid",
            "Central Nervous System",
            "Other",
            "Chin",
            "Heart",
            "Blood Vessel",
            "Floor Of Mouth",
            "Nasal Soft Tissue",
            "Nasal Cavity",
            "Lymph Node(s) Scalene",
            "Subglottis",
            "Subcutaneous Tissue",
            "Muscle",
            "Hand",
            "Sigmoid Colon",
            "Trunk",
            "Ear, Pinna (External)",
            "Rib",
            "Ganglia",
            "Splenic Flexure",
            "Diaphragm",
            "Index Finger",
            "Lymph Node(s) Pelvic",
            "Cecum",
            "Jaw",
            "Frontal Lobe",
            "Lymph Node",
            "Sciatic Nerve",
            "Foot",
            "Antecubital Fossa",
            "Esophageal; Mid",
            "Mediastinum",
            "Duodenum",
            "Lymph Node(s) Mammary",
            "Gastroesophageal Junction",
            "Amniotic Fluid",
            "Broad Ligament",
            "Hepatic",
            "Endocrine Gland",
            "Ankle",
            "Bronchiole",
            "Appendix",
            "Placenta",
            "Retroperitoneum",
            "Skin",
            "Acetabulum",
            "Bladder",
            "Pineal Gland",
            "Tendon",
            "Mediastinal Soft Tissue",
            "Supraglottis",
        },
    )
    def biospecimen_anatomic_site(self, value):
        self._set_property("biospecimen_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Bilateral", "Unknown", "Right", "Left", "Not Reported"})
    def biospecimen_laterality(self, value):
        self._set_property("biospecimen_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def catalog_reference(self, value):
        self._set_property("catalog_reference", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Sorted Cells",
            "Whole Bone Marrow",
            "Solid Tissue",
            "Mixed Adherent Suspension",
            "Fibroblasts from Bone Marrow Normal",
            "Cell",
            "Human Original Cells",
            "Not Allowed To Collect",
            "Sputum",
            "3D Air-Liquid Interface Organoid",
            "Bone Marrow Components",
            "Control Analyte",
            "Serum",
            "Not Reported",
            "3D Organoid",
            "Buccal Cells",
            "Buffy Coat",
            "2D Modified Conditionally Reprogrammed Cells",
            "Saliva",
            "Pleural Effusion",
            "Adherent Cell Line",
            "Liquid Suspension Cell Line",
            "Derived Cell Line",
            "Bone Marrow Components NOS",
            "Granulocytes",
            "Unknown",
            "Mononuclear Cells from Bone Marrow Normal",
            "2D Classical Conditionally Reprogrammed Cells",
            "3D Neurosphere",
            "Peripheral Whole Blood",
            "Plasma",
            "EBV Immortalized",
            "Lymphocytes",
            "Peripheral Blood Components NOS",
        },
    )
    def composition(self, value):
        self._set_property("composition", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def current_weight(self, value):
        self._set_property("current_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_collection(self, value):
        self._set_property("days_to_collection", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_sample_procurement(self, value):
        self._set_property("days_to_sample_procurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Not Allowed To Collect", "Yes", "Unknown", "Not Reported", "No"}
    )
    def diagnosis_pathologically_confirmed(self, value):
        self._set_property("diagnosis_pathologically_confirmed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Distal (>2cm)", "Adjacent (< or = 2cm)", "Not Reported", "Unknown"}
    )
    def distance_normal_to_tumor(self, value):
        self._set_property("distance_normal_to_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def distributor_reference(self, value):
        self._set_property("distributor_reference", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def freezing_method(self, value):
        self._set_property("freezing_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def growth_rate(self, value):
        self._set_property("growth_rate", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def initial_weight(self, value):
        self._set_property("initial_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def intermediate_dimension(self, value):
        self._set_property("intermediate_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def is_ffpe(self, value):
        self._set_property("is_ffpe", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def longest_dimension(self, value):
        self._set_property("longest_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Liquid Biopsy",
            "Radical Prostatectomy",
            "Radical Maxillectomy",
            "Endoscopic Mucosal Resection (EMR)",
            "Laparoscopic Radical Prostatectomy without Robotics",
            "Tonsillectomy",
            "Superficial Parotidectomy",
            "Aspirate",
            "Mandibulectomy",
            "Not Allowed To Collect",
            "Pancreatectomy",
            "Pneumonectomy",
            "Transoral Laser Excision",
            "Laparoscopic Radical Prostatectomy with Robotics",
            "Open Partial Nephrectomy",
            "Partial Nephrectomy",
            "Salpingo-oophorectomy",
            "Autopsy",
            "Right Hemicolectomy",
            "Wedge Resection",
            "Endo Rectal Tumor Resection",
            "Omentectomy",
            "Ascites Drainage",
            "Peritoneal Lavage",
            "Sigmoid Colectomy",
            "Open Craniotomy",
            "Buccal Mucosal Resection",
            "Pan-Procto Colectomy",
            "Simple Hysterectomy",
            "Hysterectomy NOS",
            "Parotidectomy, NOS",
            "Endoscopic Biopsy",
            "Metastasectomy",
            "Other",
            "Local Resection (Exoresection; wall resection)",
            "Transplant",
            "Total Laryngectomy",
            "Subtotal Resection",
            "Blood Draw",
            "Simple Mastectomy",
            "Glossectomy",
            "Abdomino-perineal Resection of Rectum",
            "Total Mastectomy",
            "Open Radical Prostatectomy",
            "Radical Hysterectomy",
            "Thoracentesis",
            "Core Biopsy",
            "Incisional Biopsy",
            "Partial Maxillectomy",
            "Full Hysterectomy",
            "Lumpectomy",
            "Fine Needle Aspiration",
            "Subtotal Prostatectomy",
            "Left Hemicolectomy",
            "Maxillectomy",
            "Tumor Debulking",
            "Hand Assisted Laparoscopic Radical Nephrectomy",
            "Deep Parotidectomy",
            "Whipple Procedure",
            "Total Nephrectomy",
            "Bone Marrow Aspirate",
            "Biopsy",
            "Total Hepatectomy",
            "Cystectomy",
            "Laparoscopic Biopsy",
            "Endolaryngeal Excision",
            "Orchiectomy",
            "Supraglottic Laryngectomy",
            "Indeterminant",
            "Not Reported",
            "Anterior Resection of Rectum",
            "Modified Radical Mastectomy",
            "Lymph Node Dissection",
            "Laryngopharyngectomy",
            "Palatectomy",
            "Laparoscopic Radical Nephrectomy",
            "Transurethral resection (TURBT)",
            "Punch Biopsy",
            "Transurethral Resection (TURP)",
            "Tumor Resection",
            "Gross Total Resection",
            "Other Surgical Resection",
            "Vertical Hemilaryngectomy",
            "Supracricoid Laryngectomy",
            "Partial Hepatectomy",
            "Lymphadenectomy",
            "Unknown",
            "Partial Laryngectomy",
            "Thoracoscopic Biopsy",
            "Enucleation",
            "Total Colectomy",
            "Oophorectomy",
            "Needle Biopsy",
            "Salpingectomy",
            "Surgical Resection",
            "Laparoscopic Partial Nephrectomy",
            "Excisional Biopsy",
            "Open Radical Nephrectomy",
            "Paracentesis",
            "Supracervical Hysterectomy",
            "Lobectomy",
            "Transverse Colectomy",
            "Radical Nephrectomy",
        },
    )
    def method_of_sample_procurement(self, value):
        self._set_property("method_of_sample_procurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def oct_embedded(self, value):
        self._set_property("oct_embedded", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def passage_count(self, value):
        self._set_property("passage_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def pathology_report_uuid(self, value):
        self._set_property("pathology_report_uuid", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Not Allowed To Collect",
            "FFPE",
            "Snap Frozen",
            "Not Reported",
            "Cryopreserved",
            "OCT",
            "Unknown",
            "Frozen",
            "Fresh",
        },
    )
    def preservation_method(self, value):
        self._set_property("preservation_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def sample_ordinal(self, value):
        self._set_property("sample_ordinal", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Primary Tumor",
            "Lymphoid Normal",
            "Xenograft Tissue",
            "FFPE Scrolls",
            "Human Tumor Original Cells",
            "Bone Marrow Normal",
            "DNA",
            "Blood Derived Normal",
            "Mixed Adherent Suspension",
            "Fibroblasts from Bone Marrow Normal",
            "Cell Line Derived Xenograft Tissue",
            "Metastatic",
            "Not Allowed To Collect",
            "Repli-G X (Qiagen) DNA",
            "Tumor",
            "In Situ Neoplasms",
            "Tumor Adjacent Normal - Post Neo-adjuvant Therapy",
            "Control Analyte",
            "Blood Derived Cancer - Bone Marrow",
            "Buccal Cell Normal",
            "Slides",
            "Not Reported",
            "Post neo-adjuvant therapy",
            "Benign Neoplasms",
            "Cell Lines",
            "Additional Metastatic",
            "Repli-G (Qiagen) DNA",
            "Blood Derived Liquid Biopsy",
            "EBV Immortalized Normal",
            "RNA",
            "Saliva",
            "Pleural Effusion",
            "Additional - New Primary",
            "Recurrent Blood Derived Cancer - Bone Marrow",
            "Neoplasms of Uncertain and Unknown Behavior",
            "Next Generation Cancer Model Expanded Under Non-conforming Conditions",
            "Blood Derived Cancer - Bone Marrow, Post-treatment",
            "Granulocytes",
            "Unknown",
            "Blood Derived Cancer - Peripheral Blood, Post-treatment",
            "Mononuclear Cells from Bone Marrow Normal",
            "Blood Derived Cancer - Peripheral Blood",
            "Expanded Next Generation Cancer Model",
            "FFPE Recurrent",
            "Recurrent Tumor",
            "Recurrent Blood Derived Cancer - Peripheral Blood",
            "Primary Blood Derived Cancer - Peripheral Blood",
            "Primary Xenograft Tissue",
            "Next Generation Cancer Model",
            "Solid Tissue Normal",
            "Total RNA",
            "GenomePlex (Rubicon) Amplified DNA",
            "Primary Blood Derived Cancer - Bone Marrow",
        },
    )
    def sample_type(self, value):
        self._set_property("sample_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "31",
            "50",
            "32",
            "04",
            "01",
            "61",
            "13",
            "16",
            "15",
            "18",
            "11",
            "20",
            "30",
            "86",
            "05",
            "87",
            "17",
            "10",
            "06",
            "03",
            "60",
            "08",
            "85",
            "99",
            "41",
            "02",
            "07",
            "12",
            "09",
            "14",
            "42",
            "40",
        },
    )
    def sample_type_id(self, value):
        self._set_property("sample_type_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def shortest_dimension(self, value):
        self._set_property("shortest_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Sorted Cells",
            "Whole Bone Marrow",
            "Solid Tissue",
            "Mononuclear Cells from Bone Marrow",
            "Mixed Adherent Suspension",
            "Human Original Cells",
            "Cell",
            "Sputum",
            "3D Air-Liquid Interface Organoid",
            "Bone Marrow NOS",
            "Control Analyte",
            "Serum",
            "Not Reported",
            "3D Organoid",
            "Buccal Cells",
            "Buffy Coat",
            "2D Modified Conditionally Reprogrammed Cells",
            "Saliva",
            "Pleural Effusion",
            "Adherent Cell Line",
            "Peripheral Blood NOS",
            "Liquid Suspension Cell Line",
            "Derived Cell Line",
            "Bone Marrow Components NOS",
            "Granulocytes",
            "Unknown",
            "Lymphoid",
            "2D Classical Conditionally Reprogrammed Cells",
            "3D Neurosphere",
            "Peripheral Whole Blood",
            "Plasma",
            "EBV Immortalized",
            "Lymphocytes",
            "Peripheral Blood Components NOS",
            "Fibroblasts from Bone Marrow",
        },
    )
    def specimen_type(self, value):
        self._set_property("specimen_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def time_between_clamping_and_freezing(self, value):
        self._set_property("time_between_clamping_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def time_between_excision_and_freezing(self, value):
        self._set_property("time_between_excision_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Prospective", "Retrospective"})
    def tissue_collection_type(self, value):
        self._set_property("tissue_collection_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Not Allowed To Collect",
            "Tumor",
            "Abnormal",
            "Peritumoral",
            "Normal",
            "Unknown",
            "Not Reported",
        },
    )
    def tissue_type(self, value):
        self._set_property("tissue_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Rhabdoid tumor (kidney) (RT)",
            "Clear cell sarcoma of the kidney (CCSK)",
            "Induction Failure AML (AML-IF)",
            "Diffuse Large B-Cell Lymphoma (DLBCL)",
            "NHL, anaplastic large cell lymphoma",
            "Soft tissue sarcoma, non-rhabdomyosarcoma",
            "CNS, rhabdoid tumor",
            "Neuroblastoma (NBL)",
            "CNS, low grade glioma (LGG)",
            "Non cancerous tissue",
            "Rhabdomyosarcoma",
            "Cervical Cancer (all types)",
            "NHL, Burkitt lymphoma (BL)",
            "Acute Leukemia of Ambiguous Lineage (ALAL)",
            "Anal Cancer (all types)",
            "CNS, ependymoma",
            "CNS, other",
            "Osteosarcoma (OS)",
            "Acute lymphoblastic leukemia (ALL)",
            "CNS, glioblastoma (GBM)",
            "Acute myeloid leukemia (AML)",
            "Ewing sarcoma",
            "Wilms tumor (WT)",
            "Lung Cancer (all types)",
            "CNS, medulloblastoma",
        },
    )
    def tumor_code(self, value):
        self._set_property("tumor_code", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "50",
            "71",
            "62",
            "04",
            "01",
            "63",
            "10",
            "61",
            "03",
            "60",
            "81",
            "15",
            "00",
            "64",
            "41",
            "02",
            "65",
            "20",
            "21",
            "30",
            "80",
            "52",
            "70",
            "40",
            "51",
        },
    )
    def tumor_code_id(self, value):
        self._set_property("tumor_code_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Premalignant",
            "Not Allowed To Collect",
            "New Primary",
            "Xenograft",
            "Not Reported",
            "NOS",
            "Recurrence",
            "Unknown",
            "Primary",
            "Not Applicable",
            "Metastatic",
        },
    )
    def tumor_descriptor(self, value):
        self._set_property("tumor_descriptor", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Sample)
datetime_hooks.cls_inject_updated_datetime_hook(Sample)
