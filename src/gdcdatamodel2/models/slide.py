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


class Slide(base.Node):
    __tablename__: str = "node_slide"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Slide",
        "namespace": "https://gdc.cancer.gov",
        "category": "biospecimen",
        "submittable": True,
        "downloadable": False,
        "description": "A digital image, microscopic or otherwise, of any sample, portion, or sub-part thereof. (GDC)",
        "required": ["submitter_id", "section_location"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "exclusive": False,
                "required": True,
                "subgroup": [
                    {
                        "name": "portions",
                        "backref": "slides",
                        "label": "derived_from",
                        "target_type": "portion",
                        "multiplicity": "many_to_many",
                        "required": False,
                    },
                    {
                        "name": "samples",
                        "backref": "slides",
                        "label": "derived_from",
                        "target_type": "sample",
                        "multiplicity": "many_to_many",
                        "required": False,
                    },
                ],
            }
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
            "bone_marrow_malignant_cells": {
                "description": "The text term used to indicate whether there are malignant cells in the bone marrow.",
                "termDef": {
                    "term": "Malignant Bone Marrow Indicator",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Yes", "No", "Unknown", "Not Reported"],
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
            "number_proliferating_cells": {
                "description": "Numeric value that represents the count of proliferating cells determined during pathologic review of the sample slide(s).",
                "termDef": {
                    "term": "Pathology Review Slide Proliferating Cell Count",
                    "source": "caDSR",
                    "cde_id": 5432636,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432636%20and%20ver_nr=1.0",
                },
                "type": "integer",
                "minimum": 0,
            },
            "percent_follicular_component": {
                "description": "Numeric value that represents the percentage of follicular features found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Follicular Features Percentage Value",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_rhabdoid_features": {
                "description": "Numeric value that represents the percentage of rhabdoid features found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Rhabdoid Features Percentage Value",
                    "source": "caDSR",
                    "cde_id": 6790120,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6790120%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_sarcomatoid_features": {
                "description": "Numeric value that represents the percentage of sarcomatoid features found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Sarcomatoid Features Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2429786,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2429786%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_tumor_cells": {
                "description": "Numeric value that represents the percentage of infiltration by tumor cells in a sample.",
                "termDef": {
                    "term": "Specimen Tumor Cell Percentage Value",
                    "source": "caDSR",
                    "cde_id": 5432686,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432686%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_tumor_nuclei": {
                "description": "Numeric value to represent the percentage of tumor nuclei in a malignant neoplasm sample or specimen.",
                "termDef": {
                    "term": "Malignant Neoplasm Neoplasm Nucleus Percentage Cell Value",
                    "source": "caDSR",
                    "cde_id": 2841225,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2841225%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_normal_cells": {
                "description": "Numeric value to represent the percentage of normal cell content in a malignant tumor sample or specimen.",
                "termDef": {
                    "term": "Malignant Neoplasm Normal Cell Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2841233,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2841233%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_necrosis": {
                "description": "Numeric value to represent the percentage of cell death in a malignant tumor sample or specimen.",
                "termDef": {
                    "term": "Malignant Neoplasm Necrosis Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2841237,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2841237%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_stromal_cells": {
                "description": "Numeric value to represent the percentage of reactive cells that are present in a malignant tumor sample or specimen but are not malignant such as fibroblasts, vascular structures, etc.",
                "termDef": {
                    "term": "Malignant Neoplasm Stromal Cell Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2841241,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2841241%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_inflam_infiltration": {
                "description": "Numeric value to represent local response to cellular injury, marked by capillary dilatation, edema and leukocyte infiltration; clinically, inflammation is manifest by reddness, heat, pain, swelling and loss of function, with the need to heal damaged tissue.",
                "termDef": {
                    "term": "Specimen Inflammation Change Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2897695,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2897695%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_lymphocyte_infiltration": {
                "description": "Numeric value to represent the percentage of infiltration by lymphocytes in a solid tissue sample or specimen.",
                "termDef": {
                    "term": "Specimen Lymphocyte Infiltration Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2897710,
                    "cde_version": 2.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2897710%20and%20ver_nr=2.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_monocyte_infiltration": {
                "description": "Numeric value to represent the percentage of monocyte infiltration in a sample or specimen.",
                "termDef": {
                    "term": "Specimen Monocyte Infiltration Percentage Value",
                    "source": "caDSR",
                    "cde_id": 5455535,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5455535%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_granulocyte_infiltration": {
                "description": "Numeric value to represent the percentage of infiltration by granulocytes in a tumor sample or specimen.",
                "termDef": {
                    "term": "Specimen Granulocyte Infiltration Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2897705,
                    "cde_version": 2.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2897705%20and%20ver_nr=2.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_neutrophil_infiltration": {
                "description": "Numeric value to represent the percentage of infiltration by neutrophils in a tumor sample or specimen.",
                "termDef": {
                    "term": "Malignant Neoplasm Neutrophil Infiltration Percentage Cell Value",
                    "source": "caDSR",
                    "cde_id": 2841267,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2841267%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "percent_eosinophil_infiltration": {
                "description": "Numeric value to represent the percentage of infiltration by eosinophils in a tumor sample or specimen.",
                "termDef": {
                    "term": "Specimen Eosinophilia Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2897700,
                    "cde_version": 2.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2897700%20and%20ver_nr=2.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "prostatic_chips_positive_count": {
                "description": "The text term used to describe the number of positive prostatic chips, which are generated from transurethral resection of the prostate (TURP) procedures and are generally used for relieving urinary obstruction due to nodular hyperplasia of the prostate (benign prostatic hyperplasia).",
                "termDef": {
                    "term": "Prostate Chips Positive Count",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "prostatic_chips_total_count": {
                "description": "The text term used to describe the total number of prostatic chips, which are generated from transurethral resection of the prostate (TURP) procedures and are generally used for relieving urinary obstruction due to nodular hyperplasia of the prostate (benign prostatic hyperplasia).",
                "termDef": {
                    "term": "Prostate Chips Total Count",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "prostatic_involvement_percent": {
                "description": "Numeric value that represents the percentage of prostatic involvement found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Prostatic Involvement Percentage Value",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "section_location": {
                "description": "Tissue source of the slide.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "string",
            },
            "tissue_microarray_coordinates": {
                "description": "The alphanumeric term used to describe the coordinates of a specific tissue located on a tissue microarray slide.",
                "termDef": {
                    "term": "Tissue Microarray Coordinates Value",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "string",
                "pattern": "^[a-zA-Z]\\d{1,3}(,[a-zA-Z]\\d{1,3})*$",
            },
            "portions": {
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
            "samples": {
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
        return "slide"

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
                "name": "slides",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "files": {
                "name": "slides",
                "src_type": base.Node.get_subclass("file"),
            },
            "molecular_tests": {
                "name": "slides",
                "src_type": base.Node.get_subclass("molecular_test"),
            },
            "slide_images": {
                "name": "slides",
                "src_type": base.Node.get_subclass("slide_image"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "slides",
                "type": base.Node.get_subclass("annotation"),
            },
            "files": {
                "backref": "slides",
                "type": base.Node.get_subclass("file"),
            },
            "molecular_tests": {
                "backref": "slides",
                "type": base.Node.get_subclass("molecular_test"),
            },
            "portions": {
                "backref": "slides",
                "type": base.Node.get_subclass("portion"),
            },
            "samples": {
                "backref": "slides",
                "type": base.Node.get_subclass("sample"),
            },
            "slide_images": {
                "backref": "slides",
                "type": base.Node.get_subclass("slide_image"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "portions": {
                "edge_out": "_SlideDerivedFromPortion_out",
                "dst_type": base.Node.get_subclass("portion"),
            },
            "samples": {
                "edge_out": "_SlideDerivedFromSample_out",
                "dst_type": base.Node.get_subclass("sample"),
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

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def bone_marrow_malignant_cells(self, value):
        self._set_property("bone_marrow_malignant_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def number_proliferating_cells(self, value):
        self._set_property("number_proliferating_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_follicular_component(self, value):
        self._set_property("percent_follicular_component", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_rhabdoid_features(self, value):
        self._set_property("percent_rhabdoid_features", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_sarcomatoid_features(self, value):
        self._set_property("percent_sarcomatoid_features", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_tumor_cells(self, value):
        self._set_property("percent_tumor_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_tumor_nuclei(self, value):
        self._set_property("percent_tumor_nuclei", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_normal_cells(self, value):
        self._set_property("percent_normal_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_necrosis(self, value):
        self._set_property("percent_necrosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_stromal_cells(self, value):
        self._set_property("percent_stromal_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_inflam_infiltration(self, value):
        self._set_property("percent_inflam_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_lymphocyte_infiltration(self, value):
        self._set_property("percent_lymphocyte_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_monocyte_infiltration(self, value):
        self._set_property("percent_monocyte_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_granulocyte_infiltration(self, value):
        self._set_property("percent_granulocyte_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_neutrophil_infiltration(self, value):
        self._set_property("percent_neutrophil_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_eosinophil_infiltration(self, value):
        self._set_property("percent_eosinophil_infiltration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_positive_count(self, value):
        self._set_property("prostatic_chips_positive_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_total_count(self, value):
        self._set_property("prostatic_chips_total_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_involvement_percent(self, value):
        self._set_property("prostatic_involvement_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def section_location(self, value):
        self._set_property("section_location", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def tissue_microarray_coordinates(self, value):
        self._set_property("tissue_microarray_coordinates", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Slide)
datetime_hooks.cls_inject_updated_datetime_hook(Slide)
