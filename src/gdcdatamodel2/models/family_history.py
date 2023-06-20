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


class FamilyHistory(base.Node):
    __tablename__: str = "node_familyhistory"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Family History",
        "namespace": "https://gdc.cancer.gov",
        "category": "clinical",
        "submittable": True,
        "downloadable": False,
        "description": "Record of a patient's background regarding cancer events of blood relatives.",
        "required": ["submitter_id"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "name": "cases",
                "backref": "family_histories",
                "label": "describes",
                "target_type": "case",
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
            "relationship_type": {
                "description": "The subgroup that describes the state of connectedness between members of the unit of society organized around kinship ties.",
                "termDef": {
                    "term": "Family Member Relationship Type",
                    "source": "caDSR",
                    "cde_id": 2690165,
                    "cde_version": 2.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=2690165&version=2.0",
                },
                "enum": [
                    "Adopted Brother",
                    "Adopted Daughter",
                    "Adopted Sister",
                    "Adopted Son",
                    "Adoptive Father",
                    "Adoptive Mother",
                    "Aunt",
                    "Brother",
                    "Brother-in-law",
                    "Child",
                    "Cousin",
                    "Daughter",
                    "Daughter-in-law",
                    "Domestic Partner",
                    "Father",
                    "Father-in-law",
                    "Female Cousin",
                    "Female Sibling of Adopted Child",
                    "First Cousin",
                    "First Cousin Once Removed",
                    "First Degree Relative, NOS",
                    "Foster Brother",
                    "Foster Daughter",
                    "Foster Father",
                    "Foster Mother",
                    "Foster Sister",
                    "Foster Son",
                    "Fraternal Twin Brother",
                    "Fraternal Twin Sibling",
                    "Fraternal Twin Sister",
                    "Full Brother",
                    "Full Sister",
                    "Grand Nephew",
                    "Grand Niece",
                    "Grandchild",
                    "Granddaughter",
                    "Grandfather",
                    "Grandmother",
                    "Grandparent",
                    "Grandson",
                    "Great Grandchild",
                    "Half Brother",
                    "Half Sibling",
                    "Half Sister",
                    "Husband",
                    "Identical Twin Brother",
                    "Identical Twin Sibling",
                    "Identical Twin Sister",
                    "Legal Guardian",
                    "Male Cousin",
                    "Male Sibling of Adopted Child",
                    "Maternal Aunt",
                    "Maternal First Cousin",
                    "Maternal First Cousin Once Removed",
                    "Maternal Grandfather",
                    "Maternal Grandmother",
                    "Maternal Grandparent",
                    "Maternal Great Aunt",
                    "Maternal Great Grandparent",
                    "Maternal Great Uncle",
                    "Maternal Half Brother",
                    "Maternal Half Sibling",
                    "Maternal Half Sister",
                    "Maternal Uncle",
                    "Mother",
                    "Mother-in-law",
                    "Natural Brother",
                    "Natural Child",
                    "Natural Daughter",
                    "Natural Father",
                    "Natural Grandchild",
                    "Natural Grandfather",
                    "Natural Grandmother",
                    "Natural Grandparent",
                    "Natural Mother",
                    "Natural Parent",
                    "Natural Sibling",
                    "Natural Sister",
                    "Natural Son",
                    "Nephew",
                    "Niece",
                    "Niece Second Degree Relative",
                    "Other",
                    "Parent",
                    "Paternal Aunt",
                    "Paternal First Cousin",
                    "Paternal First Cousin Once Removed",
                    "Paternal Grandfather",
                    "Paternal Grandmother",
                    "Paternal Grandparent",
                    "Paternal Great Aunt",
                    "Paternal Great Grandparent",
                    "Paternal Great Uncle",
                    "Paternal Half Brother",
                    "Paternal Half Sibling",
                    "Paternal Half Sister",
                    "Paternal Uncle",
                    "Sibling",
                    "Sister",
                    "Sister-in-law",
                    "Son",
                    "Son-in-law",
                    "Spouse",
                    "Step Child",
                    "Step Sibling",
                    "Stepbrother",
                    "Stepdaughter",
                    "Stepfather",
                    "Stepmother",
                    "Stepsister",
                    "Stepson",
                    "Twin Sibling",
                    "Uncle",
                    "Unrelated",
                    "Ward",
                    "Wife",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Adopted Brother": {
                        "description": "A male sibling who is legally adopted by one's biological parent or legal guardian.",
                        "termDef": {
                            "term": "Adopted Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166195",
                            "term_id": "C166195",
                            "term_version": "19.12e",
                        },
                    },
                    "Adopted Daughter": {
                        "description": "A female child in the parent-child relationship established by a legal adoption proceeding.",
                        "termDef": {
                            "term": "Adopted Daughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166131",
                            "term_id": "C166131",
                            "term_version": "19.12e",
                        },
                    },
                    "Adopted Sister": {
                        "description": "A female sibling who is legally adopted by one's biological parent or legal guardian.",
                        "termDef": {
                            "term": "Adopted Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166196",
                            "term_id": "C166196",
                            "term_version": "19.12e",
                        },
                    },
                    "Adopted Son": {
                        "description": "A male child in the parent-child relationship established by a legal adoption proceeding.",
                        "termDef": {
                            "term": "Adopted Son",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166132",
                            "term_id": "C166132",
                            "term_version": "19.12e",
                        },
                    },
                    "Adoptive Father": {
                        "description": "A male parent in the parent-child relationship established by a legal adoption proceeding.",
                        "termDef": {
                            "term": "Adoptive Father",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166133",
                            "term_id": "C166133",
                            "term_version": "19.12e",
                        },
                    },
                    "Adoptive Mother": {
                        "description": "A female parent in the parent-child relationship established by a legal adoption proceeding.",
                        "termDef": {
                            "term": "Adoptive Mother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166134",
                            "term_id": "C166134",
                            "term_version": "19.12e",
                        },
                    },
                    "Aunt": {
                        "description": "The sister of your father or mother; the wife of your uncle.",
                        "termDef": {
                            "term": "Aunt",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71405",
                            "term_id": "C71405",
                            "term_version": "19.12e",
                        },
                    },
                    "Brother": {
                        "description": "A male sibling.",
                        "termDef": {
                            "term": "Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25289",
                            "term_id": "C25289",
                            "term_version": "19.12e",
                        },
                    },
                    "Brother-in-law": {
                        "description": "A brother by marriage.",
                        "termDef": {
                            "term": "Brother-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71406",
                            "term_id": "C71406",
                            "term_version": "19.12e",
                        },
                    },
                    "Child": {
                        "description": "An age group comprised of individuals who are not yet an adult. The specific cut-off age will vary by purpose.",
                        "termDef": {
                            "term": "Child",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C16423",
                            "term_id": "C16423",
                            "term_version": "19.12e",
                        },
                    },
                    "Cousin": {
                        "description": "A child of your aunt or uncle or their descendents.",
                        "termDef": {
                            "term": "Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71410",
                            "term_id": "C71410",
                            "term_version": "19.12e",
                        },
                    },
                    "Daughter": {
                        "description": "A female human offspring.",
                        "termDef": {
                            "term": "Daughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25165",
                            "term_id": "C25165",
                            "term_version": "19.12e",
                        },
                    },
                    "Daughter-in-law": {
                        "description": "The wife of your son.",
                        "termDef": {
                            "term": "Daughter-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71401",
                            "term_id": "C71401",
                            "term_version": "19.12e",
                        },
                    },
                    "Domestic Partner": {
                        "description": "Indicates a person who is a member of an unmarried couple, including same sex couples, living together in longstanding relationships, that are registered or unregistered.",
                        "termDef": {
                            "term": "Domestic Partnership",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C53262",
                            "term_id": "C53262",
                            "term_version": "19.12e",
                        },
                    },
                    "Father": {
                        "description": "A male parent.",
                        "termDef": {
                            "term": "Father",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25174",
                            "term_id": "C25174",
                            "term_version": "19.12e",
                        },
                    },
                    "Father-in-law": {
                        "description": "The father of your spouse.",
                        "termDef": {
                            "term": "Father-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C68640",
                            "term_id": "C68640",
                            "term_version": "19.12e",
                        },
                    },
                    "Female Cousin": {
                        "description": "A female child of one's aunt or uncle.",
                        "termDef": {
                            "term": "Female Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165786",
                            "term_id": "C165786",
                            "term_version": "19.12e",
                        },
                    },
                    "Female Sibling of Adopted Child": {
                        "description": "A female sibling of an adopted child. The said female is a biological or legal child of the parents who facilitated the adoption.",
                        "termDef": {
                            "term": "Female Sibling of Adopted Child",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166198",
                            "term_id": "C166198",
                            "term_version": "19.12e",
                        },
                    },
                    "First Cousin": {
                        "description": "A child of your aunt or uncle.",
                        "termDef": {
                            "term": "First Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71411",
                            "term_id": "C71411",
                            "term_version": "19.12e",
                        },
                    },
                    "First Cousin Once Removed": {
                        "description": "A child of your first cousin.",
                        "termDef": {
                            "term": "First Cousin Once Removed",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71412",
                            "term_id": "C71412",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Brother": {
                        "description": "A male child being fostered by your parents or legal guardians.",
                        "termDef": {
                            "term": "Foster Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165788",
                            "term_id": "C165788",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Daughter": {
                        "description": "A female child you are fostering.",
                        "termDef": {
                            "term": "Foster Daughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165790",
                            "term_id": "C165790",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Father": {
                        "description": "A male foster parent.",
                        "termDef": {
                            "term": "Foster Father",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165792",
                            "term_id": "C165792",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Mother": {
                        "description": "A female foster parent.",
                        "termDef": {
                            "term": "Foster Mother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165793",
                            "term_id": "C165793",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Sister": {
                        "description": "A female child being fostered by your parents or legal guardians.",
                        "termDef": {
                            "term": "Foster Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165794",
                            "term_id": "C165794",
                            "term_version": "19.12e",
                        },
                    },
                    "Foster Son": {
                        "description": "A male child you are fostering.",
                        "termDef": {
                            "term": "Foster Son",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165795",
                            "term_id": "C165795",
                            "term_version": "19.12e",
                        },
                    },
                    "Fraternal Twin Brother": {
                        "description": "A male full sibling that developed from a separately fertilized ova during the same pregnancy.",
                        "termDef": {
                            "term": "Fraternal Twin Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165796",
                            "term_id": "C165796",
                            "term_version": "19.12e",
                        },
                    },
                    "Fraternal Twin Sibling": {
                        "description": "Either of the two offspring from separately fertilized ova during the same pregnancy.",
                        "termDef": {
                            "term": "Fraternal Twin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C73428",
                            "term_id": "C73428",
                            "term_version": "19.12e",
                        },
                    },
                    "Fraternal Twin Sister": {
                        "description": "A female full sibling that developed from a separately fertilized ova during the same pregnancy.",
                        "termDef": {
                            "term": "Fraternal Twin Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165797",
                            "term_id": "C165797",
                            "term_version": "19.12e",
                        },
                    },
                    "Full Brother": {
                        "description": "A male who shares with his sibling the genetic makeup inherited from both of the biological parents.",
                        "termDef": {
                            "term": "Full Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C111201",
                            "term_id": "C111201",
                            "term_version": "19.12e",
                        },
                    },
                    "Full Sister": {
                        "description": "A female who shares with her sibling the genetic makeup inherited from both of the biological parents.",
                        "termDef": {
                            "term": "Full Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C111202",
                            "term_id": "C111202",
                            "term_version": "19.12e",
                        },
                    },
                    "Grand Nephew": {
                        "description": "A male child of one's niece or nephew.",
                        "termDef": {
                            "term": "Great Nephew",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165798",
                            "term_id": "C165798",
                            "term_version": "19.12e",
                        },
                    },
                    "Grand Niece": {
                        "description": "A female child of one's niece or nephew.",
                        "termDef": {
                            "term": "Great Niece",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165846",
                            "term_id": "C165846",
                            "term_version": "19.12e",
                        },
                    },
                    "Grandchild": {
                        "description": "A child of your son or daughter.",
                        "termDef": {
                            "term": "Grandchild",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71397",
                            "term_id": "C71397",
                            "term_version": "19.12e",
                        },
                    },
                    "Granddaughter": {
                        "description": "A female grandchild.",
                        "termDef": {
                            "term": "Granddaughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71399",
                            "term_id": "C71399",
                            "term_version": "19.12e",
                        },
                    },
                    "Grandfather": {
                        "description": "The father of your father or mother.",
                        "termDef": {
                            "term": "Grandfather",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71387",
                            "term_id": "C71387",
                            "term_version": "19.12e",
                        },
                    },
                    "Grandmother": {
                        "description": "The mother of your father or mother.",
                        "termDef": {
                            "term": "Grandmother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71386",
                            "term_id": "C71386",
                            "term_version": "19.12e",
                        },
                    },
                    "Grandparent": {
                        "description": "A parent of your father or mother.",
                        "termDef": {
                            "term": "Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71385",
                            "term_id": "C71385",
                            "term_version": "19.12e",
                        },
                    },
                    "Grandson": {
                        "description": "A male grandchild.",
                        "termDef": {
                            "term": "Grandson",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71398",
                            "term_id": "C71398",
                            "term_version": "19.12e",
                        },
                    },
                    "Great Grandchild": {
                        "description": "A child of one's grandchild.",
                        "termDef": {
                            "term": "Great Grandchild",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165847",
                            "term_id": "C165847",
                            "term_version": "19.12e",
                        },
                    },
                    "Half Brother": {
                        "description": "A male sibling with whom you share a single parent.",
                        "termDef": {
                            "term": "Half Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71402",
                            "term_id": "C71402",
                            "term_version": "19.12e",
                        },
                    },
                    "Half Sibling": {
                        "description": "A sibling with whom you share a single parent.",
                        "termDef": {
                            "term": "Half Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71391",
                            "term_id": "C71391",
                            "term_version": "19.12e",
                        },
                    },
                    "Half Sister": {
                        "description": "A female sibling with whom you share a single parent.",
                        "termDef": {
                            "term": "Half Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71403",
                            "term_id": "C71403",
                            "term_version": "19.12e",
                        },
                    },
                    "Husband": {
                        "description": "A male partner in marriage.",
                        "termDef": {
                            "term": "Husband",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71588",
                            "term_id": "C71588",
                            "term_version": "19.12e",
                        },
                    },
                    "Identical Twin Brother": {
                        "description": "A male full sibling that developed from a shared ovum.",
                        "termDef": {
                            "term": "Identical Twin Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165848",
                            "term_id": "C165848",
                            "term_version": "19.12e",
                        },
                    },
                    "Identical Twin Sibling": {
                        "description": "Either of the two offspring resulting from a shared ovum.",
                        "termDef": {
                            "term": "Identical Twin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C73429",
                            "term_id": "C73429",
                            "term_version": "19.12e",
                        },
                    },
                    "Identical Twin Sister": {
                        "description": "A female full sibling that developed from a shared ovum.",
                        "termDef": {
                            "term": "Identical Twin Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165849",
                            "term_id": "C165849",
                            "term_version": "19.12e",
                        },
                    },
                    "Legal Guardian": {
                        "description": "An individual who is authorized under applicable State or local law to consent on behalf of a child or incapable person to general medical care including participation in clinical research.",
                        "termDef": {
                            "term": "Guardian",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C51828",
                            "term_id": "C51828",
                            "term_version": "19.12e",
                        },
                    },
                    "Male Cousin": {
                        "description": "A male child of one's aunt or uncle.",
                        "termDef": {
                            "term": "Male Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165850",
                            "term_id": "C165850",
                            "term_version": "19.12e",
                        },
                    },
                    "Male Sibling of Adopted Child": {
                        "description": "A male sibling of an adopted child. The said male is a biological or legal child of the parents who facilitated the adoption.",
                        "termDef": {
                            "term": "Male Sibling of Adopted Child",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166197",
                            "term_id": "C166197",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Aunt": {
                        "description": "A female relative who is a sibling of the biological mother, and who both share a common ancestor.",
                        "termDef": {
                            "term": "Biological Maternal Aunt",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96575",
                            "term_id": "C96575",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal First Cousin": {
                        "description": "A relative who is the offspring of a sibling of the biological mother and thus sharing a common ancestor.",
                        "termDef": {
                            "term": "Biological Maternal Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96576",
                            "term_id": "C96576",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal First Cousin Once Removed": {
                        "description": "A child of one's first cousin who is related by lineage through the mother's side of the family.",
                        "termDef": {
                            "term": "Maternal First Cousin Once Removed",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165851",
                            "term_id": "C165851",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Grandfather": {
                        "description": "A male relative who is the biological father of the biological mother.",
                        "termDef": {
                            "term": "Biological Maternal Grandfather",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96577",
                            "term_id": "C96577",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Grandmother": {
                        "description": "A female relative who is the biological mother of the biological mother.",
                        "termDef": {
                            "term": "Biological Maternal Grandmother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96578",
                            "term_id": "C96578",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Grandparent": {
                        "description": "A relative who is the biological parent of the biological mother.",
                        "termDef": {
                            "term": "Biological Maternal Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C111248",
                            "term_id": "C111248",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Great Aunt": {
                        "description": "The aunt of one's mother.",
                        "termDef": {
                            "term": "Maternal Great Aunt",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165853",
                            "term_id": "C165853",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Great Grandparent": {
                        "description": "A parent of one's maternal grandparent.",
                        "termDef": {
                            "term": "Maternal Great Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166127",
                            "term_id": "C166127",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Great Uncle": {
                        "description": "The uncle of one's mother.",
                        "termDef": {
                            "term": "Maternal Great Uncle",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165854",
                            "term_id": "C165854",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Half Brother": {
                        "description": "A male sibling who shares the genetic makeup inherited from only the biological mother.",
                        "termDef": {
                            "term": "Half-brother with Mother as Common Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96656",
                            "term_id": "C96656",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Half Sibling": {
                        "description": "A relative with whom you share a biological mother but you have different fathers.",
                        "termDef": {
                            "term": "Maternal Half Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166112",
                            "term_id": "C166112",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Half Sister": {
                        "description": "A female sibling who shares the genetic makeup inherited from only the biological mother.",
                        "termDef": {
                            "term": "Half-sister with Mother as Common Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96658",
                            "term_id": "C96658",
                            "term_version": "19.12e",
                        },
                    },
                    "Maternal Uncle": {
                        "description": "A male relative who is a sibling of the biological mother, and who both share a common ancestor.",
                        "termDef": {
                            "term": "Biological Maternal Uncle",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96579",
                            "term_id": "C96579",
                            "term_version": "19.12e",
                        },
                    },
                    "Mother": {
                        "description": "A female parent.",
                        "termDef": {
                            "term": "Mother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25189",
                            "term_id": "C25189",
                            "term_version": "19.12e",
                        },
                    },
                    "Mother-in-law": {
                        "description": "The mother of your spouse.",
                        "termDef": {
                            "term": "Mother-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C68639",
                            "term_id": "C68639",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Brother": {
                        "description": "A male who shares with his sibling the genetic makeup inherited from one or both of their shared biological parents.",
                        "termDef": {
                            "term": "Biological Brother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96570",
                            "term_id": "C96570",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Child": {
                        "description": "A son or daughter with genetic makeup inherited from the parent.",
                        "termDef": {
                            "term": "Biological Child",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C100807",
                            "term_id": "C100807",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Daughter": {
                        "description": "A female human offspring.",
                        "termDef": {
                            "term": "Daughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25165",
                            "term_id": "C25165",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Father": {
                        "description": "A male who contributes to the genetic makeup of his offspring through the fertilization of an ovum by his sperm.",
                        "termDef": {
                            "term": "Biological Father",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96572",
                            "term_id": "C96572",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Grandchild": {
                        "description": "A biological child of an individual's biological child.",
                        "termDef": {
                            "term": "Biological Grandchild",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C100805",
                            "term_id": "C100805",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Grandfather": {
                        "description": "A male relative who is the biological father of either the biological mother or the biological father.",
                        "termDef": {
                            "term": "Biological Grandfather",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96573",
                            "term_id": "C96573",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Grandmother": {
                        "description": "A female relative who is the biological mother of either the biological mother or the biological father.",
                        "termDef": {
                            "term": "Biological Grandmother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96574",
                            "term_id": "C96574",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Grandparent": {
                        "description": "A biological parent of the biological father or biological mother.",
                        "termDef": {
                            "term": "Biological Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C100806",
                            "term_id": "C100806",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Mother": {
                        "description": "A female who contributes to the genetic makeup of her offspring from the fertilization of her ovum.",
                        "termDef": {
                            "term": "Biological Mother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96580",
                            "term_id": "C96580",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Parent": {
                        "description": "The male who supplied the sperm or the female who supplied the egg which resulted in one's conception.",
                        "termDef": {
                            "term": "Biological Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166114",
                            "term_id": "C166114",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Sibling": {
                        "description": "A person's brother or sister with whom they share a genetic makeup inherited from one or both of their shared biological parents.",
                        "termDef": {
                            "term": "Biological Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C100809",
                            "term_id": "C100809",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Sister": {
                        "description": "A female who shares with her sibling the genetic makeup inherited from one or both of their shared biological parents.",
                        "termDef": {
                            "term": "Biological Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96586",
                            "term_id": "C96586",
                            "term_version": "19.12e",
                        },
                    },
                    "Natural Son": {
                        "description": "A male progeny with genetic makeup inherited from the parent.",
                        "termDef": {
                            "term": "Biological Son",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C150888",
                            "term_id": "C150888",
                            "term_version": "19.12e",
                        },
                    },
                    "Nephew": {
                        "description": "A son of your brother or sister.",
                        "termDef": {
                            "term": "Nephew",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71409",
                            "term_id": "C71409",
                            "term_version": "19.12e",
                        },
                    },
                    "Niece": {
                        "description": "A daughter of your brother or sister.",
                        "termDef": {
                            "term": "Niece",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71408",
                            "term_id": "C71408",
                            "term_version": "19.12e",
                        },
                    },
                    "Niece Second Degree Relative": {
                        "description": "A daughter of one's biological sibling.",
                        "termDef": {
                            "term": "Biological Niece",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166115",
                            "term_id": "C166115",
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
                    "Parent": {
                        "description": "A mother or a father; an immediate progenitor.",
                        "termDef": {
                            "term": "Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C42709",
                            "term_id": "C42709",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Aunt": {
                        "description": "A female relative who is a sibling of the biological father, and who both share a common ancestor.",
                        "termDef": {
                            "term": "Biological Paternal Aunt",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96581",
                            "term_id": "C96581",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal First Cousin": {
                        "description": "A relative who is the offspring of a sibling of the biological father and thus sharing a common ancestor.",
                        "termDef": {
                            "term": "Biological Paternal Cousin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96582",
                            "term_id": "C96582",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal First Cousin Once Removed": {
                        "description": "A child of one's first cousin who is related by lineage through the father's side of the family.",
                        "termDef": {
                            "term": "Paternal First Cousin Once Removed",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165852",
                            "term_id": "C165852",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Grandfather": {
                        "description": "A male relative who is the biological father of the biological father.",
                        "termDef": {
                            "term": "Biological Paternal Grandfather",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96583",
                            "term_id": "C96583",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Grandmother": {
                        "description": "A female relative who is the biological mother of the biological father.",
                        "termDef": {
                            "term": "Biological Paternal Grandmother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96584",
                            "term_id": "C96584",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Grandparent": {
                        "description": "A relative who is the biological parent of the biological father.",
                        "termDef": {
                            "term": "Biological Paternal Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C111286",
                            "term_id": "C111286",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Great Aunt": {
                        "description": "The aunt of one's father.",
                        "termDef": {
                            "term": "Paternal Great Aunt",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165856",
                            "term_id": "C165856",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Great Grandparent": {
                        "description": "A parent of one's paternal grandparent.",
                        "termDef": {
                            "term": "Paternal Great Grandparent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166128",
                            "term_id": "C166128",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Great Uncle": {
                        "description": "The uncle of one's father.",
                        "termDef": {
                            "term": "Paternal Great Uncle",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C165857",
                            "term_id": "C165857",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Half Brother": {
                        "description": "A male sibling who shares the genetic makeup inherited from only the biological father.",
                        "termDef": {
                            "term": "Half-brother with Father as Common Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96655",
                            "term_id": "C96655",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Half Sibling": {
                        "description": "A relative with whom you share a biological father but you have different mothers.",
                        "termDef": {
                            "term": "Paternal Half Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166113",
                            "term_id": "C166113",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Half Sister": {
                        "description": "A female sibling who shares the genetic makeup inherited from only the biological father.",
                        "termDef": {
                            "term": "Half-sister with Father as Common Parent",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96657",
                            "term_id": "C96657",
                            "term_version": "19.12e",
                        },
                    },
                    "Paternal Uncle": {
                        "description": "A male relative who is a sibling of the biological father, and who both share a common ancestor.",
                        "termDef": {
                            "term": "Biological Paternal Uncle",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C96585",
                            "term_id": "C96585",
                            "term_version": "19.12e",
                        },
                    },
                    "Sibling": {
                        "description": "A person's brother or sister.",
                        "termDef": {
                            "term": "Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25204",
                            "term_id": "C25204",
                            "term_version": "19.12e",
                        },
                    },
                    "Sister": {
                        "description": "A female sibling.",
                        "termDef": {
                            "term": "Sister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25680",
                            "term_id": "C25680",
                            "term_version": "19.12e",
                        },
                    },
                    "Sister-in-law": {
                        "description": "A sister by marriage.",
                        "termDef": {
                            "term": "Sister-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71407",
                            "term_id": "C71407",
                            "term_version": "19.12e",
                        },
                    },
                    "Son": {
                        "description": "A male human offspring.",
                        "termDef": {
                            "term": "Son",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25205",
                            "term_id": "C25205",
                            "term_version": "19.12e",
                        },
                    },
                    "Son-in-law": {
                        "description": "The husband of your daughter.",
                        "termDef": {
                            "term": "Son-in-law",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71400",
                            "term_id": "C71400",
                            "term_version": "19.12e",
                        },
                    },
                    "Spouse": {
                        "description": "A person's partner in marriage.",
                        "termDef": {
                            "term": "Spouse",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C62649",
                            "term_id": "C62649",
                            "term_version": "19.12e",
                        },
                    },
                    "Step Child": {
                        "description": "A child of one's spouse, acquired through marriage.",
                        "termDef": {
                            "term": "Step Child",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166117",
                            "term_id": "C166117",
                            "term_version": "19.12e",
                        },
                    },
                    "Step Sibling": {
                        "description": "A child of one's step parent.",
                        "termDef": {
                            "term": "Step Sibling",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166118",
                            "term_id": "C166118",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepbrother": {
                        "description": "A male child of one's step parent.",
                        "termDef": {
                            "term": "Stepbrother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166119",
                            "term_id": "C166119",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepdaughter": {
                        "description": "A female child of one's spouse, acquired through marriage.",
                        "termDef": {
                            "term": "Stepdaughter",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166123",
                            "term_id": "C166123",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepfather": {
                        "description": "A male that is related to a child or children through marriage to their biological parent.",
                        "termDef": {
                            "term": "Step Father",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C154851",
                            "term_id": "C154851",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepmother": {
                        "description": "A female who is married to a spouse with children whom are not biologically related to her.",
                        "termDef": {
                            "term": "Stepmother",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C132450",
                            "term_id": "C132450",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepsister": {
                        "description": "A female child of one's step parent.",
                        "termDef": {
                            "term": "Stepsister",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166124",
                            "term_id": "C166124",
                            "term_version": "19.12e",
                        },
                    },
                    "Stepson": {
                        "description": "A male child of one's spouse, acquired through marriage.",
                        "termDef": {
                            "term": "Stepson",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C166125",
                            "term_id": "C166125",
                            "term_version": "19.12e",
                        },
                    },
                    "Twin Sibling": {
                        "description": "Either of two offspring born from the same pregnancy.",
                        "termDef": {
                            "term": "Twin",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C73427",
                            "term_id": "C73427",
                            "term_version": "19.12e",
                        },
                    },
                    "Uncle": {
                        "description": "The brother of your father or mother; the husband of your aunt.",
                        "termDef": {
                            "term": "Uncle",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71404",
                            "term_id": "C71404",
                            "term_version": "19.12e",
                        },
                    },
                    "Unrelated": {
                        "description": "Not connected or associated e.g. by kinship.",
                        "termDef": {
                            "term": "Unrelated",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25328",
                            "term_id": "C25328",
                            "term_version": "19.12e",
                        },
                    },
                    "Ward": {
                        "description": "A person who is under the protection or in the custody of another.",
                        "termDef": {
                            "term": "Ward",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71413",
                            "term_id": "C71413",
                            "term_version": "19.12e",
                        },
                    },
                    "Wife": {
                        "description": "A female partner in marriage.",
                        "termDef": {
                            "term": "Wife",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C71587",
                            "term_id": "C71587",
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
            "relationship_gender": {
                "description": "The text term used to describe the gender of the patient's relative with a history of cancer.",
                "termDef": {
                    "term": "Relative Gender Type",
                    "source": "caDSR",
                    "cde_id": 6161021,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6161021&version=1.0",
                },
                "enum": ["female", "male", "unknown", "unspecified", "not reported"],
                "enumDef": {
                    "female": {
                        "description": "A person who belongs to the sex that normally produces ova. The term is used to indicate biological sex distinctions, or cultural gender role distinctions, or both.",
                        "termDef": {
                            "term": "Female",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C16576",
                            "term_id": "C16576",
                            "term_version": "19.12e",
                        },
                    },
                    "male": {
                        "description": "A person who belongs to the sex that normally produces sperm. The term is used to indicate biological sex distinctions, cultural gender role distinctions, or both.",
                        "termDef": {
                            "term": "Male",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C20197",
                            "term_id": "C20197",
                            "term_version": "19.12e",
                        },
                    },
                    "unknown": {
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
                    "unspecified": {
                        "description": "Not stated explicitly or in detail.",
                        "termDef": {
                            "term": "Unspecified",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C38046",
                            "term_id": "C38046",
                            "term_version": "19.12e",
                        },
                    },
                    "not reported": {
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
            "relationship_age_at_diagnosis": {
                "description": "The age (in years) when the patient's relative was first diagnosed.",
                "termDef": {
                    "term": "Relative Diagnosis Age Value",
                    "source": "caDSR",
                    "cde_id": 5300571,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=5300571&version=1.0",
                },
                "type": "number",
                "maximum": 89,
                "minimum": 0,
            },
            "relationship_primary_diagnosis": {
                "description": "The text term used to describe the malignant diagnosis of the patient's relative with a history of cancer.",
                "termDef": {
                    "term": "Relative Malignant Diagnosis Name",
                    "source": "caDSR",
                    "cde_id": 6161022,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6161022&version=1.0",
                },
                "enum": [
                    "Adrenal Gland Cancer",
                    "Basal Cell Cancer",
                    "Bile Duct Cancer",
                    "Bladder Cancer",
                    "Blood Cancer",
                    "Bone Cancer",
                    "Brain Cancer",
                    "Breast Cancer",
                    "Cancer",
                    "Cervical Cancer",
                    "Chondrosarcoma",
                    "CNS Cancer",
                    "Colorectal Cancer",
                    "Esophageal Cancer",
                    "Ewing Sarcoma",
                    "Gallbladder Cancer",
                    "Gastric Cancer",
                    "Glioblastoma",
                    "Gynecologic Cancer",
                    "Head and Neck Cancer",
                    "Hematologic Cancer",
                    "Kaposi Sarcoma",
                    "Kidney Cancer",
                    "Laryngeal Cancer",
                    "Leukemia",
                    "Liver Cancer",
                    "Lung Cancer",
                    "Lymph Node Cancer",
                    "Lymphoma",
                    "Melanoma",
                    "Mesothelioma",
                    "Multiple Myeloma",
                    "Neuroblastoma",
                    "Osteosarcoma",
                    "Ovarian Cancer",
                    "Pancreas Cancer",
                    "Pediatric Liver Cancer",
                    "Prostate Cancer",
                    "Rectal Cancer",
                    "Rhabdomyosarcoma",
                    "Sarcoma",
                    "Skin Cancer",
                    "Spleen Cancer",
                    "Testicular Cancer",
                    "Throat Cancer",
                    "Thyroid Cancer",
                    "Tongue Cancer",
                    "Tonsillar Cancer",
                    "Uterine Cancer",
                    "Wilms Tumor",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Adrenal Gland Cancer": {
                        "description": "A primary or metastatic malignant neoplasm affecting the adrenal gland.",
                        "termDef": {
                            "term": "Malignant Adrenal Gland Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9338",
                            "term_id": "C9338",
                            "term_version": "19.12e",
                        },
                    },
                    "Basal Cell Cancer": {
                        "description": "The most frequently seen skin cancer. It arises from basal cells of the epidermis and pilosebaceous units. Clinically it is divided into the following types: nodular, ulcerative, superficial, multicentric, erythematous, and sclerosing or morphea-like. More than 95% of these carcinomas occur in patients over 40. They develop on hair-bearing skin, most commonly on sun-exposed areas. Approximately 85% are found on the head and neck and the remaining 15% on the trunk and extremities. Basal cell carcinoma usually grows in a slow and indolent fashion. However, if untreated, the tumor may invade the subcutaneous fat, skeletal muscle and bone. Distant metastases are rare. Excision, curettage and irradiation cure most basal cell carcinomas.",
                        "termDef": {
                            "term": "Skin Basal Cell Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C2921",
                            "term_id": "C2921",
                            "term_version": "19.12e",
                        },
                    },
                    "Bile Duct Cancer": {
                        "description": "A carcinoma arising from the intrahepatic or extrahepatic bile ducts.",
                        "termDef": {
                            "term": "Bile Duct Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C27814",
                            "term_id": "C27814",
                            "term_version": "19.12e",
                        },
                    },
                    "Bladder Cancer": {
                        "description": "A carcinoma arising from the bladder epithelium. Approximately 90% of the bladder carcinomas are transitional cell carcinomas. The remainder are squamous cell carcinomas, adenocarcinomas and small cell neuroendocrine carcinomas.",
                        "termDef": {
                            "term": "Bladder Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4912",
                            "term_id": "C4912",
                            "term_version": "19.12e",
                        },
                    },
                    "Blood Cancer": {
                        "description": "A malignant tumor that originates from myeloid or lymphoid cells i.e., leukemias and lymphomas.",
                        "termDef": {
                            "term": "Liquid Tumor",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C116915",
                            "term_id": "C116915",
                            "term_version": "19.12e",
                        },
                    },
                    "Bone Cancer": {
                        "description": "A primary or metastatic malignant neoplasm affecting the bone or articular cartilage.",
                        "termDef": {
                            "term": "Malignant Bone Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4016",
                            "term_id": "C4016",
                            "term_version": "19.12e",
                        },
                    },
                    "Brain Cancer": {
                        "description": "A primary or metastatic malignant neoplasm affecting the brain.",
                        "termDef": {
                            "term": "Malignant Brain Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3568",
                            "term_id": "C3568",
                            "term_version": "19.12e",
                        },
                    },
                    "Breast Cancer": {
                        "description": "A carcinoma arising from the breast, most commonly the terminal ductal-lobular unit. It is the most common malignant tumor in females. Risk factors include country of birth, family history, menstrual and reproductive history, fibrocystic disease and epithelial hyperplasia, exogenous estrogens, contraceptive agents, and ionizing radiation. The vast majority of breast carcinomas are adenocarcinomas (ductal or lobular). Breast carcinoma spreads by direct invasion, by the lymphatic route, and by the blood vessel route. The most common site of lymph node involvement is the axilla.",
                        "termDef": {
                            "term": "Breast Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4872",
                            "term_id": "C4872",
                            "term_version": "19.12e",
                        },
                    },
                    "Cancer": {
                        "description": "A tumor composed of atypical neoplastic, often pleomorphic cells that invade other tissues. Malignant neoplasms often metastasize to distant anatomic sites and may recur after excision. The most common malignant neoplasms are carcinomas, Hodgkin and non-Hodgkin lymphomas, leukemias, melanomas, and sarcomas.",
                        "termDef": {
                            "term": "Malignant Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9305",
                            "term_id": "C9305",
                            "term_version": "19.12e",
                        },
                    },
                    "Cervical Cancer": {
                        "description": "A carcinoma arising from either the exocervical squamous epithelium or the endocervical glandular epithelium. The major histologic types of cervical carcinoma are: squamous carcinoma, adenocarcinoma, adenosquamous carcinoma, adenoid cystic carcinoma and undifferentiated carcinoma.",
                        "termDef": {
                            "term": "Cervical Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9039",
                            "term_id": "C9039",
                            "term_version": "19.12e",
                        },
                    },
                    "Chondrosarcoma": {
                        "description": "A malignant cartilaginous matrix-producing mesenchymal neoplasm arising from the bone and soft tissue. It usually affects middle-aged to elderly adults. The pelvic bones, ribs, shoulder girdle, and long bones are the most common sites of involvement. Most chondrosarcomas arise de novo, but some may develop in a preexisting benign cartilaginous lesion.",
                        "termDef": {
                            "term": "Chondrosarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C2946",
                            "term_id": "C2946",
                            "term_version": "19.12e",
                        },
                    },
                    "CNS Cancer": {
                        "description": "A primary or metastatic malignant neoplasm involving the brain or spinal cord. Representative examples include anaplastic astrocytoma, glioblastoma, anaplastic (malignant) meningioma, lymphoma, and metastatic carcinoma from another anatomic site.",
                        "termDef": {
                            "term": "Malignant Central Nervous System Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4627",
                            "term_id": "C4627",
                            "term_version": "19.12e",
                        },
                    },
                    "Colorectal Cancer": {
                        "description": "A malignant epithelial neoplasm that arises from the colon or rectum and invades through the muscularis mucosa into the submucosa. The vast majority are adenocarcinomas.",
                        "termDef": {
                            "term": "Colorectal Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C2955",
                            "term_id": "C2955",
                            "term_version": "19.12e",
                        },
                    },
                    "Esophageal Cancer": {
                        "description": "A malignant epithelial tumor arising from the esophageal mucosa. Two major histologic types of esophageal carcinoma have been described: squamous cell carcinoma and adenocarcinoma. This type of cancer is associated with excessive ethanol and cigarette usage.",
                        "termDef": {
                            "term": "Esophageal Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3513",
                            "term_id": "C3513",
                            "term_version": "19.12e",
                        },
                    },
                    "Ewing Sarcoma": {
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
                    "Gallbladder Cancer": {
                        "description": "A malignant tumor arising from the epithelium of the gallbladder. It is usually associated with the presence of gallstones. Clinical symptoms are not specific and usually present late in the course. Morphologically, most gallbladder carcinomas are adenocarcinomas; squamous cell carcinomas, adenosquamous carcinomas, signet ring carcinomas, and undifferentiated carcinomas can also occur.",
                        "termDef": {
                            "term": "Gallbladder Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3844",
                            "term_id": "C3844",
                            "term_version": "19.12e",
                        },
                    },
                    "Gastric Cancer": {
                        "description": "A malignant epithelial tumor of the stomach mucosa. The vast majority of gastric carcinomas are adenocarcinomas, arising from the gastric glandular epithelium.",
                        "termDef": {
                            "term": "Gastric Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4911",
                            "term_id": "C4911",
                            "term_version": "19.12e",
                        },
                    },
                    "Glioblastoma": {
                        "description": "The most malignant astrocytic tumor (WHO grade IV). It is composed of poorly differentiated neoplastic astrocytes and it is characterized by the presence of cellular polymorphism, nuclear atypia, brisk mitotic activity, vascular thrombosis, microvascular proliferation and necrosis. It typically affects adults and is preferentially located in the cerebral hemispheres. It may develop from diffuse astrocytoma WHO grade II or anaplastic astrocytoma (secondary glioblastoma, IDH-mutant), but more frequently, it manifests after a short clinical history de novo, without evidence of a less malignant precursor lesion (primary glioblastoma, IDH- wildtype). (Adapted from WHO)",
                        "termDef": {
                            "term": "Glioblastoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3058",
                            "term_id": "C3058",
                            "term_version": "19.12e",
                        },
                    },
                    "Gynecologic Cancer": {
                        "description": "A primary or metastatic malignant neoplasm involving the female reproductive system. Representative examples include endometrial carcinoma, cervical carcinoma, ovarian carcinoma, uterine corpus leiomyosarcoma, adenosarcoma, malignant mixed mesodermal (mullerian) tumor, and gestational choriocarcinoma.",
                        "termDef": {
                            "term": "Malignant Female Reproductive System Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4913",
                            "term_id": "C4913",
                            "term_version": "19.12e",
                        },
                    },
                    "Head and Neck Cancer": {
                        "description": "A primary or metastatic malignant neoplasm affecting the head and neck. Representative examples include oral cavity squamous cell carcinoma, laryngeal squamous cell carcinoma, and salivary gland carcinoma.",
                        "termDef": {
                            "term": "Malignant Head and Neck Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4013",
                            "term_id": "C4013",
                            "term_version": "19.12e",
                        },
                    },
                    "Hematologic Cancer": {
                        "description": "A neoplasm arising from hematopoietic cells found in the bone marrow, peripheral blood, lymph nodes and spleen (organs of the hematopoietic system). Hematopoietic cell neoplasms can also involve other anatomic sites (e.g. central nervous system, gastrointestinal tract), either by metastasis, direct tumor infiltration, or neoplastic transformation of extranodal lymphoid tissues. The commonest forms are the various types of leukemia, Hodgkin and non-Hodgkin lymphomas, myeloproliferative neoplasms, and myelodysplastic syndromes.",
                        "termDef": {
                            "term": "Hematopoietic and Lymphoid Cell Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C27134",
                            "term_id": "C27134",
                            "term_version": "19.12e",
                        },
                    },
                    "Kaposi Sarcoma": {
                        "description": "A malignant neoplasm characterized by a vascular proliferation which usually contains blunt endothelial cells. Erythrocyte extravasation and hemosiderin deposition are frequently present. The most frequent site of involvement is the skin; however it may also occur internally. It generally develops in people with compromised immune systems including those with acquired immune deficiency syndrome (AIDS).",
                        "termDef": {
                            "term": "Kaposi Sarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9087",
                            "term_id": "C9087",
                            "term_version": "19.12e",
                        },
                    },
                    "Kidney Cancer": {
                        "description": "A carcinoma arising from the epithelium of the renal parenchyma or the renal pelvis. The majority are renal cell carcinomas. Kidney carcinomas usually affect middle aged and elderly adults. Hematuria, abdominal pain, and a palpable mass are common symptoms.",
                        "termDef": {
                            "term": "Kidney Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9384",
                            "term_id": "C9384",
                            "term_version": "19.12e",
                        },
                    },
                    "Laryngeal Cancer": {
                        "description": "Carcinoma that arises from the laryngeal epithelium. More than 90% of laryngeal carcinomas are squamous cell carcinomas. The remainder are adenoid cystic carcinomas, mucoepidermoid carcinomas and carcinomas with neuroendocrine differentiation.",
                        "termDef": {
                            "term": "Laryngeal Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4855",
                            "term_id": "C4855",
                            "term_version": "19.12e",
                        },
                    },
                    "Leukemia": {
                        "description": "A malignant (clonal) hematologic disorder, involving hematopoietic stem cells and characterized by the presence of primitive or atypical myeloid or lymphoid cells in the bone marrow and the blood. Leukemias are classified as acute or chronic based on the degree of cellular differentiation and the predominant cell type present. Leukemia is usually associated with anemia, fever, hemorrhagic episodes, and splenomegaly. Common leukemias include acute myeloid leukemia, chronic myelogenous leukemia, acute lymphoblastic or precursor lymphoblastic leukemia, and chronic lymphocytic leukemia. Treatment is vital to patient survival; untreated, the natural course of acute leukemias is normally measured in weeks or months, while that of chronic leukemias is more often measured in months or years.",
                        "termDef": {
                            "term": "Leukemia",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3161",
                            "term_id": "C3161",
                            "term_version": "19.12e",
                        },
                    },
                    "Liver Cancer": {
                        "description": "A carcinoma that arises from the hepatocytes or intrahepatic bile ducts. The main subtypes are hepatocellular carcinoma (hepatoma) and cholangiocarcinoma.",
                        "termDef": {
                            "term": "Liver and Intrahepatic Bile Duct Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C7927",
                            "term_id": "C7927",
                            "term_version": "19.12e",
                        },
                    },
                    "Lung Cancer": {
                        "description": "A carcinoma originating in the lung. Lung carcinomas usually arise from the epithelium that lines the bronchial tree (bronchogenic carcinomas), and are classified as small cell or non-small cell carcinomas. Non-small cell lung carcinomas are usually adenocarcinomas, squamous cell carcinomas, or large cell carcinomas. Metastatic carcinomas to the lung are also common, and can be difficult to distinguish from primary tumors.",
                        "termDef": {
                            "term": "Lung Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4878",
                            "term_id": "C4878",
                            "term_version": "19.12e",
                        },
                    },
                    "Lymph Node Cancer": {
                        "description": "A primary or metastatic malignant tumor involving the lymph node. Lymphomas and metastatic carcinomas are representative examples.",
                        "termDef": {
                            "term": "Malignant Lymph Node Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C35812",
                            "term_id": "C35812",
                            "term_version": "19.12e",
                        },
                    },
                    "Lymphoma": {
                        "description": "A malignant (clonal) proliferation of B- lymphocytes or T- lymphocytes which involves the lymph nodes, bone marrow and/or extranodal sites. This category includes Non-Hodgkin lymphomas and Hodgkin lymphomas.",
                        "termDef": {
                            "term": "Lymphoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3208",
                            "term_id": "C3208",
                            "term_version": "19.12e",
                        },
                    },
                    "Melanoma": {
                        "description": "A malignant, usually aggressive tumor composed of atypical, neoplastic melanocytes. Most often, melanomas arise in the skin (cutaneous melanomas) and include the following histologic subtypes: superficial spreading melanoma, nodular melanoma, acral lentiginous melanoma, and lentigo maligna melanoma. Cutaneous melanomas may arise from acquired or congenital melanocytic or dysplastic nevi. Melanomas may also arise in other anatomic sites including the gastrointestinal system, eye, urinary tract, and reproductive system. Melanomas frequently metastasize to lymph nodes, liver, lungs, and brain.",
                        "termDef": {
                            "term": "Melanoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3224",
                            "term_id": "C3224",
                            "term_version": "19.12e",
                        },
                    },
                    "Mesothelioma": {
                        "description": "A usually malignant and aggressive neoplasm of the mesothelium which is often associated with exposure to asbestos.",
                        "termDef": {
                            "term": "Mesothelioma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3234",
                            "term_id": "C3234",
                            "term_version": "19.12e",
                        },
                    },
                    "Multiple Myeloma": {
                        "description": "A bone marrow-based plasma cell neoplasm characterized by a serum monoclonal protein and skeletal destruction with osteolytic lesions, pathological fractures, bone pain, hypercalcemia, and anemia. Clinical variants include non-secretory myeloma, smoldering myeloma, indolent myeloma, and plasma cell leukemia.",
                        "termDef": {
                            "term": "Plasma Cell Myeloma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3242",
                            "term_id": "C3242",
                            "term_version": "19.12e",
                        },
                    },
                    "Neuroblastoma": {
                        "description": "A neuroblastic tumor characterized by the presence of neuroblastic cells, the absence of ganglion cells, and the absence of a prominent Schwannian stroma formation.",
                        "termDef": {
                            "term": "Neuroblastoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3270",
                            "term_id": "C3270",
                            "term_version": "19.12e",
                        },
                    },
                    "Osteosarcoma": {
                        "description": "A usually aggressive malignant bone-forming mesenchymal neoplasm, predominantly affecting adolescents and young adults. It usually involves bones and less frequently extraosseous sites. It often involves the long bones (particularly distal femur, proximal tibia, and proximal humerus). Pain with or without a palpable mass is the most frequent clinical symptom. It may spread to other anatomic sites, particularly the lungs.",
                        "termDef": {
                            "term": "Osteosarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9145",
                            "term_id": "C9145",
                            "term_version": "19.12e",
                        },
                    },
                    "Ovarian Cancer": {
                        "description": "A primary or metastatic malignant neoplasm involving the ovary. Most primary malignant ovarian neoplasms are either carcinomas (serous, mucinous, or endometrioid adenocarcinomas) or malignant germ cell tumors. Metastatic malignant neoplasms to the ovary include carcinomas, lymphomas, and melanomas.",
                        "termDef": {
                            "term": "Malignant Ovarian Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C7431",
                            "term_id": "C7431",
                            "term_version": "19.12e",
                        },
                    },
                    "Pancreas Cancer": {
                        "description": "A carcinoma arising from the exocrine pancreas. The overwhelming majority of pancreatic carcinomas are adenocarcinomas.",
                        "termDef": {
                            "term": "Pancreatic Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3850",
                            "term_id": "C3850",
                            "term_version": "19.12e",
                        },
                    },
                    "Pediatric Liver Cancer": {
                        "description": "A malignant neoplasm of the liver developed in childhood. Representative examples include hepatoblastoma, undifferentiated (embryonal) sarcoma, and extrarenal rhabdoid tumor.",
                        "termDef": {
                            "term": "Childhood Malignant Liver Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C7708",
                            "term_id": "C7708",
                            "term_version": "19.12e",
                        },
                    },
                    "Prostate Cancer": {
                        "description": "One of the most common malignant tumors afflicting men. The majority of carcinomas arise in the peripheral zone and a minority occur in the central or the transitional zone of the prostate gland. Grossly, prostatic carcinomas appear as ill-defined yellow areas of discoloration in the prostate gland lobes. Adenocarcinomas represent the overwhelming majority of prostatic carcinomas. Prostatic-specific antigen (PSA) serum test is widely used as a screening test for the early detection of prostatic carcinoma. Treatment options include radical prostatectomy, radiation therapy, androgen ablation and cryotherapy. Watchful waiting or surveillance alone is an option for older patients with low-grade or low-stage disease.",
                        "termDef": {
                            "term": "Prostate Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4863",
                            "term_id": "C4863",
                            "term_version": "19.12e",
                        },
                    },
                    "Rectal Cancer": {
                        "description": "A malignant epithelial neoplasm that arises from the rectum and invades through the muscularis mucosa into the submucosa. The vast majority are adenocarcinomas.",
                        "termDef": {
                            "term": "Rectal Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9382",
                            "term_id": "C9382",
                            "term_version": "19.12e",
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
                    "Sarcoma": {
                        "description": "A usually aggressive malignant neoplasm of the soft tissue or bone. It arises from muscle, fat, fibrous tissue, bone, cartilage, and blood vessels. Sarcomas occur in both children and adults. The prognosis depends largely on the degree of differentiation (grade) of the neoplasm. Representative subtypes are liposarcoma, leiomyosarcoma, osteosarcoma, and chondrosarcoma.",
                        "termDef": {
                            "term": "Sarcoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9118",
                            "term_id": "C9118",
                            "term_version": "19.12e",
                        },
                    },
                    "Skin Cancer": {
                        "description": "A primary or metastatic malignant neoplasm involving the skin. Primary malignant skin neoplasms most often are carcinomas (either basal cell or squamous cell carcinomas) or melanomas. Metastatic malignant neoplasms to the skin include carcinomas and lymphomas.",
                        "termDef": {
                            "term": "Malignant Skin Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C2920",
                            "term_id": "C2920",
                            "term_version": "19.12e",
                        },
                    },
                    "Spleen Cancer": {
                        "description": "A malignant neoplasm affecting the spleen. Representative examples include leukemias, lymphomas, and sarcomas.",
                        "termDef": {
                            "term": "Malignant Splenic Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3539",
                            "term_id": "C3539",
                            "term_version": "19.12e",
                        },
                    },
                    "Testicular Cancer": {
                        "description": "A malignant tumor predominantly affecting young men and often associated with cryptorchidism. Seminoma is the most frequently seen malignant testicular germ cell tumor, followed by embryonal carcinoma and yolk sac tumor.",
                        "termDef": {
                            "term": "Malignant Testicular Germ Cell Tumor",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C9063",
                            "term_id": "C9063",
                            "term_version": "19.12e",
                        },
                    },
                    "Throat Cancer": {
                        "description": "Carcinoma, predominantly squamous cell, arising from epithelial cells of the larynx or pharynx.",
                        "termDef": {
                            "term": "Throat Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C35506",
                            "term_id": "C35506",
                            "term_version": "19.12e",
                        },
                    },
                    "Thyroid Cancer": {
                        "description": "A carcinoma arising from the thyroid gland. It includes the following main subtypes: follicular, papillary, medullary, poorly differentiated, and undifferentiated (anaplastic) carcinoma.",
                        "termDef": {
                            "term": "Thyroid Gland Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4815",
                            "term_id": "C4815",
                            "term_version": "19.12e",
                        },
                    },
                    "Tongue Cancer": {
                        "description": "A malignant tumor arising from the epithelium that covers the tongue. The vast majority of tongue carcinomas are moderately or poorly differentiated squamous cell carcinomas.",
                        "termDef": {
                            "term": "Tongue Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4824",
                            "term_id": "C4824",
                            "term_version": "19.12e",
                        },
                    },
                    "Tonsillar Cancer": {
                        "description": "A carcinoma arising from the tonsilar epithelium.",
                        "termDef": {
                            "term": "Tonsillar Carcinoma",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C4825",
                            "term_id": "C4825",
                            "term_version": "19.12e",
                        },
                    },
                    "Uterine Cancer": {
                        "description": "Primary or metastatic malignant neoplasm involving the uterine corpus and/or the cervix.",
                        "termDef": {
                            "term": "Malignant Uterine Neoplasm",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3552",
                            "term_id": "C3552",
                            "term_version": "19.12e",
                        },
                    },
                    "Wilms Tumor": {
                        "description": "An embryonal neoplasm characterized by the presence of epithelial, mesenchymal, and blastema components. The vast majority of cases arise from the kidney. A small number of cases with morphologic features resembling Wilms tumor of the kidney have been reported arising from the ovary and the cervix.",
                        "termDef": {
                            "term": "Wilms Tumor",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3267",
                            "term_id": "C3267",
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
            "relative_with_cancer_history": {
                "description": "The yes/no/unknown indicator used to describe whether any of the patient's relatives have a history of cancer.",
                "termDef": {
                    "term": "Relative Malignant Diagnosis Indicator",
                    "source": "caDSR",
                    "cde_id": 6161023,
                    "cde_version": 1.0,
                    "term_url": "https://cdebrowser.nci.nih.gov/cdebrowserClient/cdeBrowser.html#/search?publicId=6161023&version=1.0",
                },
                "enum": ["yes", "no", "unknown", "not reported"],
                "enumDef": {
                    "yes": {
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
                    "no": {
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
                    "unknown": {
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
                    "not reported": {
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
            "relatives_with_cancer_history_count": {
                "description": "The number of relatives the patient has with a known history of cancer.",
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
        },
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "family_history"

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
                "name": "family_histories",
                "src_type": base.Node.get_subclass("annotation"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "family_histories",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "family_histories",
                "type": base.Node.get_subclass("case"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "cases": {
                "edge_out": "_FamilyHistoryDescribesCase_out",
                "dst_type": base.Node.get_subclass("case"),
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

    @psqlgraph.pg_property(float, int)
    def relationship_age_at_diagnosis(self, value):
        self._set_property("relationship_age_at_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["female", "male", "not reported", "unknown", "unspecified"])
    def relationship_gender(self, value):
        self._set_property("relationship_gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Adrenal Gland Cancer",
            "Basal Cell Cancer",
            "Bile Duct Cancer",
            "Bladder Cancer",
            "Blood Cancer",
            "Bone Cancer",
            "Brain Cancer",
            "Breast Cancer",
            "CNS Cancer",
            "Cancer",
            "Cervical Cancer",
            "Chondrosarcoma",
            "Colorectal Cancer",
            "Esophageal Cancer",
            "Ewing Sarcoma",
            "Gallbladder Cancer",
            "Gastric Cancer",
            "Glioblastoma",
            "Gynecologic Cancer",
            "Head and Neck Cancer",
            "Hematologic Cancer",
            "Kaposi Sarcoma",
            "Kidney Cancer",
            "Laryngeal Cancer",
            "Leukemia",
            "Liver Cancer",
            "Lung Cancer",
            "Lymph Node Cancer",
            "Lymphoma",
            "Melanoma",
            "Mesothelioma",
            "Multiple Myeloma",
            "Neuroblastoma",
            "Not Reported",
            "Osteosarcoma",
            "Ovarian Cancer",
            "Pancreas Cancer",
            "Pediatric Liver Cancer",
            "Prostate Cancer",
            "Rectal Cancer",
            "Rhabdomyosarcoma",
            "Sarcoma",
            "Skin Cancer",
            "Spleen Cancer",
            "Testicular Cancer",
            "Throat Cancer",
            "Thyroid Cancer",
            "Tongue Cancer",
            "Tonsillar Cancer",
            "Unknown",
            "Uterine Cancer",
            "Wilms Tumor",
        ],
    )
    def relationship_primary_diagnosis(self, value):
        self._set_property("relationship_primary_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Adopted Brother",
            "Adopted Daughter",
            "Adopted Sister",
            "Adopted Son",
            "Adoptive Father",
            "Adoptive Mother",
            "Aunt",
            "Brother",
            "Brother-in-law",
            "Child",
            "Cousin",
            "Daughter",
            "Daughter-in-law",
            "Domestic Partner",
            "Father",
            "Father-in-law",
            "Female Cousin",
            "Female Sibling of Adopted Child",
            "First Cousin",
            "First Cousin Once Removed",
            "First Degree Relative, NOS",
            "Foster Brother",
            "Foster Daughter",
            "Foster Father",
            "Foster Mother",
            "Foster Sister",
            "Foster Son",
            "Fraternal Twin Brother",
            "Fraternal Twin Sibling",
            "Fraternal Twin Sister",
            "Full Brother",
            "Full Sister",
            "Grand Nephew",
            "Grand Niece",
            "Grandchild",
            "Granddaughter",
            "Grandfather",
            "Grandmother",
            "Grandparent",
            "Grandson",
            "Great Grandchild",
            "Half Brother",
            "Half Sibling",
            "Half Sister",
            "Husband",
            "Identical Twin Brother",
            "Identical Twin Sibling",
            "Identical Twin Sister",
            "Legal Guardian",
            "Male Cousin",
            "Male Sibling of Adopted Child",
            "Maternal Aunt",
            "Maternal First Cousin",
            "Maternal First Cousin Once Removed",
            "Maternal Grandfather",
            "Maternal Grandmother",
            "Maternal Grandparent",
            "Maternal Great Aunt",
            "Maternal Great Grandparent",
            "Maternal Great Uncle",
            "Maternal Half Brother",
            "Maternal Half Sibling",
            "Maternal Half Sister",
            "Maternal Uncle",
            "Mother",
            "Mother-in-law",
            "Natural Brother",
            "Natural Child",
            "Natural Daughter",
            "Natural Father",
            "Natural Grandchild",
            "Natural Grandfather",
            "Natural Grandmother",
            "Natural Grandparent",
            "Natural Mother",
            "Natural Parent",
            "Natural Sibling",
            "Natural Sister",
            "Natural Son",
            "Nephew",
            "Niece",
            "Niece Second Degree Relative",
            "Not Reported",
            "Other",
            "Parent",
            "Paternal Aunt",
            "Paternal First Cousin",
            "Paternal First Cousin Once Removed",
            "Paternal Grandfather",
            "Paternal Grandmother",
            "Paternal Grandparent",
            "Paternal Great Aunt",
            "Paternal Great Grandparent",
            "Paternal Great Uncle",
            "Paternal Half Brother",
            "Paternal Half Sibling",
            "Paternal Half Sister",
            "Paternal Uncle",
            "Sibling",
            "Sister",
            "Sister-in-law",
            "Son",
            "Son-in-law",
            "Spouse",
            "Step Child",
            "Step Sibling",
            "Stepbrother",
            "Stepdaughter",
            "Stepfather",
            "Stepmother",
            "Stepsister",
            "Stepson",
            "Twin Sibling",
            "Uncle",
            "Unknown",
            "Unrelated",
            "Ward",
            "Wife",
        ],
    )
    def relationship_type(self, value):
        self._set_property("relationship_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def relative_deceased(self, value):
        self._set_property("relative_deceased", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def relative_smoker(self, value):
        self._set_property("relative_smoker", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["no", "not reported", "unknown", "yes"])
    def relative_with_cancer_history(self, value):
        self._set_property("relative_with_cancer_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def relatives_with_cancer_history_count(self, value):
        self._set_property("relatives_with_cancer_history_count", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FamilyHistory)
datetime_hooks.cls_inject_updated_datetime_hook(FamilyHistory)
