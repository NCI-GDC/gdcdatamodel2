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


class Case(base.Node):
    __tablename__: str = "node_case"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Case",
        "namespace": "https://gdc.cancer.gov",
        "category": "administrative",
        "submittable": True,
        "downloadable": False,
        "description": "The collection of all data related to a specific subject in the context of a specific project.",
        "required": ["submitter_id", "disease_type", "primary_site"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "name": "projects",
                "backref": "cases",
                "label": "member_of",
                "target_type": "project",
                "multiplicity": "many_to_one",
                "required": True,
            },
            {
                "name": "tissue_source_sites",
                "backref": "cases",
                "label": "processed_at",
                "target_type": "tissue_source_site",
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
            "consent_type": {
                "description": "The text term used to describe the type of consent obtain from the subject for participation in the study.",
                "termDef": {
                    "term": "Subject Consent Type",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Consent by Death",
                    "Consent Exemption",
                    "Consent Waiver",
                    "Informed Consent",
                ],
            },
            "days_to_consent": {
                "description": "Number of days between the date used for index and the date the subject consent was obtained for participation in the study.",
                "termDef": {
                    "term": "Index Date to Consent Day Count",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "maximum": 32872,
                "minimum": -32872,
            },
            "days_to_lost_to_followup": {
                "description": "The number of days between the date used for index and to the date the patient was lost to follow-up.",
                "termDef": {
                    "term": "Index Date To Lost To Follow-up Day Count",
                    "source": "caDSR",
                    "cde_id": 6154721,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6154721%20and%20ver_nr=1.0",
                },
                "type": "integer",
                "maximum": 32872,
                "minimum": -32872,
            },
            "disease_type": {
                "description": "The text term used to describe the type of malignant disease, as categorized by the World Health Organization's (WHO) International Classification of Diseases for Oncology (ICD-O).",
                "termDef": {
                    "term": "ICD-O Disease Diagnosis Category",
                    "source": "caDSR",
                    "cde_id": 6161017,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6161017%20and%20ver_nr=1.0",
                },
                "enum": [
                    "Acinar Cell Neoplasms",
                    "Adenomas and Adenocarcinomas",
                    "Adnexal and Skin Appendage Neoplasms",
                    "Basal Cell Neoplasms",
                    "Blood Vessel Tumors",
                    "Chronic Myeloproliferative Disorders",
                    "Complex Epithelial Neoplasms",
                    "Complex Mixed and Stromal Neoplasms",
                    "Cystic, Mucinous and Serous Neoplasms",
                    "Ductal and Lobular Neoplasms",
                    "Epithelial Neoplasms, NOS",
                    "Fibroepithelial Neoplasms",
                    "Fibromatous Neoplasms",
                    "Germ Cell Neoplasms",
                    "Giant Cell Tumors",
                    "Gliomas",
                    "Granular Cell Tumors and Alveolar Soft Part Sarcomas",
                    "Hodgkin Lymphoma",
                    "Immunoproliferative Diseases",
                    "Leukemias, NOS",
                    "Lipomatous Neoplasms",
                    "Lymphatic Vessel Tumors",
                    "Lymphoid Leukemias",
                    "Malignant Lymphomas, NOS or Diffuse",
                    "Mast Cell Tumors",
                    "Mature B-Cell Lymphomas",
                    "Mature T- and NK-Cell Lymphomas",
                    "Meningiomas",
                    "Mesonephromas",
                    "Mesothelial Neoplasms",
                    "Miscellaneous Bone Tumors",
                    "Miscellaneous Tumors",
                    "Mucoepidermoid Neoplasms",
                    "Myelodysplastic Syndromes",
                    "Myeloid Leukemias",
                    "Myomatous Neoplasms",
                    "Myxomatous Neoplasms",
                    "Neoplasms of Histiocytes and Accessory Lymphoid Cells",
                    "Neoplasms, NOS",
                    "Nerve Sheath Tumors",
                    "Neuroepitheliomatous Neoplasms",
                    "Nevi and Melanomas",
                    "Odontogenic Tumors",
                    "Osseous and Chondromatous Neoplasms",
                    "Other Hematologic Disorders",
                    "Other Leukemias",
                    "Paragangliomas and Glomus Tumors",
                    "Plasma Cell Tumors",
                    "Precursor Cell Lymphoblastic Lymphoma",
                    "Soft Tissue Tumors and Sarcomas, NOS",
                    "Specialized Gonadal Neoplasms",
                    "Squamous Cell Neoplasms",
                    "Synovial-like Neoplasms",
                    "Thymic Epithelial Neoplasms",
                    "Transitional Cell Papillomas and Carcinomas",
                    "Trophoblastic neoplasms",
                    "Unknown",
                    "Not Reported",
                    "Not Applicable",
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
                },
            },
            "index_date": {
                "description": "The text term used to describe the reference or anchor date used when for date obfuscation, where a single date is obscurred by creating one or more date ranges in relation to this date.",
                "termDef": {
                    "term": "Index Date Type",
                    "source": "caDSR",
                    "cde_id": 6154722,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6154722%20and%20ver_nr=1.0",
                },
                "enum": [
                    "Diagnosis",
                    "First Patient Visit",
                    "First Treatment",
                    "Initial Genomic Sequencing",
                    "Recurrence",
                    "Sample Procurement",
                    "Study Enrollment",
                ],
            },
            "lost_to_followup": {
                "description": "The yes/no/unknown indicator used to describe whether a patient was unable to be contacted or seen for follow-up information.",
                "termDef": {
                    "term": "Patient Lost Follow-up Indicator",
                    "source": "caDSR",
                    "cde_id": 6161018,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6161018%20and%20ver_nr=1.0",
                },
                "enum": ["Yes", "No", "Unknown"],
                "enumDef": {
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
                },
            },
            "primary_site": {
                "description": "The text term used to describe the primary site of disease, as categorized by the World Health Organization's (WHO) International Classification of Diseases for Oncology (ICD-O). This categorization groups cases into general categories. Reference tissue_or_organ_of_origin on the diagnosis node for more specific primary sites of disease.",
                "termDef": {
                    "term": "ICD-O Primary Anatomic Site Category",
                    "source": "caDSR",
                    "cde_id": 6161019,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6161019%20and%20ver_nr=1.0",
                },
                "enum": [
                    "Accessory sinuses",
                    "Adrenal gland",
                    "Anus and anal canal",
                    "Base of tongue",
                    "Bladder",
                    "Bones, joints and articular cartilage of limbs",
                    "Bones, joints and articular cartilage of other and unspecified sites",
                    "Brain",
                    "Breast",
                    "Bronchus and lung",
                    "Cervix uteri",
                    "Colon",
                    "Connective, subcutaneous and other soft tissues",
                    "Corpus uteri",
                    "Esophagus",
                    "Eye and adnexa",
                    "Floor of mouth",
                    "Gallbladder",
                    "Gum",
                    "Heart, mediastinum, and pleura",
                    "Hematopoietic and reticuloendothelial systems",
                    "Hypopharynx",
                    "Kidney",
                    "Larynx",
                    "Lip",
                    "Liver and intrahepatic bile ducts",
                    "Lymph nodes",
                    "Meninges",
                    "Nasal cavity and middle ear",
                    "Nasopharynx",
                    "Oropharynx",
                    "Other and ill-defined digestive organs",
                    "Other and ill-defined sites",
                    "Other and ill-defined sites in lip, oral cavity and pharynx",
                    "Other and ill-defined sites within respiratory system and intrathoracic organs",
                    "Other and unspecified female genital organs",
                    "Other and unspecified major salivary glands",
                    "Other and unspecified male genital organs",
                    "Other and unspecified parts of biliary tract",
                    "Other and unspecified parts of mouth",
                    "Other and unspecified parts of tongue",
                    "Other and unspecified urinary organs",
                    "Other endocrine glands and related structures",
                    "Ovary",
                    "Palate",
                    "Pancreas",
                    "Parotid gland",
                    "Penis",
                    "Peripheral nerves and autonomic nervous system",
                    "Placenta",
                    "Prostate gland",
                    "Pyriform sinus",
                    "Rectosigmoid junction",
                    "Rectum",
                    "Renal pelvis",
                    "Retroperitoneum and peritoneum",
                    "Skin",
                    "Small intestine",
                    "Spinal cord, cranial nerves, and other parts of central nervous system",
                    "Stomach",
                    "Testis",
                    "Thymus",
                    "Thyroid gland",
                    "Tonsil",
                    "Trachea",
                    "Ureter",
                    "Uterus, NOS",
                    "Vagina",
                    "Vulva",
                    "Unknown",
                    "Not Reported",
                    "Not Applicable",
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
                },
            },
            "projects": {
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
        },
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "case"

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
                "name": "cases",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "biospecimen_supplements": {
                "name": "cases",
                "src_type": base.Node.get_subclass("biospecimen_supplement"),
            },
            "clinical_supplements": {
                "name": "cases",
                "src_type": base.Node.get_subclass("clinical_supplement"),
            },
            "clinicals": {
                "name": "cases",
                "src_type": base.Node.get_subclass("clinical"),
            },
            "demographics": {
                "name": "cases",
                "src_type": base.Node.get_subclass("demographic"),
            },
            "describing_files": {
                "name": "described_cases",
                "src_type": base.Node.get_subclass("file"),
            },
            "diagnoses": {
                "name": "cases",
                "src_type": base.Node.get_subclass("diagnosis"),
            },
            "exposures": {
                "name": "cases",
                "src_type": base.Node.get_subclass("exposure"),
            },
            "family_histories": {
                "name": "cases",
                "src_type": base.Node.get_subclass("family_history"),
            },
            "files": {
                "name": "cases",
                "src_type": base.Node.get_subclass("file"),
            },
            "follow_ups": {
                "name": "cases",
                "src_type": base.Node.get_subclass("follow_up"),
            },
            "samples": {
                "name": "cases",
                "src_type": base.Node.get_subclass("sample"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "cases",
                "type": base.Node.get_subclass("annotation"),
            },
            "biospecimen_supplements": {
                "backref": "cases",
                "type": base.Node.get_subclass("biospecimen_supplement"),
            },
            "clinical_supplements": {
                "backref": "cases",
                "type": base.Node.get_subclass("clinical_supplement"),
            },
            "clinicals": {
                "backref": "cases",
                "type": base.Node.get_subclass("clinical"),
            },
            "demographics": {
                "backref": "cases",
                "type": base.Node.get_subclass("demographic"),
            },
            "describing_files": {
                "backref": "described_cases",
                "type": base.Node.get_subclass("file"),
            },
            "diagnoses": {
                "backref": "cases",
                "type": base.Node.get_subclass("diagnosis"),
            },
            "exposures": {
                "backref": "cases",
                "type": base.Node.get_subclass("exposure"),
            },
            "family_histories": {
                "backref": "cases",
                "type": base.Node.get_subclass("family_history"),
            },
            "files": {
                "backref": "cases",
                "type": base.Node.get_subclass("file"),
            },
            "follow_ups": {
                "backref": "cases",
                "type": base.Node.get_subclass("follow_up"),
            },
            "projects": {
                "backref": "cases",
                "type": base.Node.get_subclass("project"),
            },
            "samples": {
                "backref": "cases",
                "type": base.Node.get_subclass("sample"),
            },
            "tissue_source_sites": {
                "backref": "cases",
                "type": base.Node.get_subclass("tissue_source_site"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "projects": {
                "edge_out": "_CaseMemberOfProject_out",
                "dst_type": base.Node.get_subclass("project"),
            },
            "tissue_source_sites": {
                "edge_out": "_CaseProcessedAtTissueSourceSite_out",
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
            "Consent Exemption",
            "Consent Waiver",
            "Consent by Death",
            "Informed Consent",
        ],
    )
    def consent_type(self, value):
        self._set_property("consent_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_consent(self, value):
        self._set_property("days_to_consent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_lost_to_followup(self, value):
        self._set_property("days_to_lost_to_followup", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Acinar Cell Neoplasms",
            "Adenomas and Adenocarcinomas",
            "Adnexal and Skin Appendage Neoplasms",
            "Basal Cell Neoplasms",
            "Blood Vessel Tumors",
            "Chronic Myeloproliferative Disorders",
            "Complex Epithelial Neoplasms",
            "Complex Mixed and Stromal Neoplasms",
            "Cystic, Mucinous and Serous Neoplasms",
            "Ductal and Lobular Neoplasms",
            "Epithelial Neoplasms, NOS",
            "Fibroepithelial Neoplasms",
            "Fibromatous Neoplasms",
            "Germ Cell Neoplasms",
            "Giant Cell Tumors",
            "Gliomas",
            "Granular Cell Tumors and Alveolar Soft Part Sarcomas",
            "Hodgkin Lymphoma",
            "Immunoproliferative Diseases",
            "Leukemias, NOS",
            "Lipomatous Neoplasms",
            "Lymphatic Vessel Tumors",
            "Lymphoid Leukemias",
            "Malignant Lymphomas, NOS or Diffuse",
            "Mast Cell Tumors",
            "Mature B-Cell Lymphomas",
            "Mature T- and NK-Cell Lymphomas",
            "Meningiomas",
            "Mesonephromas",
            "Mesothelial Neoplasms",
            "Miscellaneous Bone Tumors",
            "Miscellaneous Tumors",
            "Mucoepidermoid Neoplasms",
            "Myelodysplastic Syndromes",
            "Myeloid Leukemias",
            "Myomatous Neoplasms",
            "Myxomatous Neoplasms",
            "Neoplasms of Histiocytes and Accessory Lymphoid Cells",
            "Neoplasms, NOS",
            "Nerve Sheath Tumors",
            "Neuroepitheliomatous Neoplasms",
            "Nevi and Melanomas",
            "Not Applicable",
            "Not Reported",
            "Odontogenic Tumors",
            "Osseous and Chondromatous Neoplasms",
            "Other Hematologic Disorders",
            "Other Leukemias",
            "Paragangliomas and Glomus Tumors",
            "Plasma Cell Tumors",
            "Precursor Cell Lymphoblastic Lymphoma",
            "Soft Tissue Tumors and Sarcomas, NOS",
            "Specialized Gonadal Neoplasms",
            "Squamous Cell Neoplasms",
            "Synovial-like Neoplasms",
            "Thymic Epithelial Neoplasms",
            "Transitional Cell Papillomas and Carcinomas",
            "Trophoblastic neoplasms",
            "Unknown",
        ],
    )
    def disease_type(self, value):
        self._set_property("disease_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Diagnosis",
            "First Patient Visit",
            "First Treatment",
            "Initial Genomic Sequencing",
            "Recurrence",
            "Sample Procurement",
            "Study Enrollment",
        ],
    )
    def index_date(self, value):
        self._set_property("index_date", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Unknown", "Yes"])
    def lost_to_followup(self, value):
        self._set_property("lost_to_followup", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Accessory sinuses",
            "Adrenal gland",
            "Anus and anal canal",
            "Base of tongue",
            "Bladder",
            "Bones, joints and articular cartilage of limbs",
            "Bones, joints and articular cartilage of other and unspecified sites",
            "Brain",
            "Breast",
            "Bronchus and lung",
            "Cervix uteri",
            "Colon",
            "Connective, subcutaneous and other soft tissues",
            "Corpus uteri",
            "Esophagus",
            "Eye and adnexa",
            "Floor of mouth",
            "Gallbladder",
            "Gum",
            "Heart, mediastinum, and pleura",
            "Hematopoietic and reticuloendothelial systems",
            "Hypopharynx",
            "Kidney",
            "Larynx",
            "Lip",
            "Liver and intrahepatic bile ducts",
            "Lymph nodes",
            "Meninges",
            "Nasal cavity and middle ear",
            "Nasopharynx",
            "Not Applicable",
            "Not Reported",
            "Oropharynx",
            "Other and ill-defined digestive organs",
            "Other and ill-defined sites",
            "Other and ill-defined sites in lip, oral cavity and pharynx",
            "Other and ill-defined sites within respiratory system and intrathoracic organs",
            "Other and unspecified female genital organs",
            "Other and unspecified major salivary glands",
            "Other and unspecified male genital organs",
            "Other and unspecified parts of biliary tract",
            "Other and unspecified parts of mouth",
            "Other and unspecified parts of tongue",
            "Other and unspecified urinary organs",
            "Other endocrine glands and related structures",
            "Ovary",
            "Palate",
            "Pancreas",
            "Parotid gland",
            "Penis",
            "Peripheral nerves and autonomic nervous system",
            "Placenta",
            "Prostate gland",
            "Pyriform sinus",
            "Rectosigmoid junction",
            "Rectum",
            "Renal pelvis",
            "Retroperitoneum and peritoneum",
            "Skin",
            "Small intestine",
            "Spinal cord, cranial nerves, and other parts of central nervous system",
            "Stomach",
            "Testis",
            "Thymus",
            "Thyroid gland",
            "Tonsil",
            "Trachea",
            "Unknown",
            "Ureter",
            "Uterus, NOS",
            "Vagina",
            "Vulva",
        ],
    )
    def primary_site(self, value):
        self._set_property("primary_site", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Case)
datetime_hooks.cls_inject_updated_datetime_hook(Case)
