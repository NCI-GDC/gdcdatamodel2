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
        "links": [
            {
                "name": "diagnoses",
                "backref": "pathology_details",
                "label": "describes",
                "target_type": "diagnosis",
                "multiplicity": "many_to_one",
                "required": True,
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
            "additional_pathology_findings": {
                "description": "A section header that includes additional pathologic findings.",
                "termDef": {
                    "term": "Additional Pathologic Findings",
                    "source": "NCIt",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                    "term_id": "C158809",
                    "term_version": "20.10d",
                },
                "enum": [
                    "Adenomyosis",
                    "Atrophic endometrium",
                    "Atypical hyperplasia/Endometrial intraepithelial neoplasia (EIN)",
                    "Autoimmune atrophic chronic gastritis",
                    "Asbestos bodies",
                    "Benign endocervical polyp",
                    "Bilateral ovaries with endometriotic cyst and surface adhesions",
                    "Bone marrow concordant histology",
                    "Bone marrow discordant histology",
                    "Carcinoma in situ",
                    "Cirrhosis",
                    "Clostridioides difficile (c. diff)",
                    "Colonization; bacterial",
                    "Colonization; fungal",
                    "Cyst(s)",
                    "Diffuse and early nodular diabetic glomerulosclerosis",
                    "Dysplasia; high grade",
                    "Dysplasia; low grade",
                    "Endometrial polyp",
                    "Endometriosis",
                    "Endometroid carcinoma with local mucinous differentiation",
                    "Endosalpingiosis",
                    "Epithelial dysplasia",
                    "Epithelial hyperplasia",
                    "Gallbladder adenomyomatosis",
                    "Glomerular disease",
                    "Hyperkeratosis",
                    "Inflammation",
                    "Intestinal metaplasia",
                    "Keratinizing dysplasia; mild",
                    "Keratinizing dysplasia; moderate",
                    "Keratinizing dysplasia; severe (carcinoma in situ)",
                    "Leiomyoma",
                    "Leiomyomata w/ degenerative changes",
                    "Nonkeratinizing dysplasia; mild",
                    "Nonkeratinizing dysplasia; moderate",
                    "Nonkeratinizing dysplasia; severe (carcinoma in situ)",
                    "Other",
                    "Percent follicular component <= 10%",
                    "Percent follicular component > 10%",
                    "PD-L1 CPS (223C LDT) - 20%",
                    "Platinum-resistant",
                    "Pleural plaque",
                    "Pulmonary interstitial fibrosis",
                    "Sialadenitis",
                    "Sinonasal papilloma",
                    "Squamous metaplasia",
                    "Squamous papilloma; solitary",
                    "Squamous papillomatosis",
                    "Tubular (papillary) adenoma(s)",
                    "Tumor-associated lymphoid proliferation",
                    "Tumor has rough spikey edges",
                ],
            },
            "anaplasia_present": {
                "description": "Yes/no/unknown/not reported indicator used to describe whether anaplasia was present at the time of diagnosis.",
                "termDef": {
                    "term": "Anaplastic Lesion Present Indicator",
                    "source": "caDSR",
                    "cde_id": 6059599,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6059599&version=1.0",
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
            "anaplasia_present_type": {
                "description": "The text term used to describe the morphologic findings indicating the presence of a malignant cellular infiltrate characterized by the presence of large pleomorphic cells, necrosis, and high mitotic activity in a tissue sample.",
                "termDef": {
                    "term": "Anaplastic Lesion Classification Category",
                    "source": "caDSR",
                    "cde_id": 4925534,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=4925534&version=1.0",
                },
                "enum": [
                    "Absent",
                    "Diffuse",
                    "Equivocal",
                    "Focal",
                    "Present",
                    "Sclerosis",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Present": {
                        "description": "A morphologic finding indicating the presence of a malignant cellular infiltrate characterized by the presence of large pleomorphic cells, necrosis, and high mitotic activity in a tissue sample.",
                        "termDef": {
                            "term": "Anaplastic Lesion",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C36113",
                            "term_id": "C36113",
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
            "breslow_thickness": {
                "description": "The number that describes the distance, in millimeters, between the upper layer of the epidermis and the deepest point of tumor penetration.",
                "termDef": {
                    "term": "Breslow Depth Measurement",
                    "source": "caDSR",
                    "cde_id": 64809,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=64809&version=3.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "circumferential_resection_margin": {
                "description": "Numeric value used to describe the non-peritonealised bare area of rectum, comprising anterior and posterior segments, when submitted as a surgical specimen resulting from excision of cancer of the rectum.",
                "termDef": {
                    "term": "Circumferential Resection Margin Measurement",
                    "source": "caDSR",
                    "cde_id": 6161030,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6161030&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "columnar_mucosa_present": {
                "description": "Indicator noting whether columnar mucosa was present within the tissue.",
                "termDef": {
                    "term": None,
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
            "consistent_pathology_review": {
                "description": "Indicates whether a recent review of tissue is consistent with a prior pathology review.",
                "termDef": {
                    "term": "Consistent Pathology Review",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Yes", "No", "Not Reported"],
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
            "dysplasia_degree": {
                "description": "The degree to which dysplasia was involved.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "High Grade",
                    "Indefinite",
                    "Low Grade",
                    "Mild",
                    "Moderate",
                    "No Dysplasia",
                    "Severe",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "High Grade": {
                        "description": "A subjective characterization of the phenomenon of dysplasia, based on microscopic examination of the architectural and/or cytological changes in a tissue sample, that is determined to be high.",
                        "termDef": {
                            "term": "High Grade Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156083",
                            "term_id": "C156083",
                            "term_version": "20.10d",
                        },
                    },
                    "Indefinite": {
                        "description": "An indication that there is an ambiguous morphological pattern in a tissue sample such that the presence or absence of dysplasia cannot be determined.",
                        "termDef": {
                            "term": "Indefinite Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164039",
                            "term_id": "C164039",
                            "term_version": "20.10d",
                        },
                    },
                    "Low Grade": {
                        "description": "A subjective characterization of the phenomenon of dysplasia, based on microscopic examination of the architectural and/or cytological changes in a tissue sample, that is determined to be low.",
                        "termDef": {
                            "term": "Low Grade Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156084",
                            "term_id": "C156084",
                            "term_version": "20.10d",
                        },
                    },
                    "Mild": {
                        "description": "Gentle or temperate in nature or degree.",
                        "termDef": {
                            "term": "Mild",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C70666",
                            "term_id": "C70666",
                            "term_version": "20.10d",
                        },
                    },
                    "Moderate": {
                        "description": "The quality of being within reasonable or average limits; not excessive or extreme.",
                        "termDef": {
                            "term": "Moderate",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C61376",
                            "term_id": "C61376",
                            "term_version": "20.10d",
                        },
                    },
                    "No Dysplasia": {
                        "description": "An indication that signs of dysplasia were not found in a sample.",
                        "termDef": {
                            "term": "Dysplasia Negative",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164040",
                            "term_id": "C164040",
                            "term_version": "20.10d",
                        },
                    },
                    "Severe": {
                        "description": "Intensely bad or unpleasant in degree, quality or extent.",
                        "termDef": {
                            "term": "Severe",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C70667",
                            "term_id": "C70667",
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
            "dysplasia_type": {
                "description": "The type of dysplasia involved.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Epithelial",
                    "Esophageal Columnar Dysplasia",
                    "Esophageal Mucosa Columnar Dysplasia",
                    "Keratinizing",
                    "Nonkeratinizing",
                    "Other",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Esophageal Columnar Dysplasia": {
                        "description": "A morphologic finding the replacement of the normal lower esophagus squamous epithelium with columnar epithelium.",
                        "termDef": {
                            "term": "Esophageal Columnar Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C174120",
                            "term_id": "C174120",
                            "term_version": "20.10d",
                        },
                    },
                    "Keratinizing": {
                        "description": "Epithelial dysplasia in which the dysplastic changes, although limited to the lower basal zone, are so severe that there is a high probability of progression to invasive carcinoma.",
                        "termDef": {
                            "term": "Keratinizing Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C161017",
                            "term_id": "C161017",
                            "term_version": "20.10d",
                        },
                    },
                    "Nonkeratinizing": {
                        "description": "Epithelial dysplasia in which there is continuum from mild dysplasia to moderate dysplasia to severe dysplasia before the development of invasive carcinoma.",
                        "termDef": {
                            "term": "Non-Keratinizing Dysplasia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C161016",
                            "term_id": "C161016",
                            "term_version": "20.10d",
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
            "extracapsular_extension": {
                "description": "The extension of malignant tissue situated outside of a specific capsule.",
                "termDef": {
                    "term": "Extracapsular",
                    "source": "NCIt",
                    "cde_id": "C25502",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25502",
                },
                "enum": ["Extensive", "Focal", "Not Reported"],
            },
            "extranodal_extension": {
                "description": "Extension of a malignant neoplasm beyond the lymph node capsule.",
                "termDef": {
                    "term": "Extranodal Involvement",
                    "source": "NCIt",
                    "cde_id": "C117309",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C117309",
                },
                "enum": [
                    "Gross Extension",
                    "Microscopic Extension",
                    "No Extranodal Extension",
                ],
            },
            "extrascleral_extension": {
                "description": "Spread of uveal melanoma beyond the sclera.",
                "termDef": {
                    "term": "Extrascleral Extension of Uveal Melanoma",
                    "source": "NCIt",
                    "cde_id": "C111028",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C111028",
                },
                "type": "boolean",
            },
            "greatest_tumor_dimension": {
                "description": "Numeric value that represents the measurement of the widest portion of the tumor in centimeters.",
                "termDef": {
                    "term": "Tumor Longest Dimension Centimeters Measurement",
                    "source": "NCIt",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C157135",
                    "term_id": "C157135",
                    "term_version": "19.12e",
                },
                "type": "number",
                "minimum": 0,
            },
            "gross_tumor_weight": {
                "description": "Numeric value used to describe the gross pathologic tumor weight, measured in grams.",
                "termDef": {
                    "term": "Tumor Tissue Weight Number",
                    "source": "caDSR",
                    "cde_id": 6133606,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6133606&version=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "largest_extrapelvic_peritoneal_focus": {
                "description": "The text term used to describe the diameter of the largest focus originating outside of the pelvic peritoneal region.",
                "termDef": {
                    "term": "Neoplasm Largest External Pelvic Peritoneal Focus Diameter Measurement",
                    "source": "caDSR",
                    "cde_id": 6690680,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6690680&version=1.0",
                },
                "enum": [
                    "Macroscopic (2cm or less)",
                    "Macroscopic (greater than 2cm)",
                    "Microscopic",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Macroscopic (2cm or less)": {
                        "description": "Lesion with Diameter of 2 cm or Less",
                        "termDef": {
                            "term": "Lesion with Diameter of 2cm or Less",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C53696",
                            "term_id": "C53696",
                            "term_version": "20.05a",
                        },
                    },
                    "Macroscopic (greater than 2cm)": {
                        "description": "Lesion with Diameter Greater than 2 cm",
                        "termDef": {
                            "term": "Lesion with Diameter Greater than 2cm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C51138",
                            "term_id": "C51138",
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
            "lymph_node_dissection_method": {
                "description": "The method employed to remove a lymph nodes(s)",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Functional (Limited) Neck Dissection",
                    "Modified Radical Neck Dissection",
                    "Radical Neck Dissection",
                ],
            },
            "lymph_node_dissection_site": {
                "description": "The named location(s) within the body where a lymph node(s) were removed.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Neck, Left", "Neck, Right", "Neck, NOS"],
            },
            "lymph_node_involved_site": {
                "description": "The text term used to describe the anatomic site of lymph node involvement.",
                "termDef": {
                    "term": "Lymph Node Involved Site",
                    "source": "NCIt",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C33027",
                    "term_id": "C33027",
                    "term_version": "19.12e",
                },
                "enum": [
                    "Aortic",
                    "Axillary",
                    "Cervical",
                    "Epitrochlear",
                    "Femoral",
                    "Hilar",
                    "Iliac-common",
                    "Iliac-external",
                    "Iliac, NOS",
                    "Inguinal",
                    "Mediastinal",
                    "Mesenteric",
                    "None",
                    "Occipital",
                    "Paraaortic",
                    "Parotid",
                    "Pelvis, NOS",
                    "Popliteal",
                    "Retroperitoneal",
                    "Splenic",
                    "Submandibular",
                    "Supraclavicular",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Axillary": {
                        "description": "One of approximately 20-30 lymph nodes in chain formation that traverse the concavity of the underarm to the clavicle.",
                        "termDef": {
                            "term": "Axillary Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12904",
                            "term_id": "C12904",
                            "term_version": "20.10d",
                        },
                    },
                    "Cervical": {
                        "description": "Any of the lymph nodes located in the neck.",
                        "termDef": {
                            "term": "Cervical Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C32298",
                            "term_id": "C32298",
                            "term_version": "20.10d",
                        },
                    },
                    "Epitrochlear": {
                        "description": "A lymph node located above and adjacent to the elbow.",
                        "termDef": {
                            "term": "Epitrochlear Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C98182",
                            "term_id": "C98182",
                            "term_version": "20.10d",
                        },
                    },
                    "Femoral": {
                        "description": "A lymph node located in the upper inner portion of the thigh.",
                        "termDef": {
                            "term": "Femoral Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C98183",
                            "term_id": "C98183",
                            "term_version": "20.10d",
                        },
                    },
                    "Hilar": {
                        "description": "A lymph node located in the area around the hilum.",
                        "termDef": {
                            "term": "Perihilar Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C102330",
                            "term_id": "C102330",
                            "term_version": "20.10d",
                        },
                    },
                    "Iliac-common": {
                        "description": "A lymph node located adjacent to the common iliac artery. (NCI)",
                        "termDef": {
                            "term": "Common Iliac Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C103384",
                            "term_id": "C103384",
                            "term_version": "20.10d",
                        },
                    },
                    "Iliac-external": {
                        "description": "A lymph node located along the external iliac artery.",
                        "termDef": {
                            "term": "External Iliac Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C88143",
                            "term_id": "C88143",
                            "term_version": "20.10d",
                        },
                    },
                    "Iliac, NOS": {
                        "description": "One of the three lymph nodes of the pelvis: the superior gluteal, interior gluteal or sacral.",
                        "termDef": {
                            "term": "Iliac Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C32761",
                            "term_id": "C32761",
                            "term_version": "20.10d",
                        },
                    },
                    "Inguinal": {
                        "description": "A superficial or deep lymph node located in the inguinal area.",
                        "termDef": {
                            "term": "Inguinal Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C32801",
                            "term_id": "C32801",
                            "term_version": "20.10d",
                        },
                    },
                    "Mediastinal": {
                        "description": "A lymph node located in the mediastinum. Mediastinal lymph nodes are arranged in three groups, one on the lateral, another on the medial, and a third on the anterior aspect of the vessels; the third group is, however, sometimes absent.",
                        "termDef": {
                            "term": "Mediastinal Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C33073",
                            "term_id": "C33073",
                            "term_version": "20.10d",
                        },
                    },
                    "Mesenteric": {
                        "description": "A lymph node located in the mesentery.",
                        "termDef": {
                            "term": "Mesenteric Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C77641",
                            "term_id": "C77641",
                            "term_version": "20.10d",
                        },
                    },
                    "None": {
                        "description": "No person or thing, nobody, not any.",
                        "termDef": {
                            "term": "None",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C41132",
                            "term_id": "C41132",
                            "term_version": "20.10d",
                        },
                    },
                    "Occipital": {
                        "description": "A lymph node located in the back of the head adjacent to the trapezius muscle.",
                        "termDef": {
                            "term": "Occipital Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C98188",
                            "term_id": "C98188",
                            "term_version": "20.10d",
                        },
                    },
                    "Paraaortic": {
                        "description": "A lymph node located adjacent to the lumbar region of the spine.",
                        "termDef": {
                            "term": "Paraaortic Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C77643",
                            "term_id": "C77643",
                            "term_version": "20.10d",
                        },
                    },
                    "Parotid": {
                        "description": "A lymph node located close to, on, or within the parotid gland.",
                        "termDef": {
                            "term": "Parotid Gland Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C33278",
                            "term_id": "C33278",
                            "term_version": "20.10d",
                        },
                    },
                    "Popliteal": {
                        "description": "Lymph node located within the fat layer of the knee joint.",
                        "termDef": {
                            "term": "Popliteal Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C53146",
                            "term_id": "C53146",
                            "term_version": "20.10d",
                        },
                    },
                    "Retroperitoneal": {
                        "description": "A lymph node located in the retroperitoneal space.",
                        "termDef": {
                            "term": "Retroperitoneal Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C98189",
                            "term_id": "C98189",
                            "term_version": "20.10d",
                        },
                    },
                    "Splenic": {
                        "description": "Any lymph node located along the splenic artery that receives afferent drainage from the pancreas, spleen, and stomach, and which generally has their efferents join the celiac group of preaortic lymph nodes.",
                        "termDef": {
                            "term": "Splenic Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C142320",
                            "term_id": "C142320",
                            "term_version": "20.10d",
                        },
                    },
                    "Submandibular": {
                        "description": "A lymph node located beneath the floor of the oral cavity.",
                        "termDef": {
                            "term": "Submandibular Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C77650",
                            "term_id": "C77650",
                            "term_version": "20.10d",
                        },
                    },
                    "Supraclavicular": {
                        "description": "A lymph node which is located above the clavicle.",
                        "termDef": {
                            "term": "Supraclavicular Lymph Node",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C12903",
                            "term_id": "C12903",
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
            "lymph_node_involvement": {
                "description": "Indicator noting whether lymph nodes were involved.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Indeterminant",
                    "Negative",
                    "Positive",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
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
                    "Negative": {
                        "description": "A finding of normality following an examination or investigation looking for the presence of a microorganism, disease, or condition.",
                        "termDef": {
                            "term": "Negative Finding",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C38757",
                            "term_id": "C38757",
                            "term_version": "20.10d",
                        },
                    },
                    "Positive": {
                        "description": "A finding of abnormality following an examination or observation confirming something, such as the presence of a disease, condition, or microorganism.",
                        "termDef": {
                            "term": "Positive Finding",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C38758",
                            "term_id": "C38758",
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
            "lymph_nodes_positive": {
                "description": "The number of lymph nodes involved with disease as determined by pathologic examination.",
                "termDef": {
                    "term": "Lymph Node(s) Positive Number",
                    "source": "caDSR",
                    "cde_id": 89,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=89&version=3.0",
                },
                "type": "integer",
                "minimum": 0,
            },
            "lymph_nodes_removed": {
                "description": "The number of lymph nodes removed during a biopsy or surgical procedure.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["No", "Yes", "Not Reported"],
            },
            "lymph_nodes_tested": {
                "description": "The number of lymph nodes tested to determine whether lymph nodes were involved with disease as determined by a pathologic examination.",
                "termDef": {
                    "term": "Lymph Node Examined Count",
                    "source": "caDSR",
                    "cde_id": 3,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3&version=3.0",
                },
                "type": "integer",
                "minimum": 0,
            },
            "lymphatic_invasion_present": {
                "description": "A yes/no indicator to ask if small or thin-walled vessel invasion is present, indicating lymphatic involvement",
                "termDef": {
                    "term": "Lymphatic/Small vessel Invasion Ind",
                    "source": "caDSR",
                    "cde_id": 64171,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=64171&version=3.0",
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
            "margin_status": {
                "description": "The determination of the presence of actual or potential neoplastic tissue which has been left outside the boundary of a resected specimen within the patient.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Involved",
                    "Uninvolved",
                    "Indeterminant",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Involved": {
                        "description": "Specifies whether the margins of surgical resection are infiltrated by disease.",
                        "termDef": {
                            "term": "Involved Surgical Margin Indicator",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C93581",
                            "term_id": "C93581",
                            "term_version": "20.10d",
                        },
                    },
                    "Uninvolved": {
                        "description": "Indicates the absence of tumor cells at the edge of a surgically excised specimen.",
                        "termDef": {
                            "term": "Negative Surgical Margin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C48621",
                            "term_id": "C48621",
                            "term_version": "20.10d",
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
            "metaplasia_present": {
                "description": "Indicator noting whether metaplasia was present.",
                "termDef": {
                    "term": None,
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
            "morphologic_architectural_pattern": {
                "description": "A specific morphologic or pathologic architectural pattern was discovered within the sample studied.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Cohesive",
                    "Cribiform",
                    "Micropapillary",
                    "Non-cohesive",
                    "Papillary Renal Cell",
                    "Papillary, NOS",
                    "Solid",
                    "Tubular",
                ],
                "enumDef": {
                    "Cribiform": {
                        "description": "A morphologic finding indicating the presence of sheets of malignant epithelial cells punctuated by gland-like spaces in a tissue sample.",
                        "termDef": {
                            "term": "Cribriform Pattern",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C35920",
                            "term_id": "C35920",
                            "term_version": "20.10d",
                        },
                    },
                    "Micropapillary": {
                        "description": "A morphologic finding indicating the presence of an architectural pattern dominated by the presence of small papillary structures.",
                        "termDef": {
                            "term": "Micropapillary Pattern",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C36181",
                            "term_id": "C36181",
                            "term_version": "20.10d",
                        },
                    },
                    "Papillary Renal Cell": {
                        "description": "Also known as chromophil carcinoma, it represents a minority of renal cell carcinomas. It can be hereditary or sporadic. The sporadic papillary renal cell carcinoma is characterized by trisomy of chromosomes 7, 16, and 17, and loss of chromosome Y. The peak incidence is in the sixth and seven decades. It is classified as type 1 or 2, based on the cytoplasmic volume and the thickness of the lining neoplastic cells. The prognosis is more favorable than for conventional (clear cell) renal cell carcinoma.",
                        "termDef": {
                            "term": "Papillary Renal Cell Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C6975",
                            "term_id": "C6975",
                            "term_version": "20.10d",
                        },
                    },
                    "Papillary, NOS": {
                        "description": "A morphologic finding indicating the presence of a cellular infiltrate with papillary growth in a tissue sample.",
                        "termDef": {
                            "term": "Papillary Pattern",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C35911",
                            "term_id": "C35911",
                            "term_version": "20.10d",
                        },
                    },
                    "Solid": {
                        "description": "A microscopic finding indicating that the neoplastic cells are arranged in solid sheets in a tumor sample.",
                        "termDef": {
                            "term": "Solid Growth Pattern",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C36182",
                            "term_id": "C36182",
                            "term_version": "20.10d",
                        },
                    },
                    "Tubular": {
                        "description": "A morphological appearance characteristic of neoplasms which arise from the glandular or ductal (or both) epithelium, consisting of glandular or ductal neoplastic proliferations forming small tubules with a lumen lined by neoplastic cells.",
                        "termDef": {
                            "term": "Tubular Pattern",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C35925",
                            "term_id": "C35925",
                            "term_version": "20.10d",
                        },
                    },
                },
            },
            "necrosis_percent": {
                "description": "A quantitative measurement of the percent of cells undergoing necrosis compared to the number of total cells present in a sample.",
                "termDef": {
                    "term": "Percent of Necrosis",
                    "source": "NCIt",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                    "term_id": "C159481",
                    "term_version": "20.10d",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "necrosis_present": {
                "description": "Indicator describing whether the presence of necrosis was confirmed.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Yes", "No", "Not Reported"],
                "enumDef": {
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
                    }
                },
            },
            "non_nodal_regional_disease": {
                "description": "The text term used to describe whether the patient had non-nodal regional disease.",
                "termDef": {
                    "term": None,
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Absent",
                    "Indeterminate",
                    "Present",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Present": {
                        "description": "A finding of abnormality following an examination or observation confirming something, such as the presence of a disease, condition, or microorganism.",
                        "termDef": {
                            "term": "Positive Finding",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C38758",
                            "term_id": "C38758",
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
            "non_nodal_tumor_deposits": {
                "description": "The yes/no/unknown indicator used to describe the presence of tumor deposits in the pericolic or perirectal fat or in adjacent mesentery away from the leading edge of the tumor.",
                "termDef": {
                    "term": "Resected Biospecimen NonNodal Tumor Deposits Indicator",
                    "source": "caDSR",
                    "cde_id": 3107051,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3107051&version=1.0",
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
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5432636&version=1.0",
                },
                "type": "integer",
                "minimum": 0,
            },
            "percent_tumor_invasion": {
                "description": "The percentage of tumor cells spread locally in a malignant neoplasm through infiltration or destruction of adjacent tissue.",
                "termDef": {
                    "term": None,
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
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
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=2841225&version=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "perineural_invasion_present": {
                "description": "a yes/no indicator to ask if perineural invasion or infiltration of tumor or cancer is present.",
                "termDef": {
                    "term": "Tumor Perineural Invasion Ind",
                    "source": "caDSR",
                    "cde_id": 64181,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=64181&version=3.0",
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
            "peripancreatic_lymph_nodes_positive": {
                "description": "Enumerated numeric value or range of values used to describe the number of peripancreatic lymph nodes determined to be positive.",
                "termDef": {
                    "term": "Peripancreatic Lymph Node Positive Finding Range",
                    "source": "caDSR",
                    "cde_id": 5983082,
                    "cde_version": 2.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5983082&version=2.0",
                },
                "enum": ["0", "1-3", "4 or More", "Unknown", "Not Reported"],
                "enumDef": {
                    "0": {
                        "description": "A mathematical element that when added to another number yields the same number; the cardinal number meaning one less than one.",
                        "termDef": {
                            "term": "Zero",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C70430",
                            "term_id": "C70430",
                            "term_version": "20.05a",
                        },
                    },
                    "1-3": {
                        "description": "An indication that cancer cells have been detected in one, two or three lymph nodes.",
                        "termDef": {
                            "term": "One to Three Positive Lymph Nodes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C172224",
                            "term_id": "C172224",
                            "term_version": "20.10d",
                        },
                    },
                    "4 or More": {
                        "description": "An indication that cancer cells have been detected in four or more lymph nodes.",
                        "termDef": {
                            "term": "Four or More Positive Lymph Nodes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C172226",
                            "term_id": "C172226",
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
            "peripancreatic_lymph_nodes_tested": {
                "description": "The total number of peripancreatic lymph nodes tested for the presence of pancreatic cancer cells.",
                "termDef": {
                    "term": "Peripancreatic Lymph Node Examined Count",
                    "source": "caDSR",
                    "cde_id": 6050944,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6050944&version=1.0",
                },
                "type": "integer",
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
            "residual_tumor": {
                "description": "Tumor cells that remain in the body following cancer treatment.",
                "termDef": {
                    "term": "Residual Disease",
                    "source": "NCIt",
                    "cde_id": "C4809",
                    "cde_version": "21.04d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4809",
                },
                "enum": ["RX", "R0", "R1", "R2"],
            },
            "residual_tumor_measurement": {
                "description": "A measurement of the tumor cells that remain in the body following cancer treatment.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["1-10 mm", "11-20 mm", ">20 mm", "No macroscopic disease"],
            },
            "rhabdoid_percent": {
                "description": "Numeric value that represents the percentage of rhabdoid features found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Rhabdoid Features Percentage Value",
                    "source": "caDSR",
                    "cde_id": 6790120,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6790120&version=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "rhabdoid_present": {
                "description": "Indicator describing whether rhabdoid features were present.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Yes", "No", "Not Reported"],
                "enumDef": {
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
                    }
                },
            },
            "sarcomatoid_percent": {
                "description": "Numeric value that represents the percentage of sarcomatoid features found in a specific tissue sample.",
                "termDef": {
                    "term": "Specimen Sarcomatoid Features Percentage Value",
                    "source": "caDSR",
                    "cde_id": 2429786,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=2429786&version=1.0",
                },
                "type": "number",
                "maximum": 100,
                "minimum": 0,
            },
            "sarcomatoid_present": {
                "description": "Indicator describing whether sarcomatoid features were present.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Yes", "No", "Not Reported"],
                "enumDef": {
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
                    }
                },
            },
            "size_extraocular_nodule": {
                "description": "The size of the nodule that is outside the eye.",
                "termDef": {
                    "term": "Extraocular Nodule Size",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "transglottic_extension": {
                "description": "The text term used to describe an extension of the tumor beyond the opening into the ventricles and vocal cords.",
                "termDef": {
                    "term": "Transglottic Extension",
                    "source": "NCIt",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C160996",
                    "term_id": "C160996",
                    "term_version": "19.12e",
                },
                "enum": ["Absent", "Present", "Unknown", "Not Reported"],
                "enumDef": {
                    "Present": {
                        "description": "Extension of a laryngeal tumor beyond the glottic opening into the ventricles and vocal cords.",
                        "termDef": {
                            "term": "Transglottic Extension of Laryngeal Tumor",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C160996",
                            "term_id": "C160996",
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
            "tumor_largest_dimension_diameter": {
                "description": "Numeric value used to describe the maximum diameter or dimension of the primary tumor, measured in centimeters.",
                "termDef": {
                    "term": "Tumor Largest Dimension Measurement",
                    "source": "caDSR",
                    "cde_id": 64215,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=64215&version=3.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "tumor_level_prostate": {
                "description": "The level(s) of the prostate from which the tumor originated.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "array",
                "items": {"enum": ["Apex", "Middle", "Base"]},
            },
            "tumor_thickness": {
                "description": "A measurement of the thickness of a sectioned slice (of tissue or mineral or other substance) in millimeters (mm).",
                "termDef": {
                    "term": "Section Thickness",
                    "source": "NCIt",
                    "cde_id": "C176286",
                    "cde_version": "21.04d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C176286",
                },
                "type": "number",
                "minimum": 0,
            },
            "vascular_invasion_present": {
                "description": "The yes/no indicator to ask if large vessel or venous invasion was detected by surgery or presence in a tumor specimen.",
                "termDef": {
                    "term": "Tumor Vascular Invasion Ind-3",
                    "source": "caDSR",
                    "cde_id": 64358,
                    "cde_version": 3.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=64358&version=3.0",
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
            "vascular_invasion_type": {
                "description": "Text term that represents the type of vascular tumor invasion.",
                "termDef": {
                    "term": "Vascular Tumor Cell Invasion Type",
                    "source": "caDSR",
                    "cde_id": 3168001,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=3168001&version=1.0",
                },
                "enum": [
                    "Extramural",
                    "Intramural",
                    "Macro",
                    "Micro",
                    "No Vascular Invasion",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "No Vascular Invasion": {
                        "description": "An indication that signs of vascular invasion have not been found in a sample.",
                        "termDef": {
                            "term": "Vascular Invasion Negative",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164046",
                            "term_id": "C164046",
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
            "zone_of_origin_prostate": {
                "description": "The location or position of the tumor by zone of the prostate.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Peripheral zone",
                    "Transition zone",
                    "Central zone",
                    "Overlapping/multiple zones",
                    "Unknown zone",
                ],
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
        },
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
            "Adenomyosis",
            "Asbestos bodies",
            "Atrophic endometrium",
            "Atypical hyperplasia/Endometrial intraepithelial neoplasia (EIN)",
            "Autoimmune atrophic chronic gastritis",
            "Benign endocervical polyp",
            "Bilateral ovaries with endometriotic cyst and surface adhesions",
            "Bone marrow concordant histology",
            "Bone marrow discordant histology",
            "Carcinoma in situ",
            "Cirrhosis",
            "Clostridioides difficile (c. diff)",
            "Colonization; bacterial",
            "Colonization; fungal",
            "Cyst(s)",
            "Diffuse and early nodular diabetic glomerulosclerosis",
            "Dysplasia; high grade",
            "Dysplasia; low grade",
            "Endometrial polyp",
            "Endometriosis",
            "Endometroid carcinoma with local mucinous differentiation",
            "Endosalpingiosis",
            "Epithelial dysplasia",
            "Epithelial hyperplasia",
            "Extravascular Matrix Loops",
            "Gallbladder adenomyomatosis",
            "Glomerular disease",
            "Hyperkeratosis",
            "Inflammation",
            "Intestinal metaplasia",
            "Keratinizing dysplasia; mild",
            "Keratinizing dysplasia; moderate",
            "Keratinizing dysplasia; severe (carcinoma in situ)",
            "Leiomyoma",
            "Leiomyomata w/ degenerative changes",
            "Nonkeratinizing dysplasia; mild",
            "Nonkeratinizing dysplasia; moderate",
            "Nonkeratinizing dysplasia; severe (carcinoma in situ)",
            "Other",
            "Other Complex Extravascular Matrix Patterns",
            "PD-L1 CPS (223C LDT) - 20%",
            "Percent follicular component <= 10%",
            "Percent follicular component > 10%",
            "Platinum-resistant",
            "Pleural plaque",
            "Poorly Differentiated",
            "Pulmonary interstitial fibrosis",
            "Sialadenitis",
            "Sinonasal papilloma",
            "Squamous metaplasia",
            "Squamous papilloma; solitary",
            "Squamous papillomatosis",
            "Tubular (papillary) adenoma(s)",
            "Tumor has rough spikey edges",
            "Tumor-associated lymphoid proliferation",
            "Well Differentiated",
        ],
    )
    def additional_pathology_findings(self, value):
        self._set_property("additional_pathology_findings", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def anaplasia_present(self, value):
        self._set_property("anaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Absent",
            "Diffuse",
            "Equivocal",
            "Focal",
            "Not Reported",
            "Present",
            "Sclerosis",
            "Unknown",
        ],
    )
    def anaplasia_present_type(self, value):
        self._set_property("anaplasia_present_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def bone_marrow_malignant_cells(self, value):
        self._set_property("bone_marrow_malignant_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def breslow_thickness(self, value):
        self._set_property("breslow_thickness", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def circumferential_resection_margin(self, value):
        self._set_property("circumferential_resection_margin", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def columnar_mucosa_present(self, value):
        self._set_property("columnar_mucosa_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def consistent_pathology_review(self, value):
        self._set_property("consistent_pathology_review", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "High Grade",
            "Indefinite",
            "Low Grade",
            "Mild",
            "Moderate",
            "No Dysplasia",
            "Not Reported",
            "Severe",
            "Unknown",
        ],
    )
    def dysplasia_degree(self, value):
        self._set_property("dysplasia_degree", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Epithelial",
            "Esophageal Columnar Dysplasia",
            "Esophageal Mucosa Columnar Dysplasia",
            "Keratinizing",
            "Nonkeratinizing",
            "Not Reported",
            "Other",
            "Unknown",
        ],
    )
    def dysplasia_type(self, value):
        self._set_property("dysplasia_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def epithelioid_cell_percent(self, value):
        self._set_property("epithelioid_cell_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Extensive", "Focal", "Not Reported"])
    def extracapsular_extension(self, value):
        self._set_property("extracapsular_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=["Gross Extension", "Microscopic Extension", "No Extranodal Extension"],
    )
    def extranodal_extension(self, value):
        self._set_property("extranodal_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def extrascleral_extension(self, value):
        self._set_property("extrascleral_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def greatest_tumor_dimension(self, value):
        self._set_property("greatest_tumor_dimension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def gross_tumor_weight(self, value):
        self._set_property("gross_tumor_weight", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Macroscopic (2cm or less)",
            "Macroscopic (greater than 2cm)",
            "Microscopic",
            "Not Reported",
            "Unknown",
        ],
    )
    def largest_extrapelvic_peritoneal_focus(self, value):
        self._set_property("largest_extrapelvic_peritoneal_focus", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Functional (Limited) Neck Dissection",
            "Modified Radical Neck Dissection",
            "Radical Neck Dissection",
        ],
    )
    def lymph_node_dissection_method(self, value):
        self._set_property("lymph_node_dissection_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Neck, Left", "Neck, NOS", "Neck, Right"])
    def lymph_node_dissection_site(self, value):
        self._set_property("lymph_node_dissection_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Aortic",
            "Axillary",
            "Cervical",
            "Epitrochlear",
            "Femoral",
            "Hilar",
            "Iliac, NOS",
            "Iliac-common",
            "Iliac-external",
            "Inguinal",
            "Mediastinal",
            "Mesenteric",
            "None",
            "Not Reported",
            "Occipital",
            "Paraaortic",
            "Parotid",
            "Pelvis, NOS",
            "Popliteal",
            "Retroperitoneal",
            "Splenic",
            "Submandibular",
            "Supraclavicular",
            "Unknown",
        ],
    )
    def lymph_node_involved_site(self, value):
        self._set_property("lymph_node_involved_site", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Indeterminant", "Negative", "Not Reported", "Positive", "Unknown"]
    )
    def lymph_node_involvement(self, value):
        self._set_property("lymph_node_involvement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_positive(self, value):
        self._set_property("lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def lymph_nodes_removed(self, value):
        self._set_property("lymph_nodes_removed", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def lymph_nodes_tested(self, value):
        self._set_property("lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def lymphatic_invasion_present(self, value):
        self._set_property("lymphatic_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Indeterminant", "Involved", "Not Reported", "Uninvolved", "Unknown"]
    )
    def margin_status(self, value):
        self._set_property("margin_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Pathologic", "Radiologic"])
    def measurement_type(self, value):
        self._set_property("measurement_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Centimeters", "Millimeters"])
    def measurement_unit(self, value):
        self._set_property("measurement_unit", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def metaplasia_present(self, value):
        self._set_property("metaplasia_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Cohesive",
            "Cribiform",
            "Micropapillary",
            "Non-cohesive",
            "Papillary Renal Cell",
            "Papillary, NOS",
            "Solid",
            "Tubular",
        ],
    )
    def morphologic_architectural_pattern(self, value):
        self._set_property("morphologic_architectural_pattern", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def necrosis_percent(self, value):
        self._set_property("necrosis_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def necrosis_present(self, value):
        self._set_property("necrosis_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Absent", "Indeterminate", "Not Reported", "Present", "Unknown"]
    )
    def non_nodal_regional_disease(self, value):
        self._set_property("non_nodal_regional_disease", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def non_nodal_tumor_deposits(self, value):
        self._set_property("non_nodal_tumor_deposits", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def number_proliferating_cells(self, value):
        self._set_property("number_proliferating_cells", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_tumor_invasion(self, value):
        self._set_property("percent_tumor_invasion", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def percent_tumor_nuclei(self, value):
        self._set_property("percent_tumor_nuclei", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def perineural_invasion_present(self, value):
        self._set_property("perineural_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["0", "1-3", "4 or More", "Not Reported", "Unknown"])
    def peripancreatic_lymph_nodes_positive(self, value):
        self._set_property("peripancreatic_lymph_nodes_positive", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def peripancreatic_lymph_nodes_tested(self, value):
        self._set_property("peripancreatic_lymph_nodes_tested", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_positive_count(self, value):
        self._set_property("prostatic_chips_positive_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_chips_total_count(self, value):
        self._set_property("prostatic_chips_total_count", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def prostatic_involvement_percent(self, value):
        self._set_property("prostatic_involvement_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["R0", "R1", "R2", "RX"])
    def residual_tumor(self, value):
        self._set_property("residual_tumor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["1-10 mm", "11-20 mm", ">20 mm", "No macroscopic disease"])
    def residual_tumor_measurement(self, value):
        self._set_property("residual_tumor_measurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def rhabdoid_percent(self, value):
        self._set_property("rhabdoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def rhabdoid_present(self, value):
        self._set_property("rhabdoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def sarcomatoid_percent(self, value):
        self._set_property("sarcomatoid_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def sarcomatoid_present(self, value):
        self._set_property("sarcomatoid_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def size_extraocular_nodule(self, value):
        self._set_property("size_extraocular_nodule", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def spindle_cell_percent(self, value):
        self._set_property("spindle_cell_percent", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Absent", "Not Reported", "Present", "Unknown"])
    def transglottic_extension(self, value):
        self._set_property("transglottic_extension", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Deep", "Not Reported", "Superficial"])
    def tumor_depth_descriptor(self, value):
        self._set_property("tumor_depth_descriptor", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_depth_measurement(self, value):
        self._set_property("tumor_depth_measurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Few", "Many", "Moderate"])
    def tumor_infiltrating_lymphocytes(self, value):
        self._set_property("tumor_infiltrating_lymphocytes", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Few", "Many", "Moderate"])
    def tumor_infiltrating_macrophages(self, value):
        self._set_property("tumor_infiltrating_macrophages", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_largest_dimension_diameter(self, value):
        self._set_property("tumor_largest_dimension_diameter", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_length_measurement(self, value):
        self._set_property("tumor_length_measurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def tumor_level_prostate(self, value):
        self._set_property("tumor_level_prostate", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Echographic", "Pathologic"])
    def tumor_measurement_method(self, value):
        self._set_property("tumor_measurement_method", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Diffuse", "Dome", "Mushroom", "Unknown"])
    def tumor_shape(self, value):
        self._set_property("tumor_shape", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_thickness(self, value):
        self._set_property("tumor_thickness", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_width_measurement(self, value):
        self._set_property("tumor_width_measurement", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def vascular_invasion_present(self, value):
        self._set_property("vascular_invasion_present", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Extramural",
            "Intramural",
            "Macro",
            "Micro",
            "No Vascular Invasion",
            "Not Reported",
            "Unknown",
        ],
    )
    def vascular_invasion_type(self, value):
        self._set_property("vascular_invasion_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Central zone",
            "Overlapping/multiple zones",
            "Peripheral zone",
            "Transition zone",
            "Unknown zone",
        ],
    )
    def zone_of_origin_prostate(self, value):
        self._set_property("zone_of_origin_prostate", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(PathologyDetail)
datetime_hooks.cls_inject_updated_datetime_hook(PathologyDetail)
