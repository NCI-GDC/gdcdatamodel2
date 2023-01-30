from typing import Any, Dict, List, Tuple, Union, Optional

import psqlgraph
from sqlalchemy.ext import hybrid
from sqlalchemy.orm import query, Session

from .helpers import (
    base,
    datetime_hooks,
    indexes,
    related_cases,
    versioning,
    versioned_nodes,
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
            "validated",
            "error",
            "md5summing",
            "released",
            "invalid",
            "live",
            "submitted",
            "md5summed",
            "uploading",
            "validating",
            "redacted",
            "uploaded",
            "suppressed",
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
            "Lacrimal Gland",
            "Thymus",
            "Cervical Spine",
            "Hip",
            "Subcutaneous Tissue",
            "Lumbar Spine",
            "Lymph Node(s) Supraclavicular",
            "Carina",
            "Occipital Cortex",
            "Hypopharynx",
            "Stomach - Mucosa Only",
            "Bronchus",
            "Pericardium",
            "Parotid Gland",
            "Spinal Column",
            "Mitochondria",
            "Blood Vessel",
            "Hand",
            "Testis",
            "Lymph Node(s) Distant",
            "Skin",
            "Fibula",
            "Adipose",
            "Ocular Orbits",
            "Sternum",
            "Lymph Node(s) Occipital",
            "Cerebrospinal Fluid",
            "Liver",
            "Synovium",
            "Popliteal Fossa",
            "Ear",
            "Bone Marrow",
            "Hepatic Vein",
            "Vein",
            "Vulva",
            "Mediastinum",
            "Round Ligament",
            "Esophageal; Mid",
            "Anal Sphincter",
            "Fluid",
            "Hippocampus",
            "Alveolar Ridge",
            "Nasal Cavity",
            "Oral Cavity",
            "Finger",
            "Foreskin",
            "Head & Neck",
            "Lip",
            "Thyroid",
            "Subglottis",
            "Frontal Lobe",
            "Pituitary Gland",
            "Hard Palate",
            "Ischium",
            "Fibroblasts",
            "Mesothelium",
            "Vas Deferens",
            "Lymph Node(s) Iliac-Common",
            "Buccal Cavity",
            "Sinus",
            "Lymph Node(s) Paraaortic",
            "Stomach",
            "Jejunum",
            "Skull",
            "Bowel",
            "Lymph Nodes(s) Mediastinal",
            "Sciatic Nerve",
            "Adenoid",
            "Gum",
            "Penis",
            "Tonsil",
            "Retro-Orbital Region",
            "Lymph Node(s) Inguinal",
            "Descending Colon",
            "Retina",
            "Cecum",
            "Chest",
            "Tibia",
            "Kidney",
            "Appendix",
            "Hepatic",
            "Throat",
            "Mandible",
            "Unknown",
            "Maxilla",
            "Lymph Node(s) Hilar",
            "Lymph Node(s) Cervical",
            "Chest Wall",
            "Laryngopharynx",
            "Fallopian Tube",
            "Arm",
            "Lung",
            "Lymph Node(s) Epitrochlear",
            "Index Finger",
            "Ankle",
            "Groin",
            "Dermal",
            "Shoulder",
            "Ampulla Of Vater",
            "Eye",
            "Buccal Mucosa",
            "Lymph Node(s) Retroperitoneal",
            "Leg",
            "Gallbladder",
            "Knee",
            "Urinary Tract",
            "Sublingual Gland",
            "Blood",
            "Transverse Colon",
            "Mesentery",
            "Splenic Flexure",
            "Thumb",
            "Vertebra",
            "Thigh",
            "Femoral Artery",
            "Common Duct",
            "Anus",
            "Cervix",
            "Bladder",
            "Broad Ligament",
            "Bone",
            "Brow",
            "Forearm",
            "Jaw",
            "Scrotum",
            "Large Bowel",
            "Humerus",
            "Ear Canal",
            "Fundus Of Stomach",
            "Lymph Node(s) Scalene",
            "Lymph Node(s) Splenic",
            "Clitoris",
            "Small Bowel",
            "Esophageal; Distal",
            "Sinus(es), Maxillary",
            "Joint",
            "Vagina",
            "Nasal Soft Tissue",
            "Neck",
            "Cell-Line",
            "Aorta",
            "Lymph Node(s) Popliteal",
            "Ilium",
            "Omentum",
            "Buttock",
            "Parathyroid",
            "Submandibular Gland",
            "Gastroesophageal Junction",
            "Cerebellum",
            "Ureter",
            "Rectosigmoid Junction",
            "Uterus",
            "Clavicle",
            "Elbow",
            "Forehead",
            "Connective Tissue",
            "Lymph Node(s) Mammary",
            "Paraspinal Ganglion",
            "Pelvis",
            "Sacrum",
            "Ascending Colon",
            "Foot",
            "Abdominal Wall",
            "Pancreas",
            "Auditory Canal",
            "Skeletal Muscle",
            "White Blood Cells",
            "Duodenum",
            "Paranasal Sinuses",
            "Trunk",
            "Antrum",
            "Placenta",
            "Capillary",
            "Peritoneum",
            "Uvula",
            "Colon",
            "Ovary",
            "Not Reported",
            "Spinal Cord",
            "Epidural Space",
            "Nerve",
            "Nails",
            "Small Finger",
            "Leptomeninges",
            "Epididymis",
            "Floor Of Mouth",
            "Cerebral Cortex",
            "Pineal",
            "Other",
            "Pylorus",
            "Ganglia",
            "Carotid Body",
            "Heart",
            "Lymph Node(s) Pelvic",
            "Nerve(s) Cranial",
            "Esophageal; Proximal",
            "Amniotic Fluid",
            "Venous",
            "Lymph Node(s) Iliac-External",
            "Temporal Cortex",
            "Small Bowel - Mucosa Only",
            "Hepatic Duct",
            "Lymph Node(s) Internal Mammary",
            "Esophagus",
            "Lymph Node(s) Subclavicular",
            "Mediastinal Soft Tissue",
            "Lymph Node(s) Mesenteric",
            "Nasopharynx",
            "Chin",
            "Antecubital Fossa",
            "Back",
            "Pineal Gland",
            "Gastrointestinal Tract",
            "Scapula",
            "Not Allowed To Collect",
            "Scalp",
            "Esophagus - Mucosa Only",
            "Anorectum",
            "Bronchiole",
            "Lymph Node",
            "Endocrine Gland",
            "Cerebrum",
            "Larynx",
            "Lymph Node(s) Regional",
            "Bile Duct",
            "Salivary Gland",
            "Axilla",
            "Lymph Node(s) Femoral",
            "Tonsil (Pharyngeal)",
            "Diaphragm",
            "Central Nervous System",
            "Tongue",
            "Lymph Node(s) Parotid",
            "Autonomic Nervous System",
            "Rib",
            "Wrist",
            "Hepatic Flexure",
            "Rectum",
            "Femoral Vein",
            "Oral Cavity - Mucosa Only",
            "Breast",
            "Calf",
            "Periorbital Soft Tissue",
            "Ear, Pinna (External)",
            "Carotid Artery",
            "Pharynx",
            "Pleura",
            "Thorax",
            "Head - Face Or Neck, Nos",
            "Islet Cells",
            "Esophagogastric Junction",
            "Lymph Node(s) Axilla",
            "Frontal Cortex",
            "Acetabulum",
            "Ligament",
            "Colon - Mucosa Only",
            "Brain Stem",
            "Seminal Vesicle",
            "Ascending Colon Hepatic Flexure",
            "Effusion",
            "Retroperitoneum",
            "Brain",
            "Aqueous Fluid",
            "Thoracic Spine",
            "Patella",
            "Oropharynx",
            "Conjunctiva",
            "Soft Tissue",
            "Cardia",
            "Prostate",
            "Umbilical Cord",
            "Peritoneal Cavity",
            "Ring Finger",
            "Tendon",
            "Glottis",
            "Sigmoid Colon",
            "Supraglottis",
            "Muscle",
            "Abdomen",
            "Artery",
            "Ileum",
            "Lymph Node(s) Submandibular",
            "Cartilage",
            "Urethra",
            "Palate",
            "Middle Finger",
            "Adrenal",
            "Femur",
            "Spleen",
            "Trachea / Major Bronchi",
            "Aortic Body",
        },
    )
    def biospecimen_anatomic_site(self, value):
        self._set_property("biospecimen_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Left", "Unknown", "Right", "Bilateral", "Not Reported"}
    )
    def biospecimen_laterality(self, value):
        self._set_property("biospecimen_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def catalog_reference(self, value):
        self._set_property("catalog_reference", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Bone Marrow Components",
            "Plasma",
            "Derived Cell Line",
            "Granulocytes",
            "Not Allowed To Collect",
            "Peripheral Whole Blood",
            "3D Neurosphere",
            "Not Reported",
            "3D Organoid",
            "Lymphocytes",
            "Control Analyte",
            "Solid Tissue",
            "Mononuclear Cells from Bone Marrow Normal",
            "2D Classical Conditionally Reprogrammed Cells",
            "Buccal Cells",
            "Bone Marrow Components NOS",
            "Adherent Cell Line",
            "Unknown",
            "Sorted Cells",
            "EBV Immortalized",
            "Human Original Cells",
            "Liquid Suspension Cell Line",
            "Whole Bone Marrow",
            "Pleural Effusion",
            "Peripheral Blood Components NOS",
            "Sputum",
            "Serum",
            "Buffy Coat",
            "Fibroblasts from Bone Marrow Normal",
            "Saliva",
            "2D Modified Conditionally Reprogrammed Cells",
            "3D Air-Liquid Interface Organoid",
            "Cell",
            "Mixed Adherent Suspension",
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
        str, enum={"Unknown", "Yes", "Not Reported", "No", "Not Allowed To Collect"}
    )
    def diagnosis_pathologically_confirmed(self, value):
        self._set_property("diagnosis_pathologically_confirmed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Distal (>2cm)", "Adjacent (< or = 2cm)", "Not Reported"}
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
            "Left Hemicolectomy",
            "Cystectomy",
            "Not Allowed To Collect",
            "Fine Needle Aspiration",
            "Supraglottic Laryngectomy",
            "Radical Prostatectomy",
            "Partial Laryngectomy",
            "Partial Nephrectomy",
            "Bone Marrow Aspirate",
            "Simple Mastectomy",
            "Right Hemicolectomy",
            "Sigmoid Colectomy",
            "Salpingo-oophorectomy",
            "Supracricoid Laryngectomy",
            "Subtotal Resection",
            "Total Laryngectomy",
            "Pancreatectomy",
            "Laparoscopic Radical Prostatectomy without Robotics",
            "Vertical Hemilaryngectomy",
            "Lumpectomy",
            "Supracervical Hysterectomy",
            "Tonsillectomy",
            "Total Colectomy",
            "Tumor Debulking",
            "Unknown",
            "Transoral Laser Excision",
            "Laparoscopic Radical Prostatectomy with Robotics",
            "Abdomino-perineal Resection of Rectum",
            "Open Craniotomy",
            "Thoracentesis",
            "Incisional Biopsy",
            "Salpingectomy",
            "Ascites Drainage",
            "Endoscopic Biopsy",
            "Endoscopic Mucosal Resection (EMR)",
            "Core Biopsy",
            "Needle Biopsy",
            "Pan-Procto Colectomy",
            "Open Partial Nephrectomy",
            "Lobectomy",
            "Paracentesis",
            "Deep Parotidectomy",
            "Metastasectomy",
            "Thoracoscopic Biopsy",
            "Total Nephrectomy",
            "Parotidectomy, NOS",
            "Laparoscopic Radical Nephrectomy",
            "Whipple Procedure",
            "Oophorectomy",
            "Tumor Resection",
            "Pneumonectomy",
            "Autopsy",
            "Open Radical Nephrectomy",
            "Gross Total Resection",
            "Palatectomy",
            "Liquid Biopsy",
            "Punch Biopsy",
            "Orchiectomy",
            "Modified Radical Mastectomy",
            "Transverse Colectomy",
            "Radical Maxillectomy",
            "Blood Draw",
            "Transurethral resection (TURBT)",
            "Surgical Resection",
            "Laparoscopic Biopsy",
            "Not Reported",
            "Laparoscopic Partial Nephrectomy",
            "Buccal Mucosal Resection",
            "Full Hysterectomy",
            "Wedge Resection",
            "Anterior Resection of Rectum",
            "Simple Hysterectomy",
            "Transplant",
            "Lymphadenectomy",
            "Total Mastectomy",
            "Glossectomy",
            "Transurethral Resection (TURP)",
            "Other",
            "Local Resection (Exoresection; wall resection)",
            "Other Surgical Resection",
            "Maxillectomy",
            "Aspirate",
            "Endolaryngeal Excision",
            "Superficial Parotidectomy",
            "Indeterminant",
            "Excisional Biopsy",
            "Biopsy",
            "Open Radical Prostatectomy",
            "Hysterectomy NOS",
            "Laryngopharyngectomy",
            "Total Hepatectomy",
            "Enucleation",
            "Lymph Node Dissection",
            "Radical Hysterectomy",
            "Radical Nephrectomy",
            "Peritoneal Lavage",
            "Mandibulectomy",
            "Subtotal Prostatectomy",
            "Endo Rectal Tumor Resection",
            "Omentectomy",
            "Partial Hepatectomy",
            "Hand Assisted Laparoscopic Radical Nephrectomy",
            "Partial Maxillectomy",
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
            "Frozen",
            "Fresh",
            "Cryopreserved",
            "Not Allowed To Collect",
            "OCT",
            "FFPE",
            "Not Reported",
            "Snap Frozen",
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
            "Blood Derived Normal",
            "Xenograft Tissue",
            "Neoplasms of Uncertain and Unknown Behavior",
            "Granulocytes",
            "Lymphoid Normal",
            "Not Allowed To Collect",
            "Primary Tumor",
            "Blood Derived Cancer - Bone Marrow, Post-treatment",
            "Not Reported",
            "Bone Marrow Normal",
            "Blood Derived Cancer - Peripheral Blood, Post-treatment",
            "RNA",
            "Control Analyte",
            "Tumor Adjacent Normal - Post Neo-adjuvant Therapy",
            "Expanded Next Generation Cancer Model",
            "Primary Blood Derived Cancer - Peripheral Blood",
            "Cell Lines",
            "Recurrent Tumor",
            "Tumor",
            "Mononuclear Cells from Bone Marrow Normal",
            "FFPE Recurrent",
            "Recurrent Blood Derived Cancer - Bone Marrow",
            "Slides",
            "Solid Tissue Normal",
            "Buccal Cell Normal",
            "Next Generation Cancer Model",
            "Human Tumor Original Cells",
            "Post neo-adjuvant therapy",
            "Metastatic",
            "Unknown",
            "Blood Derived Cancer - Peripheral Blood",
            "Next Generation Cancer Model Expanded Under Non-conforming Conditions",
            "Recurrent Blood Derived Cancer - Peripheral Blood",
            "EBV Immortalized Normal",
            "Additional Metastatic",
            "Cell Line Derived Xenograft Tissue",
            "Benign Neoplasms",
            "Additional - New Primary",
            "DNA",
            "GenomePlex (Rubicon) Amplified DNA",
            "Pleural Effusion",
            "Blood Derived Liquid Biopsy",
            "Primary Blood Derived Cancer - Bone Marrow",
            "Total RNA",
            "FFPE Scrolls",
            "Primary Xenograft Tissue",
            "Fibroblasts from Bone Marrow Normal",
            "Blood Derived Cancer - Bone Marrow",
            "Saliva",
            "Repli-G (Qiagen) DNA",
            "Repli-G X (Qiagen) DNA",
            "Mixed Adherent Suspension",
            "In Situ Neoplasms",
        },
    )
    def sample_type(self, value):
        self._set_property("sample_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "06",
            "40",
            "05",
            "99",
            "87",
            "16",
            "11",
            "03",
            "42",
            "60",
            "31",
            "02",
            "85",
            "01",
            "08",
            "30",
            "10",
            "20",
            "15",
            "04",
            "32",
            "41",
            "14",
            "50",
            "17",
            "09",
            "86",
            "07",
            "13",
            "61",
            "12",
            "18",
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
            "Plasma",
            "Fibroblasts from Bone Marrow",
            "Derived Cell Line",
            "Granulocytes",
            "Peripheral Whole Blood",
            "3D Neurosphere",
            "Lymphoid",
            "Not Reported",
            "3D Organoid",
            "Lymphocytes",
            "Control Analyte",
            "Solid Tissue",
            "2D Classical Conditionally Reprogrammed Cells",
            "Buccal Cells",
            "Bone Marrow Components NOS",
            "Adherent Cell Line",
            "Unknown",
            "Sorted Cells",
            "EBV Immortalized",
            "Human Original Cells",
            "Liquid Suspension Cell Line",
            "Peripheral Blood NOS",
            "Mononuclear Cells from Bone Marrow",
            "Whole Bone Marrow",
            "Pleural Effusion",
            "Bone Marrow NOS",
            "Peripheral Blood Components NOS",
            "Sputum",
            "Serum",
            "Buffy Coat",
            "Saliva",
            "2D Modified Conditionally Reprogrammed Cells",
            "3D Air-Liquid Interface Organoid",
            "Cell",
            "Mixed Adherent Suspension",
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
            "Unknown",
            "Peritumoral",
            "Not Reported",
            "Abnormal",
            "Tumor",
            "Normal",
            "Not Allowed To Collect",
        },
    )
    def tissue_type(self, value):
        self._set_property("tissue_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Cervical Cancer (all types)",
            "CNS, other",
            "Lung Cancer (all types)",
            "Acute lymphoblastic leukemia (ALL)",
            "CNS, low grade glioma (LGG)",
            "Acute myeloid leukemia (AML)",
            "Rhabdoid tumor (kidney) (RT)",
            "Anal Cancer (all types)",
            "CNS, rhabdoid tumor",
            "Neuroblastoma (NBL)",
            "CNS, medulloblastoma",
            "Rhabdomyosarcoma",
            "Non cancerous tissue",
            "Soft tissue sarcoma, non-rhabdomyosarcoma",
            "Ewing sarcoma",
            "NHL, anaplastic large cell lymphoma",
            "NHL, Burkitt lymphoma (BL)",
            "CNS, ependymoma",
            "Wilms tumor (WT)",
            "Osteosarcoma (OS)",
            "Acute Leukemia of Ambiguous Lineage (ALAL)",
            "CNS, glioblastoma (GBM)",
            "Clear cell sarcoma of the kidney (CCSK)",
            "Diffuse Large B-Cell Lymphoma (DLBCL)",
            "Induction Failure AML (AML-IF)",
        },
    )
    def tumor_code(self, value):
        self._set_property("tumor_code", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "30",
            "10",
            "63",
            "20",
            "71",
            "15",
            "64",
            "04",
            "62",
            "40",
            "41",
            "00",
            "03",
            "60",
            "50",
            "02",
            "52",
            "81",
            "01",
            "70",
            "21",
            "61",
            "80",
            "51",
            "65",
        },
    )
    def tumor_code_id(self, value):
        self._set_property("tumor_code_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Metastatic",
            "Recurrence",
            "Premalignant",
            "Unknown",
            "Primary",
            "Not Allowed To Collect",
            "Not Applicable",
            "Xenograft",
            "Not Reported",
            "New Primary",
            "NOS",
        },
    )
    def tumor_descriptor(self, value):
        self._set_property("tumor_descriptor", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Sample)
datetime_hooks.cls_inject_updated_datetime_hook(Sample)
