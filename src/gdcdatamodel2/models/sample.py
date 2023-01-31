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
            "White Blood Cells",
            "Mandible",
            "Cerebrum",
            "Duodenum",
            "Gallbladder",
            "Hepatic",
            "Lymph Node(s) Iliac-Common",
            "Head & Neck",
            "Auditory Canal",
            "Gastroesophageal Junction",
            "Splenic Flexure",
            "Ischium",
            "Nasal Cavity",
            "Epididymis",
            "Pylorus",
            "Abdomen",
            "Clavicle",
            "Axilla",
            "Patella",
            "Vagina",
            "Bladder",
            "Umbilical Cord",
            "Hard Palate",
            "Lymph Node(s) Mammary",
            "Omentum",
            "Abdominal Wall",
            "Pancreas",
            "Testis",
            "Vulva",
            "Periorbital Soft Tissue",
            "Buttock",
            "Frontal Cortex",
            "Hepatic Duct",
            "Pleura",
            "Esophageal; Distal",
            "Mesothelium",
            "Groin",
            "Wrist",
            "Fibula",
            "Fallopian Tube",
            "Lymph Node(s) Paraaortic",
            "Not Reported",
            "Buccal Mucosa",
            "Maxilla",
            "Descending Colon",
            "Bile Duct",
            "Tonsil",
            "Placenta",
            "Uterus",
            "Cerebellum",
            "Transverse Colon",
            "Mitochondria",
            "Cerebral Cortex",
            "Other",
            "Ovary",
            "Oral Cavity - Mucosa Only",
            "Small Bowel - Mucosa Only",
            "Leg",
            "Cervix",
            "Urethra",
            "Connective Tissue",
            "Round Ligament",
            "Pericardium",
            "Not Allowed To Collect",
            "Salivary Gland",
            "Throat",
            "Ascending Colon",
            "Middle Finger",
            "Effusion",
            "Soft Tissue",
            "Colon",
            "Small Finger",
            "Esophagus - Mucosa Only",
            "Ear",
            "Femur",
            "Subcutaneous Tissue",
            "Foot",
            "Stomach",
            "Lymph Node(s) Axilla",
            "Sciatic Nerve",
            "Esophagogastric Junction",
            "Occipital Cortex",
            "Vas Deferens",
            "Lymph Node(s) Femoral",
            "Scapula",
            "Large Bowel",
            "Vertebra",
            "Brow",
            "Tonsil (Pharyngeal)",
            "Calf",
            "Liver",
            "Islet Cells",
            "Floor Of Mouth",
            "Kidney",
            "Supraglottis",
            "Unknown",
            "Alveolar Ridge",
            "Thoracic Spine",
            "Sigmoid Colon",
            "Peritoneum",
            "Broad Ligament",
            "Lymph Node(s) Occipital",
            "Nerve",
            "Blood",
            "Chest Wall",
            "Trunk",
            "Amniotic Fluid",
            "Gastrointestinal Tract",
            "Leptomeninges",
            "Muscle",
            "Chin",
            "Hand",
            "Diaphragm",
            "Index Finger",
            "Pineal",
            "Vein",
            "Bone",
            "Ring Finger",
            "Carotid Artery",
            "Cecum",
            "Glottis",
            "Thyroid",
            "Parathyroid",
            "Artery",
            "Lymph Node(s) Distant",
            "Mediastinal Soft Tissue",
            "Heart",
            "Lymph Node(s) Hilar",
            "Hippocampus",
            "Subglottis",
            "Colon - Mucosa Only",
            "Esophageal; Proximal",
            "Lymph Node(s) Scalene",
            "Back",
            "Thumb",
            "Cervical Spine",
            "Paranasal Sinuses",
            "Tendon",
            "Cartilage",
            "Aorta",
            "Lymph Node(s) Mesenteric",
            "Dermal",
            "Lymph Node(s) Regional",
            "Lip",
            "Nails",
            "Pharynx",
            "Lung",
            "Spleen",
            "Head - Face Or Neck, Nos",
            "Prostate",
            "Bronchiole",
            "Carotid Body",
            "Finger",
            "Lymph Node(s) Retroperitoneal",
            "Oropharynx",
            "Anal Sphincter",
            "Bowel",
            "Brain Stem",
            "Thorax",
            "Ganglia",
            "Aqueous Fluid",
            "Elbow",
            "Skin",
            "Ileum",
            "Laryngopharynx",
            "Rectosigmoid Junction",
            "Temporal Cortex",
            "Hepatic Flexure",
            "Anorectum",
            "Spinal Column",
            "Adenoid",
            "Ankle",
            "Venous",
            "Buccal Cavity",
            "Lacrimal Gland",
            "Neck",
            "Parotid Gland",
            "Small Bowel",
            "Pineal Gland",
            "Bronchus",
            "Sinus(es), Maxillary",
            "Aortic Body",
            "Ocular Orbits",
            "Arm",
            "Pelvis",
            "Hip",
            "Joint",
            "Oral Cavity",
            "Appendix",
            "Foreskin",
            "Skull",
            "Synovium",
            "Ligament",
            "Stomach - Mucosa Only",
            "Scalp",
            "Peritoneal Cavity",
            "Lymph Node(s) Submandibular",
            "Ear, Pinna (External)",
            "Ear Canal",
            "Paraspinal Ganglion",
            "Hypopharynx",
            "Penis",
            "Femoral Artery",
            "Breast",
            "Autonomic Nervous System",
            "Femoral Vein",
            "Lymph Node(s) Cervical",
            "Rib",
            "Frontal Lobe",
            "Tibia",
            "Chest",
            "Epidural Space",
            "Forehead",
            "Carina",
            "Skeletal Muscle",
            "Anus",
            "Blood Vessel",
            "Fundus Of Stomach",
            "Adipose",
            "Lymph Node(s) Iliac-External",
            "Knee",
            "Mediastinum",
            "Uvula",
            "Fluid",
            "Sinus",
            "Retroperitoneum",
            "Trachea / Major Bronchi",
            "Acetabulum",
            "Lumbar Spine",
            "Lymph Node(s) Subclavicular",
            "Lymph Node(s) Pelvic",
            "Nasopharynx",
            "Sternum",
            "Sacrum",
            "Common Duct",
            "Mesentery",
            "Bone Marrow",
            "Lymph Nodes(s) Mediastinal",
            "Ampulla Of Vater",
            "Hepatic Vein",
            "Lymph Node(s) Popliteal",
            "Central Nervous System",
            "Lymph Node(s) Supraclavicular",
            "Seminal Vesicle",
            "Gum",
            "Ilium",
            "Esophageal; Mid",
            "Larynx",
            "Lymph Node",
            "Humerus",
            "Lymph Node(s) Parotid",
            "Fibroblasts",
            "Submandibular Gland",
            "Cell-Line",
            "Tongue",
            "Lymph Node(s) Splenic",
            "Thymus",
            "Conjunctiva",
            "Rectum",
            "Adrenal",
            "Shoulder",
            "Lymph Node(s) Epitrochlear",
            "Antrum",
            "Spinal Cord",
            "Esophagus",
            "Lymph Node(s) Internal Mammary",
            "Lymph Node(s) Inguinal",
            "Retina",
            "Sublingual Gland",
            "Cerebrospinal Fluid",
            "Ascending Colon Hepatic Flexure",
            "Endocrine Gland",
            "Popliteal Fossa",
            "Scrotum",
            "Eye",
            "Nerve(s) Cranial",
            "Brain",
            "Nasal Soft Tissue",
            "Ureter",
            "Retro-Orbital Region",
            "Cardia",
            "Palate",
            "Pituitary Gland",
            "Forearm",
            "Clitoris",
            "Antecubital Fossa",
            "Thigh",
            "Jejunum",
            "Capillary",
            "Jaw",
            "Urinary Tract",
        },
    )
    def biospecimen_anatomic_site(self, value):
        self._set_property("biospecimen_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Bilateral", "Left", "Right", "Not Reported"})
    def biospecimen_laterality(self, value):
        self._set_property("biospecimen_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def catalog_reference(self, value):
        self._set_property("catalog_reference", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "3D Organoid",
            "Control Analyte",
            "Sputum",
            "Peripheral Whole Blood",
            "Whole Bone Marrow",
            "Peripheral Blood Components NOS",
            "Bone Marrow Components",
            "Liquid Suspension Cell Line",
            "Bone Marrow Components NOS",
            "Saliva",
            "2D Classical Conditionally Reprogrammed Cells",
            "Pleural Effusion",
            "Unknown",
            "Buffy Coat",
            "Human Original Cells",
            "Buccal Cells",
            "Cell",
            "Solid Tissue",
            "Derived Cell Line",
            "Not Allowed To Collect",
            "Granulocytes",
            "Sorted Cells",
            "Fibroblasts from Bone Marrow Normal",
            "Adherent Cell Line",
            "Plasma",
            "Mononuclear Cells from Bone Marrow Normal",
            "2D Modified Conditionally Reprogrammed Cells",
            "Serum",
            "Mixed Adherent Suspension",
            "3D Neurosphere",
            "EBV Immortalized",
            "Lymphocytes",
            "3D Air-Liquid Interface Organoid",
            "Not Reported",
        },
    )
    def composition(self, value):
        self._set_property("composition", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def current_weight(self, value):
        self._set_property("current_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_collection(self, value):
        self._set_property("days_to_collection", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_sample_procurement(self, value):
        self._set_property("days_to_sample_procurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Yes", "Unknown", "Not Reported", "No", "Not Allowed To Collect"}
    )
    def diagnosis_pathologically_confirmed(self, value):
        self._set_property("diagnosis_pathologically_confirmed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Adjacent (< or = 2cm)", "Not Reported", "Distal (>2cm)"}
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

    @psqlgraph.pg_property(int, float)
    def initial_weight(self, value):
        self._set_property("initial_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def intermediate_dimension(self, value):
        self._set_property("intermediate_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def is_ffpe(self, value):
        self._set_property("is_ffpe", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def longest_dimension(self, value):
        self._set_property("longest_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Right Hemicolectomy",
            "Omentectomy",
            "Total Hepatectomy",
            "Partial Nephrectomy",
            "Laparoscopic Radical Prostatectomy with Robotics",
            "Pneumonectomy",
            "Radical Nephrectomy",
            "Laparoscopic Radical Prostatectomy without Robotics",
            "Laparoscopic Partial Nephrectomy",
            "Salpingo-oophorectomy",
            "Unknown",
            "Open Radical Nephrectomy",
            "Bone Marrow Aspirate",
            "Total Nephrectomy",
            "Parotidectomy, NOS",
            "Partial Maxillectomy",
            "Incisional Biopsy",
            "Needle Biopsy",
            "Other Surgical Resection",
            "Simple Hysterectomy",
            "Vertical Hemilaryngectomy",
            "Aspirate",
            "Punch Biopsy",
            "Wedge Resection",
            "Indeterminant",
            "Total Colectomy",
            "Left Hemicolectomy",
            "Radical Hysterectomy",
            "Salpingectomy",
            "Supraglottic Laryngectomy",
            "Glossectomy",
            "Lumpectomy",
            "Surgical Resection",
            "Endoscopic Mucosal Resection (EMR)",
            "Local Resection (Exoresection; wall resection)",
            "Hand Assisted Laparoscopic Radical Nephrectomy",
            "Mandibulectomy",
            "Transoral Laser Excision",
            "Transplant",
            "Maxillectomy",
            "Abdomino-perineal Resection of Rectum",
            "Open Partial Nephrectomy",
            "Not Reported",
            "Lobectomy",
            "Thoracentesis",
            "Oophorectomy",
            "Whipple Procedure",
            "Transurethral resection (TURBT)",
            "Cystectomy",
            "Total Mastectomy",
            "Subtotal Prostatectomy",
            "Endo Rectal Tumor Resection",
            "Sigmoid Colectomy",
            "Blood Draw",
            "Lymphadenectomy",
            "Biopsy",
            "Radical Prostatectomy",
            "Tumor Resection",
            "Fine Needle Aspiration",
            "Supracricoid Laryngectomy",
            "Lymph Node Dissection",
            "Pan-Procto Colectomy",
            "Other",
            "Thoracoscopic Biopsy",
            "Full Hysterectomy",
            "Tumor Debulking",
            "Orchiectomy",
            "Open Radical Prostatectomy",
            "Paracentesis",
            "Simple Mastectomy",
            "Ascites Drainage",
            "Excisional Biopsy",
            "Pancreatectomy",
            "Partial Hepatectomy",
            "Endolaryngeal Excision",
            "Not Allowed To Collect",
            "Laparoscopic Biopsy",
            "Transurethral Resection (TURP)",
            "Superficial Parotidectomy",
            "Transverse Colectomy",
            "Laryngopharyngectomy",
            "Autopsy",
            "Hysterectomy NOS",
            "Subtotal Resection",
            "Modified Radical Mastectomy",
            "Peritoneal Lavage",
            "Supracervical Hysterectomy",
            "Palatectomy",
            "Enucleation",
            "Open Craniotomy",
            "Metastasectomy",
            "Total Laryngectomy",
            "Partial Laryngectomy",
            "Deep Parotidectomy",
            "Tonsillectomy",
            "Liquid Biopsy",
            "Buccal Mucosal Resection",
            "Radical Maxillectomy",
            "Anterior Resection of Rectum",
            "Laparoscopic Radical Nephrectomy",
            "Endoscopic Biopsy",
            "Core Biopsy",
            "Gross Total Resection",
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
            "Unknown",
            "Snap Frozen",
            "Frozen",
            "FFPE",
            "Fresh",
            "OCT",
            "Not Reported",
            "Not Allowed To Collect",
            "Cryopreserved",
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
            "Control Analyte",
            "Expanded Next Generation Cancer Model",
            "Neoplasms of Uncertain and Unknown Behavior",
            "Human Tumor Original Cells",
            "Next Generation Cancer Model",
            "Slides",
            "Tumor Adjacent Normal - Post Neo-adjuvant Therapy",
            "GenomePlex (Rubicon) Amplified DNA",
            "FFPE Recurrent",
            "EBV Immortalized Normal",
            "Next Generation Cancer Model Expanded Under Non-conforming Conditions",
            "Repli-G X (Qiagen) DNA",
            "Primary Blood Derived Cancer - Peripheral Blood",
            "Saliva",
            "Lymphoid Normal",
            "Xenograft Tissue",
            "Pleural Effusion",
            "Unknown",
            "Cell Lines",
            "Total RNA",
            "Primary Xenograft Tissue",
            "Recurrent Tumor",
            "Not Allowed To Collect",
            "Granulocytes",
            "FFPE Scrolls",
            "Buccal Cell Normal",
            "Recurrent Blood Derived Cancer - Peripheral Blood",
            "Benign Neoplasms",
            "Fibroblasts from Bone Marrow Normal",
            "In Situ Neoplasms",
            "Tumor",
            "Cell Line Derived Xenograft Tissue",
            "Mononuclear Cells from Bone Marrow Normal",
            "Blood Derived Liquid Biopsy",
            "Primary Blood Derived Cancer - Bone Marrow",
            "Metastatic",
            "Blood Derived Cancer - Peripheral Blood, Post-treatment",
            "Post neo-adjuvant therapy",
            "Additional Metastatic",
            "Primary Tumor",
            "Mixed Adherent Suspension",
            "Blood Derived Normal",
            "Blood Derived Cancer - Peripheral Blood",
            "Recurrent Blood Derived Cancer - Bone Marrow",
            "RNA",
            "Repli-G (Qiagen) DNA",
            "Blood Derived Cancer - Bone Marrow",
            "Additional - New Primary",
            "Solid Tissue Normal",
            "Bone Marrow Normal",
            "Not Reported",
            "DNA",
            "Blood Derived Cancer - Bone Marrow, Post-treatment",
        },
    )
    def sample_type(self, value):
        self._set_property("sample_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "07",
            "50",
            "60",
            "03",
            "14",
            "32",
            "85",
            "12",
            "42",
            "41",
            "11",
            "30",
            "06",
            "05",
            "61",
            "08",
            "20",
            "04",
            "01",
            "16",
            "40",
            "15",
            "09",
            "02",
            "86",
            "87",
            "99",
            "31",
            "18",
            "17",
            "13",
            "10",
        },
    )
    def sample_type_id(self, value):
        self._set_property("sample_type_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def shortest_dimension(self, value):
        self._set_property("shortest_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "3D Organoid",
            "Control Analyte",
            "Sputum",
            "Peripheral Whole Blood",
            "Whole Bone Marrow",
            "Peripheral Blood NOS",
            "Peripheral Blood Components NOS",
            "Liquid Suspension Cell Line",
            "Bone Marrow Components NOS",
            "Saliva",
            "2D Classical Conditionally Reprogrammed Cells",
            "Pleural Effusion",
            "Unknown",
            "Buffy Coat",
            "Human Original Cells",
            "Buccal Cells",
            "Mononuclear Cells from Bone Marrow",
            "Cell",
            "Solid Tissue",
            "Derived Cell Line",
            "Granulocytes",
            "Sorted Cells",
            "Adherent Cell Line",
            "Plasma",
            "Lymphoid",
            "2D Modified Conditionally Reprogrammed Cells",
            "Serum",
            "Mixed Adherent Suspension",
            "3D Neurosphere",
            "EBV Immortalized",
            "Lymphocytes",
            "3D Air-Liquid Interface Organoid",
            "Fibroblasts from Bone Marrow",
            "Bone Marrow NOS",
            "Not Reported",
        },
    )
    def specimen_type(self, value):
        self._set_property("specimen_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def time_between_clamping_and_freezing(self, value):
        self._set_property("time_between_clamping_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def time_between_excision_and_freezing(self, value):
        self._set_property("time_between_excision_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Prospective", "Retrospective"})
    def tissue_collection_type(self, value):
        self._set_property("tissue_collection_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Abnormal",
            "Unknown",
            "Peritumoral",
            "Not Reported",
            "Not Allowed To Collect",
            "Tumor",
            "Normal",
        },
    )
    def tissue_type(self, value):
        self._set_property("tissue_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Anal Cancer (all types)",
            "Rhabdoid tumor (kidney) (RT)",
            "CNS, other",
            "Clear cell sarcoma of the kidney (CCSK)",
            "NHL, Burkitt lymphoma (BL)",
            "Rhabdomyosarcoma",
            "Cervical Cancer (all types)",
            "NHL, anaplastic large cell lymphoma",
            "Non cancerous tissue",
            "Acute myeloid leukemia (AML)",
            "Acute lymphoblastic leukemia (ALL)",
            "Soft tissue sarcoma, non-rhabdomyosarcoma",
            "CNS, medulloblastoma",
            "CNS, ependymoma",
            "Wilms tumor (WT)",
            "CNS, rhabdoid tumor",
            "Ewing sarcoma",
            "Lung Cancer (all types)",
            "CNS, glioblastoma (GBM)",
            "Diffuse Large B-Cell Lymphoma (DLBCL)",
            "Neuroblastoma (NBL)",
            "Osteosarcoma (OS)",
            "CNS, low grade glioma (LGG)",
            "Acute Leukemia of Ambiguous Lineage (ALAL)",
            "Induction Failure AML (AML-IF)",
        },
    )
    def tumor_code(self, value):
        self._set_property("tumor_code", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "51",
            "00",
            "21",
            "50",
            "61",
            "62",
            "20",
            "60",
            "04",
            "01",
            "03",
            "40",
            "63",
            "15",
            "02",
            "64",
            "71",
            "81",
            "52",
            "65",
            "41",
            "70",
            "80",
            "30",
            "10",
        },
    )
    def tumor_code_id(self, value):
        self._set_property("tumor_code_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Primary",
            "Xenograft",
            "Unknown",
            "Recurrence",
            "Not Applicable",
            "NOS",
            "New Primary",
            "Metastatic",
            "Premalignant",
            "Not Allowed To Collect",
            "Not Reported",
        },
    )
    def tumor_descriptor(self, value):
        self._set_property("tumor_descriptor", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Sample)
datetime_hooks.cls_inject_updated_datetime_hook(Sample)
