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
            "Depressed Level of Consciousness",
            "Platelet Count Decreased",
            "Esophageal Necrosis",
            "Anal Pain",
            "Spinal Fracture",
            "Trigeminal Nerve Disorder",
            "Growth Accelerated",
            "Rectal Obstruction",
            "Fat Atrophy",
            "Hematosalpinx",
            "Neck Soft Tissue Necrosis",
            "Burn",
            "Rash Maculo-Papular",
            "Retinopathy",
            "Superficial Soft Tissue Fibrosis",
            "Serum Amylase Increased",
            "Salivary Gland Fistula",
            "Floaters",
            "Postoperative Hemorrhage",
            "Pancreas Infection",
            "Suicide Attempt",
            "Pancreatic Enzymes Decreased",
            "Myalgia",
            "Arthralgia",
            "Skin Hypopigmentation",
            "Autoimmune Disorder",
            "Urinary Tract Pain",
            "Visceral Arterial Ischemia",
            "Investigations - Other",
            "Vaginal Perforation",
            "Vas Deferens Anastomotic Leak",
            "Disseminated Intravascular Coagulation",
            "Nipple Deformity",
            "Hyperparathyroidism",
            "Portal Vein Thrombosis",
            "Hemorrhoidal Hemorrhage",
            "Hepatic Hemorrhage",
            "Hypersomnia",
            "Dysphasia",
            "Purpura",
            "Esophageal Perforation",
            "Lip Infection",
            "Scleral Disorder",
            "Glossopharyngeal Nerve Disorder",
            "Accessory Nerve Disorder",
            "Atrial Fibrillation",
            "Cervicitis Infection",
            "Stroke",
            "Hyperkalemia",
            "Death Neonatal",
            "Heart Failure",
            "Injury to Carotid Artery",
            "Joint Range of Motion Decreased Cervical Spine",
            "Duodenal Infection",
            "Thromboembolic Event",
            "Wheezing",
            "Hearing Impaired",
            "Hypertriglyceridemia",
            "Eye Disorders - Other",
            "Intraoperative Musculoskeletal Injury",
            "Breast Atrophy",
            "Joint Effusion",
            "Epistaxis",
            "Pharyngeal Hemorrhage",
            "Aspartate Aminotransferase Increased",
            "Hemolysis",
            "Glaucoma",
            "Otitis Media",
            "Anal Hemorrhage",
            "Leukocytosis",
            "Hyperhidrosis",
            "Sinus Bradycardia",
            "Fallopian Tube Perforation",
            "Urostomy Obstruction",
            "Cognitive Disturbance",
            "Central Nervous System Necrosis",
            "Myelitis",
            "Peripheral Sensory Neuropathy",
            "Bronchopulmonary Hemorrhage",
            "Rectal Fistula",
            "External Ear Inflammation",
            "Toothache",
            "Laryngeal Mucositis",
            "Enterocolitis",
            "Periorbital Edema",
            "Pancreatic Hemorrhage",
            "Retinal Detachment",
            "Scoliosis",
            "Chest Wall Pain",
            "Watering Eyes",
            "Radiation Recall Reaction (Dermatologic)",
            "Rectal Perforation",
            "Small Intestinal Stenosis",
            "Small Intestine Ulcer",
            "Euphoria",
            "Intraoperative Respiratory Injury",
            "Forced Expiratory Volume Decreased",
            "Penile Pain",
            "Respiratory Failure",
            "Joint Range of Motion Decreased Lumbar Spine",
            "Pain in Extremity",
            "Pharyngolaryngeal Pain",
            "Hemoglobinuria",
            "Iron Overload",
            "Abdominal Pain",
            "Flashing Lights",
            "Anal Necrosis",
            "Ileal Fistula",
            "Alanine Aminotransferase Increased",
            "Female Genital Tract Fistula",
            "Activated Partial Thromboplastin Time Prolonged",
            "Prostatic Hemorrhage",
            "Anxiety",
            "Anal Ulcer",
            "Tinnitus",
            "Esophageal Obstruction",
            "Hypotension",
            "Bruising",
            "Hyponatremia",
            "Device Related Infection",
            "Intraoperative Hepatobiliary Injury",
            "Oculomotor Nerve Disorder",
            "Bile Duct Stenosis",
            "Atrioventricular Block First Degree",
            "CPK Increased",
            "Libido Decreased",
            "Neoplasms Benign, Malignant and Unspecified (Incl Cysts and Polyps) - Other",
            "Pancreatic Duct Stenosis",
            "Wound Infection",
            "Spleen Disorder",
            "Acoustic Nerve Disorder NOS",
            "Dyspepsia",
            "Kidney Anastomotic Leak",
            "Wrist Fracture",
            "Muscle Weakness Upper Limb",
            "Intraoperative Endocrine Injury",
            "IVth Nerve Disorder",
            "Delayed Orgasm",
            "Lipase Increased",
            "Anal Fistula",
            "Ileal Obstruction",
            "Bronchospasm",
            "Cheilitis",
            "Gastrointestinal Pain",
            "Duodenal Perforation",
            "Sneezing",
            "Ventricular Arrhythmia",
            "Hypertension",
            "Venous Injury",
            "Laryngeal Stenosis",
            "Renal Colic",
            "Colonic Hemorrhage",
            "Urinary Retention",
            "Back Pain",
            "Retroperitoneal Hemorrhage",
            "Seizure",
            "Uterine Hemorrhage",
            "Death NOS",
            "Phlebitis",
            "Gastric Fistula",
            "Duodenal Stenosis",
            "Esophageal Infection",
            "Appendicitis Perforated",
            "Vaginal Obstruction",
            "Hyperthyroidism",
            "Nail Discoloration",
            "Intraoperative Venous Injury",
            "Metabolism and Nutrition Disorders - Other",
            "Restrictive Cardiomyopathy",
            "Haptoglobin Decreased",
            "Injection Site Reaction",
            "Sinusitis",
            "Vagus Nerve Disorder",
            "Intraoperative Splenic Injury",
            "Flank Pain",
            "Upper Respiratory Infection",
            "Lymphedema",
            "Ovarian Rupture",
            "Spasticity",
            "Hypertrichosis",
            "Perforation Bile Duct",
            "Electrocardiogram QT Corrected Interval Prolonged",
            "Pruritus",
            "Tumor Lysis Syndrome",
            "Ileal Hemorrhage",
            "Eyelid Function Disorder",
            "Hypernatremia",
            "Ejection Fraction Decreased",
            "Gastric Anastomotic Leak",
            "Ataxia",
            "Malabsorption",
            "Postnasal Drip",
            "Telangiectasia",
            "Tracheal Fistula",
            "Vaginal Discharge",
            "Esophageal Fistula",
            "Lip Pain",
            "Abdominal Soft Tissue Necrosis",
            "Creatinine Increased",
            "Gum Infection",
            "Muscle Weakness Lower Limb",
            "Vaginal Pain",
            "Muscle Weakness Trunk",
            "Hyperglycemia",
            "Ischemia Cerebrovascular",
            "Peripheral Ischemia",
            "Chills",
            "Intraoperative Skin Injury",
            "Sick Sinus Syndrome",
            "Flatulence",
            "Hiccups",
            "Gallbladder Infection",
            "Colonic Fistula",
            "Feminization Acquired",
            "Diarrhea",
            "Atrioventricular Block Complete",
            "Stoma Site Infection",
            "Edema Trunk",
            "Erythema Multiforme",
            "Keratitis",
            "Small Intestinal Mucositis",
            "Intraoperative Arterial Injury",
            "Cardiac Troponin T Increased",
            "Gynecomastia",
            "Growth Suppression",
            "Bronchial Fistula",
            "Pleural Effusion",
            "Stridor",
            "Cholesterol High",
            "Lymphocyte Count Decreased",
            "Urostomy Stenosis",
            "Pulmonary Fistula",
            "Endocarditis Infective",
            "Urinary Tract Obstruction",
            "Radiculitis",
            "Alkalosis",
            "Hirsutism",
            "Blood Bilirubin Increased",
            "Ovarian Infection",
            "Pharyngeal Fistula",
            "Tracheostomy Site Bleeding",
            "Neck Edema",
            "Pancreatic Necrosis",
            "Multi-Organ Failure",
            "Peripheral Motor Neuropathy",
            "Arteritis Infective",
            "Ventricular Tachycardia",
            "Photosensitivity",
            "Jejunal Obstruction",
            "Gastric Stenosis",
            "Acute Kidney Injury",
            "Hoarseness",
            "Arthritis",
            "Blood Prolactin Abnormal",
            "Adrenal Insufficiency",
            "Non-Cardiac Chest Pain",
            "Blood Corticotrophin Decreased",
            "Intraoperative Reproductive Tract Injury",
            "Pain of Skin",
            "Pancreatic Anastomotic Leak",
            "Pelvic Infection",
            "Fallopian Tube Anastomotic Leak",
            "Bullous Dermatitis",
            "Laryngospasm",
            "Vestibular Disorder",
            "Toxic Epidermal Necrolysis",
            "Urostomy Leak",
            "Flu Like Symptoms",
            "Gastrointestinal Fistula",
            "Soft Tissue Necrosis Lower Limb",
            "Conduction Disorder",
            "Jejunal Stenosis",
            "Sinus Tachycardia",
            "Photophobia",
            "Acute Coronary Syndrome",
            "Endocrine Disorders - Other",
            "Hypoparathyroidism",
            "Nystagmus",
            "Unequal Limb Length",
            "Catheter Related Infection",
            "Chest Pain - Cardiac",
            "Lordosis",
            "Erythroderma",
            "Hypomagnesemia",
            "Vomiting",
            "Depression",
            "Rash Acneiform",
            "Capillary Leak Syndrome",
            "Gastroesophageal Reflux Disease",
            "Libido Increased",
            "Restlessness",
            "CD4 Lymphocytes Decreased",
            "Hypermagnesemia",
            "Olfactory Nerve Disorder",
            "Colonic Obstruction",
            "Gastric Perforation",
            "Hepatitis Viral",
            "Bone Infection",
            "Hematoma",
            "Papulopustular Rash",
            "Soft Tissue Infection",
            "Rectal Ulcer",
            "Serum Sickness",
            "Pneumonitis",
            "Spermatic Cord Obstruction",
            "Movements Involuntary",
            "Atelectasis",
            "Facial Muscle Weakness",
            "Trismus",
            "Hepatic Failure",
            "Rash Pustular",
            "Cardiac Arrest",
            "Left Ventricular Systolic Dysfunction",
            "Portal Hypertension",
            "Seroma",
            "Colitis",
            "Fibrosis Deep Connective Tissue",
            "Penile Infection",
            "White Blood Cell Decreased",
            "Anorgasmia",
            "INR Increased",
            "Gingival Pain",
            "Spermatic Cord Hemorrhage",
            "Intestinal Stoma Leak",
            "Rectal Stenosis",
            "Nausea",
            "General Disorders and Administration Site Conditions - Other",
            "Bronchial Infection",
            "Oral Pain",
            "Myositis",
            "Premature Menopause",
            "Soft Tissue Necrosis Upper Limb",
            "Growth Hormone Abnormal",
            "Fibrinogen Decreased",
            "Colonic Ulcer",
            "Genital Edema",
            "Cecal Hemorrhage",
            "Infections and Infestations - Other",
            "Tracheal Mucositis",
            "Chronic Kidney Disease",
            "Alopecia",
            "Gallbladder Pain",
            "Hot Flashes",
            "Pain",
            "Proteinuria",
            "Gastritis",
            "Tracheal Hemorrhage",
            "Unintended Pregnancy",
            "Phlebitis Infective",
            "Syncope",
            "Hypothyroidism",
            "Urticaria",
            "Delayed Puberty",
            "Ear and Labyrinth Disorders - Other",
            "Hip Fracture",
            "Cystitis Noninfective",
            "Gallbladder Obstruction",
            "Intraoperative Neurological Injury",
            "Lower Gastrointestinal Hemorrhage",
            "Palmar-Plantar Erythrodysesthesia Syndrome",
            "Dysesthesia",
            "Breast Infection",
            "Skin Induration",
            "Hypophosphatemia",
            "Supraventricular Tachycardia",
            "Azoospermia",
            "Rectal Pain",
            "Ventricular Fibrillation",
            "Hepatic Infection",
            "Meningismus",
            "Esophageal Hemorrhage",
            "Pharyngeal Necrosis",
            "Stomach Pain",
            "Flushing",
            "Febrile Neutropenia",
            "Esophageal Anastomotic Leak",
            "Prostate Infection",
            "Pulmonary Edema",
            "Retinal Vascular Disorder",
            "Myocarditis",
            "Lethargy",
            "Neck Pain",
            "Vitreous Hemorrhage",
            "Laryngopharyngeal Dysesthesia",
            "Jejunal Hemorrhage",
            "Intestinal Stoma Obstruction",
            "Papilledema",
            "Infusion Related Reaction",
            "Infusion Site Extravasation",
            "Obstruction Gastric",
            "Dehydration",
            "Leukoencephalopathy",
            "Encephalitis Infection",
            "Buttock Pain",
            "Ileus",
            "Psychiatric Disorders - Other",
            "Cushingoid",
            "Palpitations",
            "Laryngitis",
            "Salivary Gland Infection",
            "Scalp Pain",
            "Blurred Vision",
            "Corneal Ulcer",
            "Vertigo",
            "Fall",
            "Esophageal Ulcer",
            "Hyperuricemia",
            "Skin Atrophy",
            "Bladder Perforation",
            "Scrotal Pain",
            "Acidosis",
            "Jejunal Ulcer",
            "Malaise",
            "Dry Skin",
            "Rectal Hemorrhage",
            "Renal and Urinary Disorders - Other",
            "Akathisia",
            "Immune System Disorders - Other",
            "Kyphosis",
            "Blood Gonadotrophin Abnormal",
            "Perineal Pain",
            "Small Intestinal Obstruction",
            "Aortic Injury",
            "Delusions",
            "Fetal Growth Retardation",
            "Suicidal Ideation",
            "Gastroparesis",
            "Anal Mucositis",
            "Pulmonary Valve Disease",
            "Obesity",
            "Eye Pain",
            "Intraoperative Gastrointestinal Injury",
            "Pelvic Pain",
            "Hydrocephalus",
            "Pulmonary Fibrosis",
            "Phantom Pain",
            "Vaginal Fistula",
            "Conjunctivitis Infective",
            "Esophageal Stenosis",
            "Virilization",
            "Tracheal Obstruction",
            "Allergic Rhinitis",
            "Gallbladder Perforation",
            "Gait Disturbance",
            "Neutrophil Count Decreased",
            "Encephalopathy",
            "Intraoperative Hemorrhage",
            "Cerebrospinal Fluid Leakage",
            "Large Intestinal Anastomotic Leak",
            "Body Odor",
            "Stomal Ulcer",
            "Dysgeusia",
            "GGT Increased",
            "Pharyngeal Anastomotic Leak",
            "Transient Ischemic Attacks",
            "Pneumothorax",
            "Small Intestinal Anastomotic Leak",
            "Splenic Infection",
            "Injury to Superior Vena Cava",
            "Psychosis",
            "Tremor",
            "Kidney Infection",
            "Pyramidal Tract Syndrome",
            "Ureteric Anastomotic Leak",
            "Optic Nerve Disorder",
            "Ear Pain",
            "Mucositis Oral",
            "Biliary Fistula",
            "Biliary Tract Infection",
            "Stenosis of Gastrointestinal Stoma",
            "Tooth Infection",
            "Arterial Injury",
            "Uterine Anastomotic Leak",
            "Uterine Infection",
            "Vaginal Inflammation",
            "Hepatic Necrosis",
            "Superior Vena Cava Syndrome",
            "Uveitis",
            "Skin Hyperpigmentation",
            "Postoperative Thoracic Procedure Complication",
            "Edema Face",
            "Ileal Ulcer",
            "Neuralgia",
            "Pharyngeal Stenosis",
            "Laryngeal Obstruction",
            "Injury to Jugular Vein",
            "Sepsis",
            "Ileal Stenosis",
            "Abdominal Distension",
            "Nasal Congestion",
            "Hemorrhoids",
            "Urethral Anastomotic Leak",
            "Duodenal Obstruction",
            "Uterine Perforation",
            "Lymph Gland Infection",
            "Esophageal Pain",
            "Reversible Posterior Leukoencephalopathy Syndrome",
            "Conjunctivitis",
            "Rectal Mucositis",
            "Uterine Pain",
            "Enterocolitis Infectious",
            "Vaginal Dryness",
            "Edema Limbs",
            "Injury, Poisoning and Procedural Complications - Other",
            "Osteoporosis",
            "Sleep Apnea",
            "Aortic Valve Disease",
            "Surgical and Medical Procedures - Other",
            "Dermatitis Radiation",
            "Ileal Perforation",
            "Premature Delivery",
            "Anorectal Infection",
            "Fatigue",
            "Osteonecrosis of Jaw",
            "Paroxysmal Atrial Tachycardia",
            "Pelvic Floor Muscle Weakness",
            "Pregnancy, Puerperium and Perinatal Conditions - Other",
            "Hemoglobin Increased",
            "Pharyngeal Mucositis",
            "Urinary Urgency",
            "Carbon Monoxide Diffusing Capacity Decreased",
            "Edema Cerebral",
            "Renal Hemorrhage",
            "Typhlitis",
            "Duodenal Fistula",
            "Glucose Intolerance",
            "Infective Myositis",
            "Hallucinations",
            "Tracheal Stenosis",
            "Colonic Perforation",
            "Aspiration",
            "Localized Edema",
            "Intraoperative Breast Injury",
            "Recurrent Laryngeal Nerve Palsy",
            "Weight Gain",
            "Bronchial Obstruction",
            "Joint Infection",
            "Pleuritic Pain",
            "Cardiac Troponin I Increased",
            "Concentration Impairment",
            "Intestinal Stoma Site Bleeding",
            "Lymph Node Pain",
            "Generalized Muscle Weakness",
            "Fever",
            "Jejunal Fistula",
            "Hypocalcemia",
            "Hypoglossal Nerve Disorder",
            "Hypohidrosis",
            "Nail Ridging",
            "Encephalomyelitis Infection",
            "Skin Infection",
            "Right Ventricular Dysfunction",
            "Dysarthria",
            "Intraoperative Cardiac Injury",
            "Mediastinal Infection",
            "Vaginal Hemorrhage",
            "Esophageal Varices Hemorrhage",
            "Bone Marrow Hypocellular",
            "Ejaculation Disorder",
            "Social Circumstances - Other",
            "Dyspnea",
            "Tooth Development Disorder",
            "Hepatobiliary Disorders - Other",
            "Hypokalemia",
            "Gallbladder Necrosis",
            "Rectal Anastomotic Leak",
            "Rectal Necrosis",
            "Prolapse of Intestinal Stoma",
            "Menorrhagia",
            "Gastrointestinal Stoma Necrosis",
            "Fallopian Tube Stenosis",
            "Presyncope",
            "Asystole",
            "Peritoneal Necrosis",
            "Vascular Disorders - Other",
            "Hypercalcemia",
            "Abdominal Infection",
            "Gastric Hemorrhage",
            "Dental Caries",
            "Myocardial Infarction",
            "Pericarditis",
            "Urostomy Site Bleeding",
            "Uterine Obstruction",
            "Laryngeal Inflammation",
            "Cough",
            "Alcohol Intolerance",
            "Testicular Pain",
            "Vaginal Stricture",
            "Personality Change",
            "Adult Respiratory Distress Syndrome",
            "Chylothorax",
            "Gastric Necrosis",
            "Laryngeal Fistula",
            "Hypoalbuminemia",
            "Skin and Subcutaneous Tissue Disorders - Other",
            "Laryngeal Edema",
            "Testicular Hemorrhage",
            "Bronchopleural Fistula",
            "Facial Pain",
            "Abducens Nerve Disorder",
            "Retinal Tear",
            "Intra-Abdominal Hemorrhage",
            "Hypoglycemia",
            "Fallopian Tube Obstruction",
            "Duodenal Ulcer",
            "Blood Antidiuretic Hormone Abnormal",
            "Fecal Incontinence",
            "Tracheitis",
            "Congenital, Familial and Genetic Disorders - Other",
            "Mania",
            "Biliary Anastomotic Leak",
            "Night Blindness",
            "Ovarian Hemorrhage",
            "Superficial Thrombophlebitis",
            "Treatment Related Secondary Malignancy",
            "Cranial Nerve Infection",
            "Vasculitis",
            "Meningitis",
            "Hematuria",
            "Muscle Weakness Right-Sided",
            "Testicular Disorder",
            "Ankle Fracture",
            "Vulval Infection",
            "Mediastinal Hemorrhage",
            "Wound Complication",
            "Upper Gastrointestinal Hemorrhage",
            "Dysmenorrhea",
            "Bladder Anastomotic Leak",
            "Pericardial Tamponade",
            "Hepatic Pain",
            "Urinary Fistula",
            "Oral Cavity Fistula",
            "Gastric Ulcer",
            "Head Soft Tissue Necrosis",
            "Lactation Disorder",
            "Paresthesia",
            "Vaginal Infection",
            "Anorexia",
            "Cataract",
            "Appendicitis",
            "Bladder Spasm",
            "Dry Eye",
            "Retinoic Acid Syndrome",
            "Fracture",
            "Sore Throat",
            "Bronchial Stricture",
            "Irritability",
            "Intraoperative Renal Injury",
            "Nervous System Disorders - Other",
            "Extrapyramidal Disorder",
            "Prolapse of Urostomy",
            "Erectile Dysfunction",
            "Ascites",
            "Prostatic Pain",
            "Enterovesical Fistula",
            "Lymph Leakage",
            "Cytokine Release Syndrome",
            "Uterine Fistula",
            "Menopause",
            "Dry Mouth",
            "Gastrointestinal Disorders - Other",
            "Musculoskeletal and Connective Tissue Disorders - Other",
            "Tumor Pain",
            "Urine Output Decreased",
            "Agitation",
            "Lung Infection",
            "Bone Pain",
            "Pericardial Effusion",
            "Lymphocyte Count Increased",
            "Muscle Weakness Left-Sided",
            "Anemia",
            "Weight Loss",
            "Extraocular Muscle Paresis",
            "Leukemia Secondary to Oncology Chemotherapy",
            "Jejunal Perforation",
            "Dysphagia",
            "Thrombotic Thrombocytopenic Purpura",
            "Scrotal Infection",
            "Urinary Tract Infection",
            "Esophagitis",
            "Duodenal Hemorrhage",
            "Insomnia",
            "Intracranial Hemorrhage",
            "Paronychia",
            "Bladder Infection",
            "Cholecystitis",
            "Hypoxia",
            "Oral Dysesthesia",
            "Ovulation Pain",
            "Laryngeal Hemorrhage",
            "Irregular Menstruation",
            "Mitral Valve Disease",
            "Lymphocele",
            "Stevens-Johnson Syndrome",
            "Rhinitis Infective",
            "Headache",
            "Vaginismus",
            "Pharyngitis",
            "Precocious Puberty",
            "Apnea",
            "Sudden Death NOS",
            "Pleural Infection",
            "Salivary Duct Inflammation",
            "Confusion",
            "Corneal Infection",
            "Vital Capacity Abnormal",
            "Vasovagal Reaction",
            "Joint Range of Motion Decreased",
            "Reproductive System and Breast Disorders - Other",
            "Fetal Death",
            "Bloating",
            "Pancreatic Fistula",
            "Dizziness",
            "Dyspareunia",
            "Atrial Flutter",
            "Oligospermia",
            "Memory Impairment",
            "Tricuspid Valve Disease",
            "Anaphylaxis",
            "Brachial Plexopathy",
            "Oral Hemorrhage",
            "Nail Loss",
            "Anal Stenosis",
            "Avascular Necrosis",
            "Exostosis",
            "Proctitis",
            "Allergic Reaction",
            "Wound Dehiscence",
            "Cardiac Disorders - Other",
            "Intraoperative Head and Neck Injury",
            "Periorbital Infection",
            "Prostatic Obstruction",
            "Spermatic Cord Anastomotic Leak",
            "Blood and Lymphatic System Disorders - Other",
            "Intraoperative Ear Injury",
            "Cecal Infection",
            "Respiratory, Thoracic and Mediastinal Disorders - Other",
            "Constipation",
            "Endophthalmitis",
            "Peritoneal Infection",
            "External Ear Pain",
            "Amnesia",
            "Productive Cough",
            "Tooth Discoloration",
            "Vascular Access Complication",
            "Breast Pain",
            "Musculoskeletal Deformity",
            "Mucosal Infection",
            "Sinus Disorder",
            "Hypothermia",
            "Renal Calculi",
            "Gastrointestinal Anastomotic Leak",
            "Voice Alteration",
            "Skin Ulceration",
            "Aphonia",
            "Pulmonary Hypertension",
            "Mobitz Type I",
            "Intraoperative Urinary Injury",
            "Gallbladder Fistula",
            "Middle Ear Inflammation",
            "Hemolytic Uremic Syndrome",
            "Alkaline Phosphatase Increased",
            "Colonic Stenosis",
            "Peripheral Nerve Infection",
            "Sinus Pain",
            "Nail Infection",
            "Somnolence",
            "Urinary Frequency",
            "Pancreatitis",
            "Myelodysplastic Syndrome",
            "Lipohypertrophy",
            "Delirium",
            "Eye Infection",
            "Urinary Incontinence",
            "Facial Nerve Disorder",
            "Constrictive Pericarditis",
            "Urine Discoloration",
            "Periodontal Disease",
            "Urethral Infection",
            "Otitis Externa",
            "Mobitz (Type) II Atrioventricular Block",
            "Wolff-Parkinson-White Syndrome",
            "Vaginal Anastomotic Leak",
            "Small Intestinal Perforation",
            "Pleural Hemorrhage",
            "Small Intestine Infection",
            "Arachnoiditis",
            "Injury to Inferior Vena Cava",
            "Intraoperative Ocular Injury",
            "Pelvic Soft Tissue Necrosis",
        },
    )
    def adverse_event(self, value):
        self._set_property("adverse_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Grade 1", "Grade 2", "Grade 5", "Grade 4", "Grade 3"})
    def adverse_event_grade(self, value):
        self._set_property("adverse_event_grade", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Progressive Multifocal Leukoencephalopathy",
            "Coccidioidomycosis",
            "Salmonella Septicemia",
            "Mycobacterium tuberculosis",
            "Mycobacterium avium Complex",
            "Isosporiasis",
            "Candidiasis",
            "Wasting Syndrome",
            "Pneumocystis Pneumonia",
            "Mycobacterium, NOS",
            "Cryptosporidiosis, Chronic Intestinal",
            "Encephalopathy",
            "Herpes Simplex Virus",
            "Cryptococcosis",
            "Cytomegalovirus",
            "Histoplasmosis",
            "Toxoplasmosis",
            "Nocardiosis",
            "Pneumonia, NOS",
        },
    )
    def aids_risk_factors(self, value):
        self._set_property("aids_risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def barretts_esophagus_goblet_cells_present(self, value):
        self._set_property("barretts_esophagus_goblet_cells_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def body_surface_area(self, value):
        self._set_property("body_surface_area", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def bmi(self, value):
        self._set_property("bmi", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def cause_of_response(self, value):
        self._set_property("cause_of_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def cd4_count(self, value):
        self._set_property("cd4_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Hemophiliac",
            "Intravenous Drug User",
            "None",
            "Transfusion Recipient",
            "Heterosexual Contact",
            "Not Reported",
            "Homosexual Contact",
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
            "Insulin Controlled Diabetes",
            "Liver Cirrhosis (Liver Disease)",
            "Clonal Hematopoiesis",
            "Peripheral Vascular Disease",
            "Hypospadias",
            "Peripheral Neuropathy",
            "Arrhythmia",
            "Transient Ischemic Attack",
            "Chloroma",
            "DVT/PE",
            "Methicillin-Resistant Staphylococcus aureus (MRSA)",
            "Lupus",
            "Diabetes",
            "Rheumatoid Arthritis",
            "Fibromyalgia",
            "Peutz-Jeghers Disease",
            "Chronic Pancreatitis",
            "Low Grade Liver Dysplastic Nodule",
            "Obesity",
            "Asthma",
            "Gonadal Dysfunction",
            "Denys-Drash Syndrome",
            "Diverticulitis",
            "Eczema",
            "Metabolic Syndrome",
            "Pulmonary Fibrosis",
            "Cirrhosis, Unknown Etiology",
            "Lymphamatoid Papulosis",
            "Sjogren's Syndrome",
            "CNS Infection",
            "Adrenocortical Insufficiency",
            "Fibrosis",
            "Smoking",
            "Human Papillomavirus Infection",
            "Pulmonary Hemorrhage",
            "Atrial Fibrillation",
            "Hepatitis B Infection",
            "MAI",
            "Stroke",
            "Arthritis",
            "Diet Controlled Diabetes",
            "Bone Fracture(s)",
            "Hepatitis",
            "Turcot Syndrome",
            "Blood Clots",
            "Not Reported",
            "Dermatomyosis",
            "Colon Polyps",
            "Chronic Systemic Steroid Use",
            "Interstitial Pneumontis or ARDS",
            "Osteoporosis or Osteopenia",
            "Lynch Syndrome",
            "Glaucoma",
            "Primary Sclerosing Cholangitis",
            "Adenocarcinoma",
            "Mycobacterium avium Complex",
            "Anemia",
            "Herpes",
            "Other",
            "EBV Lymphoproliferation",
            "Syphilis",
            "Cataracts",
            "Urinary Tract Infection",
            "Staph Osteomyelitis",
            "Crohn's Disease",
            "Psoriasis",
            "Hyperlipidemia",
            "Hodgkin Lymphoma",
            "Depression",
            "Beckwith-Wiedemann",
            "Gastroesophageal Reflux Disease",
            "Hemihypertrophy",
            "Renal Failure (Requiring Dialysis)",
            "Epilepsy",
            "Renal Dialysis",
            "Ataxia-telangiectasia",
            "Hashimoto's Thyroiditis",
            "Cholelithiasis",
            "Neuroendocrine Tumor",
            "Diabetes, Type II",
            "Rubinstein-Taybi Syndrome",
            "Iron Overload",
            "Cancer",
            "Sleep apnea",
            "Glycogen Storage Disease",
            "Nonalcoholic Steatohepatitis",
            "Hypercholesterolemia",
            "H. pylori Infection",
            "Congestive Heart Failure (CHF)",
            "Anxiety",
            "Chronic Fatigue Syndrome",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Shingles",
            "Bronchitis",
            "Headache",
            "Renal Insufficiency",
            "Hepatitis, Chronic",
            "Other Pulmonary Complications",
            "Diabetic Neuropathy",
            "High Grade Liver Dysplastic Nodule",
            "Pain (Various)",
            "Connective Tissue Disorder",
            "Sarcoidosis",
            "Osteoarthritis",
            "HUS/TTP",
            "Other Cancer Within 5 Years",
            "Ulcerative Colitis",
            "Coronary Artery Disease",
            "Hepatitis A Infection",
            "Alpha-1 Antitrypsin",
            "Unknown",
            "COPD",
            "ITP",
            "Malaria",
            "Steatosis",
            "Allergies",
            "Hypertension",
            "Biliary Disorder",
            "Lymphocytic Meningitis",
            "Joint Replacement",
            "Avascular Necrosis",
            "Kidney Disease",
            "Cerebrovascular Disease",
            "Varicella Zoster Virus",
            "Acute Renal Failure",
            "Peptic Ulcer (Ulcer)",
            "Seizure",
            "Chronic Renal Failure",
            "Intraductal Papillary Mucinous Neoplasm",
            "Adenomatous Polyposis Coli",
            "Barrett's Esophagus",
            "Cryptogenic Organizing Pneumonia",
            "Other Nonmalignant Systemic Disease",
            "Behcet's Disease",
            "Calcium Channel Blockers",
            "Gastritis",
            "Chlamydia",
            "Treponema pallidum",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Ischemic Heart Disease",
            "Hypothyroidism",
            "Pregnancy in Patient or Partner",
            "Hypercalcemia",
            "Myocardial Infarction",
            "Wagr Syndrome",
            "HIV / AIDS",
            "Pneumocystis Pneumonia",
            "Li-Fraumeni Syndrome",
            "Common Variable Immunodeficiency",
            "Herpes Zoster",
            "Tyrosinemia",
            "Gout",
            "Organ transplant (site)",
            "Inflammatory Bowel Disease",
            "Basal Cell Carcinoma",
            "Down Syndrome",
            "GERD",
            "Pancreatitis",
            "Dyslipidemia",
            "Hepatitis C Infection",
            "Hereditary Non-polyposis Colon Cancer",
            "Liver Toxicity (Non-Infectious)",
            "Thyroid Disease, Non-Cancer",
            "Bacteroides fragilis",
            "Cytomegalovirus (CMV)",
            "Epstein-Barr Virus",
            "Cryptococcal Meningitis",
            "Hemorrhagic Cystitis",
            "Myasthenia Gravis",
            "Hyperglycemia",
            "Tuberculosis",
            "Fanconi Anemia",
            "Familial Adenomatous Polyposis",
            "Abnormal Glucose Level",
            "Deep Vein Thrombosis / Thromboembolism",
            "Rheumatologic Disease",
            "Celiac Disease",
            "Heart Disease",
            "Staphylococcus aureus",
            "Gorlin Syndrome",
        },
    )
    def comorbidity(self, value):
        self._set_property("comorbidity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Histology", "Not Reported", "Pathology", "Radiology"}
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

    @psqlgraph.pg_property(int, type(None))
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
            "Linagliptin",
            "Thiazolidinedione",
            "Biguanide",
            "Diet",
            "Injected Insulin",
            "Alpha-Glucosidase Inhibitor",
            "Insulin",
            "Not Reported",
            "Other",
            "Oral Hypoglycemic",
            "Sulfonylurea",
        },
    )
    def diabetes_treatment_type(self, value):
        self._set_property("diabetes_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Non-CR/Non-PD-Non-CR/Non-PD",
            "SPD-Surgical Progression",
            "AJ-Adjuvant Therapy",
            "PD-Progressive Disease",
            "SD-Stable Disease",
            "NR-No Response",
            "IPD-Immunoprogression",
            "PSR-Pseudoresponse",
            "RPD-Radiographic Progressive Disease",
            "Unknown",
            "RD-Responsive Disease",
            "RP-Response",
            "MX-Mixed Response",
            "PA-Palliative Therapy",
            "NPB-No Palliative Benefit",
            "PB-Palliative Benefit",
            "CR-Complete Response",
            "CPD-Clinical Progression",
            "TF-Tumor Free",
            "DU-Disease Unchanged",
            "PDM-Persistent Distant Metastasis",
            "PR-Partial Response",
            "WT-With Tumor",
            "IMR-Immunoresponse",
            "BED-Biochemical Evidence of Disease",
            "PLD-Persistent Locoregional Disease",
            "MR-Minimal/Marginal response",
            "TE-Too Early",
            "sCR-Stringent Complete Response",
            "CRU-Complete Response Unconfirmed",
            "VGPR-Very Good Partial Response",
            "Not Reported",
            "PPD-Pseudoprogression",
        },
    )
    def disease_response(self, value):
        self._set_property("disease_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def dlco_ref_predictive_percent(self, value):
        self._set_property("dlco_ref_predictive_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "2", "0", "3", "5", "Not Reported", "1", "4"})
    def ecog_performance_status(self, value):
        self._set_property("ecog_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Histologic Confirmation", "Convincing Image Source"})
    def evidence_of_progression_type(self, value):
        self._set_property("evidence_of_progression_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Convincing Image Source",
            "Positive Biomarker(s)",
            "Histologic Confirmation",
            "Biopsy with Histologic Confirmation",
            "Physical Examination",
        },
    )
    def evidence_of_recurrence_type(self, value):
        self._set_property("evidence_of_recurrence_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Red & Violet",
            "Gray",
            "Hazel",
            "Brown",
            "Blue",
            "Amber",
            "Not Reported",
            "Green",
            "Other",
        },
    )
    def eye_color(self, value):
        self._set_property("eye_color", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def fev1_ref_post_bronch_percent(self, value):
        self._set_property("fev1_ref_post_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def fev1_ref_pre_bronch_percent(self, value):
        self._set_property("fev1_ref_pre_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def fev1_fvc_pre_bronch_percent(self, value):
        self._set_property("fev1_fvc_pre_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def fev1_fvc_post_bronch_percent(self, value):
        self._set_property("fev1_fvc_post_bronch_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Event",
            "None",
            "Death",
            "Progression",
            "Censored",
            "Second Malignant Neoplasm",
            "Not Reported",
            "Other",
            "Death without Remission",
            "Relapse",
            "Induction Death",
            "Induction Failure",
        },
    )
    def first_event(self, value):
        self._set_property("first_event", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def haart_treatment_indicator(self, value):
        self._set_property("haart_treatment_indicator", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def height(self, value):
        self._set_property("height", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def hepatitis_sustained_virological_response(self, value):
        self._set_property("hepatitis_sustained_virological_response", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def history_of_tumor(self, value):
        self._set_property("history_of_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Phenochromocytoma or Paraganglioma",
            "Colorectal Cancer",
            "Lower Grade Glioma",
        },
    )
    def history_of_tumor_type(self, value):
        self._set_property("history_of_tumor_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def hiv_viral_load(self, value):
        self._set_property("hiv_viral_load", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Not Reported", "Progestin", "Progestin and Estrogen"}
    )
    def hormonal_contraceptive_type(self, value):
        self._set_property("hormonal_contraceptive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={"Former User", "Current User", "Unknown", "Never Used", "Not Reported"},
    )
    def hormonal_contraceptive_use(self, value):
        self._set_property("hormonal_contraceptive_use", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Progesterone and Estrogen",
            "Estrogen only",
            "Not Reported",
            "Progesterone only",
        },
    )
    def hormone_replacement_therapy_type(self, value):
        self._set_property("hormone_replacement_therapy_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "59",
            "39",
            "51",
            "73",
            "58",
            "33",
            "66",
            "16",
            "Other",
            "63",
            "52",
            "Unknown",
            "56",
            "53",
            "68",
            "31",
            "35",
            "26",
            "18",
            "70",
            "Not Reported",
            "82",
            "45",
        },
    )
    def hpv_positive_type(self, value):
        self._set_property("hpv_positive_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Microscopic Parametrium",
            "Macroscopic Parametrium",
            "Unknown",
            "Vagina",
            "Not Reported",
            "None",
            "Bladder",
        },
    )
    def hysterectomy_margins_involved(self, value):
        self._set_property("hysterectomy_margins_involved", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Radical Hysterectomy",
            "Unknown",
            "Not performed",
            "Not Reported",
            "Hysterectomy, NOS",
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
            "Kidney Involvement",
            "Lung Involvement",
            "Normal",
            "Retroperitoneal Lymph Node Involvement",
            "Not Reported",
            "Liver Involvement",
            "Carcinomatosis",
        },
    )
    def imaging_findings(self, value):
        self._set_property("imaging_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Indeterminate",
            "Unknown",
            "Not Reported",
            "Negative",
            "Positive",
            "Not Performed",
        },
    )
    def imaging_result(self, value):
        self._set_property("imaging_result", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def imaging_suv(self, value):
        self._set_property("imaging_suv", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def imaging_suv_max(self, value):
        self._set_property("imaging_suv_max", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"CT Scan", "99mTc Bone Scintigraphy", "MRI", "PET"})
    def imaging_type(self, value):
        self._set_property("imaging_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Methotrexate",
            "Unknown",
            "None",
            "Anti-TNF Therapy",
            "Cyclophosphamide",
            "Not Reported",
            "Other",
            "Azathioprine",
        },
    )
    def immunosuppressive_treatment_type(self, value):
        self._set_property("immunosuppressive_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "100",
            "90",
            "50",
            "Unknown",
            "20",
            "70",
            "60",
            "Not Reported",
            "40",
            "80",
            "30",
            "0",
            "10",
        },
    )
    def karnofsky_performance_status(self, value):
        self._set_property("karnofsky_performance_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Postmenopausal",
            "Perimenopausal",
            "Not Reported",
            "Premenopausal",
        },
    )
    def menopause_status(self, value):
        self._set_property("menopause_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
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
            "Stillbirth",
            "Spontaneous Abortion",
            "Miscarriage",
            "Ectopic Pregnancy",
            "Not Reported",
            "Live Birth",
            "Induced Abortion",
        },
    )
    def pregnancy_outcome(self, value):
        self._set_property("pregnancy_outcome", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Colonoscopy", "Not Reported", "Endoscopy"})
    def procedures_performed(self, value):
        self._set_property("procedures_performed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def progression_or_recurrence(self, value):
        self._set_property("progression_or_recurrence", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Soft palate, NOS",
            "Mandible",
            "Duodenum",
            "Overlapping lesion of connective, subcutaneous and other soft tissues",
            "Anterior mediastinum",
            "Cerebrum",
            "Brain stem",
            "Gallbladder",
            "Orbit, NOS",
            "Tail of pancreas",
            "Cheek mucosa",
            "Prostate gland",
            "Small intestine, NOS",
            "Posterior wall of oropharynx",
            "Skin of scalp and neck",
            "Overlapping lesion of bones, joints and articular cartilage",
            "Upper respiratory tract, NOS",
            "Pylorus",
            "Epididymis",
            "Kidney, NOS",
            "Lymph nodes of inguinal region or leg",
            "Fundus uteri",
            "Endocrine gland, NOS",
            "Uterus, NOS",
            "Myometrium",
            "Testis, NOS",
            "Mediastinum, NOS",
            "Hepatic flexure of colon",
            "Pleura, NOS",
            "Aortic body and other paraganglia",
            "Dorsal surface of tongue, NOS",
            "Overlapping lesion of accessory sinuses",
            "Lower gum",
            "Lingual tonsil",
            "Peripheral nerves and autonomic nervous system of head, face, and neck",
            "Mouth, NOS",
            "Upper lobe, lung",
            "Peritoneum, NOS",
            "Dome of bladder",
            "Tonsil, NOS",
            "Broad ligament",
            "Overlapping lesion of colon",
            "Lower-inner quadrant of breast",
            "Hard palate",
            "Connective, subcutaneous and other soft tissues of abdomen",
            "Connective, subcutaneous and other soft tissues of thorax",
            "Overlapping lesion of lip",
            "Descending colon",
            "Lower-outer quadrant of breast",
            "Not Reported",
            "Rib, sternum, clavicle and associated joints",
            "Connective, subcutaneous and other soft tissues of upper limb and shoulder",
            "Tongue, NOS",
            "External ear",
            "Overlapping lesion of pancreas",
            "Other ill-defined sites",
            "Placenta",
            "Thoracic esophagus",
            "Pituitary gland",
            "Overlapping lesion of esophagus",
            "Lesser curvature of stomach, NOS",
            "Overlapping lesion of breast",
            "Ovary",
            "Postcricoid region",
            "Posterior wall of hypopharynx",
            "Waldeyer ring",
            "Overlapping lesion of urinary organs",
            "Anterior floor of mouth",
            "Pyriform sinus",
            "Urethra",
            "Fallopian tube",
            "Pelvis, NOS",
            "Nasopharynx, NOS",
            "Lower lobe, lung",
            "Male genital organs, NOS",
            "Breast, NOS",
            "External lower lip",
            "Endometrium",
            "Reticuloendothelial system, NOS",
            "Overlapping lesion of female genital organs",
            "Vestibule of mouth",
            "Parathyroid gland",
            "Peripheral nerves and autonomic nervous system of trunk, NOS",
            "Connective, subcutaneous and other soft tissues of trunk, NOS",
            "Overlapping lesion of major salivary glands",
            "Bone marrow",
            "Tonsillar pillar",
            "Peripheral nerves and autonomic nervous system of upper limb and shoulder",
            "Overlapping lesions of oropharynx",
            "Cranial nerve, NOS",
            "Middle third of esophagus",
            "Other specified parts of female genital organs",
            "Skin, NOS",
            "Lip, NOS",
            "Tonsillar fossa",
            "Rectosigmoid junction",
            "Overlapping lesion of respiratory system and intrathoracic organs",
            "Overlapping lesion of tongue",
            "Middle ear",
            "Liver",
            "Posterior wall of nasopharynx",
            "Lymph nodes of axilla or arm",
            "Supraglottis",
            "Unknown",
            "Lower limb, NOS",
            "Penis, NOS",
            "Pineal gland",
            "Frontal lobe",
            "Vertebral column",
            "Body of penis",
            "Undescended testis",
            "Acoustic nerve",
            "Mucosa of lip, NOS",
            "Middle lobe, lung",
            "Bones of skull and face and associated joints",
            "Posterior mediastinum",
            "Ciliary body",
            "Blood",
            "Overlapping lesion of vulva",
            "Short bones of lower limb and associated joints",
            "Overlapping lesion of digestive system",
            "Intrahepatic bile duct",
            "Overlapping lesion of eye and adnexa",
            "Vulva, NOS",
            "Cecum",
            "Ventricle, NOS",
            "Glottis",
            "Base of tongue, NOS",
            "Choroid",
            "Peripheral nerves and autonomic nervous system of pelvis",
            "Lung, NOS",
            "Overlapping lesion of bladder",
            "Ethmoid sinus",
            "Islets of Langerhans",
            "Heart",
            "Subglottis",
            "Female genital tract, NOS",
            "Spermatic cord",
            "Lower third of esophagus",
            "Endocervix",
            "Mucosa of lower lip",
            "Renal pelvis",
            "Labium majus",
            "Skin of lower limb and hip",
            "Upper limb, NOS",
            "Pelvic lymph nodes",
            "External lip, NOS",
            "Retromolar area",
            "Branchial cleft",
            "Cloacogenic zone",
            "Head, face or neck, NOS",
            "Overlapping lesion of larynx",
            "Spleen",
            "Overlapping lesion of biliary tract",
            "Main bronchus",
            "Nipple",
            "Parotid gland",
            "Glans penis",
            "Lateral wall of oropharynx",
            "Peripheral nerves and autonomic nervous system of lower limb and hip",
            "Thyroid gland",
            "Splenic flexure of colon",
            "Isthmus uteri",
            "Overlapping lesion of peripheral nerves and autonomic nervous system",
            "Greater curvature of stomach, NOS",
            "Stomach, NOS",
            "Cauda equina",
            "Medulla of adrenal gland",
            "Upper-inner quadrant of breast",
            "Bone, NOS",
            "Ileum",
            "Temporal lobe",
            "Skin of other and unspecified parts of face",
            "Skin of lip, NOS",
            "Cervix uteri",
            "Pelvic bones, sacrum, coccyx and associated joints",
            "Biliary tract, NOS",
            "Superior wall of nasopharynx",
            "Connective, subcutaneous and other soft tissues of lower limb and hip",
            "Exocervix",
            "Gastrointestinal tract, NOS",
            "Brain, NOS",
            "Upper-outer quadrant of breast",
            "Overlapping lesion of lip, oral cavity and pharynx",
            "Connective, subcutaneous and other soft tissues, NOS",
            "Eye, NOS",
            "Lateral wall of nasopharynx",
            "Anterior 2/3 of tongue, NOS",
            "Descended testis",
            "Bladder neck",
            "Posterior wall of bladder",
            "Eyelid",
            "Hematopoietic system, NOS",
            "Occipital lobe",
            "Anterior wall of nasopharynx",
            "Prepuce",
            "Hypopharynx, NOS",
            "Palate, NOS",
            "Lymph nodes of multiple regions",
            "Pancreatic duct",
            "Appendix",
            "Sublingual gland",
            "Olfactory nerve",
            "Overlapping lesion of male genital organs",
            "Cardia, NOS",
            "Sphenoid sinus",
            "Nervous system, NOS",
            "Cerebral meninges",
            "Spinal cord",
            "Thorax, NOS",
            "Abdominal esophagus",
            "Upper gum",
            "Overlapping lesion of ill-defined sites",
            "Anus, NOS",
            "Trachea",
            "Vagina, NOS",
            "Overlapping lesion of palate",
            "Other specified parts of pancreas",
            "Paraurethral gland",
            "Lacrimal gland",
            "Submandibular gland",
            "Unknown primary site",
            "Meninges, NOS",
            "Long bones of upper limb, scapula and associated joints",
            "Adrenal gland, NOS",
            "Laryngeal cartilage",
            "Long bones of lower limb and associated joints",
            "Anterior surface of epiglottis",
            "Extrahepatic bile duct",
            "Overlapping lesion of cervix uteri",
            "Overlapping lesion of nasopharynx",
            "Sigmoid colon",
            "Connective, subcutaneous and other soft tissues of pelvis",
            "Craniopharyngeal duct",
            "Round ligament",
            "Meckel diverticulum",
            "Skin of trunk",
            "Other specified parts of male genital organs",
            "Autonomic nervous system, NOS",
            "Ventral surface of tongue, NOS",
            "Cortex of adrenal gland",
            "Frontal sinus",
            "Overlapping lesion of tonsil",
            "Body of pancreas",
            "Overlapping lesion of hypopharynx",
            "Ampulla of Vater",
            "Overlapping lesion of rectum, anus and anal canal",
            "Trigone of bladder",
            "Vallecula",
            "Overlapping lesion of skin",
            "Anterior wall of bladder",
            "Bone of limb, NOS",
            "Uvula",
            "Axillary tail of breast",
            "Oropharynx, NOS",
            "Retroperitoneum",
            "Commissure of lip",
            "Parametrium",
            "Anal canal",
            "Floor of mouth, NOS",
            "Labium minus",
            "Peripheral nerves and autonomic nervous system of thorax",
            "Head of pancreas",
            "Urachus",
            "Uterine adnexa",
            "Abdomen, NOS",
            "Hypopharyngeal aspect of aryepiglottic fold",
            "Pancreas, NOS",
            "Skin of upper limb and shoulder",
            "Spinal meninges",
            "Parietal lobe",
            "Corpus uteri",
            "Ill-defined sites within respiratory system",
            "Transverse colon",
            "Overlapping lesion of small intestine",
            "Optic nerve",
            "Overlapping lesion of floor of mouth",
            "Bladder, NOS",
            "Connective, subcutaneous and other soft tissues of head, face, and neck",
            "Short bones of upper limb and associated joints",
            "Carotid body",
            "Larynx, NOS",
            "Nasal cavity",
            "Mucosa of upper lip",
            "Overlapping lesion of brain",
            "Overlapping lesion of endocrine glands and related structures",
            "Lateral wall of bladder",
            "Colon, NOS",
            "Pharynx, NOS",
            "Overlapping lesion of brain and central nervous system",
            "Gum, NOS",
            "Overlapping lesion of corpus uteri",
            "Lateral floor of mouth",
            "Lymph node, NOS",
            "Overlapping lesion of stomach",
            "Thymus",
            "Conjunctiva",
            "Cervical esophagus",
            "Body of stomach",
            "Accessory sinus, NOS",
            "Ascending colon",
            "Intra-abdominal lymph nodes",
            "Central portion of breast",
            "Upper third of esophagus",
            "Retina",
            "Border of tongue",
            "Overlapping lesion of retroperitoneum and peritoneum",
            "External upper lip",
            "Overlapping lesion of bones, joints and articular cartilage of limbs",
            "Maxillary sinus",
            "Specified parts of peritoneum",
            "Ureteric orifice",
            "Peripheral nerves and autonomic nervous system of abdomen",
            "Fundus of stomach",
            "Rectum, NOS",
            "Esophagus, NOS",
            "Ureter",
            "Gastric antrum",
            "Overlapping lesion of other and unspecified parts of mouth",
            "Lymph nodes of head, face and neck",
            "Clitoris",
            "Cerebellum, NOS",
            "Overlapping lesion of penis",
            "Scrotum, NOS",
            "Jejunum",
            "Major salivary gland, NOS",
            "Intestinal tract, NOS",
            "Intrathoracic lymph nodes",
            "Cornea, NOS",
            "Urinary system, NOS",
            "Overlapping lesion of lung",
            "Overlapping lesion of heart, mediastinum and pleura",
        },
    )
    def progression_or_recurrence_anatomic_site(self, value):
        self._set_property("progression_or_recurrence_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Distant",
            "Local",
            "Unknown",
            "Locoregional",
            "Not Reported",
            "Biochemical",
            "Regional",
        },
    )
    def progression_or_recurrence_type(self, value):
        self._set_property("progression_or_recurrence_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def recist_targeted_regions_number(self, value):
        self._set_property("recist_targeted_regions_number", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def recist_targeted_regions_sum(self, value):
        self._set_property("recist_targeted_regions_sum", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Surgically Treated",
            "Unknown",
            "H2 Blockers",
            "Not Applicable",
            "Medically Treated",
            "No Treatment",
            "Not Reported",
            "Proton Pump Inhibitors",
            "Antacids",
        },
    )
    def reflux_treatment_type(self, value):
        self._set_property("reflux_treatment_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Escherichia coli",
            "Allergy, Processed Foods",
            "Hypospadias",
            "Autoimmune Atrophic Chronic Gastritis",
            "Recurrent Pyogenic Cholangitis",
            "Chloroma",
            "Androgen Excess",
            "Tobacco, Smoking",
            "Chronic Hepatitis",
            "Sensory Changes",
            "Rheumatoid Arthritis",
            "Nonalcoholic Fatty Liver Disease",
            "BAP1 Tumor Predisposition Syndrome",
            "Chronic Pancreatitis",
            "Endosalpingiosis",
            "Allergy, Bee",
            "Diabetes, NOS",
            "Obesity",
            "Hereditary Leiomyomatosis and Renal Cell Carcinoma",
            "Allergy, Fruit",
            "Asthma",
            "HIV",
            "Denys-Drash Syndrome",
            "Human Herpesvirus-6 (HHV-6)",
            "Undescended Testis",
            "Diverticulitis",
            "Eczema",
            "Metabolic Syndrome",
            "Lymphamatoid Papulosis",
            "Sjogren's Syndrome",
            "Fibrosis",
            "Human Papillomavirus Infection",
            "Allergy, Nuts",
            "Hepatitis B Infection",
            "Turcot Syndrome",
            "Motor / Movement Change",
            "Allergy, Wasp",
            "Colonization, Bacterial",
            "Not Reported",
            "Dermatomyosis",
            "Colon Polyps",
            "Chronic Systemic Steroid Use",
            "Adenomyosis",
            "Tubulointerstitial Disease",
            "Lynch Syndrome",
            "Nodular Prostatic Hyperplasia",
            "Serous tubal intraepithelial carcinoma (STIC)",
            "Allergy, Meat",
            "Primary Sclerosing Cholangitis",
            "Tobacco, NOS",
            "Mycobacterium avium Complex",
            "Alcoholic Liver Disease",
            "Anemia",
            "Benign Prostatic Hyperplasia",
            "Allergy, Food, NOS",
            "Sialadenitis",
            "EBV Lymphoproliferation",
            "Syphilis",
            "Human Herpesvirus-8 (HHV-8)",
            "Lymphocytic Thyroiditis",
            "Cowden Syndrome",
            "High Grade Dysplasia",
            "Low Grade Dysplasia",
            "Hodgkin Lymphoma",
            "Gastric Polyp(s)",
            "Beckwith-Wiedemann",
            "Cyst(s)",
            "Hemihypertrophy",
            "None",
            "Allergy, Mold or Dust",
            "Altered Mental Status",
            "Skin Rash",
            "Ataxia-telangiectasia",
            "Hashimoto's Thyroiditis",
            "Cholelithiasis",
            "Vision Changes",
            "Diabetes, Type II",
            "Rubinstein-Taybi Syndrome",
            "Iron Overload",
            "Cancer",
            "Nonalcoholic Steatohepatitis",
            "Reflux Disease",
            "H. pylori Infection",
            "Polycystic Ovarian Syndrome (PCOS)",
            "Shingles",
            "Headache",
            "Neurocystericerosis",
            "Hereditary Breast Cancer",
            "Adenosis (Atypical Adenomatous Hyperplasia)",
            "Oral Contraceptives",
            "Endometriosis",
            "Sarcoidosis",
            "Allergy, Cat",
            "Hereditary Ovarian Cancer",
            "Parasitic Disease of Biliary Tract",
            "Hepatitis A Infection",
            "Allergy, Eggs",
            "Unknown",
            "Rubella",
            "Helicobacter Pylori-Associated Gastritis",
            "Hemochromatosis",
            "Hereditary Papillary Renal Cell Carcinoma",
            "Malaria",
            "Estrogen Excess",
            "Steatosis",
            "Lymphocytic Meningitis",
            "Hereditary Renal Cell Carcinoma",
            "High-grade Prostatic Intraepithelial Neoplasia (PIN)",
            "Varicella Zoster Virus",
            "Chronic Kidney Disease",
            "Inherited Genetic Syndrome, NOS",
            "Seizure",
            "Birt-Hogg-Dube Syndrome",
            "Barrett's Esophagus",
            "Glomerular Disease",
            "Inflammation",
            "Colonization, Fungal",
            "Behcet's Disease",
            "Alpha-1 Antitrypsin Deficiency",
            "Gastritis",
            "Chlamydia",
            "Treponema pallidum",
            "BRCA Family History",
            "Autoimmune Lymphoproliferative Syndrome (ALPS)",
            "Hereditary Hemorrhagic Telangiectasia",
            "Allergy, Dairy or Lactose",
            "Epithelial Dysplasia",
            "Hereditary Prostate Cancer",
            "Diet",
            "Squamous Metaplasia",
            "Tattoo",
            "Hepatic Encephalopathy",
            "Wagr Syndrome",
            "Hay Fever",
            "Pneumocystis Pneumonia",
            "Li-Fraumeni Syndrome",
            "Hematologic Disorder, NOS",
            "Epithelial Hyperplasia",
            "Allergy, Seafood",
            "Inflammation, Hyperkeratosis",
            "Allergy, Animal, NOS",
            "Cortisol Excess",
            "Down Syndrome",
            "Mineralcorticoids Excess",
            "Common variable immune deficiency (CVID)",
            "Cirrhosis",
            "Thyroid Nodular Hyperplasia",
            "Tobacco, Smokeless",
            "Hereditary Kidney Oncocytoma",
            "Myelodysplastic Syndrome",
            "Pancreatitis",
            "Hepatitis C Infection",
            "Gilbert's Syndrome",
            "Succinate Dehydrogenase-Deficient Renal Cell Carcinoma",
            "Bacteroides fragilis",
            "Tuberous Sclerosis",
            "Allergy, Ant",
            "Cytomegalovirus (CMV)",
            "Epstein-Barr Virus",
            "Intestinal Metaplasia",
            "Diabetes, Type I",
            "Cryptococcal Meningitis",
            "Hepatitis, NOS",
            "Myasthenia Gravis",
            "Tumor-associated Lymphoid Proliferation",
            "Tuberculosis",
            "Fanconi Anemia",
            "Familial Adenomatous Polyposis",
            "Abnormal Glucose Level",
            "Alcohol Consumption",
            "Allergy, Dog",
            "Herpes Zoster",
            "Vascular Disease",
            "Von Hippel-Lindau Syndrome",
            "Staphylococcus aureus",
            "Gorlin Syndrome",
        },
    )
    def risk_factor(self, value):
        self._set_property("risk_factor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def risk_factors(self, value):
        self._set_property("risk_factors", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Both Clinical and Biochemical Assessments",
            "Not Reported",
            "Biochemical Assessment",
            "Clinical Assessment",
        },
    )
    def risk_factor_method_of_diagnosis(self, value):
        self._set_property("risk_factor_method_of_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def risk_factor_treatment(self, value):
        self._set_property("risk_factor_treatment", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"PSMA", "Choline", "Axumin", "Acetate", "Sodium Fluoride"})
    def scan_tracer_used(self, value):
        self._set_property("scan_tracer_used", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Childhood",
            "Initial Diagnosis",
            "Post Adjuvant Therapy",
            "Preoperative",
            "Prior to Treatment",
            "Adulthood",
            "Other",
            "Post Secondary Therapy",
            "Follow-up",
            "Adjuvant Therapy",
            "Adolescence",
            "Recurrence/Progression",
            "Post Hormone Therapy",
            "Prior to Diagnosis",
            "Not Reported",
            "Last Contact",
            "Postoperative",
        },
    )
    def timepoint_category(self, value):
        self._set_property("timepoint_category", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def undescended_testis_corrected(self, value):
        self._set_property("undescended_testis_corrected", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def undescended_testis_corrected_age(self, value):
        self._set_property("undescended_testis_corrected_age", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Right", "Bilateral", "Not Reported", "Left"})
    def undescended_testis_corrected_laterality(self, value):
        self._set_property("undescended_testis_corrected_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Spontaneous Descent",
            "Hormones",
            "Not Reported",
            "Testis Removed",
            "Orchiopexy",
        },
    )
    def undescended_testis_corrected_method(self, value):
        self._set_property("undescended_testis_corrected_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def undescended_testis_history(self, value):
        self._set_property("undescended_testis_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Right", "Bilateral", "Not Reported", "Left"})
    def undescended_testis_history_laterality(self, value):
        self._set_property("undescended_testis_history_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "HBV Genotype",
            "Unknown",
            "Hepatitis B Surface Antigen",
            "Hepatitis C Antibody",
            "HBV DNA",
            "HBV Core Antibody",
            "HBV Surface Antibody",
            "HCV Genotype",
            "Hepatitis C Virus RNA",
            "Not Reported",
        },
    )
    def viral_hepatitis_serologies(self, value):
        self._set_property("viral_hepatitis_serologies", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def weight(self, value):
        self._set_property("weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def year_of_follow_up(self, value):
        self._set_property("year_of_follow_up", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FollowUp)
datetime_hooks.cls_inject_updated_datetime_hook(FollowUp)
