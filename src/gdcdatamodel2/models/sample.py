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
        "links": [
            {
                "name": "cases",
                "backref": "samples",
                "label": "derived_from",
                "target_type": "case",
                "multiplicity": "many_to_one",
                "required": True,
            },
            {
                "name": "tissue_source_sites",
                "backref": "samples",
                "label": "processed_at",
                "target_type": "tissue_source_site",
                "multiplicity": "one_to_one",
                "required": False,
            },
            {
                "name": "diagnoses",
                "backref": "samples",
                "label": "related_to",
                "target_type": "diagnosis",
                "multiplicity": "many_to_one",
                "required": False,
            },
            {
                "name": "parent_samples",
                "backref": "child_samples",
                "label": "derived_from",
                "target_type": "sample",
                "multiplicity": "many_to_one",
                "required": False,
            },
        ],
        "properties": {
            "type": {"type": "string"},
            "id": {
                "common": {
                    "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                    "termDef": {
                        "term": "Universally Unique Identifier",
                        "source": "NCIt",
                        "cde_id": "C54100",
                        "cde_version": None,
                        "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                    },
                },
                "type": "string",
                "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                "systemAlias": "node_id",
            },
            "submitter_id": {
                "description": "A project-specific identifier for a node. This property is the calling card/nickname/alias for a unit of submission. It can be used in place of the uuid for identifying or recalling a node.",
                "type": "string",
            },
            "batch_id": {
                "description": "GDC submission batch indicator. It is unique within the context of a project.",
                "type": "integer",
            },
            "state": {
                "common": {
                    "description": "The current state of the object.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "default": "validated",
                "downloadable": [
                    "uploaded",
                    "md5summed",
                    "validating",
                    "validated",
                    "error",
                    "invalid",
                    "released",
                ],
                "public": ["live"],
                "oneOf": [
                    {
                        "enum": [
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
                        ]
                    },
                    {"enum": ["validated", "submitted", "released"]},
                ],
            },
            "project_id": {
                "common": {
                    "description": "Unique ID for any specific defined piece of work that is undertaken or attempted to meet a single requirement.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "type": "string",
            },
            "created_datetime": {
                "common": {
                    "description": "A combination of date and time of day in the form [-]CCYY-MM-DDThh:mm:ss[Z|(+|-)hh:mm]",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "oneOf": [{"type": "string", "format": "date-time"}, {"type": "null"}],
            },
            "updated_datetime": {
                "common": {
                    "description": "A combination of date and time of day in the form [-]CCYY-MM-DDThh:mm:ss[Z|(+|-)hh:mm]",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "oneOf": [{"type": "string", "format": "date-time"}, {"type": "null"}],
            },
            "biospecimen_anatomic_site": {
                "description": "Text term that represents the name of the primary disease site of the submitted tumor sample.",
                "termDef": {
                    "term": "Submitted Tumor Sample Primary Anatomic Site",
                    "source": "caDSR",
                    "cde_id": 4742851,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=4742851&version=1.0",
                },
                "enum": [
                    "Abdomen",
                    "Abdominal Wall",
                    "Acetabulum",
                    "Adenoid",
                    "Adipose",
                    "Adrenal",
                    "Alveolar Ridge",
                    "Amniotic Fluid",
                    "Ampulla Of Vater",
                    "Anal Sphincter",
                    "Ankle",
                    "Anorectum",
                    "Antecubital Fossa",
                    "Antrum",
                    "Anus",
                    "Aorta",
                    "Aortic Body",
                    "Appendix",
                    "Aqueous Fluid",
                    "Arm",
                    "Artery",
                    "Ascending Colon",
                    "Ascending Colon Hepatic Flexure",
                    "Auditory Canal",
                    "Autonomic Nervous System",
                    "Axilla",
                    "Back",
                    "Bile Duct",
                    "Bladder",
                    "Blood",
                    "Blood Vessel",
                    "Bone",
                    "Bone Marrow",
                    "Bowel",
                    "Brain",
                    "Brain Stem",
                    "Breast",
                    "Broad Ligament",
                    "Bronchiole",
                    "Bronchus",
                    "Brow",
                    "Buccal Cavity",
                    "Buccal Mucosa",
                    "Buttock",
                    "Calf",
                    "Capillary",
                    "Cardia",
                    "Carina",
                    "Carotid Artery",
                    "Carotid Body",
                    "Cartilage",
                    "Cecum",
                    "Cell-Line",
                    "Central Nervous System",
                    "Cerebellum",
                    "Cerebral Cortex",
                    "Cerebrospinal Fluid",
                    "Cerebrum",
                    "Cervical Spine",
                    "Cervix",
                    "Chest",
                    "Chest Wall",
                    "Chin",
                    "Clavicle",
                    "Clitoris",
                    "Colon",
                    "Colon - Mucosa Only",
                    "Common Duct",
                    "Conjunctiva",
                    "Connective Tissue",
                    "Dermal",
                    "Descending Colon",
                    "Diaphragm",
                    "Duodenum",
                    "Ear",
                    "Ear Canal",
                    "Ear, Pinna (External)",
                    "Effusion",
                    "Elbow",
                    "Endocrine Gland",
                    "Epididymis",
                    "Epidural Space",
                    "Esophageal; Distal",
                    "Esophageal; Mid",
                    "Esophageal; Proximal",
                    "Esophagogastric Junction",
                    "Esophagus",
                    "Esophagus - Mucosa Only",
                    "Eye",
                    "Fallopian Tube",
                    "Femoral Artery",
                    "Femoral Vein",
                    "Femur",
                    "Fibroblasts",
                    "Fibula",
                    "Finger",
                    "Floor Of Mouth",
                    "Fluid",
                    "Foot",
                    "Forearm",
                    "Forehead",
                    "Foreskin",
                    "Frontal Cortex",
                    "Frontal Lobe",
                    "Fundus Of Stomach",
                    "Gallbladder",
                    "Ganglia",
                    "Gastroesophageal Junction",
                    "Gastrointestinal Tract",
                    "Glottis",
                    "Groin",
                    "Gum",
                    "Hand",
                    "Hard Palate",
                    "Head - Face Or Neck, Nos",
                    "Head & Neck",
                    "Heart",
                    "Hepatic",
                    "Hepatic Duct",
                    "Hepatic Flexure",
                    "Hepatic Vein",
                    "Hip",
                    "Hippocampus",
                    "Humerus",
                    "Hypopharynx",
                    "Ileum",
                    "Ilium",
                    "Index Finger",
                    "Ischium",
                    "Islet Cells",
                    "Jaw",
                    "Jejunum",
                    "Joint",
                    "Kidney",
                    "Knee",
                    "Lacrimal Gland",
                    "Large Bowel",
                    "Laryngopharynx",
                    "Larynx",
                    "Leg",
                    "Leptomeninges",
                    "Ligament",
                    "Lip",
                    "Liver",
                    "Lumbar Spine",
                    "Lung",
                    "Lymph Node",
                    "Lymph Node(s) Axilla",
                    "Lymph Node(s) Cervical",
                    "Lymph Node(s) Distant",
                    "Lymph Node(s) Epitrochlear",
                    "Lymph Node(s) Femoral",
                    "Lymph Node(s) Hilar",
                    "Lymph Node(s) Iliac-Common",
                    "Lymph Node(s) Iliac-External",
                    "Lymph Node(s) Inguinal",
                    "Lymph Node(s) Internal Mammary",
                    "Lymph Node(s) Mammary",
                    "Lymph Node(s) Mesenteric",
                    "Lymph Node(s) Occipital",
                    "Lymph Node(s) Paraaortic",
                    "Lymph Node(s) Parotid",
                    "Lymph Node(s) Pelvic",
                    "Lymph Node(s) Popliteal",
                    "Lymph Node(s) Regional",
                    "Lymph Node(s) Retroperitoneal",
                    "Lymph Node(s) Scalene",
                    "Lymph Node(s) Splenic",
                    "Lymph Node(s) Subclavicular",
                    "Lymph Node(s) Submandibular",
                    "Lymph Node(s) Supraclavicular",
                    "Lymph Nodes(s) Mediastinal",
                    "Mandible",
                    "Maxilla",
                    "Mediastinal Soft Tissue",
                    "Mediastinum",
                    "Mesentery",
                    "Mesothelium",
                    "Middle Finger",
                    "Mitochondria",
                    "Muscle",
                    "Nails",
                    "Nasal Cavity",
                    "Nasal Soft Tissue",
                    "Nasopharynx",
                    "Neck",
                    "Nerve",
                    "Nerve(s) Cranial",
                    "Not Allowed To Collect",
                    "Occipital Cortex",
                    "Ocular Orbits",
                    "Omentum",
                    "Oral Cavity",
                    "Oral Cavity - Mucosa Only",
                    "Oropharynx",
                    "Other",
                    "Ovary",
                    "Palate",
                    "Pancreas",
                    "Paranasal Sinuses",
                    "Paraspinal Ganglion",
                    "Parathyroid",
                    "Parotid Gland",
                    "Patella",
                    "Pelvis",
                    "Penis",
                    "Pericardium",
                    "Periorbital Soft Tissue",
                    "Peritoneal Cavity",
                    "Peritoneum",
                    "Pharynx",
                    "Pineal",
                    "Pineal Gland",
                    "Pituitary Gland",
                    "Placenta",
                    "Pleura",
                    "Popliteal Fossa",
                    "Prostate",
                    "Pylorus",
                    "Rectosigmoid Junction",
                    "Rectum",
                    "Retina",
                    "Retro-Orbital Region",
                    "Retroperitoneum",
                    "Rib",
                    "Ring Finger",
                    "Round Ligament",
                    "Sacrum",
                    "Salivary Gland",
                    "Scalp",
                    "Scapula",
                    "Sciatic Nerve",
                    "Scrotum",
                    "Seminal Vesicle",
                    "Shoulder",
                    "Sigmoid Colon",
                    "Sinus",
                    "Sinus(es), Maxillary",
                    "Skeletal Muscle",
                    "Skin",
                    "Skull",
                    "Small Bowel",
                    "Small Bowel - Mucosa Only",
                    "Small Finger",
                    "Soft Tissue",
                    "Spinal Column",
                    "Spinal Cord",
                    "Spleen",
                    "Splenic Flexure",
                    "Sternum",
                    "Stomach",
                    "Stomach - Mucosa Only",
                    "Subcutaneous Tissue",
                    "Subglottis",
                    "Sublingual Gland",
                    "Submandibular Gland",
                    "Supraglottis",
                    "Synovium",
                    "Temporal Cortex",
                    "Tendon",
                    "Testis",
                    "Thigh",
                    "Thoracic Spine",
                    "Thorax",
                    "Throat",
                    "Thumb",
                    "Thymus",
                    "Thyroid",
                    "Tibia",
                    "Tongue",
                    "Tonsil",
                    "Tonsil (Pharyngeal)",
                    "Trachea / Major Bronchi",
                    "Transverse Colon",
                    "Trunk",
                    "Umbilical Cord",
                    "Ureter",
                    "Urethra",
                    "Urinary Tract",
                    "Uterus",
                    "Uvula",
                    "Vagina",
                    "Vas Deferens",
                    "Vein",
                    "Venous",
                    "Vertebra",
                    "Vulva",
                    "White Blood Cells",
                    "Wrist",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Bone Marrow": {
                        "description": "The tissue occupying the spaces of bone. It consists of blood vessel sinuses and a network of hematopoietic cells which give rise to the red cells, white cells, and megakaryocytes.",
                        "termDef": {
                            "term": "Bone Marrow",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12431",
                            "term_id": "C12431",
                            "term_version": "20.05a",
                        },
                    },
                    "Buccal Mucosa": {
                        "description": "The mucosal membranes located on the inside of the cheek, in the buccal cavity.",
                        "termDef": {
                            "term": "Buccal Mucosa",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12505",
                            "term_id": "C12505",
                            "term_version": "20.10d",
                        },
                    },
                    "Cerebrospinal Fluid": {
                        "description": "The fluid that is contained within the brain ventricles, the subarachnoid space and the central canal of the spinal cord.",
                        "termDef": {
                            "term": "Cerebrospinal Fluid",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12692",
                            "term_id": "C12692",
                            "term_version": "20.05a",
                        },
                    },
                    "Connective Tissue": {
                        "description": "Supporting tissue that surrounds other tissues and organs. Specialized connective tissue includes bone, cartilage, blood, and fat.",
                        "termDef": {
                            "term": "Connective Tissue",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12374",
                            "term_id": "C12374",
                            "term_version": "20.10d",
                        },
                    },
                    "Frontal Lobe": {
                        "description": "The part of the brain located anterior to the parietal lobes at the front of each cerebral hemisphere.",
                        "termDef": {
                            "term": "Frontal Lobe",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12352",
                            "term_id": "C12352",
                            "term_version": "20.05a",
                        },
                    },
                    "Neck": {
                        "description": "The region that connects the head to the rest of the body.",
                        "termDef": {
                            "term": "Neck",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C13063",
                            "term_id": "C13063",
                            "term_version": "20.10d",
                        },
                    },
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Other": {
                        "description": "Different than the one(s) previously specified or mentioned.",
                        "termDef": {
                            "term": "Other",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17649",
                            "term_id": "C17649",
                            "term_version": "19.12e",
                        },
                    },
                    "Soft Tissue": {
                        "description": "A general term comprising tissue that is not hardened or calcified; including muscle, fat, blood vessels, nerves, tendons, ligaments and fascia.",
                        "termDef": {
                            "term": "Soft Tissue",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12471",
                            "term_id": "C12471",
                            "term_version": "20.05a",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "biospecimen_laterality": {
                "description": "For tumors in paired organs, designates the side on which the specimen was obtained.",
                "termDef": {
                    "term": "Specimen Laterality",
                    "source": "caDSR",
                    "cde_id": 2007875,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=2007875&version=1.0",
                },
                "enum": ["Bilateral", "Left", "Right", "Unknown", "Not Reported"],
                "enumDef": {
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "catalog_reference": {
                "description": "HCMI catalog reference number for cancer model.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "string",
            },
            "composition": {
                "description": "Text term that represents the cellular composition of the sample.",
                "termDef": {
                    "term": "Biospecimen Cellular Composition Type",
                    "source": "caDSR",
                    "cde_id": 5432591,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432591&version=1.0",
                },
                "enum": [
                    "2D Classical Conditionally Reprogrammed Cells",
                    "2D Modified Conditionally Reprogrammed Cells",
                    "3D Air-Liquid Interface Organoid",
                    "3D Neurosphere",
                    "3D Organoid",
                    "Adherent Cell Line",
                    "Bone Marrow Components",
                    "Bone Marrow Components NOS",
                    "Buccal Cells",
                    "Buffy Coat",
                    "Cell",
                    "Control Analyte",
                    "Derived Cell Line",
                    "EBV Immortalized",
                    "Fibroblasts from Bone Marrow Normal",
                    "Granulocytes",
                    "Human Original Cells",
                    "Liquid Suspension Cell Line",
                    "Lymphocytes",
                    "Mixed Adherent Suspension",
                    "Mononuclear Cells from Bone Marrow Normal",
                    "Not Allowed To Collect",
                    "Peripheral Blood Components NOS",
                    "Peripheral Whole Blood",
                    "Plasma",
                    "Pleural Effusion",
                    "Saliva",
                    "Serum",
                    "Solid Tissue",
                    "Sorted Cells",
                    "Sputum",
                    "Whole Bone Marrow",
                    "Unknown",
                    "Not Reported",
                ],
                "deprecated_enum": ["Not Allowed To Collect"],
                "enumDef": {
                    "Buffy Coat": {
                        "description": "The middle layer of an anticoagulated blood specimen following separation by centrifugation. It contains most of the white blood cells and platelets.",
                        "termDef": {
                            "term": "Buffy Coat",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C84507",
                            "term_id": "C84507",
                            "term_version": "20.10d",
                        },
                    },
                    "Lymphocytes": {
                        "description": "The determination of the number of lymphocytes in a blood sample.",
                        "termDef": {
                            "term": "Lymphocyte Count",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C51949",
                            "term_id": "C51949",
                            "term_version": "20.10d",
                        },
                    },
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Plasma": {
                        "description": "Plasma is the fluid (noncellular) portion of the circulating blood, as distinguished from the serum that is the fluid portion of the blood obtained by removal of the fibrin clot and blood cells after coagulation.",
                        "termDef": {
                            "term": "Plasma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C13356",
                            "term_id": "C13356",
                            "term_version": "20.10d",
                        },
                    },
                    "Saliva": {
                        "description": "The watery fluid in the mouth made by the salivary glands. Saliva moistens food to help digestion and it helps protect the mouth against infections.",
                        "termDef": {
                            "term": "Saliva",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C13275",
                            "term_id": "C13275",
                            "term_version": "20.10d",
                        },
                    },
                    "Serum": {
                        "description": "The clear portion of the blood that remains after the removal of the blood cells and the clotting proteins.",
                        "termDef": {
                            "term": "Serum",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C13325",
                            "term_id": "C13325",
                            "term_version": "20.10d",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "current_weight": {
                "description": "Numeric value that represents the current weight of the sample, measured in milligrams.",
                "termDef": {
                    "term": "Tissue Sample Current Weight Milligram Value",
                    "source": "caDSR",
                    "cde_id": 5432606,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432606&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "days_to_collection": {
                "description": "The number of days from the index date to the date a sample was collected for a specific study or project.",
                "termDef": {
                    "term": "Biospecimen Collection Date Less Initial Pathologic Diagnosis Date Calculated Day Value",
                    "source": "caDSR",
                    "cde_id": 3008340,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3008340&version=1.0",
                },
                "type": "integer",
                "maximum": 32872,
                "minimum": -32872,
            },
            "days_to_sample_procurement": {
                "description": "The number of days from the index date to the date a patient underwent a procedure (e.g. surgical resection) yielding a sample that was eventually used for research.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "maximum": 32872,
                "minimum": -32872,
            },
            "diagnosis_pathologically_confirmed": {
                "description": "The histologic description of tissue or cells confirmed by a pathology review of frozen or formalin fixed slide(s) completed after the diagnostic pathology review of the tumor sample used to extract analyte(s).",
                "termDef": {
                    "term": "Post-Diagnostic Pathology Review Confirmation",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Not Allowed To Collect",
                    "Yes",
                    "No",
                    "Unknown",
                    "Not Reported",
                ],
                "deprecated_enum": ["Not Allowed To Collect"],
                "enumDef": {
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Yes": {
                        "description": "The affirmative response to a question.",
                        "termDef": {
                            "term": "Yes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C49488",
                            "term_id": "C49488",
                            "term_version": "19.12e",
                        },
                    },
                    "No": {
                        "description": "The non-affirmative response to a question.",
                        "termDef": {
                            "term": "No",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C49487",
                            "term_id": "C49487",
                            "term_version": "19.12e",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "distance_normal_to_tumor": {
                "description": "Text term to signify the distance between the tumor tissue and the normal control tissue that was procured for matching normal DNA.",
                "termDef": {
                    "term": "Tumor To Normal Control Tissue DNA Distance Category",
                    "source": "caDSR",
                    "cde_id": 3088708,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3088708&version=1.0",
                },
                "enum": [
                    "Adjacent (< or = 2cm)",
                    "Distal (>2cm)",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "distributor_reference": {
                "description": "Distributor reference number for cancer model.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "string",
            },
            "freezing_method": {
                "description": "Text term that represents the method used for freezing the sample.",
                "termDef": {
                    "term": "Tissue Sample Freezing Method Type",
                    "source": "caDSR",
                    "cde_id": 5432607,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432607&version=1.0",
                },
                "type": "string",
            },
            "growth_rate": {
                "description": "Rate at which the model grows, measured as hours to time to split.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "minimum": 0,
            },
            "initial_weight": {
                "description": "Numeric value that represents the initial weight of the sample, measured in milligrams.",
                "termDef": {
                    "term": "Tissue Sample Initial Weight Milligram Value",
                    "source": "caDSR",
                    "cde_id": 5432605,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432605&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "intermediate_dimension": {
                "description": "Intermediate dimension of the sample, in millimeters.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "is_ffpe": {
                "description": "Indicator to signify whether or not the tissue sample was fixed in formalin and embedded in paraffin (FFPE).",
                "termDef": {
                    "term": "Specimen Processing Formalin Fixed Paraffin Embedded Tissue Indicator",
                    "source": "caDSR",
                    "cde_id": 4170557,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=4170557&version=1.0",
                },
                "type": "boolean",
            },
            "longest_dimension": {
                "description": "Numeric value that represents the longest dimension of the sample, measured in millimeters.",
                "termDef": {
                    "term": "Tissue Sample Longest Dimension Millimeter Measurement",
                    "source": "caDSR",
                    "cde_id": 5432602,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432602&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "method_of_sample_procurement": {
                "description": "The method used to procure the sample used to extract analyte(s).",
                "termDef": {
                    "term": "Method of Sample Procurement",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Abdomino-perineal Resection of Rectum",
                    "Anterior Resection of Rectum",
                    "Ascites Drainage",
                    "Aspirate",
                    "Autopsy",
                    "Biopsy",
                    "Blood Draw",
                    "Bone Marrow Aspirate",
                    "Buccal Mucosal Resection",
                    "Core Biopsy",
                    "Cystectomy",
                    "Deep Parotidectomy",
                    "Endo Rectal Tumor Resection",
                    "Endolaryngeal Excision",
                    "Endoscopic Biopsy",
                    "Endoscopic Mucosal Resection (EMR)",
                    "Enucleation",
                    "Excisional Biopsy",
                    "Fine Needle Aspiration",
                    "Full Hysterectomy",
                    "Glossectomy",
                    "Gross Total Resection",
                    "Hand Assisted Laparoscopic Radical Nephrectomy",
                    "Hysterectomy NOS",
                    "Incisional Biopsy",
                    "Indeterminant",
                    "Laparoscopic Biopsy",
                    "Laparoscopic Partial Nephrectomy",
                    "Laparoscopic Radical Nephrectomy",
                    "Laparoscopic Radical Prostatectomy with Robotics",
                    "Laparoscopic Radical Prostatectomy without Robotics",
                    "Laryngopharyngectomy",
                    "Left Hemicolectomy",
                    "Liquid Biopsy",
                    "Lobectomy",
                    "Local Resection (Exoresection; wall resection)",
                    "Lumpectomy",
                    "Lymph Node Dissection",
                    "Lymphadenectomy",
                    "Mandibulectomy",
                    "Maxillectomy",
                    "Metastasectomy",
                    "Modified Radical Mastectomy",
                    "Needle Biopsy",
                    "Not Allowed To Collect",
                    "Omentectomy",
                    "Oophorectomy",
                    "Open Craniotomy",
                    "Open Partial Nephrectomy",
                    "Open Radical Nephrectomy",
                    "Open Radical Prostatectomy",
                    "Orchiectomy",
                    "Other",
                    "Other Surgical Resection",
                    "Palatectomy",
                    "Pan-Procto Colectomy",
                    "Pancreatectomy",
                    "Paracentesis",
                    "Parotidectomy, NOS",
                    "Partial Hepatectomy",
                    "Partial Laryngectomy",
                    "Partial Maxillectomy",
                    "Partial Nephrectomy",
                    "Peritoneal Lavage",
                    "Pneumonectomy",
                    "Punch Biopsy",
                    "Radical Hysterectomy",
                    "Radical Maxillectomy",
                    "Radical Nephrectomy",
                    "Radical Prostatectomy",
                    "Right Hemicolectomy",
                    "Salpingectomy",
                    "Salpingo-oophorectomy",
                    "Sigmoid Colectomy",
                    "Simple Hysterectomy",
                    "Simple Mastectomy",
                    "Subtotal Prostatectomy",
                    "Subtotal Resection",
                    "Superficial Parotidectomy",
                    "Supracervical Hysterectomy",
                    "Supracricoid Laryngectomy",
                    "Supraglottic Laryngectomy",
                    "Surgical Resection",
                    "Thoracentesis",
                    "Thoracoscopic Biopsy",
                    "Tonsillectomy",
                    "Total Colectomy",
                    "Total Hepatectomy",
                    "Total Laryngectomy",
                    "Total Mastectomy",
                    "Total Nephrectomy",
                    "Transoral Laser Excision",
                    "Transplant",
                    "Transurethral resection (TURBT)",
                    "Transurethral Resection (TURP)",
                    "Transverse Colectomy",
                    "Tumor Debulking",
                    "Tumor Resection",
                    "Vertical Hemilaryngectomy",
                    "Wedge Resection",
                    "Whipple Procedure",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Autopsy": {
                        "description": "A postmortem examination of the body that includes an examination of the internal organs and structures after dissection to determine the cause of death and the nature of pathological changes.",
                        "termDef": {
                            "term": "Autopsy",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25153",
                            "term_id": "C25153",
                            "term_version": "19.12e",
                        },
                    },
                    "Indeterminant": {
                        "description": "Cannot distinguish between two or more possible values in the current context.",
                        "termDef": {
                            "term": "Indeterminate",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C48658",
                            "term_id": "C48658",
                            "term_version": "20.10d",
                        },
                    },
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Other": {
                        "description": "Different than the one(s) previously specified or mentioned.",
                        "termDef": {
                            "term": "Other",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17649",
                            "term_id": "C17649",
                            "term_version": "19.12e",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "oct_embedded": {
                "description": "Indicator of whether or not the sample was embedded in Optimal Cutting Temperature (OCT) compound.",
                "termDef": {
                    "term": "Tissue Sample Optimal Cutting Temperature Compound Embedding Indicator",
                    "source": "caDSR",
                    "cde_id": 5432538,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432538&version=1.0",
                },
                "type": "string",
            },
            "passage_count": {
                "description": "Number of passages (splits) between the original tissue and this model.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "minimum": 0,
            },
            "pathology_report_uuid": {
                "description": "UUID of the related pathology report.",
                "type": "string",
            },
            "preservation_method": {
                "description": "Text term that represents the method used to preserve the sample.",
                "termDef": {
                    "term": "Tissue Sample Preservation Method Type",
                    "source": "caDSR",
                    "cde_id": 5432521,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432521&version=1.0",
                },
                "enum": [
                    "Cryopreserved",
                    "FFPE",
                    "Fresh",
                    "Frozen",
                    "Not Allowed To Collect",
                    "OCT",
                    "Snap Frozen",
                    "Unknown",
                    "Not Reported",
                ],
                "deprecated_enum": ["Not Allowed To Collect"],
                "enumDef": {
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "sample_ordinal": {
                "description": "A number describing the samples place in an ordered sequence.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "minimum": 1,
            },
            "sample_type": {
                "description": "Text term to describe the source of a biospecimen used for a laboratory test.",
                "termDef": {
                    "term": "Specimen Type Collection Biospecimen Type",
                    "source": "caDSR",
                    "cde_id": 3111302,
                    "cde_version": 2.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3111302&version=2.0",
                },
                "enum": [
                    "Additional - New Primary",
                    "Additional Metastatic",
                    "Benign Neoplasms",
                    "Blood Derived Cancer - Bone Marrow",
                    "Blood Derived Cancer - Bone Marrow, Post-treatment",
                    "Blood Derived Cancer - Peripheral Blood",
                    "Blood Derived Cancer - Peripheral Blood, Post-treatment",
                    "Blood Derived Liquid Biopsy",
                    "Blood Derived Normal",
                    "Bone Marrow Normal",
                    "Buccal Cell Normal",
                    "Cell Line Derived Xenograft Tissue",
                    "Cell Lines",
                    "Control Analyte",
                    "DNA",
                    "EBV Immortalized Normal",
                    "Expanded Next Generation Cancer Model",
                    "FFPE Recurrent",
                    "FFPE Scrolls",
                    "Fibroblasts from Bone Marrow Normal",
                    "GenomePlex (Rubicon) Amplified DNA",
                    "Granulocytes",
                    "Human Tumor Original Cells",
                    "In Situ Neoplasms",
                    "Lymphoid Normal",
                    "Metastatic",
                    "Mixed Adherent Suspension",
                    "Mononuclear Cells from Bone Marrow Normal",
                    "Neoplasms of Uncertain and Unknown Behavior",
                    "Next Generation Cancer Model",
                    "Next Generation Cancer Model Expanded Under Non-conforming Conditions",
                    "Not Allowed To Collect",
                    "Pleural Effusion",
                    "Post neo-adjuvant therapy",
                    "Primary Blood Derived Cancer - Bone Marrow",
                    "Primary Blood Derived Cancer - Peripheral Blood",
                    "Primary Tumor",
                    "Primary Xenograft Tissue",
                    "Recurrent Blood Derived Cancer - Bone Marrow",
                    "Recurrent Blood Derived Cancer - Peripheral Blood",
                    "Recurrent Tumor",
                    "Repli-G (Qiagen) DNA",
                    "Repli-G X (Qiagen) DNA",
                    "RNA",
                    "Saliva",
                    "Slides",
                    "Solid Tissue Normal",
                    "Total RNA",
                    "Tumor",
                    "Tumor Adjacent Normal - Post Neo-adjuvant Therapy",
                    "Xenograft Tissue",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "DNA": {
                        "description": "A long linear double-stranded polymer formed from nucleotides attached to a deoxyribose backbone and found in the nucleus of a cell; associated with the transmission of genetic information.",
                        "termDef": {
                            "term": "DNA",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C449",
                            "term_id": "C449",
                            "term_version": "20.10d",
                        },
                    },
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Saliva": {
                        "description": "The watery fluid in the mouth made by the salivary glands. Saliva moistens food to help digestion and it helps protect the mouth against infections.",
                        "termDef": {
                            "term": "Saliva",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C13275",
                            "term_id": "C13275",
                            "term_version": "20.10d",
                        },
                    },
                    "Total RNA": {
                        "description": "A biological sample comprised of all of the RNA collected from an experimental subject.",
                        "termDef": {
                            "term": "Total RNA",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C163995",
                            "term_id": "C163995",
                            "term_version": "20.10d",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "sample_type_id": {
                "description": "The accompanying sample type id for the sample type.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "20",
                    "30",
                    "31",
                    "32",
                    "40",
                    "41",
                    "42",
                    "50",
                    "60",
                    "61",
                    "85",
                    "86",
                    "87",
                    "99",
                ],
            },
            "shortest_dimension": {
                "description": "Numeric value that represents the shortest dimension of the sample, measured in millimeters.",
                "termDef": {
                    "term": "Tissue Sample Short Dimension Millimeter Measurement",
                    "source": "caDSR",
                    "cde_id": 5432603,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432603&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "specimen_type": {
                "description": "The type of a material sample taken from a biological entity for testing, diagnostic, propagation, treatment or research purposes. This includes particular types of cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory substances.",
                "termDef": {
                    "term": "Biospecimen Type",
                    "source": "NCIt",
                    "cde_id": "C70713",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C70713",
                },
                "enum": [
                    "2D Classical Conditionally Reprogrammed Cells",
                    "2D Modified Conditionally Reprogrammed Cells",
                    "3D Air-Liquid Interface Organoid",
                    "3D Neurosphere",
                    "3D Organoid",
                    "Adherent Cell Line",
                    "Bone Marrow Components NOS",
                    "Bone Marrow NOS",
                    "Buccal Cells",
                    "Buffy Coat",
                    "Cell",
                    "Control Analyte",
                    "Derived Cell Line",
                    "EBV Immortalized",
                    "Fibroblasts from Bone Marrow",
                    "Granulocytes",
                    "Human Original Cells",
                    "Liquid Suspension Cell Line",
                    "Lymphocytes",
                    "Lymphoid",
                    "Mixed Adherent Suspension",
                    "Mononuclear Cells from Bone Marrow",
                    "Peripheral Blood Components NOS",
                    "Peripheral Blood NOS",
                    "Peripheral Whole Blood",
                    "Plasma",
                    "Pleural Effusion",
                    "Saliva",
                    "Serum",
                    "Solid Tissue",
                    "Sorted Cells",
                    "Sputum",
                    "Whole Bone Marrow",
                    "Unknown",
                    "Not Reported",
                ],
            },
            "time_between_clamping_and_freezing": {
                "description": "Numeric representation of the elapsed time between the surgical clamping of blood supply and freezing of the sample, measured in minutes.",
                "termDef": {
                    "term": "Tissue Sample Clamping and Freezing Elapsed Minute Time",
                    "source": "caDSR",
                    "cde_id": 5432611,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432611&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "time_between_excision_and_freezing": {
                "description": "Numeric representation of the elapsed time between the excision and freezing of the sample, measured in minutes.",
                "termDef": {
                    "term": "Tissue Sample Excision and Freezing Elapsed Minute Time",
                    "source": "caDSR",
                    "cde_id": 5432612,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432612&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "tissue_collection_type": {
                "description": "The text term used to describe the tyoe of collection used to obtain tissue.",
                "termDef": {
                    "term": "Tissue Collection Type",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Prospective", "Retrospective"],
            },
            "tissue_type": {
                "description": "Text term that represents a description of the kind of tissue collected with respect to disease status or proximity to tumor tissue.",
                "termDef": {
                    "term": "Tissue Sample Description Type",
                    "source": "caDSR",
                    "cde_id": 5432687,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432687&version=1.0",
                },
                "enum": [
                    "Tumor",
                    "Normal",
                    "Abnormal",
                    "Peritumoral",
                    "Not Allowed To Collect",
                    "Unknown",
                    "Not Reported",
                ],
                "deprecated_enum": ["Not Allowed To Collect"],
                "enumDef": {
                    "Normal": {
                        "description": "Being approximately average or within certain limits; conforming with or constituting a norm or standard or level or type or social norm.",
                        "termDef": {
                            "term": "Normal",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C14165",
                            "term_id": "C14165",
                            "term_version": "20.10d",
                        },
                    },
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "tumor_code": {
                "description": "Diagnostic tumor code of the tissue sample source.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Acute Leukemia of Ambiguous Lineage (ALAL)",
                    "Acute lymphoblastic leukemia (ALL)",
                    "Acute myeloid leukemia (AML)",
                    "Anal Cancer (all types)",
                    "Cervical Cancer (all types)",
                    "Clear cell sarcoma of the kidney (CCSK)",
                    "CNS, ependymoma",
                    "CNS, glioblastoma (GBM)",
                    "CNS, low grade glioma (LGG)",
                    "CNS, medulloblastoma",
                    "CNS, other",
                    "CNS, rhabdoid tumor",
                    "Diffuse Large B-Cell Lymphoma (DLBCL)",
                    "Ewing sarcoma",
                    "Induction Failure AML (AML-IF)",
                    "Lung Cancer (all types)",
                    "Neuroblastoma (NBL)",
                    "NHL, anaplastic large cell lymphoma",
                    "NHL, Burkitt lymphoma (BL)",
                    "Non cancerous tissue",
                    "Osteosarcoma (OS)",
                    "Rhabdoid tumor (kidney) (RT)",
                    "Rhabdomyosarcoma",
                    "Soft tissue sarcoma, non-rhabdomyosarcoma",
                    "Wilms tumor (WT)",
                ],
                "enumDef": {
                    "Ewing sarcoma": {
                        "description": "A small round cell tumor that lacks morphologic, immunohistochemical, and electron microscopic evidence of neuroectodermal differentiation. It represents one of the two ends of the spectrum called Ewing sarcoma/peripheral neuroectodermal tumor. It affects mostly males under age 20, and it can occur in soft tissue or bone. Pain and the presence of a mass are the most common clinical symptoms.",
                        "termDef": {
                            "term": "Ewing Sarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4817",
                            "term_id": "C4817",
                            "term_version": "20.05a",
                        },
                    },
                    "Rhabdomyosarcoma": {
                        "description": "A rare aggressive malignant mesenchymal neoplasm arising from skeletal muscle. It usually occurs in children and young adults. Only a small percentage of tumors arise in the skeletal muscle of the extremities. The majority arise in other anatomical sites.",
                        "termDef": {
                            "term": "Rhabdomyosarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3359",
                            "term_id": "C3359",
                            "term_version": "19.12e",
                        },
                    },
                },
            },
            "tumor_code_id": {
                "description": "BCR-defined id code for the tumor sample.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "10",
                    "15",
                    "20",
                    "21",
                    "30",
                    "40",
                    "41",
                    "50",
                    "51",
                    "52",
                    "60",
                    "61",
                    "62",
                    "63",
                    "64",
                    "65",
                    "70",
                    "71",
                    "80",
                    "81",
                ],
            },
            "tumor_descriptor": {
                "description": "Text that describes the kind of disease present in the tumor specimen as related to a specific timepoint.",
                "termDef": {
                    "term": "Tumor Tissue Disease Description Type",
                    "source": "caDSR",
                    "cde_id": 3288124,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3288124&version=1.0",
                },
                "enum": [
                    "Metastatic",
                    "New Primary",
                    "NOS",
                    "Not Allowed To Collect",
                    "Not Applicable",
                    "Premalignant",
                    "Primary",
                    "Recurrence",
                    "Xenograft",
                    "Unknown",
                    "Not Reported",
                ],
                "deprecated_enum": ["Not Allowed To Collect"],
                "enumDef": {
                    "Not Allowed To Collect": {
                        "description": "An indicator that specifies that a collection event was not permitted.",
                        "termDef": {
                            "term": "Not Allowed To Collect",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C141478",
                            "term_id": "C141478",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Applicable": {
                        "description": "Determination of a value is not relevant in the current context.",
                        "termDef": {
                            "term": "Not Applicable",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C48660",
                            "term_id": "C48660",
                            "term_version": "20.10d",
                        },
                    },
                    "Unknown": {
                        "description": "Not known, not observed, not recorded, or refused.",
                        "termDef": {
                            "term": "Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17998",
                            "term_id": "C17998",
                            "term_version": "19.12e",
                        },
                    },
                    "Not Reported": {
                        "description": "Not provided or available.",
                        "termDef": {
                            "term": "Not Reported",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C43234",
                            "term_id": "C43234",
                            "term_version": "20.05a",
                        },
                    },
                },
            },
            "cases": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": True,
                            "properties": {
                                "id": {
                                    "common": {
                                        "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                        "termDef": {
                                            "term": "Universally Unique Identifier",
                                            "source": "NCIt",
                                            "cde_id": "C54100",
                                            "cde_version": None,
                                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                        },
                                    },
                                    "type": "string",
                                    "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                    "systemAlias": "node_id",
                                },
                                "submitter_id": {"type": "string"},
                            },
                            "minItems": 1,
                            "maxItems": 1,
                        },
                    },
                    {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "id": {
                                "common": {
                                    "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                    "termDef": {
                                        "term": "Universally Unique Identifier",
                                        "source": "NCIt",
                                        "cde_id": "C54100",
                                        "cde_version": None,
                                        "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                    },
                                },
                                "type": "string",
                                "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                "systemAlias": "node_id",
                            },
                            "submitter_id": {"type": "string"},
                        },
                    },
                ]
            },
            "tissue_source_sites": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": True,
                            "properties": {
                                "id": {
                                    "common": {
                                        "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                        "termDef": {
                                            "term": "Universally Unique Identifier",
                                            "source": "NCIt",
                                            "cde_id": "C54100",
                                            "cde_version": None,
                                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                        },
                                    },
                                    "type": "string",
                                    "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                    "systemAlias": "node_id",
                                },
                                "submitter_id": {"type": "string"},
                            },
                            "minItems": 1,
                            "maxItems": 1,
                        },
                    },
                    {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "id": {
                                "common": {
                                    "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                    "termDef": {
                                        "term": "Universally Unique Identifier",
                                        "source": "NCIt",
                                        "cde_id": "C54100",
                                        "cde_version": None,
                                        "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                    },
                                },
                                "type": "string",
                                "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                "systemAlias": "node_id",
                            },
                            "submitter_id": {"type": "string"},
                        },
                    },
                ]
            },
            "diagnoses": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": True,
                            "properties": {
                                "id": {
                                    "common": {
                                        "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                        "termDef": {
                                            "term": "Universally Unique Identifier",
                                            "source": "NCIt",
                                            "cde_id": "C54100",
                                            "cde_version": None,
                                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                        },
                                    },
                                    "type": "string",
                                    "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                    "systemAlias": "node_id",
                                },
                                "submitter_id": {"type": "string"},
                            },
                            "minItems": 1,
                            "maxItems": 1,
                        },
                    },
                    {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "id": {
                                "common": {
                                    "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                    "termDef": {
                                        "term": "Universally Unique Identifier",
                                        "source": "NCIt",
                                        "cde_id": "C54100",
                                        "cde_version": None,
                                        "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                    },
                                },
                                "type": "string",
                                "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                "systemAlias": "node_id",
                            },
                            "submitter_id": {"type": "string"},
                        },
                    },
                ]
            },
            "parent_samples": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": True,
                            "properties": {
                                "id": {
                                    "common": {
                                        "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                        "termDef": {
                                            "term": "Universally Unique Identifier",
                                            "source": "NCIt",
                                            "cde_id": "C54100",
                                            "cde_version": None,
                                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                        },
                                    },
                                    "type": "string",
                                    "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                    "systemAlias": "node_id",
                                },
                                "submitter_id": {"type": "string"},
                            },
                            "minItems": 1,
                            "maxItems": 1,
                        },
                    },
                    {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "id": {
                                "common": {
                                    "description": "A 128-bit identifier. Depending on the mechanism used to generate it, it is either guaranteed to be different from all other UUIDs/GUIDs generated until 3400 AD or extremely likely to be different. Its relatively small size lends itself well to sorting, ordering, and hashing of all sorts, storing in databases, simple allocation, and ease of programming in general.",
                                    "termDef": {
                                        "term": "Universally Unique Identifier",
                                        "source": "NCIt",
                                        "cde_id": "C54100",
                                        "cde_version": None,
                                        "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&version=16.02d&ns=NCI_Thesaurus&code=C54100",
                                    },
                                },
                                "type": "string",
                                "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                                "systemAlias": "node_id",
                            },
                            "submitter_id": {"type": "string"},
                        },
                    },
                ]
            },
        },
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
        enum=[
            "error",
            "invalid",
            "live",
            "md5summed",
            "md5summing",
            "redacted",
            "released",
            "submitted",
            "suppressed",
            "uploaded",
            "uploading",
            "validated",
            "validating",
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

    @psqlgraph.pg_property(
        str,
        enum=[
            "Abdomen",
            "Abdominal Wall",
            "Acetabulum",
            "Adenoid",
            "Adipose",
            "Adrenal",
            "Alveolar Ridge",
            "Amniotic Fluid",
            "Ampulla Of Vater",
            "Anal Sphincter",
            "Ankle",
            "Anorectum",
            "Antecubital Fossa",
            "Antrum",
            "Anus",
            "Aorta",
            "Aortic Body",
            "Appendix",
            "Aqueous Fluid",
            "Arm",
            "Artery",
            "Ascending Colon",
            "Ascending Colon Hepatic Flexure",
            "Auditory Canal",
            "Autonomic Nervous System",
            "Axilla",
            "Back",
            "Bile Duct",
            "Bladder",
            "Blood",
            "Blood Vessel",
            "Bone",
            "Bone Marrow",
            "Bowel",
            "Brain",
            "Brain Stem",
            "Breast",
            "Broad Ligament",
            "Bronchiole",
            "Bronchus",
            "Brow",
            "Buccal Cavity",
            "Buccal Mucosa",
            "Buttock",
            "Calf",
            "Capillary",
            "Cardia",
            "Carina",
            "Carotid Artery",
            "Carotid Body",
            "Cartilage",
            "Cecum",
            "Cell-Line",
            "Central Nervous System",
            "Cerebellum",
            "Cerebral Cortex",
            "Cerebrospinal Fluid",
            "Cerebrum",
            "Cervical Spine",
            "Cervix",
            "Chest",
            "Chest Wall",
            "Chin",
            "Clavicle",
            "Clitoris",
            "Colon",
            "Colon - Mucosa Only",
            "Common Duct",
            "Conjunctiva",
            "Connective Tissue",
            "Dermal",
            "Descending Colon",
            "Diaphragm",
            "Duodenum",
            "Ear",
            "Ear Canal",
            "Ear, Pinna (External)",
            "Effusion",
            "Elbow",
            "Endocrine Gland",
            "Epididymis",
            "Epidural Space",
            "Esophageal; Distal",
            "Esophageal; Mid",
            "Esophageal; Proximal",
            "Esophagogastric Junction",
            "Esophagus",
            "Esophagus - Mucosa Only",
            "Eye",
            "Fallopian Tube",
            "Femoral Artery",
            "Femoral Vein",
            "Femur",
            "Fibroblasts",
            "Fibula",
            "Finger",
            "Floor Of Mouth",
            "Fluid",
            "Foot",
            "Forearm",
            "Forehead",
            "Foreskin",
            "Frontal Cortex",
            "Frontal Lobe",
            "Fundus Of Stomach",
            "Gallbladder",
            "Ganglia",
            "Gastroesophageal Junction",
            "Gastrointestinal Tract",
            "Glottis",
            "Groin",
            "Gum",
            "Hand",
            "Hard Palate",
            "Head & Neck",
            "Head - Face Or Neck, Nos",
            "Heart",
            "Hepatic",
            "Hepatic Duct",
            "Hepatic Flexure",
            "Hepatic Vein",
            "Hip",
            "Hippocampus",
            "Humerus",
            "Hypopharynx",
            "Ileum",
            "Ilium",
            "Index Finger",
            "Ischium",
            "Islet Cells",
            "Jaw",
            "Jejunum",
            "Joint",
            "Kidney",
            "Knee",
            "Lacrimal Gland",
            "Large Bowel",
            "Laryngopharynx",
            "Larynx",
            "Leg",
            "Leptomeninges",
            "Ligament",
            "Lip",
            "Liver",
            "Lumbar Spine",
            "Lung",
            "Lymph Node",
            "Lymph Node(s) Axilla",
            "Lymph Node(s) Cervical",
            "Lymph Node(s) Distant",
            "Lymph Node(s) Epitrochlear",
            "Lymph Node(s) Femoral",
            "Lymph Node(s) Hilar",
            "Lymph Node(s) Iliac-Common",
            "Lymph Node(s) Iliac-External",
            "Lymph Node(s) Inguinal",
            "Lymph Node(s) Internal Mammary",
            "Lymph Node(s) Mammary",
            "Lymph Node(s) Mesenteric",
            "Lymph Node(s) Occipital",
            "Lymph Node(s) Paraaortic",
            "Lymph Node(s) Parotid",
            "Lymph Node(s) Pelvic",
            "Lymph Node(s) Popliteal",
            "Lymph Node(s) Regional",
            "Lymph Node(s) Retroperitoneal",
            "Lymph Node(s) Scalene",
            "Lymph Node(s) Splenic",
            "Lymph Node(s) Subclavicular",
            "Lymph Node(s) Submandibular",
            "Lymph Node(s) Supraclavicular",
            "Lymph Nodes(s) Mediastinal",
            "Mandible",
            "Maxilla",
            "Mediastinal Soft Tissue",
            "Mediastinum",
            "Mesentery",
            "Mesothelium",
            "Middle Finger",
            "Mitochondria",
            "Muscle",
            "Nails",
            "Nasal Cavity",
            "Nasal Soft Tissue",
            "Nasopharynx",
            "Neck",
            "Nerve",
            "Nerve(s) Cranial",
            "Not Allowed To Collect",
            "Not Reported",
            "Occipital Cortex",
            "Ocular Orbits",
            "Omentum",
            "Oral Cavity",
            "Oral Cavity - Mucosa Only",
            "Oropharynx",
            "Other",
            "Ovary",
            "Palate",
            "Pancreas",
            "Paranasal Sinuses",
            "Paraspinal Ganglion",
            "Parathyroid",
            "Parotid Gland",
            "Patella",
            "Pelvis",
            "Penis",
            "Pericardium",
            "Periorbital Soft Tissue",
            "Peritoneal Cavity",
            "Peritoneum",
            "Pharynx",
            "Pineal",
            "Pineal Gland",
            "Pituitary Gland",
            "Placenta",
            "Pleura",
            "Popliteal Fossa",
            "Prostate",
            "Pylorus",
            "Rectosigmoid Junction",
            "Rectum",
            "Retina",
            "Retro-Orbital Region",
            "Retroperitoneum",
            "Rib",
            "Ring Finger",
            "Round Ligament",
            "Sacrum",
            "Salivary Gland",
            "Scalp",
            "Scapula",
            "Sciatic Nerve",
            "Scrotum",
            "Seminal Vesicle",
            "Shoulder",
            "Sigmoid Colon",
            "Sinus",
            "Sinus(es), Maxillary",
            "Skeletal Muscle",
            "Skin",
            "Skull",
            "Small Bowel",
            "Small Bowel - Mucosa Only",
            "Small Finger",
            "Soft Tissue",
            "Spinal Column",
            "Spinal Cord",
            "Spleen",
            "Splenic Flexure",
            "Sternum",
            "Stomach",
            "Stomach - Mucosa Only",
            "Subcutaneous Tissue",
            "Subglottis",
            "Sublingual Gland",
            "Submandibular Gland",
            "Supraglottis",
            "Synovium",
            "Temporal Cortex",
            "Tendon",
            "Testis",
            "Thigh",
            "Thoracic Spine",
            "Thorax",
            "Throat",
            "Thumb",
            "Thymus",
            "Thyroid",
            "Tibia",
            "Tongue",
            "Tonsil",
            "Tonsil (Pharyngeal)",
            "Trachea / Major Bronchi",
            "Transverse Colon",
            "Trunk",
            "Umbilical Cord",
            "Unknown",
            "Ureter",
            "Urethra",
            "Urinary Tract",
            "Uterus",
            "Uvula",
            "Vagina",
            "Vas Deferens",
            "Vein",
            "Venous",
            "Vertebra",
            "Vulva",
            "White Blood Cells",
            "Wrist",
        ],
    )
    def biospecimen_anatomic_site(self, value):
        self._set_property("biospecimen_anatomic_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Bilateral", "Left", "Not Reported", "Right", "Unknown"])
    def biospecimen_laterality(self, value):
        self._set_property("biospecimen_laterality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def catalog_reference(self, value):
        self._set_property("catalog_reference", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "2D Classical Conditionally Reprogrammed Cells",
            "2D Modified Conditionally Reprogrammed Cells",
            "3D Air-Liquid Interface Organoid",
            "3D Neurosphere",
            "3D Organoid",
            "Adherent Cell Line",
            "Bone Marrow Components",
            "Bone Marrow Components NOS",
            "Buccal Cells",
            "Buffy Coat",
            "Cell",
            "Control Analyte",
            "Derived Cell Line",
            "EBV Immortalized",
            "Fibroblasts from Bone Marrow Normal",
            "Granulocytes",
            "Human Original Cells",
            "Liquid Suspension Cell Line",
            "Lymphocytes",
            "Mixed Adherent Suspension",
            "Mononuclear Cells from Bone Marrow Normal",
            "Not Allowed To Collect",
            "Not Reported",
            "Peripheral Blood Components NOS",
            "Peripheral Whole Blood",
            "Plasma",
            "Pleural Effusion",
            "Saliva",
            "Serum",
            "Solid Tissue",
            "Sorted Cells",
            "Sputum",
            "Unknown",
            "Whole Bone Marrow",
        ],
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
        str, enum=["No", "Not Allowed To Collect", "Not Reported", "Unknown", "Yes"]
    )
    def diagnosis_pathologically_confirmed(self, value):
        self._set_property("diagnosis_pathologically_confirmed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Adjacent (< or = 2cm)", "Distal (>2cm)", "Not Reported", "Unknown"]
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
        enum=[
            "Abdomino-perineal Resection of Rectum",
            "Anterior Resection of Rectum",
            "Ascites Drainage",
            "Aspirate",
            "Autopsy",
            "Biopsy",
            "Blood Draw",
            "Bone Marrow Aspirate",
            "Buccal Mucosal Resection",
            "Core Biopsy",
            "Cystectomy",
            "Deep Parotidectomy",
            "Endo Rectal Tumor Resection",
            "Endolaryngeal Excision",
            "Endoscopic Biopsy",
            "Endoscopic Mucosal Resection (EMR)",
            "Enucleation",
            "Excisional Biopsy",
            "Fine Needle Aspiration",
            "Full Hysterectomy",
            "Glossectomy",
            "Gross Total Resection",
            "Hand Assisted Laparoscopic Radical Nephrectomy",
            "Hysterectomy NOS",
            "Incisional Biopsy",
            "Indeterminant",
            "Laparoscopic Biopsy",
            "Laparoscopic Partial Nephrectomy",
            "Laparoscopic Radical Nephrectomy",
            "Laparoscopic Radical Prostatectomy with Robotics",
            "Laparoscopic Radical Prostatectomy without Robotics",
            "Laryngopharyngectomy",
            "Left Hemicolectomy",
            "Liquid Biopsy",
            "Lobectomy",
            "Local Resection (Exoresection; wall resection)",
            "Lumpectomy",
            "Lymph Node Dissection",
            "Lymphadenectomy",
            "Mandibulectomy",
            "Maxillectomy",
            "Metastasectomy",
            "Modified Radical Mastectomy",
            "Needle Biopsy",
            "Not Allowed To Collect",
            "Not Reported",
            "Omentectomy",
            "Oophorectomy",
            "Open Craniotomy",
            "Open Partial Nephrectomy",
            "Open Radical Nephrectomy",
            "Open Radical Prostatectomy",
            "Orchiectomy",
            "Other",
            "Other Surgical Resection",
            "Palatectomy",
            "Pan-Procto Colectomy",
            "Pancreatectomy",
            "Paracentesis",
            "Parotidectomy, NOS",
            "Partial Hepatectomy",
            "Partial Laryngectomy",
            "Partial Maxillectomy",
            "Partial Nephrectomy",
            "Peritoneal Lavage",
            "Pneumonectomy",
            "Punch Biopsy",
            "Radical Hysterectomy",
            "Radical Maxillectomy",
            "Radical Nephrectomy",
            "Radical Prostatectomy",
            "Right Hemicolectomy",
            "Salpingectomy",
            "Salpingo-oophorectomy",
            "Sigmoid Colectomy",
            "Simple Hysterectomy",
            "Simple Mastectomy",
            "Subtotal Prostatectomy",
            "Subtotal Resection",
            "Superficial Parotidectomy",
            "Supracervical Hysterectomy",
            "Supracricoid Laryngectomy",
            "Supraglottic Laryngectomy",
            "Surgical Resection",
            "Thoracentesis",
            "Thoracoscopic Biopsy",
            "Tonsillectomy",
            "Total Colectomy",
            "Total Hepatectomy",
            "Total Laryngectomy",
            "Total Mastectomy",
            "Total Nephrectomy",
            "Transoral Laser Excision",
            "Transplant",
            "Transurethral Resection (TURP)",
            "Transurethral resection (TURBT)",
            "Transverse Colectomy",
            "Tumor Debulking",
            "Tumor Resection",
            "Unknown",
            "Vertical Hemilaryngectomy",
            "Wedge Resection",
            "Whipple Procedure",
        ],
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
        enum=[
            "Cryopreserved",
            "EDTA",
            "FFPE",
            "Fresh",
            "Frozen",
            "Not Allowed To Collect",
            "Not Reported",
            "OCT",
            "Snap Frozen",
            "Unknown",
        ],
    )
    def preservation_method(self, value):
        self._set_property("preservation_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def sample_ordinal(self, value):
        self._set_property("sample_ordinal", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Additional - New Primary",
            "Additional Metastatic",
            "Benign Neoplasms",
            "Blood Derived Cancer - Bone Marrow",
            "Blood Derived Cancer - Bone Marrow, Post-treatment",
            "Blood Derived Cancer - Peripheral Blood",
            "Blood Derived Cancer - Peripheral Blood, Post-treatment",
            "Blood Derived Liquid Biopsy",
            "Blood Derived Normal",
            "Bone Marrow Normal",
            "Buccal Cell Normal",
            "Cell Line Derived Xenograft Tissue",
            "Cell Lines",
            "Control Analyte",
            "DNA",
            "EBV Immortalized Normal",
            "Expanded Next Generation Cancer Model",
            "FFPE Recurrent",
            "FFPE Scrolls",
            "Fibroblasts from Bone Marrow Normal",
            "GenomePlex (Rubicon) Amplified DNA",
            "Granulocytes",
            "Human Tumor Original Cells",
            "In Situ Neoplasms",
            "Lymphoid Normal",
            "Metastatic",
            "Mixed Adherent Suspension",
            "Mononuclear Cells from Bone Marrow Normal",
            "Neoplasms of Uncertain and Unknown Behavior",
            "Next Generation Cancer Model",
            "Next Generation Cancer Model Expanded Under Non-conforming Conditions",
            "Not Allowed To Collect",
            "Not Reported",
            "Pleural Effusion",
            "Post neo-adjuvant therapy",
            "Primary Blood Derived Cancer - Bone Marrow",
            "Primary Blood Derived Cancer - Peripheral Blood",
            "Primary Tumor",
            "Primary Xenograft Tissue",
            "RNA",
            "Recurrent Blood Derived Cancer - Bone Marrow",
            "Recurrent Blood Derived Cancer - Peripheral Blood",
            "Recurrent Tumor",
            "Repli-G (Qiagen) DNA",
            "Repli-G X (Qiagen) DNA",
            "Saliva",
            "Slides",
            "Solid Tissue Normal",
            "Total RNA",
            "Tumor",
            "Tumor Adjacent Normal - Post Neo-adjuvant Therapy",
            "Unknown",
            "Xenograft Tissue",
        ],
    )
    def sample_type(self, value):
        self._set_property("sample_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "20",
            "30",
            "31",
            "32",
            "40",
            "41",
            "42",
            "50",
            "60",
            "61",
            "85",
            "86",
            "87",
            "99",
        ],
    )
    def sample_type_id(self, value):
        self._set_property("sample_type_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def shortest_dimension(self, value):
        self._set_property("shortest_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "2D Classical Conditionally Reprogrammed Cells",
            "2D Modified Conditionally Reprogrammed Cells",
            "3D Air-Liquid Interface Organoid",
            "3D Neurosphere",
            "3D Organoid",
            "Adherent Cell Line",
            "Bone Marrow Components NOS",
            "Bone Marrow NOS",
            "Buccal Cells",
            "Buffy Coat",
            "Cell",
            "Control Analyte",
            "Derived Cell Line",
            "Derived Cell Lines and Sorted Cells",
            "EBV Immortalized",
            "Fibroblasts from Bone Marrow",
            "Granulocytes",
            "Human Original Cells",
            "Liquid Suspension Cell Line",
            "Lymphocytes",
            "Lymphoid",
            "Mixed Adherent Suspension",
            "Mononuclear Cells from Bone Marrow",
            "Not Reported",
            "Peripheral Blood Components NOS",
            "Peripheral Blood NOS",
            "Peripheral Whole Blood",
            "Plasma",
            "Pleural Effusion",
            "Saliva",
            "Serum",
            "Solid Tissue",
            "Sorted Cells",
            "Sputum",
            "Unknown",
            "Whole Bone Marrow",
        ],
    )
    def specimen_type(self, value):
        self._set_property("specimen_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def time_between_clamping_and_freezing(self, value):
        self._set_property("time_between_clamping_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def time_between_excision_and_freezing(self, value):
        self._set_property("time_between_excision_and_freezing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Prospective", "Retrospective"])
    def tissue_collection_type(self, value):
        self._set_property("tissue_collection_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Abnormal",
            "Normal",
            "Not Allowed To Collect",
            "Not Reported",
            "Peritumoral",
            "Tumor",
            "Unknown",
        ],
    )
    def tissue_type(self, value):
        self._set_property("tissue_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Acute Leukemia of Ambiguous Lineage (ALAL)",
            "Acute lymphoblastic leukemia (ALL)",
            "Acute myeloid leukemia (AML)",
            "Anal Cancer (all types)",
            "CNS, ependymoma",
            "CNS, glioblastoma (GBM)",
            "CNS, low grade glioma (LGG)",
            "CNS, medulloblastoma",
            "CNS, other",
            "CNS, rhabdoid tumor",
            "Cervical Cancer (all types)",
            "Clear cell sarcoma of the kidney (CCSK)",
            "Diffuse Large B-Cell Lymphoma (DLBCL)",
            "Ewing sarcoma",
            "Induction Failure AML (AML-IF)",
            "Lung Cancer (all types)",
            "NHL, Burkitt lymphoma (BL)",
            "NHL, anaplastic large cell lymphoma",
            "Neuroblastoma (NBL)",
            "Non cancerous tissue",
            "Osteosarcoma (OS)",
            "Rhabdoid tumor (kidney) (RT)",
            "Rhabdomyosarcoma",
            "Soft tissue sarcoma, non-rhabdomyosarcoma",
            "Wilms tumor (WT)",
        ],
    )
    def tumor_code(self, value):
        self._set_property("tumor_code", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "00",
            "01",
            "02",
            "03",
            "04",
            "10",
            "15",
            "20",
            "21",
            "30",
            "40",
            "41",
            "50",
            "51",
            "52",
            "60",
            "61",
            "62",
            "63",
            "64",
            "65",
            "70",
            "71",
            "80",
            "81",
        ],
    )
    def tumor_code_id(self, value):
        self._set_property("tumor_code_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Metastatic",
            "NOS",
            "New Primary",
            "Not Allowed To Collect",
            "Not Applicable",
            "Not Reported",
            "Premalignant",
            "Primary",
            "Recurrence",
            "Unknown",
            "Xenograft",
        ],
    )
    def tumor_descriptor(self, value):
        self._set_property("tumor_descriptor", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Sample)
datetime_hooks.cls_inject_updated_datetime_hook(Sample)
