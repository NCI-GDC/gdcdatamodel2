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


class FollowUp(base.Node):
    __tablename__: str = "node_followup"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Follow-Up",
        "namespace": "https://gdc.cancer.gov",
        "category": "clinical",
        "submittable": True,
        "downloadable": False,
        "description": "A visit by a patient or study participant to a medical professional. A clinical encounter that encompasses planned and unplanned trial interventions, procedures and assessments that may be performed on a subject. A visit has a start and an end, each described with a rule. The process by which information about the health status of an individual is obtained before and after a study has officially closed; an activity that continues something that has already begun or that repeats something that has already been done.",
        "required": ["submitter_id", "days_to_follow_up", "cases"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "follow_up"

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
                "name": "follow_ups",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "molecular_tests": {
                "name": "follow_ups",
                "src_type": base.Node.get_subclass("molecular_test"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "follow_ups",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "follow_ups",
                "type": base.Node.get_subclass("case"),
            },
            "diagnoses": {
                "backref": "follow_ups",
                "type": base.Node.get_subclass("diagnosis"),
            },
            "molecular_tests": {
                "backref": "follow_ups",
                "type": base.Node.get_subclass("molecular_test"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "cases": {
                "edge_out": "_FollowUpDescribesCase_out",
                "dst_type": base.Node.get_subclass("case"),
            },
            "diagnoses": {
                "edge_out": "_FollowUpDescribesDiagnosis_out",
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
            "Gastrointestinal Anastomotic Leak",
            "Abdominal Soft Tissue Necrosis",
            "Nipple Deformity",
            "Ileal Fistula",
            "Adult Respiratory Distress Syndrome",
            "Jejunal Stenosis",
            "Duodenal Fistula",
            "Facial Muscle Weakness",
            "Muscle Weakness Upper Limb",
            "Duodenal Infection",
            "Skin Hyperpigmentation",
            "Flatulence",
            "Hip Fracture",
            "Pulmonary Valve Disease",
            "Blood Antidiuretic Hormone Abnormal",
            "Enterocolitis Infectious",
            "Joint Range of Motion Decreased Lumbar Spine",
            "Anorgasmia",
            "Flashing Lights",
            "Hemorrhoidal Hemorrhage",
            "Oligospermia",
            "Laryngeal Fistula",
            "Investigations - Other",
            "Cecal Infection",
            "Prolapse of Intestinal Stoma",
            "Sick Sinus Syndrome",
            "Dyspnea",
            "Myalgia",
            "Enterocolitis",
            "Purpura",
            "Bone Marrow Hypocellular",
            "Cardiac Disorders - Other",
            "Hypertriglyceridemia",
            "Blood Bilirubin Increased",
            "Hypocalcemia",
            "Dysgeusia",
            "Ileal Stenosis",
            "Ear Pain",
            "Peripheral Ischemia",
            "Leukoencephalopathy",
            "Cardiac Troponin I Increased",
            "Gallbladder Pain",
            "Edema Cerebral",
            "Intraoperative Head and Neck Injury",
            "Meningismus",
            "Dysarthria",
            "Gallbladder Fistula",
            "Dry Mouth",
            "Fetal Growth Retardation",
            "Vasculitis",
            "Bladder Perforation",
            "Tracheal Stenosis",
            "Allergic Rhinitis",
            "Hot Flashes",
            "Intraoperative Reproductive Tract Injury",
            "Photosensitivity",
            "Hypertrichosis",
            "Apnea",
            "Psychosis",
            "Urine Output Decreased",
            "Hypoglossal Nerve Disorder",
            "Pulmonary Fibrosis",
            "GGT Increased",
            "Neoplasms Benign, Malignant and Unspecified (Incl Cysts and Polyps) - Other",
            "Ventricular Tachycardia",
            "Injury to Jugular Vein",
            "Vaginal Dryness",
            "Unintended Pregnancy",
            "Nail Infection",
            "Intraoperative Musculoskeletal Injury",
            "Rectal Hemorrhage",
            "Postoperative Thoracic Procedure Complication",
            "Peripheral Motor Neuropathy",
            "Febrile Neutropenia",
            "Atrioventricular Block Complete",
            "Bladder Infection",
            "Chills",
            "Movements Involuntary",
            "Body Odor",
            "Pancreatitis",
            "Dry Skin",
            "Hyperthyroidism",
            "Intra-Abdominal Hemorrhage",
            "Biliary Tract Infection",
            "Growth Suppression",
            "Rectal Anastomotic Leak",
            "Floaters",
            "Hypophosphatemia",
            "Arachnoiditis",
            "Osteonecrosis of Jaw",
            "Lipase Increased",
            "Urostomy Obstruction",
            "Personality Change",
            "Weight Loss",
            "INR Increased",
            "Hepatic Necrosis",
            "Sore Throat",
            "Spermatic Cord Anastomotic Leak",
            "Vagus Nerve Disorder",
            "Cystitis Noninfective",
            "Mobitz Type I",
            "Lymph Node Pain",
            "Urinary Urgency",
            "Lymphocele",
            "Gastritis",
            "Lethargy",
            "Catheter Related Infection",
            "Retinal Tear",
            "Bile Duct Stenosis",
            "Vaginal Fistula",
            "Cholecystitis",
            "Anal Mucositis",
            "Central Nervous System Necrosis",
            "Pharyngeal Necrosis",
            "Treatment Related Secondary Malignancy",
            "Uterine Obstruction",
            "Perforation Bile Duct",
            "Depression",
            "Proteinuria",
            "Renal Calculi",
            "Superficial Soft Tissue Fibrosis",
            "Chylothorax",
            "Ileal Ulcer",
            "Anal Hemorrhage",
            "Prostate Infection",
            "Rash Pustular",
            "Otitis Media",
            "Corneal Infection",
            "Intraoperative Ear Injury",
            "Small Intestinal Mucositis",
            "Vaginal Infection",
            "Intraoperative Ocular Injury",
            "Depressed Level of Consciousness",
            "Lordosis",
            "Intestinal Stoma Site Bleeding",
            "Fallopian Tube Anastomotic Leak",
            "Laryngeal Obstruction",
            "Pain",
            "Urinary Tract Infection",
            "Spinal Fracture",
            "Vital Capacity Abnormal",
            "Cytokine Release Syndrome",
            "Libido Decreased",
            "Pancreatic Fistula",
            "Mediastinal Hemorrhage",
            "Spleen Disorder",
            "Hypoxia",
            "Vas Deferens Anastomotic Leak",
            "Hypothermia",
            "Precocious Puberty",
            "Pancreatic Anastomotic Leak",
            "Penile Infection",
            "Oculomotor Nerve Disorder",
            "Tricuspid Valve Disease",
            "Ileal Hemorrhage",
            "Vasovagal Reaction",
            "Vaginal Hemorrhage",
            "Death Neonatal",
            "Abdominal Distension",
            "Death NOS",
            "Cerebrospinal Fluid Leakage",
            "Dermatitis Radiation",
            "Dysmenorrhea",
            "Pericardial Effusion",
            "Aspartate Aminotransferase Increased",
            "Somnolence",
            "Hirsutism",
            "Injury, Poisoning and Procedural Complications - Other",
            "Small Intestinal Anastomotic Leak",
            "Hepatic Pain",
            "Gastroesophageal Reflux Disease",
            "Tracheostomy Site Bleeding",
            "Duodenal Perforation",
            "Carbon Monoxide Diffusing Capacity Decreased",
            "Lymph Leakage",
            "Vaginal Perforation",
            "Peripheral Sensory Neuropathy",
            "Toxic Epidermal Necrolysis",
            "Hoarseness",
            "Muscle Weakness Trunk",
            "Cataract",
            "Mucositis Oral",
            "Infusion Site Extravasation",
            "Bronchopleural Fistula",
            "Hemolytic Uremic Syndrome",
            "Hypohidrosis",
            "Typhlitis",
            "Asystole",
            "Pain in Extremity",
            "Spermatic Cord Obstruction",
            "Serum Amylase Increased",
            "Tooth Discoloration",
            "Urine Discoloration",
            "Blood Prolactin Abnormal",
            "Encephalomyelitis Infection",
            "Urinary Incontinence",
            "Disseminated Intravascular Coagulation",
            "Reversible Posterior Leukoencephalopathy Syndrome",
            "Vaginal Discharge",
            "Thromboembolic Event",
            "Arteritis Infective",
            "Esophageal Perforation",
            "Bronchospasm",
            "Hepatitis Viral",
            "Leukocytosis",
            "Duodenal Obstruction",
            "Lower Gastrointestinal Hemorrhage",
            "Mucosal Infection",
            "Myocarditis",
            "Photophobia",
            "Skin Ulceration",
            "Hemolysis",
            "Acoustic Nerve Disorder NOS",
            "Chronic Kidney Disease",
            "Lymphedema",
            "Laryngospasm",
            "Skin Induration",
            "Uterine Perforation",
            "Hypothyroidism",
            "Salivary Gland Fistula",
            "Tumor Lysis Syndrome",
            "Generalized Muscle Weakness",
            "Sinus Disorder",
            "Intraoperative Neurological Injury",
            "Leukemia Secondary to Oncology Chemotherapy",
            "Portal Vein Thrombosis",
            "Oral Cavity Fistula",
            "Atelectasis",
            "Azoospermia",
            "Fallopian Tube Perforation",
            "Bladder Spasm",
            "Arthritis",
            "IVth Nerve Disorder",
            "Peripheral Nerve Infection",
            "Sneezing",
            "Hemorrhoids",
            "Kidney Anastomotic Leak",
            "Seroma",
            "Testicular Hemorrhage",
            "Dry Eye",
            "Postnasal Drip",
            "Hypernatremia",
            "Serum Sickness",
            "Colonic Stenosis",
            "Oral Pain",
            "Intestinal Stoma Leak",
            "Urinary Tract Obstruction",
            "Tracheal Obstruction",
            "Optic Nerve Disorder",
            "Spermatic Cord Hemorrhage",
            "Gastric Ulcer",
            "Gastric Anastomotic Leak",
            "Esophageal Ulcer",
            "Radiculitis",
            "Erythroderma",
            "Rectal Necrosis",
            "Sepsis",
            "Acute Kidney Injury",
            "Pharyngitis",
            "Gum Infection",
            "Jejunal Perforation",
            "Forced Expiratory Volume Decreased",
            "Erythema Multiforme",
            "Ileal Obstruction",
            "External Ear Pain",
            "Ascites",
            "Esophagitis",
            "Pancreatic Enzymes Decreased",
            "Multi-Organ Failure",
            "Iron Overload",
            "Accessory Nerve Disorder",
            "Female Genital Tract Fistula",
            "Urethral Infection",
            "Heart Failure",
            "Dental Caries",
            "Capillary Leak Syndrome",
            "Constipation",
            "Gallbladder Perforation",
            "Mitral Valve Disease",
            "Scrotal Infection",
            "Rectal Stenosis",
            "Hearing Impaired",
            "Bone Infection",
            "Ischemia Cerebrovascular",
            "Cardiac Troponin T Increased",
            "Hypoglycemia",
            "Soft Tissue Necrosis Lower Limb",
            "Retinal Vascular Disorder",
            "Gastric Necrosis",
            "Dysesthesia",
            "Pelvic Soft Tissue Necrosis",
            "Platelet Count Decreased",
            "Epistaxis",
            "Hiccups",
            "Hepatic Failure",
            "Dizziness",
            "Nervous System Disorders - Other",
            "Hemoglobin Increased",
            "Bloating",
            "Intraoperative Renal Injury",
            "Retinoic Acid Syndrome",
            "Amnesia",
            "Vertigo",
            "Esophageal Pain",
            "Alanine Aminotransferase Increased",
            "Cholesterol High",
            "Middle Ear Inflammation",
            "Urostomy Leak",
            "Meningitis",
            "Flank Pain",
            "Edema Limbs",
            "Hydrocephalus",
            "Gait Disturbance",
            "Injury to Carotid Artery",
            "Hyperparathyroidism",
            "Transient Ischemic Attacks",
            "Brachial Plexopathy",
            "Pregnancy, Puerperium and Perinatal Conditions - Other",
            "Localized Edema",
            "Colitis",
            "Alcohol Intolerance",
            "Gallbladder Necrosis",
            "Gynecomastia",
            "Corneal Ulcer",
            "Intraoperative Cardiac Injury",
            "Anal Stenosis",
            "Vascular Access Complication",
            "Menopause",
            "Toothache",
            "Irritability",
            "Ankle Fracture",
            "Small Intestine Ulcer",
            "Memory Impairment",
            "Vaginal Inflammation",
            "Esophageal Infection",
            "Left Ventricular Systolic Dysfunction",
            "Intraoperative Gastrointestinal Injury",
            "Atrioventricular Block First Degree",
            "Nail Loss",
            "Esophageal Stenosis",
            "Weight Gain",
            "Peritoneal Necrosis",
            "Infusion Related Reaction",
            "Nausea",
            "Conduction Disorder",
            "Gastrointestinal Pain",
            "Keratitis",
            "Pulmonary Fistula",
            "Bladder Anastomotic Leak",
            "Fracture",
            "Alkalosis",
            "Fallopian Tube Obstruction",
            "Laryngeal Edema",
            "Retroperitoneal Hemorrhage",
            "Cardiac Arrest",
            "Pharyngolaryngeal Pain",
            "Gingival Pain",
            "Uveitis",
            "Hypoparathyroidism",
            "Unequal Limb Length",
            "Vascular Disorders - Other",
            "Restlessness",
            "Rash Acneiform",
            "Exostosis",
            "Urostomy Stenosis",
            "Esophageal Necrosis",
            "Anal Fistula",
            "Glucose Intolerance",
            "Ovarian Infection",
            "Delirium",
            "Urinary Tract Pain",
            "Eyelid Function Disorder",
            "Abducens Nerve Disorder",
            "Hematosalpinx",
            "Joint Effusion",
            "Social Circumstances - Other",
            "Hypotension",
            "Ear and Labyrinth Disorders - Other",
            "Ovulation Pain",
            "Esophageal Hemorrhage",
            "Thrombotic Thrombocytopenic Purpura",
            "Penile Pain",
            "Hyperuricemia",
            "Rectal Obstruction",
            "Gastric Stenosis",
            "Portal Hypertension",
            "Pharyngeal Mucositis",
            "Sinus Bradycardia",
            "External Ear Inflammation",
            "Dehydration",
            "Stridor",
            "Infections and Infestations - Other",
            "Respiratory, Thoracic and Mediastinal Disorders - Other",
            "Glossopharyngeal Nerve Disorder",
            "Burn",
            "Jejunal Ulcer",
            "Laryngitis",
            "Superior Vena Cava Syndrome",
            "Phlebitis Infective",
            "Nystagmus",
            "Phantom Pain",
            "Urethral Anastomotic Leak",
            "Metabolism and Nutrition Disorders - Other",
            "Conjunctivitis Infective",
            "Mobitz (Type) II Atrioventricular Block",
            "Ejaculation Disorder",
            "Irregular Menstruation",
            "Muscle Weakness Left-Sided",
            "Virilization",
            "Vaginal Stricture",
            "Intraoperative Urinary Injury",
            "Cecal Hemorrhage",
            "Premature Delivery",
            "Conjunctivitis",
            "Insomnia",
            "Intracranial Hemorrhage",
            "Myelitis",
            "Pharyngeal Fistula",
            "Phlebitis",
            "Bone Pain",
            "Stomach Pain",
            "Hypomagnesemia",
            "Jejunal Fistula",
            "Ovarian Hemorrhage",
            "Endocarditis Infective",
            "Paresthesia",
            "Musculoskeletal and Connective Tissue Disorders - Other",
            "Flu Like Symptoms",
            "Upper Respiratory Infection",
            "Lip Infection",
            "Anal Ulcer",
            "Suicide Attempt",
            "Visceral Arterial Ischemia",
            "Gastric Fistula",
            "Intraoperative Hemorrhage",
            "Renal Colic",
            "Voice Alteration",
            "Dysphasia",
            "Biliary Anastomotic Leak",
            "Jejunal Obstruction",
            "Bronchopulmonary Hemorrhage",
            "Recurrent Laryngeal Nerve Palsy",
            "Avascular Necrosis",
            "Oral Dysesthesia",
            "Blood Corticotrophin Decreased",
            "Wound Infection",
            "Gastrointestinal Stoma Necrosis",
            "Psychiatric Disorders - Other",
            "Presyncope",
            "Suicidal Ideation",
            "Eye Disorders - Other",
            "Ventricular Fibrillation",
            "Hyperglycemia",
            "Small Intestinal Perforation",
            "Glaucoma",
            "Syncope",
            "Anemia",
            "Non-Cardiac Chest Pain",
            "Esophageal Varices Hemorrhage",
            "Spasticity",
            "Neuralgia",
            "Fat Atrophy",
            "Pleuritic Pain",
            "Hallucinations",
            "Pulmonary Edema",
            "Joint Infection",
            "Hypersomnia",
            "Scoliosis",
            "Restrictive Cardiomyopathy",
            "Pancreas Infection",
            "Lymphocyte Count Increased",
            "Intraoperative Hepatobiliary Injury",
            "Hematoma",
            "Fibrinogen Decreased",
            "Gastric Hemorrhage",
            "Skin Atrophy",
            "Duodenal Stenosis",
            "Aphonia",
            "Buttock Pain",
            "Dysphagia",
            "Lymphocyte Count Decreased",
            "Watering Eyes",
            "Sinus Pain",
            "Testicular Disorder",
            "Venous Injury",
            "Bronchial Obstruction",
            "Muscle Weakness Right-Sided",
            "Laryngeal Mucositis",
            "Tooth Development Disorder",
            "Akathisia",
            "Rash Maculo-Papular",
            "Salivary Gland Infection",
            "Extraocular Muscle Paresis",
            "Wound Complication",
            "Pericardial Tamponade",
            "Pelvic Floor Muscle Weakness",
            "Radiation Recall Reaction (Dermatologic)",
            "Tracheal Mucositis",
            "Ileus",
            "Laryngeal Inflammation",
            "Lymph Gland Infection",
            "Urinary Retention",
            "Esophageal Anastomotic Leak",
            "Hyponatremia",
            "General Disorders and Administration Site Conditions - Other",
            "Fetal Death",
            "Tracheal Fistula",
            "Vaginal Anastomotic Leak",
            "Hepatic Infection",
            "Endophthalmitis",
            "Pericarditis",
            "Confusion",
            "Periorbital Infection",
            "Pyramidal Tract Syndrome",
            "Prostatic Obstruction",
            "Adrenal Insufficiency",
            "Joint Range of Motion Decreased Cervical Spine",
            "Scalp Pain",
            "Stomal Ulcer",
            "Tinnitus",
            "Neck Soft Tissue Necrosis",
            "Hypercalcemia",
            "Ventricular Arrhythmia",
            "Allergic Reaction",
            "Sudden Death NOS",
            "Bronchial Fistula",
            "Rectal Pain",
            "Cheilitis",
            "Cushingoid",
            "Growth Hormone Abnormal",
            "Headache",
            "Injection Site Reaction",
            "Ovarian Rupture",
            "Colonic Fistula",
            "Gastrointestinal Disorders - Other",
            "Hypermagnesemia",
            "Aspiration",
            "Delayed Puberty",
            "Gastric Perforation",
            "Renal and Urinary Disorders - Other",
            "Myocardial Infarction",
            "Papilledema",
            "Sleep Apnea",
            "Ureteric Anastomotic Leak",
            "Esophageal Fistula",
            "Pancreatic Hemorrhage",
            "Anal Pain",
            "Neutrophil Count Decreased",
            "Laryngopharyngeal Dysesthesia",
            "CPK Increased",
            "Prolapse of Urostomy",
            "Skin Hypopigmentation",
            "Soft Tissue Infection",
            "Fibrosis Deep Connective Tissue",
            "Oral Hemorrhage",
            "Renal Hemorrhage",
            "Vulval Infection",
            "Acute Coronary Syndrome",
            "Anorexia",
            "Uterine Pain",
            "Olfactory Nerve Disorder",
            "Biliary Fistula",
            "Edema Face",
            "Hypertension",
            "Uterine Anastomotic Leak",
            "Duodenal Ulcer",
            "Pulmonary Hypertension",
            "Tracheal Hemorrhage",
            "Periodontal Disease",
            "Bruising",
            "Ejection Fraction Decreased",
            "Tooth Infection",
            "Uterine Infection",
            "Vomiting",
            "White Blood Cell Decreased",
            "Alkaline Phosphatase Increased",
            "Pleural Hemorrhage",
            "Endocrine Disorders - Other",
            "Immune System Disorders - Other",
            "Dyspareunia",
            "Pelvic Pain",
            "Hepatobiliary Disorders - Other",
            "Fecal Incontinence",
            "Urinary Frequency",
            "Superficial Thrombophlebitis",
            "Muscle Weakness Lower Limb",
            "Head Soft Tissue Necrosis",
            "Arterial Injury",
            "Infective Myositis",
            "Aortic Injury",
            "Periorbital Edema",
            "Small Intestine Infection",
            "Feminization Acquired",
            "Pharyngeal Anastomotic Leak",
            "Aortic Valve Disease",
            "Postoperative Hemorrhage",
            "Cranial Nerve Infection",
            "Anxiety",
            "Blood and Lymphatic System Disorders - Other",
            "Rectal Ulcer",
            "Blood Gonadotrophin Abnormal",
            "Urticaria",
            "Fall",
            "Appendicitis",
            "Extrapyramidal Disorder",
            "Surgical and Medical Procedures - Other",
            "Facial Nerve Disorder",
            "Upper Gastrointestinal Hemorrhage",
            "Activated Partial Thromboplastin Time Prolonged",
            "Sinus Tachycardia",
            "Sinusitis",
            "Vaginal Pain",
            "Pain of Skin",
            "Vestibular Disorder",
            "Tumor Pain",
            "Osteoporosis",
            "Flushing",
            "Acidosis",
            "Stenosis of Gastrointestinal Stoma",
            "Rhinitis Infective",
            "Vitreous Hemorrhage",
            "Splenic Infection",
            "Injury to Superior Vena Cava",
            "Urostomy Site Bleeding",
            "Ileal Perforation",
            "Breast Infection",
            "Eye Infection",
            "Pancreatic Duct Stenosis",
            "Erectile Dysfunction",
            "Hypoalbuminemia",
            "Night Blindness",
            "Hemoglobinuria",
            "Palmar-Plantar Erythrodysesthesia Syndrome",
            "Perineal Pain",
            "Musculoskeletal Deformity",
            "Stoma Site Infection",
            "Vaginal Obstruction",
            "Intraoperative Breast Injury",
            "Pancreatic Necrosis",
            "Bronchial Infection",
            "Pharyngeal Hemorrhage",
            "Trigeminal Nerve Disorder",
            "Pleural Infection",
            "Lipohypertrophy",
            "Colonic Perforation",
            "Constrictive Pericarditis",
            "Large Intestinal Anastomotic Leak",
            "Uterine Fistula",
            "Blurred Vision",
            "Abdominal Pain",
            "Intestinal Stoma Obstruction",
            "Palpitations",
            "Abdominal Infection",
            "Autoimmune Disorder",
            "Esophageal Obstruction",
            "Joint Range of Motion Decreased",
            "Wheezing",
            "Right Ventricular Dysfunction",
            "Alopecia",
            "Retinal Detachment",
            "Retinopathy",
            "Soft Tissue Necrosis Upper Limb",
            "CD4 Lymphocytes Decreased",
            "Hypokalemia",
            "Uterine Hemorrhage",
            "Intraoperative Arterial Injury",
            "Anorectal Infection",
            "Otitis Externa",
            "Malaise",
            "Hepatic Hemorrhage",
            "Facial Pain",
            "Lip Pain",
            "Gallbladder Infection",
            "Vaginismus",
            "Gastrointestinal Fistula",
            "Euphoria",
            "Agitation",
            "Neck Pain",
            "Prostatic Pain",
            "Neck Edema",
            "Pneumothorax",
            "Intraoperative Skin Injury",
            "Nasal Congestion",
            "Fatigue",
            "Bullous Dermatitis",
            "Myositis",
            "Breast Atrophy",
            "Fallopian Tube Stenosis",
            "Dyspepsia",
            "Skin Infection",
            "Pelvic Infection",
            "Testicular Pain",
            "Laryngeal Hemorrhage",
            "Injury to Inferior Vena Cava",
            "Tremor",
            "Edema Trunk",
            "Malabsorption",
            "Fever",
            "Obstruction Gastric",
            "Hyperkalemia",
            "Atrial Flutter",
            "Congenital, Familial and Genetic Disorders - Other",
            "Chest Pain - Cardiac",
            "Jejunal Hemorrhage",
            "Nail Discoloration",
            "Kyphosis",
            "Proctitis",
            "Gastroparesis",
            "Delayed Orgasm",
            "Concentration Impairment",
            "Kidney Infection",
            "Laryngeal Stenosis",
            "Pleural Effusion",
            "Intraoperative Respiratory Injury",
            "Ataxia",
            "Mediastinal Infection",
            "Myelodysplastic Syndrome",
            "Enterovesical Fistula",
            "Obesity",
            "Libido Increased",
            "Pneumonitis",
            "Skin and Subcutaneous Tissue Disorders - Other",
            "Productive Cough",
            "Peritoneal Infection",
            "Gallbladder Obstruction",
            "Telangiectasia",
            "Back Pain",
            "Diarrhea",
            "Intraoperative Splenic Injury",
            "Rectal Mucositis",
            "Hematuria",
            "Hyperhidrosis",
            "Device Related Infection",
            "Duodenal Hemorrhage",
            "Tracheitis",
            "Stevens-Johnson Syndrome",
            "Pruritus",
            "Intraoperative Venous Injury",
            "Wrist Fracture",
            "Colonic Obstruction",
            "Papulopustular Rash",
            "Rectal Fistula",
            "Colonic Hemorrhage",
            "Salivary Duct Inflammation",
            "Pharyngeal Stenosis",
            "Reproductive System and Breast Disorders - Other",
            "Bronchial Stricture",
            "Urinary Fistula",
            "Cognitive Disturbance",
            "Encephalitis Infection",
            "Encephalopathy",
            "Cough",
            "Scrotal Pain",
            "Scleral Disorder",
            "Paroxysmal Atrial Tachycardia",
            "Stroke",
            "Growth Accelerated",
            "Appendicitis Perforated",
            "Intraoperative Endocrine Injury",
            "Premature Menopause",
            "Colonic Ulcer",
            "Breast Pain",
            "Paronychia",
            "Prostatic Hemorrhage",
            "Supraventricular Tachycardia",
            "Seizure",
            "Eye Pain",
            "Menorrhagia",
            "Small Intestinal Stenosis",
            "Nail Ridging",
            "Creatinine Increased",
            "Lactation Disorder",
            "Small Intestinal Obstruction",
            "Lung Infection",
            "Rectal Perforation",
            "Anal Necrosis",
            "Trismus",
            "Atrial Fibrillation",
            "Respiratory Failure",
            "Chest Wall Pain",
            "Cervicitis Infection",
            "Wolff-Parkinson-White Syndrome",
            "Mania",
            "Anaphylaxis",
            "Wound Dehiscence",
            "Haptoglobin Decreased",
            "Delusions",
            "Arthralgia",
            "Genital Edema",
            "Electrocardiogram QT Corrected Interval Prolonged",
        },
    )
    def adverse_event(self, value):
        self._set_property("adverse_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Grade 2", "Grade 1", "Grade 4", "Grade 3", "Grade 5"})
    def adverse_event_grade(self, value):
        self._set_property("adverse_event_grade", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Mycobacterium, NOS",
            "Coccidioidomycosis",
            "Salmonella Septicemia",
            "Toxoplasmosis",
            "Histoplasmosis",
            "Mycobacterium tuberculosis",
            "Cryptococcosis",
            "Encephalopathy",
            "Nocardiosis",
            "Wasting Syndrome",
            "Herpes Simplex Virus",
            "Cryptosporidiosis, Chronic Intestinal",
            "Isosporiasis",
            "Progressive Multifocal Leukoencephalopathy",
            "Pneumocystis Pneumonia",
            "Pneumonia, NOS",
            "Candidiasis",
            "Cytomegalovirus",
            "Mycobacterium avium Complex",
        },
    )
    def aids_risk_factors(self, value):
        self._set_property("aids_risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def barretts_esophagus_goblet_cells_present(self, value):
        self._set_property("barretts_esophagus_goblet_cells_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def body_surface_area(self, value):
        self._set_property("body_surface_area", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def bmi(self, value):
        self._set_property("bmi", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def cause_of_response(self, value):
        self._set_property("cause_of_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def cd4_count(self, value):
        self._set_property("cd4_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Homosexual Contact",
            "None",
            "Not Reported",
            "Heterosexual Contact",
            "Hemophiliac",
            "Unknown",
            "Transfusion Recipient",
            "Intravenous Drug User",
        },
    )
    def cdc_hiv_risk_factors(self, value):
        self._set_property("cdc_hiv_risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def comorbidities(self, value):
        self._set_property("comorbidities", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Rubinstein-Taybi Syndrome",
            "Adenocarcinoma",
            "Human Papillomavirus Infection",
            "Hypertension",
            "Metabolic Syndrome",
            "Other Pulmonary Complications",
            "Malaria",
            "Kidney Disease",
            "Basal Cell Carcinoma",
            "Gorlin Syndrome",
            "Alpha-1 Antitrypsin",
            "Herpes Zoster",
            "Allergies",
            "Diet Controlled Diabetes",
            "Bone Fracture(s)",
            "Pain (Various)",
            "Liver Cirrhosis (Liver Disease)",
            "Clonal Hematopoiesis",
            "Hepatitis C Infection",
            "Mycobacterium avium Complex",
            "COPD",
            "Chronic Fatigue Syndrome",
            "Staph Osteomyelitis",
            "Calcium Channel Blockers",
            "Li-Fraumeni Syndrome",
            "Chlamydia",
            "Osteoarthritis",
            "Barrett's Esophagus",
            "Hemorrhagic Cystitis",
            "Tuberculosis",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Organ transplant (site)",
            "Renal Insufficiency",
            "Hypothyroidism",
            "Anxiety",
            "Renal Failure (Requiring Dialysis)",
            "Bronchitis",
            "Hashimoto's Thyroiditis",
            "Hepatitis B Infection",
            "Turcot Syndrome",
            "Coronary Artery Disease",
            "Arthritis",
            "Hereditary Non-polyposis Colon Cancer",
            "Hepatitis A Infection",
            "Epstein-Barr Virus",
            "Ischemic Heart Disease",
            "H. pylori Infection",
            "Other Cancer Within 5 Years",
            "Fibromyalgia",
            "Crohn's Disease",
            "Pregnancy in Patient or Partner",
            "Deep Vein Thrombosis / Thromboembolism",
            "Pulmonary Fibrosis",
            "Transient Ischemic Attack",
            "Cirrhosis, Unknown Etiology",
            "Ataxia-telangiectasia",
            "High Grade Liver Dysplastic Nodule",
            "Hypercholesterolemia",
            "Colon Polyps",
            "CNS Infection",
            "Lymphamatoid Papulosis",
            "Dyslipidemia",
            "Neuroendocrine Tumor",
            "Diabetes, Type II",
            "Rheumatologic Disease",
            "Liver Toxicity (Non-Infectious)",
            "Renal Dialysis",
            "Avascular Necrosis",
            "Connective Tissue Disorder",
            "Cytomegalovirus (CMV)",
            "Pancreatitis",
            "Rheumatoid Arthritis",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Unknown",
            "Myasthenia Gravis",
            "HUS/TTP",
            "Lynch Syndrome",
            "Joint Replacement",
            "Shingles",
            "Hypospadias",
            "Hyperglycemia",
            "Cerebrovascular Disease",
            "Osteoporosis or Osteopenia",
            "Pneumocystis Pneumonia",
            "Glaucoma",
            "Treponema pallidum",
            "Wagr Syndrome",
            "Anemia",
            "GERD",
            "Iron Overload",
            "Psoriasis",
            "Smoking",
            "Peptic Ulcer (Ulcer)",
            "Pulmonary Hemorrhage",
            "Glycogen Storage Disease",
            "Sleep apnea",
            "Adrenocortical Insufficiency",
            "Lymphocytic Meningitis",
            "Gastritis",
            "Behcet's Disease",
            "Varicella Zoster Virus",
            "Intraductal Papillary Mucinous Neoplasm",
            "Dermatomyosis",
            "Tyrosinemia",
            "Eczema",
            "Cholelithiasis",
            "Hemihypertrophy",
            "Chloroma",
            "Heart Disease",
            "Common Variable Immunodeficiency",
            "Other",
            "Epilepsy",
            "MAI",
            "Blood Clots",
            "Adenomatous Polyposis Coli",
            "Peripheral Vascular Disease",
            "HIV / AIDS",
            "Obesity",
            "Biliary Disorder",
            "Inflammatory Bowel Disease",
            "Diverticulitis",
            "Depression",
            "Steatosis",
            "Congestive Heart Failure (CHF)",
            "Arrhythmia",
            "Gout",
            "EBV Lymphoproliferation",
            "Acute Renal Failure",
            "Methicillin-Resistant Staphylococcus aureus (MRSA)",
            "Chronic Renal Failure",
            "DVT/PE",
            "Herpes",
            "Hepatitis",
            "Peripheral Neuropathy",
            "Other Nonmalignant Systemic Disease",
            "Chronic Pancreatitis",
            "Cryptogenic Organizing Pneumonia",
            "Hypercalcemia",
            "Lupus",
            "Cataracts",
            "Denys-Drash Syndrome",
            "Sarcoidosis",
            "Stroke",
            "Diabetes",
            "Sjogren's Syndrome",
            "Ulcerative Colitis",
            "Urinary Tract Infection",
            "Down Syndrome",
            "Hepatitis, Chronic",
            "Hyperlipidemia",
            "Low Grade Liver Dysplastic Nodule",
            "Nonalcoholic Steatohepatitis",
            "Peutz-Jeghers Disease",
            "Not Reported",
            "Seizure",
            "Bacteroides fragilis",
            "Insulin Controlled Diabetes",
            "Celiac Disease",
            "Headache",
            "Interstitial Pneumontis or ARDS",
            "Staphylococcus aureus",
            "Hodgkin Lymphoma",
            "Thyroid Disease, Non-Cancer",
            "Cancer",
            "ITP",
            "Diabetic Neuropathy",
            "Atrial Fibrillation",
            "Myocardial Infarction",
            "Beckwith-Wiedemann",
            "Primary Sclerosing Cholangitis",
            "Syphilis",
            "Gastroesophageal Reflux Disease",
            "Familial Adenomatous Polyposis",
            "Fibrosis",
            "Gonadal Dysfunction",
            "Asthma",
            "Abnormal Glucose Level",
            "Chronic Systemic Steroid Use",
            "Cryptococcal Meningitis",
            "Fanconi Anemia",
        },
    )
    def comorbidity(self, value):
        self._set_property("comorbidity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Pathology", "Radiology", "Unknown", "Histology", "Not Reported"}
    )
    def comorbidity_method_of_diagnosis(self, value):
        self._set_property("comorbidity_method_of_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_adverse_event(self, value):
        self._set_property("days_to_adverse_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_comorbidity(self, value):
        self._set_property("days_to_comorbidity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_first_event(self, value):
        self._set_property("days_to_first_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), int)
    def days_to_follow_up(self, value):
        self._set_property("days_to_follow_up", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_imaging(self, value):
        self._set_property("days_to_imaging", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_progression(self, value):
        self._set_property("days_to_progression", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_progression_free(self, value):
        self._set_property("days_to_progression_free", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_recurrence(self, value):
        self._set_property("days_to_recurrence", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_risk_factor(self, value):
        self._set_property("days_to_risk_factor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Diet",
            "Oral Hypoglycemic",
            "Sulfonylurea",
            "Linagliptin",
            "Other",
            "Not Reported",
            "Unknown",
            "Thiazolidinedione",
            "Biguanide",
            "Injected Insulin",
            "Insulin",
            "Alpha-Glucosidase Inhibitor",
        },
    )
    def diabetes_treatment_type(self, value):
        self._set_property("diabetes_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "sCR-Stringent Complete Response",
            "MX-Mixed Response",
            "PSR-Pseudoresponse",
            "IMR-Immunoresponse",
            "BED-Biochemical Evidence of Disease",
            "RP-Response",
            "PB-Palliative Benefit",
            "PPD-Pseudoprogression",
            "PDM-Persistent Distant Metastasis",
            "PA-Palliative Therapy",
            "IPD-Immunoprogression",
            "DU-Disease Unchanged",
            "PLD-Persistent Locoregional Disease",
            "SPD-Surgical Progression",
            "TE-Too Early",
            "Not Reported",
            "SD-Stable Disease",
            "PR-Partial Response",
            "RPD-Radiographic Progressive Disease",
            "CRU-Complete Response Unconfirmed",
            "Non-CR/Non-PD-Non-CR/Non-PD",
            "TF-Tumor Free",
            "WT-With Tumor",
            "Unknown",
            "NR-No Response",
            "MR-Minimal/Marginal response",
            "VGPR-Very Good Partial Response",
            "PD-Progressive Disease",
            "CPD-Clinical Progression",
            "AJ-Adjuvant Therapy",
            "RD-Responsive Disease",
            "NPB-No Palliative Benefit",
            "CR-Complete Response",
        },
    )
    def disease_response(self, value):
        self._set_property("disease_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def dlco_ref_predictive_percent(self, value):
        self._set_property("dlco_ref_predictive_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"1", "0", "3", "4", "5", "2", "Not Reported", "Unknown"})
    def ecog_performance_status(self, value):
        self._set_property("ecog_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Convincing Image Source", "Histologic Confirmation"})
    def evidence_of_progression_type(self, value):
        self._set_property("evidence_of_progression_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Convincing Image Source",
            "Biopsy with Histologic Confirmation",
            "Positive Biomarker(s)",
            "Physical Examination",
            "Histologic Confirmation",
        },
    )
    def evidence_of_recurrence_type(self, value):
        self._set_property("evidence_of_recurrence_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Hazel",
            "Blue",
            "Other",
            "Red & Violet",
            "Not Reported",
            "Amber",
            "Green",
            "Gray",
            "Brown",
        },
    )
    def eye_color(self, value):
        self._set_property("eye_color", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def fev1_ref_post_bronch_percent(self, value):
        self._set_property("fev1_ref_post_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def fev1_ref_pre_bronch_percent(self, value):
        self._set_property("fev1_ref_pre_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def fev1_fvc_pre_bronch_percent(self, value):
        self._set_property("fev1_fvc_pre_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def fev1_fvc_post_bronch_percent(self, value):
        self._set_property("fev1_fvc_post_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "None",
            "Death",
            "Censored",
            "Induction Failure",
            "Other",
            "Death without Remission",
            "Relapse",
            "Second Malignant Neoplasm",
            "Not Reported",
            "Induction Death",
            "Event",
            "Progression",
        },
    )
    def first_event(self, value):
        self._set_property("first_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def haart_treatment_indicator(self, value):
        self._set_property("haart_treatment_indicator", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def height(self, value):
        self._set_property("height", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def hepatitis_sustained_virological_response(self, value):
        self._set_property("hepatitis_sustained_virological_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Yes", "No"})
    def history_of_tumor(self, value):
        self._set_property("history_of_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Lower Grade Glioma",
            "Phenochromocytoma or Paraganglioma",
            "Colorectal Cancer",
        },
    )
    def history_of_tumor_type(self, value):
        self._set_property("history_of_tumor_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def hiv_viral_load(self, value):
        self._set_property("hiv_viral_load", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Progestin and Estrogen", "Progestin", "Not Reported", "Unknown"}
    )
    def hormonal_contraceptive_type(self, value):
        self._set_property("hormonal_contraceptive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={"Current User", "Never Used", "Former User", "Unknown", "Not Reported"},
    )
    def hormonal_contraceptive_use(self, value):
        self._set_property("hormonal_contraceptive_use", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Progesterone and Estrogen",
            "Progesterone only",
            "Estrogen only",
            "Unknown",
            "Not Reported",
        },
    )
    def hormone_replacement_therapy_type(self, value):
        self._set_property("hormone_replacement_therapy_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "31",
            "66",
            "Other",
            "63",
            "35",
            "53",
            "68",
            "45",
            "33",
            "16",
            "82",
            "Unknown",
            "39",
            "56",
            "18",
            "58",
            "Not Reported",
            "26",
            "73",
            "52",
            "70",
            "59",
            "51",
        },
    )
    def hpv_positive_type(self, value):
        self._set_property("hpv_positive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Vagina",
            "None",
            "Macroscopic Parametrium",
            "Microscopic Parametrium",
            "Bladder",
            "Unknown",
            "Not Reported",
        },
    )
    def hysterectomy_margins_involved(self, value):
        self._set_property("hysterectomy_margins_involved", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Simple Hysterectomy",
            "Not performed",
            "Hysterectomy, NOS",
            "Unknown",
            "Not Reported",
            "Radical Hysterectomy",
        },
    )
    def hysterectomy_type(self, value):
        self._set_property("hysterectomy_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def imaging_anatomic_site(self, value):
        self._set_property("imaging_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Liver Involvement",
            "Vena Cava Involvement/Thrombus",
            "Not Reported",
            "Retroperitoneal Lymph Node Involvement",
            "Carcinomatosis",
            "Lung Involvement",
            "Kidney Involvement",
            "Normal",
        },
    )
    def imaging_findings(self, value):
        self._set_property("imaging_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Not Performed",
            "Negative",
            "Indeterminate",
            "Not Reported",
            "Positive",
        },
    )
    def imaging_result(self, value):
        self._set_property("imaging_result", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def imaging_suv(self, value):
        self._set_property("imaging_suv", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def imaging_suv_max(self, value):
        self._set_property("imaging_suv_max", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"99mTc Bone Scintigraphy", "PET", "CT Scan", "MRI"})
    def imaging_type(self, value):
        self._set_property("imaging_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "None",
            "Azathioprine",
            "Other",
            "Methotrexate",
            "Anti-TNF Therapy",
            "Not Reported",
            "Unknown",
            "Cyclophosphamide",
        },
    )
    def immunosuppressive_treatment_type(self, value):
        self._set_property("immunosuppressive_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "0",
            "Unknown",
            "Not Reported",
            "10",
            "100",
            "60",
            "20",
            "90",
            "30",
            "50",
            "80",
            "70",
            "40",
        },
    )
    def karnofsky_performance_status(self, value):
        self._set_property("karnofsky_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Postmenopausal",
            "Premenopausal",
            "Perimenopausal",
            "Unknown",
            "Not Reported",
        },
    )
    def menopause_status(self, value):
        self._set_property("menopause_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def nadir_cd4_count(self, value):
        self._set_property("nadir_cd4_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def pancreatitis_onset_year(self, value):
        self._set_property("pancreatitis_onset_year", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Negative", "Not Reported", "Positive"})
    def peritoneal_washing_results(self, value):
        self._set_property("peritoneal_washing_results", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def pregnancy_count(self, value):
        self._set_property("pregnancy_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Spontaneous Abortion",
            "Stillbirth",
            "Live Birth",
            "Not Reported",
            "Induced Abortion",
            "Miscarriage",
            "Unknown",
            "Ectopic Pregnancy",
        },
    )
    def pregnancy_outcome(self, value):
        self._set_property("pregnancy_outcome", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Endoscopy", "Colonoscopy", "Not Reported", "Unknown"})
    def procedures_performed(self, value):
        self._set_property("procedures_performed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def progression_or_recurrence(self, value):
        self._set_property("progression_or_recurrence", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Anterior 2/3 of tongue, NOS",
            "Overlapping lesion of hypopharynx",
            "Anterior mediastinum",
            "Eyelid",
            "Endometrium",
            "Round ligament",
            "Myometrium",
            "Blood",
            "Ventral surface of tongue, NOS",
            "Branchial cleft",
            "Short bones of upper limb and associated joints",
            "Colon, NOS",
            "Skin of lip, NOS",
            "Conjunctiva",
            "Posterior mediastinum",
            "Urinary system, NOS",
            "Uvula",
            "Body of stomach",
            "Optic nerve",
            "Dorsal surface of tongue, NOS",
            "Intestinal tract, NOS",
            "Palate, NOS",
            "Kidney, NOS",
            "Thymus",
            "Liver",
            "Lingual tonsil",
            "Anal canal",
            "External lip, NOS",
            "Unknown primary site",
            "Ciliary body",
            "Overlapping lesion of colon",
            "Cheek mucosa",
            "Esophagus, NOS",
            "Ileum",
            "Upper limb, NOS",
            "Overlapping lesion of palate",
            "Vestibule of mouth",
            "Pancreatic duct",
            "Carotid body",
            "Specified parts of peritoneum",
            "Overlapping lesion of larynx",
            "Bladder, NOS",
            "Descended testis",
            "Spermatic cord",
            "Lymph nodes of multiple regions",
            "Bladder neck",
            "Gastrointestinal tract, NOS",
            "Hard palate",
            "Pelvis, NOS",
            "Ampulla of Vater",
            "Craniopharyngeal duct",
            "Autonomic nervous system, NOS",
            "Gallbladder",
            "Connective, subcutaneous and other soft tissues, NOS",
            "Nipple",
            "Posterior wall of hypopharynx",
            "Cervix uteri",
            "Prostate gland",
            "Unknown",
            "Retromolar area",
            "Brain stem",
            "Main bronchus",
            "Lateral wall of nasopharynx",
            "Other specified parts of pancreas",
            "Peripheral nerves and autonomic nervous system of thorax",
            "Parathyroid gland",
            "Cornea, NOS",
            "Parametrium",
            "Pineal gland",
            "Ill-defined sites within respiratory system",
            "Hypopharynx, NOS",
            "Anterior wall of nasopharynx",
            "Overlapping lesion of lip",
            "Peripheral nerves and autonomic nervous system of abdomen",
            "Overlapping lesion of biliary tract",
            "Overlapping lesion of male genital organs",
            "Hypopharyngeal aspect of aryepiglottic fold",
            "Posterior wall of bladder",
            "Skin, NOS",
            "Overlapping lesion of lip, oral cavity and pharynx",
            "Major salivary gland, NOS",
            "Floor of mouth, NOS",
            "Splenic flexure of colon",
            "Stomach, NOS",
            "Maxillary sinus",
            "Islets of Langerhans",
            "Superior wall of nasopharynx",
            "Parietal lobe",
            "Peripheral nerves and autonomic nervous system of upper limb and shoulder",
            "Overlapping lesion of major salivary glands",
            "Vulva, NOS",
            "Small intestine, NOS",
            "Endocrine gland, NOS",
            "Overlapping lesion of small intestine",
            "Orbit, NOS",
            "Vertebral column",
            "Ovary",
            "Sublingual gland",
            "Body of penis",
            "Abdominal esophagus",
            "Aortic body and other paraganglia",
            "Occipital lobe",
            "Gastric antrum",
            "External upper lip",
            "Exocervix",
            "Head, face or neck, NOS",
            "Vagina, NOS",
            "Epididymis",
            "Urethra",
            "Pylorus",
            "Overlapping lesion of cervix uteri",
            "Eye, NOS",
            "Fundus uteri",
            "Lesser curvature of stomach, NOS",
            "Overlapping lesion of connective, subcutaneous and other soft tissues",
            "Tail of pancreas",
            "Tonsil, NOS",
            "Peritoneum, NOS",
            "Not Reported",
            "Middle third of esophagus",
            "Lip, NOS",
            "Soft palate, NOS",
            "Fundus of stomach",
            "Oropharynx, NOS",
            "External ear",
            "Lateral wall of bladder",
            "Ethmoid sinus",
            "Overlapping lesion of bones, joints and articular cartilage of limbs",
            "Spinal cord",
            "Dome of bladder",
            "Accessory sinus, NOS",
            "Upper-inner quadrant of breast",
            "Thoracic esophagus",
            "Short bones of lower limb and associated joints",
            "Meninges, NOS",
            "Meckel diverticulum",
            "Clitoris",
            "Frontal sinus",
            "Nervous system, NOS",
            "Cervical esophagus",
            "Isthmus uteri",
            "Broad ligament",
            "Bone, NOS",
            "Pituitary gland",
            "Overlapping lesion of urinary organs",
            "Middle lobe, lung",
            "Overlapping lesion of brain and central nervous system",
            "Connective, subcutaneous and other soft tissues of pelvis",
            "Ureter",
            "Overlapping lesion of respiratory system and intrathoracic organs",
            "Endocervix",
            "Upper-outer quadrant of breast",
            "Undescended testis",
            "Bone of limb, NOS",
            "Mediastinum, NOS",
            "Larynx, NOS",
            "Base of tongue, NOS",
            "Waldeyer ring",
            "Overlapping lesion of peripheral nerves and autonomic nervous system",
            "Overlapping lesion of nasopharynx",
            "Head of pancreas",
            "Testis, NOS",
            "Retina",
            "Connective, subcutaneous and other soft tissues of head, face, and neck",
            "Mucosa of lip, NOS",
            "Overlapping lesions of oropharynx",
            "Long bones of lower limb and associated joints",
            "Adrenal gland, NOS",
            "Penis, NOS",
            "Cloacogenic zone",
            "Body of pancreas",
            "Anterior wall of bladder",
            "Greater curvature of stomach, NOS",
            "Overlapping lesion of bladder",
            "Other ill-defined sites",
            "Lower third of esophagus",
            "Anterior surface of epiglottis",
            "Nasopharynx, NOS",
            "Overlapping lesion of penis",
            "Prepuce",
            "Middle ear",
            "Skin of scalp and neck",
            "Overlapping lesion of female genital organs",
            "Sphenoid sinus",
            "Hematopoietic system, NOS",
            "Overlapping lesion of skin",
            "Connective, subcutaneous and other soft tissues of upper limb and shoulder",
            "Trigone of bladder",
            "Ascending colon",
            "Intrahepatic bile duct",
            "Frontal lobe",
            "Anus, NOS",
            "Skin of other and unspecified parts of face",
            "Overlapping lesion of pancreas",
            "Lung, NOS",
            "Long bones of upper limb, scapula and associated joints",
            "Overlapping lesion of ill-defined sites",
            "Overlapping lesion of breast",
            "Tonsillar fossa",
            "Labium minus",
            "Thyroid gland",
            "Cerebrum",
            "Connective, subcutaneous and other soft tissues of thorax",
            "Rectosigmoid junction",
            "Overlapping lesion of heart, mediastinum and pleura",
            "Lymph node, NOS",
            "Rectum, NOS",
            "Intra-abdominal lymph nodes",
            "Border of tongue",
            "Skin of trunk",
            "Corpus uteri",
            "Overlapping lesion of endocrine glands and related structures",
            "Connective, subcutaneous and other soft tissues of trunk, NOS",
            "Nasal cavity",
            "Overlapping lesion of stomach",
            "Paraurethral gland",
            "Medulla of adrenal gland",
            "Biliary tract, NOS",
            "Upper respiratory tract, NOS",
            "Other specified parts of male genital organs",
            "Fallopian tube",
            "Commissure of lip",
            "Lower-inner quadrant of breast",
            "Peripheral nerves and autonomic nervous system of pelvis",
            "Parotid gland",
            "Hepatic flexure of colon",
            "Connective, subcutaneous and other soft tissues of abdomen",
            "Overlapping lesion of floor of mouth",
            "Mandible",
            "Bones of skull and face and associated joints",
            "Urachus",
            "Upper gum",
            "Lateral floor of mouth",
            "Overlapping lesion of tonsil",
            "Rib, sternum, clavicle and associated joints",
            "Sigmoid colon",
            "Overlapping lesion of retroperitoneum and peritoneum",
            "Pelvic bones, sacrum, coccyx and associated joints",
            "Pharynx, NOS",
            "Posterior wall of nasopharynx",
            "Pleura, NOS",
            "Bone marrow",
            "Lymph nodes of axilla or arm",
            "Peripheral nerves and autonomic nervous system of trunk, NOS",
            "Female genital tract, NOS",
            "Male genital organs, NOS",
            "Labium majus",
            "Tongue, NOS",
            "Overlapping lesion of digestive system",
            "Spleen",
            "Jejunum",
            "Ventricle, NOS",
            "Mucosa of lower lip",
            "Skin of lower limb and hip",
            "Scrotum, NOS",
            "Cerebral meninges",
            "Glottis",
            "Spinal meninges",
            "Breast, NOS",
            "Lymph nodes of head, face and neck",
            "Pyriform sinus",
            "Overlapping lesion of bones, joints and articular cartilage",
            "Overlapping lesion of rectum, anus and anal canal",
            "Lacrimal gland",
            "Cardia, NOS",
            "Overlapping lesion of accessory sinuses",
            "Anterior floor of mouth",
            "Peripheral nerves and autonomic nervous system of head, face, and neck",
            "Heart",
            "Lower gum",
            "Overlapping lesion of lung",
            "Brain, NOS",
            "Upper lobe, lung",
            "Uterine adnexa",
            "Subglottis",
            "Upper third of esophagus",
            "Central portion of breast",
            "Laryngeal cartilage",
            "Gum, NOS",
            "Cerebellum, NOS",
            "External lower lip",
            "Connective, subcutaneous and other soft tissues of lower limb and hip",
            "Overlapping lesion of tongue",
            "Extrahepatic bile duct",
            "Trachea",
            "Acoustic nerve",
            "Olfactory nerve",
            "Cranial nerve, NOS",
            "Peripheral nerves and autonomic nervous system of lower limb and hip",
            "Skin of upper limb and shoulder",
            "Lower limb, NOS",
            "Tonsillar pillar",
            "Descending colon",
            "Submandibular gland",
            "Posterior wall of oropharynx",
            "Vallecula",
            "Overlapping lesion of brain",
            "Lymph nodes of inguinal region or leg",
            "Cecum",
            "Temporal lobe",
            "Abdomen, NOS",
            "Pancreas, NOS",
            "Renal pelvis",
            "Lateral wall of oropharynx",
            "Overlapping lesion of eye and adnexa",
            "Cortex of adrenal gland",
            "Cauda equina",
            "Duodenum",
            "Overlapping lesion of other and unspecified parts of mouth",
            "Mucosa of upper lip",
            "Ureteric orifice",
            "Overlapping lesion of vulva",
            "Lower-outer quadrant of breast",
            "Lower lobe, lung",
            "Overlapping lesion of corpus uteri",
            "Thorax, NOS",
            "Choroid",
            "Transverse colon",
            "Postcricoid region",
            "Pelvic lymph nodes",
            "Mouth, NOS",
            "Appendix",
            "Reticuloendothelial system, NOS",
            "Placenta",
            "Overlapping lesion of esophagus",
            "Retroperitoneum",
            "Uterus, NOS",
            "Other specified parts of female genital organs",
            "Glans penis",
            "Intrathoracic lymph nodes",
            "Axillary tail of breast",
            "Supraglottis",
        },
    )
    def progression_or_recurrence_anatomic_site(self, value):
        self._set_property("progression_or_recurrence_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Biochemical",
            "Local",
            "Locoregional",
            "Unknown",
            "Regional",
            "Distant",
            "Not Reported",
        },
    )
    def progression_or_recurrence_type(self, value):
        self._set_property("progression_or_recurrence_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def recist_targeted_regions_number(self, value):
        self._set_property("recist_targeted_regions_number", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def recist_targeted_regions_sum(self, value):
        self._set_property("recist_targeted_regions_sum", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Not Reported",
            "No Treatment",
            "Antacids",
            "H2 Blockers",
            "Medically Treated",
            "Unknown",
            "Not Applicable",
            "Surgically Treated",
            "Proton Pump Inhibitors",
        },
    )
    def reflux_treatment_type(self, value):
        self._set_property("reflux_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Rubinstein-Taybi Syndrome",
            "Alpha-1 Antitrypsin Deficiency",
            "Allergy, Nuts",
            "Common variable immune deficiency (CVID)",
            "Human Papillomavirus Infection",
            "Metabolic Syndrome",
            "Malaria",
            "Benign Prostatic Hyperplasia",
            "Adenosis (Atypical Adenomatous Hyperplasia)",
            "Alcoholic Liver Disease",
            "Gilbert's Syndrome",
            "Gorlin Syndrome",
            "Abnormal Glucose Level",
            "Herpes Zoster",
            "None",
            "Allergy, Processed Foods",
            "Cirrhosis",
            "Hepatitis C Infection",
            "Mycobacterium avium Complex",
            "Autoimmune Atrophic Chronic Gastritis",
            "Human Herpesvirus-6 (HHV-6)",
            "Hay Fever",
            "Li-Fraumeni Syndrome",
            "Chlamydia",
            "Chronic Kidney Disease",
            "Barrett's Esophagus",
            "Diabetes, NOS",
            "Tuberculosis",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Human Herpesvirus-8 (HHV-8)",
            "Squamous Metaplasia",
            "Inflammation",
            "Epithelial Hyperplasia",
            "Hashimoto's Thyroiditis",
            "Skin Rash",
            "Hepatitis B Infection",
            "Turcot Syndrome",
            "Gastric Polyp(s)",
            "Succinate Dehydrogenase-Deficient Renal Cell Carcinoma",
            "Tuberous Sclerosis",
            "Oral Contraceptives",
            "Hepatitis A Infection",
            "Epstein-Barr Virus",
            "Allergy, Wasp",
            "H. pylori Infection",
            "Helicobacter Pylori-Associated Gastritis",
            "BRCA Family History",
            "Thyroid Nodular Hyperplasia",
            "Vascular Disease",
            "Ataxia-telangiectasia",
            "Hereditary Breast Cancer",
            "Colon Polyps",
            "Allergy, Eggs",
            "Lymphocytic Thyroiditis",
            "Altered Mental Status",
            "Lymphamatoid Papulosis",
            "Colonization, Bacterial",
            "Escherichia coli",
            "Diabetes, Type II",
            "Tubulointerstitial Disease",
            "Low Grade Dysplasia",
            "Cytomegalovirus (CMV)",
            "Pancreatitis",
            "Allergy, Dairy or Lactose",
            "High-grade Prostatic Intraepithelial Neoplasia (PIN)",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Allergy, Ant",
            "Myasthenia Gravis",
            "Rheumatoid Arthritis",
            "Unknown",
            "Lynch Syndrome",
            "Motor / Movement Change",
            "Cowden Syndrome",
            "Hepatitis, NOS",
            "Shingles",
            "Allergy, Seafood",
            "Hypospadias",
            "Alcohol Consumption",
            "Parasitic Disease of Biliary Tract",
            "Treponema pallidum",
            "Allergy, Dog",
            "Pneumocystis Pneumonia",
            "Tumor-associated Lymphoid Proliferation",
            "Wagr Syndrome",
            "Sensory Changes",
            "Hepatic Encephalopathy",
            "Anemia",
            "Hereditary Hemorrhagic Telangiectasia",
            "Epithelial Dysplasia",
            "Allergy, Food, NOS",
            "Iron Overload",
            "Undescended Testis",
            "Hereditary Prostate Cancer",
            "Recurrent Pyogenic Cholangitis",
            "Neurocystericerosis",
            "Lymphocytic Meningitis",
            "BAP1 Tumor Predisposition Syndrome",
            "Behcet's Disease",
            "Gastritis",
            "Hereditary Papillary Renal Cell Carcinoma",
            "Colonization, Fungal",
            "Varicella Zoster Virus",
            "Nodular Prostatic Hyperplasia",
            "Dermatomyosis",
            "Allergy, Bee",
            "Cholelithiasis",
            "Eczema",
            "Hereditary Kidney Oncocytoma",
            "Allergy, Mold or Dust",
            "Hemihypertrophy",
            "Hereditary Renal Cell Carcinoma",
            "Chloroma",
            "Sialadenitis",
            "Myelodysplastic Syndrome",
            "Obesity",
            "Diverticulitis",
            "Chronic Systemic Steroid Use",
            "Cortisol Excess",
            "Von Hippel-Lindau Syndrome",
            "Steatosis",
            "Vision Changes",
            "Endometriosis",
            "EBV Lymphoproliferation",
            "Intestinal Metaplasia",
            "Diet",
            "Allergy, Meat",
            "Allergy, Cat",
            "Tobacco, Smoking",
            "Allergy, Fruit",
            "Endosalpingiosis",
            "Allergy, Animal, NOS",
            "High Grade Dysplasia",
            "Inflammation, Hyperkeratosis",
            "Tobacco, Smokeless",
            "Chronic Pancreatitis",
            "Sarcoidosis",
            "Denys-Drash Syndrome",
            "Sjogren's Syndrome",
            "Glomerular Disease",
            "Down Syndrome",
            "Diabetes, Type I",
            "Nonalcoholic Steatohepatitis",
            "Hereditary Leiomyomatosis and Renal Cell Carcinoma",
            "Rubella",
            "HIV",
            "Not Reported",
            "Mineralcorticoids Excess",
            "Seizure",
            "Bacteroides fragilis",
            "Birt-Hogg-Dube Syndrome",
            "Headache",
            "Staphylococcus aureus",
            "Hodgkin Lymphoma",
            "Adenomyosis",
            "Cancer",
            "Androgen Excess",
            "Inherited Genetic Syndrome, NOS",
            "Hematologic Disorder, NOS",
            "Tattoo",
            "Beckwith-Wiedemann",
            "Primary Sclerosing Cholangitis",
            "Chronic Hepatitis",
            "Tobacco, NOS",
            "Reflux Disease",
            "Syphilis",
            "Nonalcoholic Fatty Liver Disease",
            "Serous tubal intraepithelial carcinoma (STIC)",
            "Familial Adenomatous Polyposis",
            "Fibrosis",
            "Hemochromatosis",
            "Asthma",
            "Hereditary Ovarian Cancer",
            "Cyst(s)",
            "Estrogen Excess",
            "Cryptococcal Meningitis",
            "Fanconi Anemia",
        },
    )
    def risk_factor(self, value):
        self._set_property("risk_factor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property()
    def risk_factors(self, value):
        self._set_property("risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Clinical Assessment",
            "Both Clinical and Biochemical Assessments",
            "Biochemical Assessment",
            "Not Reported",
        },
    )
    def risk_factor_method_of_diagnosis(self, value):
        self._set_property("risk_factor_method_of_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def risk_factor_treatment(self, value):
        self._set_property("risk_factor_treatment", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"PSMA", "Axumin", "Acetate", "Sodium Fluoride", "Choline"})
    def scan_tracer_used(self, value):
        self._set_property("scan_tracer_used", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Adjuvant Therapy",
            "Post Adjuvant Therapy",
            "Prior to Diagnosis",
            "Other",
            "Last Contact",
            "Prior to Treatment",
            "Adolescence",
            "Postoperative",
            "Recurrence/Progression",
            "Initial Diagnosis",
            "Post Secondary Therapy",
            "Not Reported",
            "Adulthood",
            "Post Hormone Therapy",
            "Follow-up",
            "Preoperative",
            "Childhood",
        },
    )
    def timepoint_category(self, value):
        self._set_property("timepoint_category", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Yes", "No"})
    def undescended_testis_corrected(self, value):
        self._set_property("undescended_testis_corrected", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def undescended_testis_corrected_age(self, value):
        self._set_property("undescended_testis_corrected_age", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Right", "Left", "Bilateral", "Not Reported"})
    def undescended_testis_corrected_laterality(self, value):
        self._set_property("undescended_testis_corrected_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Orchiopexy",
            "Testis Removed",
            "Hormones",
            "Spontaneous Descent",
            "Not Reported",
        },
    )
    def undescended_testis_corrected_method(self, value):
        self._set_property("undescended_testis_corrected_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Yes", "No"})
    def undescended_testis_history(self, value):
        self._set_property("undescended_testis_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Right", "Left", "Bilateral", "Not Reported"})
    def undescended_testis_history_laterality(self, value):
        self._set_property("undescended_testis_history_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Hepatitis C Virus RNA",
            "HBV Core Antibody",
            "Not Reported",
            "HBV Surface Antibody",
            "Hepatitis B Surface Antigen",
            "Hepatitis C Antibody",
            "Unknown",
            "HBV DNA",
            "HCV Genotype",
            "HBV Genotype",
        },
    )
    def viral_hepatitis_serologies(self, value):
        self._set_property("viral_hepatitis_serologies", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def weight(self, value):
        self._set_property("weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def year_of_follow_up(self, value):
        self._set_property("year_of_follow_up", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FollowUp)
datetime_hooks.cls_inject_updated_datetime_hook(FollowUp)
