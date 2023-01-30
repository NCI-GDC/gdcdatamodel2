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
            "Gastric Stenosis",
            "Encephalomyelitis Infection",
            "Paronychia",
            "Pelvic Pain",
            "Hemolytic Uremic Syndrome",
            "Renal Colic",
            "Bronchial Stricture",
            "Pericardial Effusion",
            "Bronchopleural Fistula",
            "Endophthalmitis",
            "Skin Hyperpigmentation",
            "Burn",
            "Duodenal Infection",
            "Hallucinations",
            "Prostate Infection",
            "Small Intestine Infection",
            "Hiccups",
            "Death Neonatal",
            "Creatinine Increased",
            "Facial Nerve Disorder",
            "General Disorders and Administration Site Conditions - Other",
            "Trigeminal Nerve Disorder",
            "Wound Dehiscence",
            "Delayed Orgasm",
            "Vagus Nerve Disorder",
            "Laryngeal Fistula",
            "Arteritis Infective",
            "Anorectal Infection",
            "Intestinal Stoma Leak",
            "Joint Range of Motion Decreased",
            "Vaginal Pain",
            "Tracheal Fistula",
            "Bone Pain",
            "Superficial Thrombophlebitis",
            "Intracranial Hemorrhage",
            "Urinary Urgency",
            "Blood Prolactin Abnormal",
            "Colonic Perforation",
            "Carbon Monoxide Diffusing Capacity Decreased",
            "Fever",
            "CPK Increased",
            "Neutrophil Count Decreased",
            "Delirium",
            "Hepatic Hemorrhage",
            "Fibrinogen Decreased",
            "Pancreatic Enzymes Decreased",
            "Rash Maculo-Papular",
            "Small Intestinal Mucositis",
            "Postnasal Drip",
            "Abdominal Infection",
            "Fetal Growth Retardation",
            "Hematosalpinx",
            "Intraoperative Musculoskeletal Injury",
            "Catheter Related Infection",
            "Fallopian Tube Obstruction",
            "INR Increased",
            "Nail Loss",
            "Palmar-Plantar Erythrodysesthesia Syndrome",
            "Injury, Poisoning and Procedural Complications - Other",
            "Extrapyramidal Disorder",
            "Musculoskeletal Deformity",
            "Nail Infection",
            "Sinus Pain",
            "Ataxia",
            "Anemia",
            "Obesity",
            "Confusion",
            "Alkaline Phosphatase Increased",
            "Head Soft Tissue Necrosis",
            "Unequal Limb Length",
            "Hyperthyroidism",
            "Uterine Infection",
            "Left Ventricular Systolic Dysfunction",
            "Papulopustular Rash",
            "Chylothorax",
            "Pulmonary Hypertension",
            "Colonic Stenosis",
            "Mucosal Infection",
            "Pharyngitis",
            "Skin Atrophy",
            "Lymphocele",
            "Sudden Death NOS",
            "Duodenal Hemorrhage",
            "Glaucoma",
            "Anal Mucositis",
            "Gait Disturbance",
            "Flu Like Symptoms",
            "Vulval Infection",
            "Vaginal Discharge",
            "Gallbladder Pain",
            "Fetal Death",
            "Mucositis Oral",
            "Activated Partial Thromboplastin Time Prolonged",
            "Laryngeal Edema",
            "Hearing Impaired",
            "Acidosis",
            "Encephalopathy",
            "Vaginal Stricture",
            "Hypoglycemia",
            "Radiation Recall Reaction (Dermatologic)",
            "Urinary Tract Infection",
            "Ejaculation Disorder",
            "Esophageal Obstruction",
            "Thromboembolic Event",
            "Skin Ulceration",
            "Hepatitis Viral",
            "Soft Tissue Infection",
            "Superficial Soft Tissue Fibrosis",
            "Lip Pain",
            "Myelodysplastic Syndrome",
            "Blood and Lymphatic System Disorders - Other",
            "Enterocolitis Infectious",
            "Blood Antidiuretic Hormone Abnormal",
            "Menorrhagia",
            "Malabsorption",
            "Oral Dysesthesia",
            "Alanine Aminotransferase Increased",
            "Hepatic Pain",
            "Adult Respiratory Distress Syndrome",
            "Vasovagal Reaction",
            "Hypertriglyceridemia",
            "Soft Tissue Necrosis Upper Limb",
            "Perforation Bile Duct",
            "Small Intestinal Stenosis",
            "Mania",
            "Pulmonary Valve Disease",
            "Arthralgia",
            "Leukemia Secondary to Oncology Chemotherapy",
            "Cataract",
            "Intraoperative Venous Injury",
            "Hyponatremia",
            "Vestibular Disorder",
            "Colonic Hemorrhage",
            "Ovarian Rupture",
            "Injury to Jugular Vein",
            "Bladder Perforation",
            "Body Odor",
            "Cheilitis",
            "Obstruction Gastric",
            "Conjunctivitis",
            "Tracheitis",
            "Paresthesia",
            "Esophageal Fistula",
            "Breast Infection",
            "Anal Ulcer",
            "Cough",
            "Small Intestinal Perforation",
            "Wrist Fracture",
            "Ascites",
            "Intraoperative Ocular Injury",
            "Rectal Necrosis",
            "Malaise",
            "Penile Pain",
            "Cerebrospinal Fluid Leakage",
            "Vasculitis",
            "Muscle Weakness Left-Sided",
            "Capillary Leak Syndrome",
            "Lactation Disorder",
            "Vascular Disorders - Other",
            "Pain",
            "Laryngeal Obstruction",
            "Lower Gastrointestinal Hemorrhage",
            "Diarrhea",
            "Irritability",
            "Gastric Hemorrhage",
            "Azoospermia",
            "Suicide Attempt",
            "Seizure",
            "Urinary Retention",
            "Postoperative Hemorrhage",
            "Myocardial Infarction",
            "Salivary Gland Fistula",
            "Periorbital Edema",
            "Cecal Infection",
            "Hepatic Failure",
            "Rectal Stenosis",
            "Uterine Obstruction",
            "Dermatitis Radiation",
            "Growth Accelerated",
            "Duodenal Perforation",
            "Portal Hypertension",
            "Uveitis",
            "Bladder Infection",
            "Peripheral Ischemia",
            "Spinal Fracture",
            "Pelvic Floor Muscle Weakness",
            "Ventricular Fibrillation",
            "Device Related Infection",
            "Dysarthria",
            "Hypoalbuminemia",
            "Pain in Extremity",
            "Movements Involuntary",
            "Intraoperative Splenic Injury",
            "Edema Face",
            "Cardiac Troponin I Increased",
            "Prostatic Pain",
            "Hypoxia",
            "Concentration Impairment",
            "Rectal Mucositis",
            "Scoliosis",
            "Hypohidrosis",
            "Atrial Flutter",
            "Vomiting",
            "Hematoma",
            "Laryngeal Inflammation",
            "Arachnoiditis",
            "Peripheral Motor Neuropathy",
            "Retinal Tear",
            "Muscle Weakness Upper Limb",
            "Disseminated Intravascular Coagulation",
            "Colitis",
            "Conjunctivitis Infective",
            "Joint Range of Motion Decreased Lumbar Spine",
            "Sinus Bradycardia",
            "Epistaxis",
            "IVth Nerve Disorder",
            "Abdominal Soft Tissue Necrosis",
            "Night Blindness",
            "Hemoglobin Increased",
            "Jejunal Ulcer",
            "Ileus",
            "Vaginal Obstruction",
            "Gallbladder Necrosis",
            "Suicidal Ideation",
            "Osteonecrosis of Jaw",
            "Sick Sinus Syndrome",
            "Injection Site Reaction",
            "Urostomy Site Bleeding",
            "Pancreas Infection",
            "Laryngeal Stenosis",
            "Tracheal Stenosis",
            "Neck Pain",
            "Premature Menopause",
            "Laryngospasm",
            "Upper Respiratory Infection",
            "Virilization",
            "Postoperative Thoracic Procedure Complication",
            "Proteinuria",
            "Fibrosis Deep Connective Tissue",
            "Facial Pain",
            "Right Ventricular Dysfunction",
            "Pharyngolaryngeal Pain",
            "Buttock Pain",
            "Appendicitis",
            "Blood Gonadotrophin Abnormal",
            "Personality Change",
            "Purpura",
            "Hemorrhoids",
            "Lymphocyte Count Decreased",
            "Anal Pain",
            "Hepatic Necrosis",
            "Photophobia",
            "Intraoperative Urinary Injury",
            "Dysphasia",
            "Anxiety",
            "Muscle Weakness Right-Sided",
            "Tracheostomy Site Bleeding",
            "Eye Disorders - Other",
            "Cardiac Arrest",
            "Pleural Infection",
            "Generalized Muscle Weakness",
            "Aortic Injury",
            "Pericarditis",
            "Salivary Duct Inflammation",
            "Sepsis",
            "Scalp Pain",
            "Corneal Infection",
            "Pulmonary Edema",
            "Delusions",
            "Soft Tissue Necrosis Lower Limb",
            "Duodenal Stenosis",
            "Skin Induration",
            "Pelvic Soft Tissue Necrosis",
            "Irregular Menstruation",
            "Lip Infection",
            "Urinary Fistula",
            "Vertigo",
            "Social Circumstances - Other",
            "Vaginal Inflammation",
            "Dyspareunia",
            "Esophageal Pain",
            "Vaginismus",
            "Aspartate Aminotransferase Increased",
            "Amnesia",
            "Gynecomastia",
            "Eye Infection",
            "Central Nervous System Necrosis",
            "Urostomy Leak",
            "Bronchial Fistula",
            "Exostosis",
            "Esophageal Perforation",
            "Fall",
            "Gastric Perforation",
            "Pharyngeal Necrosis",
            "Pharyngeal Anastomotic Leak",
            "Nail Ridging",
            "Colonic Obstruction",
            "Vas Deferens Anastomotic Leak",
            "Wound Infection",
            "Thrombotic Thrombocytopenic Purpura",
            "Weight Loss",
            "Myositis",
            "Akathisia",
            "Duodenal Ulcer",
            "Cholecystitis",
            "Bile Duct Stenosis",
            "Anal Fistula",
            "Platelet Count Decreased",
            "Urostomy Obstruction",
            "Aortic Valve Disease",
            "Rash Acneiform",
            "Watering Eyes",
            "Genital Edema",
            "Facial Muscle Weakness",
            "Cervicitis Infection",
            "Colonic Fistula",
            "Toxic Epidermal Necrolysis",
            "Nystagmus",
            "Rectal Pain",
            "Joint Effusion",
            "Urostomy Stenosis",
            "Gastrointestinal Pain",
            "Ankle Fracture",
            "Bullous Dermatitis",
            "Chest Pain - Cardiac",
            "Electrocardiogram QT Corrected Interval Prolonged",
            "Esophageal Infection",
            "Urethral Anastomotic Leak",
            "Dry Mouth",
            "Nausea",
            "Ileal Fistula",
            "Urinary Frequency",
            "Intraoperative Gastrointestinal Injury",
            "Insomnia",
            "External Ear Pain",
            "Gastritis",
            "Lung Infection",
            "Pharyngeal Hemorrhage",
            "Wheezing",
            "Respiratory Failure",
            "Lymphedema",
            "Nipple Deformity",
            "Uterine Anastomotic Leak",
            "Hyperkalemia",
            "Ileal Perforation",
            "Retinal Detachment",
            "Bladder Spasm",
            "Tumor Pain",
            "Lethargy",
            "Endocrine Disorders - Other",
            "Duodenal Obstruction",
            "Injury to Inferior Vena Cava",
            "Joint Range of Motion Decreased Cervical Spine",
            "Muscle Weakness Trunk",
            "Pulmonary Fibrosis",
            "Musculoskeletal and Connective Tissue Disorders - Other",
            "Esophageal Necrosis",
            "Forced Expiratory Volume Decreased",
            "Typhlitis",
            "Portal Vein Thrombosis",
            "Pharyngeal Stenosis",
            "Anal Hemorrhage",
            "Libido Decreased",
            "Alcohol Intolerance",
            "Floaters",
            "Tracheal Hemorrhage",
            "Hydrocephalus",
            "Alkalosis",
            "Somnolence",
            "Ventricular Tachycardia",
            "Urinary Tract Obstruction",
            "Laryngitis",
            "Leukoencephalopathy",
            "Recurrent Laryngeal Nerve Palsy",
            "Memory Impairment",
            "Vaginal Fistula",
            "Allergic Rhinitis",
            "Hot Flashes",
            "Agitation",
            "Nail Discoloration",
            "Esophageal Ulcer",
            "Urinary Tract Pain",
            "Prostatic Hemorrhage",
            "Ovulation Pain",
            "Dyspepsia",
            "Heart Failure",
            "Pancreatic Fistula",
            "Tooth Infection",
            "Congenital, Familial and Genetic Disorders - Other",
            "Injury to Superior Vena Cava",
            "Renal Calculi",
            "Scleral Disorder",
            "Proctitis",
            "Bladder Anastomotic Leak",
            "Hyperhidrosis",
            "Esophageal Varices Hemorrhage",
            "Testicular Disorder",
            "Kyphosis",
            "Bronchial Obstruction",
            "Urethral Infection",
            "Tracheal Obstruction",
            "Dysmenorrhea",
            "Gastric Fistula",
            "Pleuritic Pain",
            "Infective Myositis",
            "Bloating",
            "Flank Pain",
            "Tremor",
            "Urinary Incontinence",
            "Intraoperative Hemorrhage",
            "Atrioventricular Block First Degree",
            "Intraoperative Arterial Injury",
            "Gastrointestinal Disorders - Other",
            "Intraoperative Skin Injury",
            "Serum Amylase Increased",
            "Neck Edema",
            "Pneumonitis",
            "Rectal Ulcer",
            "Gastrointestinal Anastomotic Leak",
            "Perineal Pain",
            "Weight Gain",
            "Hypotension",
            "Uterine Perforation",
            "Pancreatitis",
            "Conduction Disorder",
            "Pancreatic Hemorrhage",
            "Injury to Carotid Artery",
            "Olfactory Nerve Disorder",
            "Spermatic Cord Hemorrhage",
            "Depression",
            "Lymph Gland Infection",
            "Small Intestine Ulcer",
            "Supraventricular Tachycardia",
            "Infusion Related Reaction",
            "Ureteric Anastomotic Leak",
            "Allergic Reaction",
            "Chronic Kidney Disease",
            "Jejunal Hemorrhage",
            "Pleural Hemorrhage",
            "Vaginal Dryness",
            "Otitis Externa",
            "Periodontal Disease",
            "Myelitis",
            "Intra-Abdominal Hemorrhage",
            "Optic Nerve Disorder",
            "Adrenal Insufficiency",
            "Apnea",
            "Retinopathy",
            "Atrial Fibrillation",
            "Psychiatric Disorders - Other",
            "Renal Hemorrhage",
            "Jejunal Obstruction",
            "Restlessness",
            "Death NOS",
            "Tumor Lysis Syndrome",
            "Gastroparesis",
            "Glucose Intolerance",
            "Prolapse of Intestinal Stoma",
            "Gallbladder Infection",
            "Gallbladder Obstruction",
            "Lymph Node Pain",
            "Hypersomnia",
            "Prostatic Obstruction",
            "Cholesterol High",
            "Skin and Subcutaneous Tissue Disorders - Other",
            "Cytokine Release Syndrome",
            "Meningismus",
            "Non-Cardiac Chest Pain",
            "Biliary Tract Infection",
            "Depressed Level of Consciousness",
            "Hyperuricemia",
            "Skin Hypopigmentation",
            "Esophageal Stenosis",
            "Middle Ear Inflammation",
            "Seroma",
            "Laryngeal Mucositis",
            "Fallopian Tube Anastomotic Leak",
            "Abdominal Pain",
            "Prolapse of Urostomy",
            "Hypothermia",
            "Multi-Organ Failure",
            "Vascular Access Complication",
            "Acoustic Nerve Disorder NOS",
            "Rectal Anastomotic Leak",
            "Atrioventricular Block Complete",
            "Nasal Congestion",
            "Neuralgia",
            "Eyelid Function Disorder",
            "Hypoparathyroidism",
            "Pelvic Infection",
            "Gastrointestinal Stoma Necrosis",
            "Radiculitis",
            "Flashing Lights",
            "Gingival Pain",
            "Cardiac Troponin T Increased",
            "Muscle Weakness Lower Limb",
            "Myalgia",
            "Bronchial Infection",
            "Fallopian Tube Stenosis",
            "Jejunal Perforation",
            "Telangiectasia",
            "Mediastinal Hemorrhage",
            "Anal Stenosis",
            "Renal and Urinary Disorders - Other",
            "Dysesthesia",
            "Intraoperative Head and Neck Injury",
            "Hypertrichosis",
            "Biliary Anastomotic Leak",
            "Pulmonary Fistula",
            "Breast Atrophy",
            "Wound Complication",
            "Infusion Site Extravasation",
            "Serum Sickness",
            "Bone Marrow Hypocellular",
            "Lymph Leakage",
            "Respiratory, Thoracic and Mediastinal Disorders - Other",
            "Otitis Media",
            "Psychosis",
            "Skin Infection",
            "Premature Delivery",
            "Gastric Anastomotic Leak",
            "Growth Suppression",
            "Testicular Pain",
            "Intestinal Stoma Obstruction",
            "Ileal Ulcer",
            "Vital Capacity Abnormal",
            "Vaginal Anastomotic Leak",
            "Acute Kidney Injury",
            "Euphoria",
            "Cardiac Disorders - Other",
            "Feminization Acquired",
            "Pericardial Tamponade",
            "Tooth Discoloration",
            "Laryngeal Hemorrhage",
            "Arterial Injury",
            "Mediastinal Infection",
            "Fracture",
            "Dry Skin",
            "Phlebitis Infective",
            "Kidney Infection",
            "Glossopharyngeal Nerve Disorder",
            "Hoarseness",
            "Joint Infection",
            "Pyramidal Tract Syndrome",
            "Oral Hemorrhage",
            "Splenic Infection",
            "Esophageal Hemorrhage",
            "Pancreatic Necrosis",
            "Cystitis Noninfective",
            "Myocarditis",
            "Paroxysmal Atrial Tachycardia",
            "Urticaria",
            "Hypoglossal Nerve Disorder",
            "Edema Limbs",
            "Edema Trunk",
            "Sneezing",
            "Blurred Vision",
            "Hypermagnesemia",
            "Gastric Necrosis",
            "Stomach Pain",
            "Back Pain",
            "Constrictive Pericarditis",
            "Hip Fracture",
            "Intraoperative Ear Injury",
            "Voice Alteration",
            "Blood Bilirubin Increased",
            "Growth Hormone Abnormal",
            "Pneumothorax",
            "Ear Pain",
            "Fecal Incontinence",
            "Breast Pain",
            "Hypomagnesemia",
            "Fallopian Tube Perforation",
            "Headache",
            "Fat Atrophy",
            "Bronchopulmonary Hemorrhage",
            "Cognitive Disturbance",
            "Hypertension",
            "Endocarditis Infective",
            "Penile Infection",
            "Urine Discoloration",
            "Tooth Development Disorder",
            "CD4 Lymphocytes Decreased",
            "Gallbladder Fistula",
            "Erectile Dysfunction",
            "Accessory Nerve Disorder",
            "Chills",
            "Ovarian Infection",
            "Scrotal Pain",
            "Stevens-Johnson Syndrome",
            "Peritoneal Infection",
            "Pruritus",
            "Ovarian Hemorrhage",
            "Rhinitis Infective",
            "Laryngopharyngeal Dysesthesia",
            "Rectal Fistula",
            "Investigations - Other",
            "Intraoperative Endocrine Injury",
            "Intraoperative Breast Injury",
            "Hypophosphatemia",
            "Edema Cerebral",
            "Jejunal Stenosis",
            "Fatigue",
            "Acute Coronary Syndrome",
            "Kidney Anastomotic Leak",
            "Vaginal Perforation",
            "Osteoporosis",
            "Presyncope",
            "Sinusitis",
            "Superior Vena Cava Syndrome",
            "Hematuria",
            "Abdominal Distension",
            "Hypercalcemia",
            "Dental Caries",
            "Intraoperative Renal Injury",
            "Nervous System Disorders - Other",
            "Scrotal Infection",
            "Pregnancy, Puerperium and Perinatal Conditions - Other",
            "Pharyngeal Fistula",
            "Alopecia",
            "Peripheral Nerve Infection",
            "GGT Increased",
            "Esophagitis",
            "Febrile Neutropenia",
            "Transient Ischemic Attacks",
            "Anaphylaxis",
            "Sleep Apnea",
            "Anorexia",
            "Rectal Perforation",
            "Phantom Pain",
            "Hypothyroidism",
            "Meningitis",
            "Visceral Arterial Ischemia",
            "Menopause",
            "Cranial Nerve Infection",
            "Libido Increased",
            "Oligospermia",
            "Gastroesophageal Reflux Disease",
            "Intraoperative Hepatobiliary Injury",
            "Spleen Disorder",
            "Dyspnea",
            "Hypokalemia",
            "Dysgeusia",
            "Pancreatic Anastomotic Leak",
            "Hyperglycemia",
            "Palpitations",
            "Neoplasms Benign, Malignant and Unspecified (Incl Cysts and Polyps) - Other",
            "Spermatic Cord Obstruction",
            "Retroperitoneal Hemorrhage",
            "Venous Injury",
            "Rectal Obstruction",
            "Stenosis of Gastrointestinal Stoma",
            "Intraoperative Cardiac Injury",
            "Immune System Disorders - Other",
            "Lipase Increased",
            "Hirsutism",
            "Jejunal Fistula",
            "Sore Throat",
            "Mobitz (Type) II Atrioventricular Block",
            "Vitreous Hemorrhage",
            "Leukocytosis",
            "Stomal Ulcer",
            "Autoimmune Disorder",
            "Lipohypertrophy",
            "Tricuspid Valve Disease",
            "Vaginal Hemorrhage",
            "White Blood Cell Decreased",
            "Asystole",
            "Encephalitis Infection",
            "Mitral Valve Disease",
            "Treatment Related Secondary Malignancy",
            "Intraoperative Neurological Injury",
            "Eye Pain",
            "Hemolysis",
            "Gum Infection",
            "Ileal Hemorrhage",
            "Localized Edema",
            "Gastric Ulcer",
            "Phlebitis",
            "Appendicitis Perforated",
            "Hepatic Infection",
            "Biliary Fistula",
            "Dehydration",
            "Pleural Effusion",
            "Infections and Infestations - Other",
            "Testicular Hemorrhage",
            "Intestinal Stoma Site Bleeding",
            "Oral Cavity Fistula",
            "Reproductive System and Breast Disorders - Other",
            "Flatulence",
            "Ileal Obstruction",
            "Female Genital Tract Fistula",
            "Hemoglobinuria",
            "Flushing",
            "Unintended Pregnancy",
            "Corneal Ulcer",
            "Spermatic Cord Anastomotic Leak",
            "Abducens Nerve Disorder",
            "Ileal Stenosis",
            "Erythroderma",
            "Intraoperative Respiratory Injury",
            "Peritoneal Necrosis",
            "Rectal Hemorrhage",
            "Bruising",
            "Brachial Plexopathy",
            "Oculomotor Nerve Disorder",
            "Stoma Site Infection",
            "Constipation",
            "Esophageal Anastomotic Leak",
            "Ejection Fraction Decreased",
            "Erythema Multiforme",
            "Lymphocyte Count Increased",
            "Aphonia",
            "External Ear Inflammation",
            "Productive Cough",
            "Dry Eye",
            "Stroke",
            "Surgical and Medical Procedures - Other",
            "Hemorrhoidal Hemorrhage",
            "Ischemia Cerebrovascular",
            "Avascular Necrosis",
            "Bone Infection",
            "Cushingoid",
            "Cecal Hemorrhage",
            "Upper Gastrointestinal Hemorrhage",
            "Sinus Disorder",
            "Gastrointestinal Fistula",
            "Delayed Puberty",
            "Enterovesical Fistula",
            "Atelectasis",
            "Colonic Ulcer",
            "Precocious Puberty",
            "Small Intestinal Obstruction",
            "Photosensitivity",
            "Pain of Skin",
            "Gallbladder Perforation",
            "Syncope",
            "Haptoglobin Decreased",
            "Hypocalcemia",
            "Arthritis",
            "Hyperparathyroidism",
            "Ear and Labyrinth Disorders - Other",
            "Toothache",
            "Blood Corticotrophin Decreased",
            "Dysphagia",
            "Uterine Hemorrhage",
            "Uterine Pain",
            "Wolff-Parkinson-White Syndrome",
            "Retinoic Acid Syndrome",
            "Aspiration",
            "Bronchospasm",
            "Papilledema",
            "Lordosis",
            "Tinnitus",
            "Vaginal Infection",
            "Iron Overload",
            "Oral Pain",
            "Rash Pustular",
            "Uterine Fistula",
            "Keratitis",
            "Salivary Gland Infection",
            "Mobitz Type I",
            "Spasticity",
            "Stridor",
            "Urine Output Decreased",
            "Dizziness",
            "Ventricular Arrhythmia",
            "Trismus",
            "Restrictive Cardiomyopathy",
            "Anorgasmia",
            "Chest Wall Pain",
            "Hypernatremia",
            "Neck Soft Tissue Necrosis",
            "Tracheal Mucositis",
            "Enterocolitis",
            "Metabolism and Nutrition Disorders - Other",
            "Hepatobiliary Disorders - Other",
            "Large Intestinal Anastomotic Leak",
            "Anal Necrosis",
            "Sinus Tachycardia",
            "Reversible Posterior Leukoencephalopathy Syndrome",
            "Duodenal Fistula",
            "Intraoperative Reproductive Tract Injury",
            "Periorbital Infection",
            "Peripheral Sensory Neuropathy",
            "Extraocular Muscle Paresis",
            "Retinal Vascular Disorder",
            "Pharyngeal Mucositis",
            "Small Intestinal Anastomotic Leak",
            "Pancreatic Duct Stenosis",
        },
    )
    def adverse_event(self, value):
        self._set_property("adverse_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Grade 1", "Grade 4", "Grade 5", "Grade 2", "Grade 3"}
    )
    def adverse_event_grade(self, value):
        self._set_property("adverse_event_grade", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Candidiasis",
            "Pneumocystis Pneumonia",
            "Wasting Syndrome",
            "Toxoplasmosis",
            "Cytomegalovirus",
            "Histoplasmosis",
            "Encephalopathy",
            "Progressive Multifocal Leukoencephalopathy",
            "Mycobacterium tuberculosis",
            "Pneumonia, NOS",
            "Isosporiasis",
            "Coccidioidomycosis",
            "Cryptococcosis",
            "Nocardiosis",
            "Mycobacterium, NOS",
            "Herpes Simplex Virus",
            "Cryptosporidiosis, Chronic Intestinal",
            "Salmonella Septicemia",
            "Mycobacterium avium Complex",
        },
    )
    def aids_risk_factors(self, value):
        self._set_property("aids_risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
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
            "Unknown",
            "None",
            "Intravenous Drug User",
            "Hemophiliac",
            "Transfusion Recipient",
            "Not Reported",
            "Homosexual Contact",
            "Heterosexual Contact",
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
            "Metabolic Syndrome",
            "Diabetes, Type II",
            "Gorlin Syndrome",
            "Chronic Fatigue Syndrome",
            "Peutz-Jeghers Disease",
            "Dyslipidemia",
            "Cholelithiasis",
            "Blood Clots",
            "Hemihypertrophy",
            "Pregnancy in Patient or Partner",
            "Other Cancer Within 5 Years",
            "Thyroid Disease, Non-Cancer",
            "Down Syndrome",
            "HIV / AIDS",
            "Peptic Ulcer (Ulcer)",
            "GERD",
            "Sarcoidosis",
            "Hypercalcemia",
            "Epstein-Barr Virus",
            "Pneumocystis Pneumonia",
            "Basal Cell Carcinoma",
            "Insulin Controlled Diabetes",
            "Cryptogenic Organizing Pneumonia",
            "Osteoarthritis",
            "Acute Renal Failure",
            "Hyperlipidemia",
            "Rheumatoid Arthritis",
            "Low Grade Liver Dysplastic Nodule",
            "Pancreatitis",
            "HUS/TTP",
            "Diverticulitis",
            "Peripheral Vascular Disease",
            "High Grade Liver Dysplastic Nodule",
            "Depression",
            "Ulcerative Colitis",
            "Denys-Drash Syndrome",
            "Lymphamatoid Papulosis",
            "Ataxia-telangiectasia",
            "Calcium Channel Blockers",
            "Glycogen Storage Disease",
            "Intraductal Papillary Mucinous Neoplasm",
            "Beckwith-Wiedemann",
            "Bone Fracture(s)",
            "Chlamydia",
            "Alpha-1 Antitrypsin",
            "Hypothyroidism",
            "Hepatitis, Chronic",
            "Gastroesophageal Reflux Disease",
            "Diabetes",
            "Atrial Fibrillation",
            "Fibromyalgia",
            "Human Papillomavirus Infection",
            "Hyperglycemia",
            "Not Reported",
            "Syphilis",
            "Abnormal Glucose Level",
            "Eczema",
            "Wagr Syndrome",
            "Anxiety",
            "Celiac Disease",
            "Hepatitis A Infection",
            "CNS Infection",
            "Herpes Zoster",
            "Anemia",
            "Obesity",
            "H. pylori Infection",
            "Other",
            "Arrhythmia",
            "Staph Osteomyelitis",
            "Hypospadias",
            "Biliary Disorder",
            "Adenomatous Polyposis Coli",
            "Cancer",
            "Barrett's Esophagus",
            "Allergies",
            "Hereditary Non-polyposis Colon Cancer",
            "Peripheral Neuropathy",
            "Glaucoma",
            "Liver Cirrhosis (Liver Disease)",
            "Sleep apnea",
            "Kidney Disease",
            "MAI",
            "Nonalcoholic Steatohepatitis",
            "Psoriasis",
            "Neuroendocrine Tumor",
            "Tuberculosis",
            "COPD",
            "Fibrosis",
            "Liver Toxicity (Non-Infectious)",
            "Hypercholesterolemia",
            "Urinary Tract Infection",
            "Joint Replacement",
            "Hemorrhagic Cystitis",
            "Adenocarcinoma",
            "Interstitial Pneumontis or ARDS",
            "Staphylococcus aureus",
            "Deep Vein Thrombosis / Thromboembolism",
            "Hepatitis B Infection",
            "Chronic Renal Failure",
            "Stroke",
            "Smoking",
            "Avascular Necrosis",
            "Diabetic Neuropathy",
            "Cataracts",
            "Cirrhosis, Unknown Etiology",
            "Sjogren's Syndrome",
            "Tyrosinemia",
            "Diet Controlled Diabetes",
            "Mycobacterium avium Complex",
            "Transient Ischemic Attack",
            "Unknown",
            "Renal Insufficiency",
            "Treponema pallidum",
            "Cryptococcal Meningitis",
            "Ischemic Heart Disease",
            "Connective Tissue Disorder",
            "Crohn's Disease",
            "Pain (Various)",
            "Hodgkin Lymphoma",
            "Cytomegalovirus (CMV)",
            "Fanconi Anemia",
            "Rubinstein-Taybi Syndrome",
            "Epilepsy",
            "Other Nonmalignant Systemic Disease",
            "Common Variable Immunodeficiency",
            "Shingles",
            "Arthritis",
            "Turcot Syndrome",
            "Gastritis",
            "Chronic Pancreatitis",
            "Colon Polyps",
            "DVT/PE",
            "Organ transplant (site)",
            "Inflammatory Bowel Disease",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Lymphocytic Meningitis",
            "Asthma",
            "Gout",
            "Iron Overload",
            "Malaria",
            "Pulmonary Fibrosis",
            "Coronary Artery Disease",
            "Other Pulmonary Complications",
            "Methicillin-Resistant Staphylococcus aureus (MRSA)",
            "Hepatitis",
            "Pulmonary Hemorrhage",
            "Hepatitis C Infection",
            "Steatosis",
            "Bronchitis",
            "Dermatomyosis",
            "Familial Adenomatous Polyposis",
            "Hashimoto's Thyroiditis",
            "EBV Lymphoproliferation",
            "Herpes",
            "Lupus",
            "Primary Sclerosing Cholangitis",
            "ITP",
            "Renal Failure (Requiring Dialysis)",
            "Seizure",
            "Varicella Zoster Virus",
            "Rheumatologic Disease",
            "Behcet's Disease",
            "Myocardial Infarction",
            "Chloroma",
            "Clonal Hematopoiesis",
            "Heart Disease",
            "Lynch Syndrome",
            "Myasthenia Gravis",
            "Li-Fraumeni Syndrome",
            "Adrenocortical Insufficiency",
            "Osteoporosis or Osteopenia",
            "Bacteroides fragilis",
            "Chronic Systemic Steroid Use",
            "Gonadal Dysfunction",
            "Headache",
            "Cerebrovascular Disease",
            "Hypertension",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Congestive Heart Failure (CHF)",
            "Renal Dialysis",
        },
    )
    def comorbidity(self, value):
        self._set_property("comorbidity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Radiology", "Histology", "Not Reported", "Pathology"}
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
            "Unknown",
            "Alpha-Glucosidase Inhibitor",
            "Thiazolidinedione",
            "Linagliptin",
            "Oral Hypoglycemic",
            "Injected Insulin",
            "Insulin",
            "Not Reported",
            "Sulfonylurea",
            "Biguanide",
            "Diet",
            "Other",
        },
    )
    def diabetes_treatment_type(self, value):
        self._set_property("diabetes_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "CR-Complete Response",
            "VGPR-Very Good Partial Response",
            "WT-With Tumor",
            "PR-Partial Response",
            "Not Reported",
            "PA-Palliative Therapy",
            "NR-No Response",
            "SD-Stable Disease",
            "RP-Response",
            "RPD-Radiographic Progressive Disease",
            "AJ-Adjuvant Therapy",
            "PD-Progressive Disease",
            "PDM-Persistent Distant Metastasis",
            "Non-CR/Non-PD-Non-CR/Non-PD",
            "RD-Responsive Disease",
            "sCR-Stringent Complete Response",
            "Unknown",
            "SPD-Surgical Progression",
            "TF-Tumor Free",
            "BED-Biochemical Evidence of Disease",
            "TE-Too Early",
            "NPB-No Palliative Benefit",
            "PB-Palliative Benefit",
            "IMR-Immunoresponse",
            "IPD-Immunoprogression",
            "PPD-Pseudoprogression",
            "CPD-Clinical Progression",
            "MX-Mixed Response",
            "MR-Minimal/Marginal response",
            "PLD-Persistent Locoregional Disease",
            "DU-Disease Unchanged",
            "CRU-Complete Response Unconfirmed",
            "PSR-Pseudoresponse",
        },
    )
    def disease_response(self, value):
        self._set_property("disease_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def dlco_ref_predictive_percent(self, value):
        self._set_property("dlco_ref_predictive_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "4", "2", "Not Reported", "3", "0", "5", "1"}
    )
    def ecog_performance_status(self, value):
        self._set_property("ecog_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Histologic Confirmation", "Convincing Image Source"}
    )
    def evidence_of_progression_type(self, value):
        self._set_property("evidence_of_progression_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Histologic Confirmation",
            "Convincing Image Source",
            "Biopsy with Histologic Confirmation",
            "Physical Examination",
            "Positive Biomarker(s)",
        },
    )
    def evidence_of_recurrence_type(self, value):
        self._set_property("evidence_of_recurrence_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Amber",
            "Red & Violet",
            "Other",
            "Blue",
            "Not Reported",
            "Brown",
            "Gray",
            "Green",
            "Hazel",
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
            "Censored",
            "Death without Remission",
            "Death",
            "Induction Failure",
            "Relapse",
            "Event",
            "Second Malignant Neoplasm",
            "Not Reported",
            "Progression",
            "Induction Death",
            "Other",
        },
    )
    def first_event(self, value):
        self._set_property("first_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def haart_treatment_indicator(self, value):
        self._set_property("haart_treatment_indicator", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def height(self, value):
        self._set_property("height", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def hepatitis_sustained_virological_response(self, value):
        self._set_property("hepatitis_sustained_virological_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "No", "Yes"})
    def history_of_tumor(self, value):
        self._set_property("history_of_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Colorectal Cancer",
            "Phenochromocytoma or Paraganglioma",
            "Lower Grade Glioma",
        },
    )
    def history_of_tumor_type(self, value):
        self._set_property("history_of_tumor_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def hiv_viral_load(self, value):
        self._set_property("hiv_viral_load", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Progestin", "Progestin and Estrogen", "Not Reported"}
    )
    def hormonal_contraceptive_type(self, value):
        self._set_property("hormonal_contraceptive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={"Unknown", "Not Reported", "Former User", "Current User", "Never Used"},
    )
    def hormonal_contraceptive_use(self, value):
        self._set_property("hormonal_contraceptive_use", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Estrogen only",
            "Progesterone only",
            "Unknown",
            "Not Reported",
            "Progesterone and Estrogen",
        },
    )
    def hormone_replacement_therapy_type(self, value):
        self._set_property("hormone_replacement_therapy_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "59",
            "63",
            "39",
            "Not Reported",
            "73",
            "56",
            "53",
            "16",
            "58",
            "45",
            "35",
            "31",
            "33",
            "52",
            "68",
            "66",
            "70",
            "26",
            "51",
            "82",
            "18",
            "Other",
        },
    )
    def hpv_positive_type(self, value):
        self._set_property("hpv_positive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "None",
            "Macroscopic Parametrium",
            "Bladder",
            "Not Reported",
            "Vagina",
            "Microscopic Parametrium",
        },
    )
    def hysterectomy_margins_involved(self, value):
        self._set_property("hysterectomy_margins_involved", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Not performed",
            "Not Reported",
            "Hysterectomy, NOS",
            "Radical Hysterectomy",
            "Simple Hysterectomy",
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
            "Vena Cava Involvement/Thrombus",
            "Lung Involvement",
            "Kidney Involvement",
            "Normal",
            "Liver Involvement",
            "Retroperitoneal Lymph Node Involvement",
            "Carcinomatosis",
            "Not Reported",
        },
    )
    def imaging_findings(self, value):
        self._set_property("imaging_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Negative",
            "Not Performed",
            "Not Reported",
            "Indeterminate",
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

    @psqlgraph.pg_property(
        str, enum={"MRI", "CT Scan", "99mTc Bone Scintigraphy", "PET"}
    )
    def imaging_type(self, value):
        self._set_property("imaging_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Cyclophosphamide",
            "None",
            "Anti-TNF Therapy",
            "Other",
            "Not Reported",
            "Azathioprine",
            "Methotrexate",
        },
    )
    def immunosuppressive_treatment_type(self, value):
        self._set_property("immunosuppressive_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "30",
            "60",
            "50",
            "Not Reported",
            "10",
            "20",
            "90",
            "100",
            "0",
            "70",
            "40",
            "80",
        },
    )
    def karnofsky_performance_status(self, value):
        self._set_property("karnofsky_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Postmenopausal",
            "Not Reported",
            "Premenopausal",
            "Perimenopausal",
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

    @psqlgraph.pg_property(str, enum={"Negative", "Positive", "Not Reported"})
    def peritoneal_washing_results(self, value):
        self._set_property("peritoneal_washing_results", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def pregnancy_count(self, value):
        self._set_property("pregnancy_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Ectopic Pregnancy",
            "Induced Abortion",
            "Live Birth",
            "Stillbirth",
            "Miscarriage",
            "Spontaneous Abortion",
            "Not Reported",
        },
    )
    def pregnancy_outcome(self, value):
        self._set_property("pregnancy_outcome", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Colonoscopy", "Endoscopy", "Unknown", "Not Reported"}
    )
    def procedures_performed(self, value):
        self._set_property("procedures_performed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def progression_or_recurrence(self, value):
        self._set_property("progression_or_recurrence", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Intra-abdominal lymph nodes",
            "Middle ear",
            "Fundus of stomach",
            "Intestinal tract, NOS",
            "Posterior mediastinum",
            "Thymus",
            "Prostate gland",
            "Eye, NOS",
            "Parietal lobe",
            "Overlapping lesion of digestive system",
            "Overlapping lesion of tonsil",
            "Overlapping lesion of hypopharynx",
            "Occipital lobe",
            "Endometrium",
            "Pelvic bones, sacrum, coccyx and associated joints",
            "Pleura, NOS",
            "Greater curvature of stomach, NOS",
            "Body of pancreas",
            "Anterior wall of nasopharynx",
            "Uterine adnexa",
            "Other specified parts of pancreas",
            "Connective, subcutaneous and other soft tissues of trunk, NOS",
            "Skin of scalp and neck",
            "Bladder, NOS",
            "Anterior surface of epiglottis",
            "Overlapping lesion of nasopharynx",
            "Anterior wall of bladder",
            "Gastrointestinal tract, NOS",
            "Short bones of upper limb and associated joints",
            "Overlapping lesion of colon",
            "Middle lobe, lung",
            "Body of penis",
            "Waldeyer ring",
            "Upper lobe, lung",
            "Liver",
            "Cerebral meninges",
            "Short bones of lower limb and associated joints",
            "Optic nerve",
            "Fallopian tube",
            "Oropharynx, NOS",
            "Peripheral nerves and autonomic nervous system of lower limb and hip",
            "Peripheral nerves and autonomic nervous system of head, face, and neck",
            "Thorax, NOS",
            "Acoustic nerve",
            "Spinal cord",
            "Ampulla of Vater",
            "Overlapping lesion of bones, joints and articular cartilage of limbs",
            "Long bones of upper limb, scapula and associated joints",
            "Uterus, NOS",
            "Larynx, NOS",
            "Overlapping lesion of skin",
            "Cervical esophagus",
            "Small intestine, NOS",
            "Pharynx, NOS",
            "Thyroid gland",
            "Bone of limb, NOS",
            "Overlapping lesion of brain and central nervous system",
            "Overlapping lesion of small intestine",
            "Intrathoracic lymph nodes",
            "Connective, subcutaneous and other soft tissues, NOS",
            "Abdomen, NOS",
            "Subglottis",
            "Thoracic esophagus",
            "Retromolar area",
            "Posterior wall of bladder",
            "Broad ligament",
            "Unknown primary site",
            "Commissure of lip",
            "Sphenoid sinus",
            "Female genital tract, NOS",
            "Lower-outer quadrant of breast",
            "Spermatic cord",
            "Pelvic lymph nodes",
            "Jejunum",
            "Vallecula",
            "Connective, subcutaneous and other soft tissues of lower limb and hip",
            "Overlapping lesion of palate",
            "Myometrium",
            "Overlapping lesion of male genital organs",
            "Overlapping lesion of penis",
            "Autonomic nervous system, NOS",
            "Pelvis, NOS",
            "Paraurethral gland",
            "Head, face or neck, NOS",
            "Retina",
            "Cecum",
            "Vagina, NOS",
            "Appendix",
            "Cervix uteri",
            "Kidney, NOS",
            "Tonsillar fossa",
            "Mandible",
            "Unknown",
            "Endocrine gland, NOS",
            "Islets of Langerhans",
            "Body of stomach",
            "Lacrimal gland",
            "Pineal gland",
            "Lymph nodes of multiple regions",
            "Cortex of adrenal gland",
            "Pyriform sinus",
            "Lateral wall of oropharynx",
            "Intrahepatic bile duct",
            "Overlapping lesion of major salivary glands",
            "Peripheral nerves and autonomic nervous system of abdomen",
            "Connective, subcutaneous and other soft tissues of abdomen",
            "Choroid",
            "Dome of bladder",
            "Overlapping lesion of floor of mouth",
            "Upper limb, NOS",
            "Overlapping lesion of brain",
            "Gallbladder",
            "Ascending colon",
            "Accessory sinus, NOS",
            "Overlapping lesion of rectum, anus and anal canal",
            "Trigone of bladder",
            "Testis, NOS",
            "Nasopharynx, NOS",
            "Overlapping lesion of ill-defined sites",
            "Palate, NOS",
            "Ventral surface of tongue, NOS",
            "Other specified parts of male genital organs",
            "Rectum, NOS",
            "Overlapping lesion of respiratory system and intrathoracic organs",
            "Prepuce",
            "External ear",
            "Superior wall of nasopharynx",
            "Blood",
            "Breast, NOS",
            "Glans penis",
            "Lymph nodes of axilla or arm",
            "Mediastinum, NOS",
            "Cardia, NOS",
            "Lingual tonsil",
            "Male genital organs, NOS",
            "Overlapping lesion of other and unspecified parts of mouth",
            "Biliary tract, NOS",
            "External upper lip",
            "Rectosigmoid junction",
            "Other ill-defined sites",
            "Meninges, NOS",
            "Sublingual gland",
            "Lower third of esophagus",
            "Peripheral nerves and autonomic nervous system of pelvis",
            "Anal canal",
            "Specified parts of peritoneum",
            "Middle third of esophagus",
            "Overlapping lesion of bladder",
            "Esophagus, NOS",
            "Skin of lip, NOS",
            "Anus, NOS",
            "Brain, NOS",
            "Clitoris",
            "Bladder neck",
            "Lateral wall of nasopharynx",
            "Olfactory nerve",
            "Overlapping lesion of bones, joints and articular cartilage",
            "Connective, subcutaneous and other soft tissues of pelvis",
            "Gum, NOS",
            "Parametrium",
            "Connective, subcutaneous and other soft tissues of thorax",
            "Renal pelvis",
            "Major salivary gland, NOS",
            "Sigmoid colon",
            "Anterior floor of mouth",
            "Overlapping lesion of accessory sinuses",
            "Overlapping lesion of lip",
            "Bone marrow",
            "Overlapping lesion of endocrine glands and related structures",
            "Nipple",
            "Tongue, NOS",
            "Lymph node, NOS",
            "Labium majus",
            "Base of tongue, NOS",
            "Labium minus",
            "Frontal sinus",
            "Nervous system, NOS",
            "Postcricoid region",
            "Ureter",
            "Mucosa of lower lip",
            "Submandibular gland",
            "Mucosa of upper lip",
            "Stomach, NOS",
            "Parotid gland",
            "Abdominal esophagus",
            "Lesser curvature of stomach, NOS",
            "Peripheral nerves and autonomic nervous system of thorax",
            "Ethmoid sinus",
            "Endocervix",
            "Cheek mucosa",
            "Upper-inner quadrant of breast",
            "Overlapping lesion of eye and adnexa",
            "Connective, subcutaneous and other soft tissues of head, face, and neck",
            "Duodenum",
            "Rib, sternum, clavicle and associated joints",
            "Placenta",
            "Lateral floor of mouth",
            "Brain stem",
            "Eyelid",
            "Round ligament",
            "Branchial cleft",
            "Uvula",
            "Lip, NOS",
            "Posterior wall of nasopharynx",
            "Frontal lobe",
            "Ovary",
            "Splenic flexure of colon",
            "Ureteric orifice",
            "Not Reported",
            "Central portion of breast",
            "Overlapping lesion of biliary tract",
            "Lower gum",
            "Skin of upper limb and shoulder",
            "Mouth, NOS",
            "Upper third of esophagus",
            "Bones of skull and face and associated joints",
            "Hypopharyngeal aspect of aryepiglottic fold",
            "Lung, NOS",
            "Overlapping lesion of retroperitoneum and peritoneum",
            "Fundus uteri",
            "Epididymis",
            "Soft palate, NOS",
            "Axillary tail of breast",
            "Pylorus",
            "Undescended testis",
            "Overlapping lesion of corpus uteri",
            "Nasal cavity",
            "Heart",
            "Tonsillar pillar",
            "Ventricle, NOS",
            "Overlapping lesion of connective, subcutaneous and other soft tissues",
            "Cerebellum, NOS",
            "Pituitary gland",
            "Isthmus uteri",
            "Floor of mouth, NOS",
            "Lateral wall of bladder",
            "Mucosa of lip, NOS",
            "Anterior mediastinum",
            "Medulla of adrenal gland",
            "Other specified parts of female genital organs",
            "Descended testis",
            "Extrahepatic bile duct",
            "Vulva, NOS",
            "Ill-defined sites within respiratory system",
            "Peritoneum, NOS",
            "Overlapping lesion of urinary organs",
            "Head of pancreas",
            "Peripheral nerves and autonomic nervous system of trunk, NOS",
            "Vestibule of mouth",
            "Overlapping lesions of oropharynx",
            "Meckel diverticulum",
            "Cerebrum",
            "Upper gum",
            "Carotid body",
            "Lower-inner quadrant of breast",
            "Tonsil, NOS",
            "Craniopharyngeal duct",
            "Upper-outer quadrant of breast",
            "Connective, subcutaneous and other soft tissues of upper limb and shoulder",
            "Overlapping lesion of tongue",
            "Vertebral column",
            "Overlapping lesion of lip, oral cavity and pharynx",
            "Reticuloendothelial system, NOS",
            "Border of tongue",
            "Hematopoietic system, NOS",
            "Cauda equina",
            "Dorsal surface of tongue, NOS",
            "Main bronchus",
            "Colon, NOS",
            "Overlapping lesion of larynx",
            "Posterior wall of hypopharynx",
            "Adrenal gland, NOS",
            "Overlapping lesion of lung",
            "Overlapping lesion of pancreas",
            "Peripheral nerves and autonomic nervous system of upper limb and shoulder",
            "Spinal meninges",
            "Pancreas, NOS",
            "Skin of other and unspecified parts of face",
            "Overlapping lesion of heart, mediastinum and pleura",
            "Overlapping lesion of stomach",
            "Trachea",
            "External lip, NOS",
            "Overlapping lesion of esophagus",
            "Bone, NOS",
            "Lower lobe, lung",
            "External lower lip",
            "Cornea, NOS",
            "Urinary system, NOS",
            "Upper respiratory tract, NOS",
            "Skin of trunk",
            "Gastric antrum",
            "Exocervix",
            "Cloacogenic zone",
            "Anterior 2/3 of tongue, NOS",
            "Hard palate",
            "Skin, NOS",
            "Corpus uteri",
            "Aortic body and other paraganglia",
            "Penis, NOS",
            "Retroperitoneum",
            "Lymph nodes of inguinal region or leg",
            "Posterior wall of oropharynx",
            "Tail of pancreas",
            "Transverse colon",
            "Conjunctiva",
            "Orbit, NOS",
            "Overlapping lesion of peripheral nerves and autonomic nervous system",
            "Maxillary sinus",
            "Overlapping lesion of female genital organs",
            "Long bones of lower limb and associated joints",
            "Overlapping lesion of cervix uteri",
            "Glottis",
            "Supraglottis",
            "Cranial nerve, NOS",
            "Ileum",
            "Scrotum, NOS",
            "Urachus",
            "Overlapping lesion of vulva",
            "Pancreatic duct",
            "Urethra",
            "Ciliary body",
            "Parathyroid gland",
            "Skin of lower limb and hip",
            "Temporal lobe",
            "Lymph nodes of head, face and neck",
            "Laryngeal cartilage",
            "Lower limb, NOS",
            "Hypopharynx, NOS",
            "Spleen",
            "Hepatic flexure of colon",
            "Overlapping lesion of breast",
            "Descending colon",
        },
    )
    def progression_or_recurrence_anatomic_site(self, value):
        self._set_property("progression_or_recurrence_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Local",
            "Locoregional",
            "Regional",
            "Not Reported",
            "Biochemical",
            "Distant",
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
            "Unknown",
            "Antacids",
            "Proton Pump Inhibitors",
            "No Treatment",
            "Surgically Treated",
            "H2 Blockers",
            "Medically Treated",
            "Not Applicable",
            "Not Reported",
        },
    )
    def reflux_treatment_type(self, value):
        self._set_property("reflux_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Metabolic Syndrome",
            "Diabetes, NOS",
            "Epithelial Dysplasia",
            "Diabetes, Type II",
            "Colonization, Fungal",
            "Gorlin Syndrome",
            "Inherited Genetic Syndrome, NOS",
            "Allergy, Animal, NOS",
            "Oral Contraceptives",
            "Cholelithiasis",
            "Hereditary Papillary Renal Cell Carcinoma",
            "Hemihypertrophy",
            "HIV",
            "Vascular Disease",
            "Tobacco, NOS",
            "Skin Rash",
            "BRCA Family History",
            "Human Herpesvirus-6 (HHV-6)",
            "Down Syndrome",
            "Vision Changes",
            "Sensory Changes",
            "Sarcoidosis",
            "Epstein-Barr Virus",
            "Pneumocystis Pneumonia",
            "Tattoo",
            "Allergy, Dog",
            "Epithelial Hyperplasia",
            "Rheumatoid Arthritis",
            "Pancreatitis",
            "Diverticulitis",
            "Squamous Metaplasia",
            "Von Hippel-Lindau Syndrome",
            "Denys-Drash Syndrome",
            "Hereditary Leiomyomatosis and Renal Cell Carcinoma",
            "Allergy, Fruit",
            "Altered Mental Status",
            "Cyst(s)",
            "Lymphamatoid Papulosis",
            "Hereditary Breast Cancer",
            "Serous tubal intraepithelial carcinoma (STIC)",
            "Chronic Kidney Disease",
            "Hematologic Disorder, NOS",
            "Ataxia-telangiectasia",
            "Endosalpingiosis",
            "Allergy, Ant",
            "Beckwith-Wiedemann",
            "Chlamydia",
            "Rubella",
            "Allergy, Wasp",
            "Escherichia coli",
            "Human Papillomavirus Infection",
            "Not Reported",
            "Adenomyosis",
            "Syphilis",
            "Helicobacter Pylori-Associated Gastritis",
            "Abnormal Glucose Level",
            "Allergy, Meat",
            "Eczema",
            "Hemochromatosis",
            "Wagr Syndrome",
            "Human Herpesvirus-8 (HHV-8)",
            "Hepatic Encephalopathy",
            "Herpes Zoster",
            "Hepatitis A Infection",
            "Endometriosis",
            "Anemia",
            "Obesity",
            "H. pylori Infection",
            "Allergy, Cat",
            "Recurrent Pyogenic Cholangitis",
            "Tubulointerstitial Disease",
            "Hypospadias",
            "Undescended Testis",
            "Cancer",
            "Common variable immune deficiency (CVID)",
            "Barrett's Esophagus",
            "Chronic Hepatitis",
            "Estrogen Excess",
            "Reflux Disease",
            "Hereditary Renal Cell Carcinoma",
            "Benign Prostatic Hyperplasia",
            "Succinate Dehydrogenase-Deficient Renal Cell Carcinoma",
            "Allergy, Food, NOS",
            "Allergy, Nuts",
            "Nonalcoholic Steatohepatitis",
            "Tuberculosis",
            "Fibrosis",
            "BAP1 Tumor Predisposition Syndrome",
            "Mineralcorticoids Excess",
            "Birt-Hogg-Dube Syndrome",
            "Allergy, Seafood",
            "Hereditary Hemorrhagic Telangiectasia",
            "Staphylococcus aureus",
            "Cowden Syndrome",
            "Hepatitis B Infection",
            "Inflammation, Hyperkeratosis",
            "Myelodysplastic Syndrome",
            "Sialadenitis",
            "Glomerular Disease",
            "Thyroid Nodular Hyperplasia",
            "Allergy, Eggs",
            "Nodular Prostatic Hyperplasia",
            "Tuberous Sclerosis",
            "Allergy, Bee",
            "Sjogren's Syndrome",
            "Diet",
            "Mycobacterium avium Complex",
            "High Grade Dysplasia",
            "Unknown",
            "Gilbert's Syndrome",
            "Treponema pallidum",
            "Lymphocytic Thyroiditis",
            "Cryptococcal Meningitis",
            "Motor / Movement Change",
            "Nonalcoholic Fatty Liver Disease",
            "Hereditary Kidney Oncocytoma",
            "Alcohol Consumption",
            "Intestinal Metaplasia",
            "Allergy, Processed Foods",
            "Hodgkin Lymphoma",
            "Alpha-1 Antitrypsin Deficiency",
            "Cytomegalovirus (CMV)",
            "Low Grade Dysplasia",
            "Fanconi Anemia",
            "Rubinstein-Taybi Syndrome",
            "Adenosis (Atypical Adenomatous Hyperplasia)",
            "Androgen Excess",
            "Gastric Polyp(s)",
            "Hepatitis, NOS",
            "Tobacco, Smoking",
            "Tumor-associated Lymphoid Proliferation",
            "Shingles",
            "Allergy, Mold or Dust",
            "Inflammation",
            "None",
            "Turcot Syndrome",
            "Gastritis",
            "Chronic Pancreatitis",
            "Colon Polyps",
            "Diabetes, Type I",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Lymphocytic Meningitis",
            "Colonization, Bacterial",
            "Hereditary Ovarian Cancer",
            "Asthma",
            "Iron Overload",
            "Hay Fever",
            "Malaria",
            "Cortisol Excess",
            "Hepatitis C Infection",
            "Steatosis",
            "Dermatomyosis",
            "Familial Adenomatous Polyposis",
            "Hashimoto's Thyroiditis",
            "EBV Lymphoproliferation",
            "Tobacco, Smokeless",
            "Primary Sclerosing Cholangitis",
            "Seizure",
            "Alcoholic Liver Disease",
            "Allergy, Dairy or Lactose",
            "Varicella Zoster Virus",
            "High-grade Prostatic Intraepithelial Neoplasia (PIN)",
            "Behcet's Disease",
            "Chloroma",
            "Lynch Syndrome",
            "Myasthenia Gravis",
            "Li-Fraumeni Syndrome",
            "Bacteroides fragilis",
            "Chronic Systemic Steroid Use",
            "Headache",
            "Cirrhosis",
            "Neurocystericerosis",
            "Parasitic Disease of Biliary Tract",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Hereditary Prostate Cancer",
            "Autoimmune Atrophic Chronic Gastritis",
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
            "Biochemical Assessment",
            "Clinical Assessment",
            "Both Clinical and Biochemical Assessments",
            "Not Reported",
        },
    )
    def risk_factor_method_of_diagnosis(self, value):
        self._set_property("risk_factor_method_of_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def risk_factor_treatment(self, value):
        self._set_property("risk_factor_treatment", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Sodium Fluoride", "PSMA", "Choline", "Axumin", "Acetate"}
    )
    def scan_tracer_used(self, value):
        self._set_property("scan_tracer_used", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Last Contact",
            "Follow-up",
            "Postoperative",
            "Not Reported",
            "Adolescence",
            "Preoperative",
            "Recurrence/Progression",
            "Initial Diagnosis",
            "Post Adjuvant Therapy",
            "Prior to Treatment",
            "Adjuvant Therapy",
            "Childhood",
            "Adulthood",
            "Post Secondary Therapy",
            "Prior to Diagnosis",
            "Post Hormone Therapy",
            "Other",
        },
    )
    def timepoint_category(self, value):
        self._set_property("timepoint_category", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "No", "Yes"})
    def undescended_testis_corrected(self, value):
        self._set_property("undescended_testis_corrected", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def undescended_testis_corrected_age(self, value):
        self._set_property("undescended_testis_corrected_age", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Left", "Not Reported", "Right", "Bilateral"})
    def undescended_testis_corrected_laterality(self, value):
        self._set_property("undescended_testis_corrected_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Orchiopexy",
            "Hormones",
            "Spontaneous Descent",
            "Not Reported",
            "Testis Removed",
        },
    )
    def undescended_testis_corrected_method(self, value):
        self._set_property("undescended_testis_corrected_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "No", "Yes"})
    def undescended_testis_history(self, value):
        self._set_property("undescended_testis_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Left", "Not Reported", "Right", "Bilateral"})
    def undescended_testis_history_laterality(self, value):
        self._set_property("undescended_testis_history_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "HCV Genotype",
            "HBV DNA",
            "HBV Core Antibody",
            "Hepatitis C Antibody",
            "HBV Surface Antibody",
            "Not Reported",
            "Hepatitis B Surface Antigen",
            "HBV Genotype",
            "Hepatitis C Virus RNA",
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
