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


class Exposure(base.Node):
    __tablename__: str = "node_exposure"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Exposure",
        "namespace": "https://gdc.cancer.gov",
        "category": "clinical",
        "submittable": True,
        "downloadable": False,
        "description": "Clinically relevant patient information not immediately resulting from genetic predispositions.",
        "required": ["submitter_id"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "name": "cases",
                "backref": "exposures",
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
            "age_at_last_exposure": {
                "description": "The study participant's age at the time they were last exposed.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "maximum": 89,
                "minimum": 0,
            },
            "age_at_onset": {
                "description": "Numeric value used to represent the age of the patient when exposure to a specific environmental factor began.",
                "termDef": {
                    "term": "Patient Environmental Exposure Onset Age Day Value",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
                "maximum": 89,
                "minimum": 0,
            },
            "alcohol_days_per_week": {
                "description": "Numeric value used to describe the average number of days each week that a person consumes an alcoholic beverage.",
                "termDef": {
                    "term": "Alcohol Consumption Weekly Days Usage Number",
                    "source": "caDSR",
                    "cde_id": 3114013,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3114013%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 7,
                "minimum": 0,
            },
            "alcohol_drinks_per_day": {
                "description": "Numeric value used to describe the average number of alcoholic beverages a person consumes per day.",
                "termDef": {
                    "term": "Person Daily Alcohol Consumption Count",
                    "source": "caDSR",
                    "cde_id": 3124961,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3124961%20and%20ver_nr=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "alcohol_frequency": {
                "description": "Describes how often the subject drinks alcohol.",
                "termDef": {
                    "term": "Alcohol Frequency",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Daily Drinker", "Weekly Drinker"],
            },
            "alcohol_history": {
                "description": "A response to a question that asks whether the participant has consumed at least 12 drinks of any kind of alcoholic beverage in their lifetime.",
                "termDef": {
                    "term": "Alcohol Lifetime History Indicator",
                    "source": "caDSR",
                    "cde_id": 2201918,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2201918%20and%20ver_nr=1.0",
                },
                "enum": ["Yes", "No", "yes", "no", "Unknown", "Not Reported"],
                "deprecated_enum": ["no", "yes"],
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
            "alcohol_intensity": {
                "description": "Category to describe the patient's current level of alcohol use as self-reported by the patient.",
                "termDef": {
                    "term": "Person Self-Report Alcoholic Beverage Exposure Category",
                    "source": "caDSR",
                    "cde_id": 3457767,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3457767%20and%20ver_nr=1.0",
                },
                "enum": [
                    "Drinker",
                    "Heavy Drinker",
                    "Lifelong Non-Drinker",
                    "Non-Drinker",
                    "Occasional Drinker",
                    "Social Drinker",
                    "Unknown",
                    "Not Reported",
                ],
                "enumDef": {
                    "Drinker": {
                        "description": "An individual who drinks at least once per week with regularity.",
                        "termDef": {
                            "term": "Drinker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126383",
                            "term_id": "C126383",
                            "term_version": "19.12e",
                        },
                    },
                    "Heavy Drinker": {
                        "description": "A man who drinks more than 14 standard drinks per week or a woman who drinks more than 7 standard drinks per week.",
                        "termDef": {
                            "term": "Heavy Drinker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126384",
                            "term_id": "C126384",
                            "term_version": "19.12e",
                        },
                    },
                    "Lifelong Non-Drinker": {
                        "description": "An individual who does not drink at the present time and who claims that they have never been a drinker.",
                        "termDef": {
                            "term": "Lifelong Non-Drinker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126380",
                            "term_id": "C126380",
                            "term_version": "19.12e",
                        },
                    },
                    "Non-Drinker": {
                        "description": "An individual who does not drink at the present time. This is a heterogeneous group comprising both lifelong teetotallers and ex-drinkers.",
                        "termDef": {
                            "term": "Non-Drinker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126379",
                            "term_id": "C126379",
                            "term_version": "19.12e",
                        },
                    },
                    "Occasional Drinker": {
                        "description": "An individual who drinks from time to time, but generally less than once per week.",
                        "termDef": {
                            "term": "Occasional Drinker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C126382",
                            "term_id": "C126382",
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
            "alcohol_type": {
                "description": "A specific type of alcohol.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Beer", "Liquor", "Wine", "Other", "Unknown", "Not Reported"],
                "enumDef": {
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
            "asbestos_exposure": {
                "description": "The yes/no/unknown indicator used to describe whether the patient was exposed to asbestos.",
                "termDef": {
                    "term": "Asbestos Exposure Ind-3",
                    "source": "caDSR",
                    "cde_id": 1253,
                    "cde_version": 3.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=1253%20and%20ver_nr=3.0",
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
            "asbestos_exposure_type": {
                "description": "The type of asbestos exposure the study participant experienced.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Amosite", "Crocidolite"],
            },
            "chemical_exposure_type": {
                "description": "The specific type of contact with a chemical substance through touch, inhalation, or ingestion.",
                "termDef": {
                    "term": "Chemical Exposure",
                    "source": "NCIt",
                    "cde_id": "C36290",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C36290",
                },
                "type": "array",
                "items": {
                    "enum": [
                        "Agent Orange",
                        "Aluminum",
                        "Arsenic",
                        "Asbestos",
                        "Benzene",
                        "Cadmium",
                        "Chemical Exposure, NOS",
                        "Chromium",
                        "Coal Gas, Coal Tar, Coal Tar Pitch, and Derivatives",
                        "Coke Oven Emission",
                        "Copper",
                        "Diesel Exhaust",
                        "Disinfectant",
                        "Formaldehyde",
                        "Methylene Chloride",
                        "Occupational Soldering/Welding Smoke Exposure",
                        "Oil",
                        "Pesticide",
                        "Petroleum Hydrocarbon Compound",
                        "Resin Fumes",
                        "Sodium Borate",
                        "Solvent",
                        "Tetrachloroethylene",
                        "Toluene",
                        "Not Reported",
                    ]
                },
            },
            "cigarettes_per_day": {
                "description": "The average number of cigarettes smoked per day.",
                "termDef": {
                    "term": "Smoking Use Average Number",
                    "source": "caDSR",
                    "cde_id": 2001716,
                    "cde_version": 4.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2001716%20and%20ver_nr=4.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "coal_dust_exposure": {
                "description": "The yes/no/unknown indicator used to describe whether a patient was exposed to fine powder derived by the crushing of coal.",
                "termDef": {
                    "term": "Person Coal Dust Exposure Indicator",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
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
            "environmental_tobacco_smoke_exposure": {
                "description": "The yes/no/unknown indicator used to describe whether a patient was exposed to smoke that is emitted from burning tobacco, including cigarettes, pipes, and cigars. This includes tobacco smoke exhaled by smokers.",
                "termDef": {
                    "term": "Person Environmental Tobacco Smoke Exposure Indicator",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
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
            "exposure_duration": {
                "description": "Text term used to describe the length of time the patient was exposed to an environmental factor.",
                "termDef": {
                    "term": "Patient Exposure Duration",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Six Weeks or More", "Unknown", "Not Reported"],
                "enumDef": {
                    "Six Weeks or More": {
                        "description": "The text term used to describe a time period of six calendar weeks or longer.",
                        "termDef": {
                            "term": "Six Weeks or More",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": None,
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
            "exposure_duration_hrs_per_day": {
                "description": "The duration (in hours per day) that a person was exposed.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "maximum": 24,
                "minimum": 0,
            },
            "exposure_duration_years": {
                "description": "The period of time from start to finish of exposure, in years.",
                "termDef": {
                    "term": "Exposure Duration",
                    "source": "NCIt",
                    "cde_id": "C83280",
                    "cde_version": "21.04d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C83280",
                },
                "type": "integer",
                "maximum": 89,
                "minimum": 0,
            },
            "exposure_source": {
                "description": "The source or location where the patient was exposed.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Occupational", "Secondary", "Unknown"],
            },
            "exposure_type": {
                "description": "The text term used to describe the type of environmental exposure.",
                "termDef": {
                    "term": "Patient Exposure Type",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Asbestos",
                    "Chemical",
                    "Coal Dust",
                    "Dust, NOS",
                    "Marijuana",
                    "Radiation",
                    "Radon",
                    "Respirable Crystalline Silica",
                    "Smoke",
                    "Smokeless Tobacco",
                    "Tobacco",
                    "Wood Dust",
                ],
                "enumDef": {
                    "Dust, NOS": {
                        "description": "A fine powdery material such as dry earth or pollen that can be blown about in the air.",
                        "termDef": {
                            "term": "Dust",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C84281",
                            "term_id": "C84281",
                            "term_version": "23.03d",
                        },
                    },
                    "Marijuana": {
                        "description": "Any part of, or extract from, the female hemp plant Cannabis sativa. Marijuana contains cannabinoids, substances with hallucinogenic, psychoactive, and addictive properties. This agent has potential use for treating cancer pain and cachexia.",
                        "termDef": {
                            "term": "Marijuana",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C26659",
                            "term_id": "C26659",
                            "term_version": "19.12e",
                        },
                    },
                    "Tobacco": {
                        "description": "The dried cured leaves of the tobacco plant, Nicotiana tabacum, used for smoking, chewing, or snuff. Tobacco contains nicotine, a stimulant, and other biologically active ingredients having carcinogenic properties.",
                        "termDef": {
                            "term": "Tobacco",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C891",
                            "term_id": "C891",
                            "term_version": "19.12e",
                        },
                    },
                },
            },
            "occupation_duration_years": {
                "description": "The number of years a patient worked in a specific occupation.",
                "termDef": {
                    "term": "Person Occupation Years Number",
                    "source": "caDSR",
                    "cde_id": 2435424,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2435424%20and%20ver_nr=1.0",
                },
                "type": "integer",
                "maximum": 89,
                "minimum": 0,
            },
            "occupation_type": {
                "description": "A categorization of the principal activity that a person does to earn money, as defined by the International Classification of Occupation (ISCO).",
                "termDef": {
                    "term": "Occupation",
                    "source": "NCIt",
                    "cde_id": "C25193",
                    "cde_version": "22.11d",
                    "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25193",
                },
                "type": "array",
                "items": {
                    "enum": [
                        "Administration Professionals",
                        "Administrative and Specialized Secretaries",
                        "Agricultural, Forestry and Fishery Labourers",
                        "Animal Producers",
                        "Architects, Planners, Surveyors and Designers",
                        "Armed Forces Occupations, Other Ranks",
                        "Artistic, Cultural and Culinary Associate Professionals",
                        "Assemblers",
                        "Authors, Journalists and Linguists",
                        "Blacksmiths, Toolmakers and Related Trades Workers",
                        "Building and Housekeeping Supervisors",
                        "Building Finishers and Related Trades Workers",
                        "Building Frame and Related Trades Workers",
                        "Business Services Agents",
                        "Business Services and Administration Managers",
                        "Car, Van and Motorcycle Drivers",
                        "Cashiers and Ticket Clerks",
                        "Chemical and Photographic Products Plant and Machine Operators",
                        "Child Care Workers and Teachers' Aides",
                        "Client Information Workers",
                        "Commissioned Armed Forces Officers",
                        "Cooks",
                        "Creative and Performing Artists",
                        "Database and Network Professionals",
                        "Domestic, Hotel and Office Cleaners and Helpers",
                        "Electrical Equipment Installers and Repairers",
                        "Electronics and Telecommunications Installers and Repairers",
                        "Electrotechnology Engineers",
                        "Engineering Professionals (excluding Electrotechnology)",
                        "Finance Professionals",
                        "Financial and Mathematical Associate Professionals",
                        "Fishery Workers, Hunters and Trappers",
                        "Food and Related Products Machine Operators",
                        "Food Preparation Assistants",
                        "Food Processing and Related Trades Workers",
                        "Forestry and Related Workers",
                        "Garment and Related Trades Workers",
                        "General Office Clerks",
                        "Government Regulatory Associate Professionals",
                        "Hairdressers, Beauticians and Related Workers",
                        "Handicraft Workers",
                        "Heavy Truck and Bus Drivers",
                        "Hotel and Restaurant Managers",
                        "Information and Communications Technology Operations and User Support Technicians",
                        "Information and Communications Technology Service managers",
                        "Keyboard Operators",
                        "Legal Professionals",
                        "Legal, Social and Religious Associate Professionals",
                        "Legislators and Senior Officials",
                        "Librarians, Archivists and Curators",
                        "Life Science Professionals",
                        "Life Science Technicians and Related Associate Professionals",
                        "Locomotive Engine Drivers and Related Workers",
                        "Machinery Mechanics and Repairers",
                        "Managing Directors and Chief Executives",
                        "Manufacturing Labourers",
                        "Manufacturing, Mining, Construction and Distribution Managers",
                        "Market Gardeners and Crop Growers",
                        "Material Recording and Transport Clerks",
                        "Mathematicians, Actuaries and Statisticians",
                        "Medical and Pharmaceutical Technicians",
                        "Medical Doctors",
                        "Metal Processing and Finishing Plant Operators",
                        "Mining and Construction Labourers",
                        "Mining and Mineral Processing Plant Operators",
                        "Mining, Manufacturing and Construction Supervisors",
                        "Mixed Crop and Animal Producers",
                        "Mobile Plant Operators",
                        "Non-commissioned Armed Forces Officers",
                        "Numerical Clerks",
                        "Nursing and Midwifery Associate Professionals",
                        "Nursing and Midwifery Professionals",
                        "Other Clerical Support Workers",
                        "Other Craft and Related Workers",
                        "Other Elementary Workers",
                        "Other Health Associate Professionals",
                        "Other Health Professionals",
                        "Other Personal Services Workers",
                        "Other Sales Workers",
                        "Other Services Managers",
                        "Other Stationary Plant and Machine Operators",
                        "Other Teaching Professionals",
                        "Painters, Building Structure Cleaners and Related Trades Workers",
                        "Paramedical Practitioners",
                        "Personal Care Workers in Health Services",
                        "Physical and Earth Science Professionals",
                        "Physical and Engineering Science Technicians",
                        "Primary School and Early Childhood Teachers",
                        "Printing Trades Workers",
                        "Process Control Technicians",
                        "Production Managers in Agriculture, Forestry and Fisheries",
                        "Professional Services Managers",
                        "Protective Services Workers",
                        "Refuse Workers",
                        "Retail and Wholesale Trade Managers",
                        "Rubber, Plastic and Paper Products Machine Operators",
                        "Sales and Purchasing Agents and Brokers",
                        "Sales, Marketing and Development Managers",
                        "Sales, Marketing and Public Relations Professionals",
                        "Secondary Education Teachers",
                        "Secretaries (general)",
                        "Sheet and Structural Metal Workers, Moulders and Welders, and Related Workers",
                        "Ship and Aircraft Controllers and Technicians",
                        "Ships' Deck Crews and Related Workers",
                        "Shop Salespersons",
                        "Social and Religious Professionals",
                        "Software and Applications Developers and Analysts",
                        "Sports and Fitness Workers",
                        "Street and Market Salespersons",
                        "Street and Related Service Workers",
                        "Street Vendors (excluding Food)",
                        "Subsistence Crop Farmers",
                        "Subsistence Fishers, Hunters, Trappers and Gatherers",
                        "Subsistence Livestock Farmers",
                        "Subsistence Mixed Crop and Livestock Farmers",
                        "Telecommunications and Broadcasting Technicians",
                        "Tellers, Money Collectors and Related Clerks",
                        "Textile, Fur and Leather Products Machine Operators",
                        "Traditional and Complementary Medicine Associate Professionals",
                        "Traditional and Complementary Medicine Professionals",
                        "Transport and Storage Labourers",
                        "Travel Attendants, Conductors and Guides",
                        "University and Higher Education Teachers",
                        "Vehicle, Window, Laundry and Other Hand Cleaning Workers",
                        "Veterinarians",
                        "Veterinary Technicians and Assistants",
                        "Vocational education teachers",
                        "Waiters and Bartenders",
                        "Wood Processing and Papermaking Plant Operators",
                        "Wood Treaters, Cabinet-makers and Related Trades Workers",
                    ]
                },
            },
            "pack_years_smoked": {
                "description": "Numeric computed value to represent lifetime tobacco exposure defined as number of cigarettes smoked per day x number of years smoked divided by 20.",
                "termDef": {
                    "term": "Person Cigarette Smoking History Pack Year Value",
                    "source": "caDSR",
                    "cde_id": 2955385,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2955385%20and%20ver_nr=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "parent_with_radiation_exposure": {
                "description": "Indicates whether the patient's parent(s) were exposed to radiation",
                "termDef": {
                    "term": None,
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
            "radon_exposure": {
                "description": "The yes/no/unknown indicator used to describe whether the patient was exposed to radon.",
                "termDef": {
                    "term": "Person Lifetime Risk Radon Exposure Indicator",
                    "source": "caDSR",
                    "cde_id": 2816352,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2816352%20and%20ver_nr=1.0",
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
            "respirable_crystalline_silica_exposure": {
                "description": "The yes/no/unknown indicator used to describe whether a patient was exposed to respirable crystalline silica, a widespread, naturally occurring, crystalline metal oxide that consists of different forms including quartz, cristobalite, tridymite, tripoli, ganister, chert, and novaculite.",
                "termDef": {
                    "term": "Person Respirable Cystalline Silica Exposure Indicator",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
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
            "secondhand_smoke_as_child": {
                "description": "The text term used to indicate whether the patient was exposed to secondhand smoke as a child.",
                "termDef": {
                    "term": "Smoking History Secondhand Smoke Exposure Indicator",
                    "source": "caDSR",
                    "cde_id": 6841888,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6841888%20and%20ver_nr=1.0",
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
            "smoking_frequency": {
                "description": "The text term used to generally describe how often the patient smokes.",
                "termDef": {
                    "term": "Person Smoking Frequency",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Every day", "Some days", "Unknown"],
                "enumDef": {
                    "Every day": {
                        "description": "Occurring or done each day.",
                        "termDef": {
                            "term": "Daily",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C25473",
                            "term_id": "C25473",
                            "term_version": "19.12e",
                        },
                    },
                    "Some days": {
                        "description": "A response indicating that an individual experiences or experienced something on some days.",
                        "termDef": {
                            "term": "Some Days",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C131735",
                            "term_id": "C131735",
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
            "time_between_waking_and_first_smoke": {
                "description": "The text term used to describe the approximate amount of time elapsed between the time the patient wakes up in the morning to the time they smoke their first cigarette.",
                "termDef": {
                    "term": "Person Smoking Frequency",
                    "source": "caDSR",
                    "cde_id": 3279220,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3279220%20and%20ver_nr=1.0",
                },
                "enum": [
                    "Within 5 Minutes",
                    "6-30 Minutes",
                    "31-60 Minutes",
                    "After 60 Minutes",
                    "Unknown",
                ],
                "enumDef": {
                    "Within 5 Minutes": {
                        "description": "An indication that less than 5 minutes passes between waking and smoking the first cigarette of the day.",
                        "termDef": {
                            "term": "Time Between Waking and First Smoke - Within 5 Minutes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164121",
                            "term_id": "C164121",
                            "term_version": "19.12e",
                        },
                    },
                    "6-30 Minutes": {
                        "description": "An indication that between 6 and 30 minutes passes between waking and smoking the first cigarette of the day.",
                        "termDef": {
                            "term": "Time Between Waking and First Smoke - Between 6 and 30 Minutes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164124",
                            "term_id": "C164124",
                            "term_version": "19.12e",
                        },
                    },
                    "31-60 Minutes": {
                        "description": "An indication that between 31 and 60 minutes passes between waking and smoking the first cigarette of the day.",
                        "termDef": {
                            "term": "Time Between Waking and First Smoke - Between 31 and 60 Minutes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164126",
                            "term_id": "C164126",
                            "term_version": "19.12e",
                        },
                    },
                    "After 60 Minutes": {
                        "description": "An indication that more than 60 minutes passes between waking and smoking the first cigarette of the day.",
                        "termDef": {
                            "term": "Time Between Waking and First Smoke - After 60 Minutes",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164127",
                            "term_id": "C164127",
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
            "tobacco_smoking_onset_year": {
                "description": "The year in which the participant began smoking.",
                "termDef": {
                    "term": "Started Smoking Year",
                    "source": "caDSR",
                    "cde_id": 2228604,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2228604%20and%20ver_nr=1.0",
                },
                "type": "integer",
                "maximum": 2050,
                "minimum": 1900,
            },
            "tobacco_smoking_quit_year": {
                "description": "The year in which the participant quit smoking.",
                "termDef": {
                    "term": "Stopped Smoking Year",
                    "source": "caDSR",
                    "cde_id": 2228610,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2228610%20and%20ver_nr=1.0",
                },
                "type": "integer",
                "maximum": 2050,
                "minimum": 1900,
            },
            "tobacco_smoking_status": {
                "description": "Category describing current smoking status and smoking history as self-reported by a patient.",
                "termDef": {
                    "term": "Patient Smoking History Category",
                    "source": "caDSR",
                    "cde_id": 2181650,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2181650%20and%20ver_nr=1.0",
                },
                "enum": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "Current Reformed Smoker, Duration Not Specified",
                    "Current Reformed Smoker for < or = 15 yrs",
                    "Current Reformed Smoker for > 15 yrs",
                    "Current Smoker",
                    "Lifelong Non-Smoker",
                    "Smoker at Diagnosis",
                    "Smoking history not documented",
                    "Unknown",
                    "Not Reported",
                    "Not Allowed To Collect",
                ],
                "deprecated_enum": [
                    "Not Allowed To Collect",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
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
                    "1": {
                        "description": "A person who has never smoked at the time of the interview or has smoked less than 100 cigarettes in their life.",
                        "termDef": {
                            "term": "Never Smoker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C65108",
                            "term_id": "C65108",
                            "term_version": "19.12e",
                        },
                    },
                    "2": {
                        "description": "An adult who has smoked 100 cigarettes in his or her lifetime and who currently smokes cigarettes. Includes daily smokers and non-daily smokers (also known as occasional smokers).",
                        "termDef": {
                            "term": "Current Smoker",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C67147",
                            "term_id": "C67147",
                            "term_version": "19.12e",
                        },
                    },
                    "3": {
                        "description": "An individual who stopped smoking more than 15 years prior.",
                        "termDef": {
                            "term": "Current Reformed Smoker, More than 15 Years",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156828",
                            "term_id": "C156828",
                            "term_version": "19.12e",
                        },
                    },
                    "4": {
                        "description": "An individual who stopped smoking within the past 15 years.",
                        "termDef": {
                            "term": "Current Reformed Smoker Within Past 15 Years",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156829",
                            "term_id": "C156829",
                            "term_version": "19.12e",
                        },
                    },
                    "5": {
                        "description": "An individual who stopped smoking an unknown number of years prior.",
                        "termDef": {
                            "term": "Current Reformed Smoker, Years Unknown",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156830",
                            "term_id": "C156830",
                            "term_version": "19.12e",
                        },
                    },
                    "6": {
                        "description": "An indication that a person was a smoker at the time they received a pathologic diagnosis.",
                        "termDef": {
                            "term": "Smoking at Diagnosis",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164079",
                            "term_id": "C164079",
                            "term_version": "19.12e",
                        },
                    },
                    "7": {
                        "description": "An indication that the smoking history of an individual is unavailable.",
                        "termDef": {
                            "term": "Smoking History Not Available",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C156831",
                            "term_id": "C156831",
                            "term_version": "19.12e",
                        },
                    },
                },
            },
            "type_of_smoke_exposure": {
                "description": "The text term used to describe the patient's specific type of smoke exposure.",
                "termDef": {
                    "term": "Person Smoke Exposure Type",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Accidental building fire smoke",
                    "Accidental fire smoke, grass",
                    "Accidental fire smoke, NOS",
                    "Accidental forest fire smoke",
                    "Accidental vehicle fire smoke",
                    "Aircraft smoke",
                    "Burning tree smoke",
                    "Coal smoke, NOS",
                    "Cooking-related smoke, NOS",
                    "Electrical fire smoke",
                    "Electronic cigarette smoke, NOS",
                    "Environmental tobacco smoke",
                    "Factory smokestack smoke",
                    "Field burning smoke",
                    "Fire smoke, NOS",
                    "Furnace or boiler smoke",
                    "Gas burning smoke, propane",
                    "Grease fire smoke",
                    "Grilling smoke",
                    "Hashish smoke",
                    "Indoor stove or fireplace smoke, coal burning",
                    "Indoor stove or fireplace smoke, NOS",
                    "Indoor stove or fireplace smoke, wood burning",
                    "Machine smoke",
                    "Marijuana smoke",
                    "No Smoke Exposure",
                    "Oil burning smoke, Kerosene",
                    "Oil burning smoke, NOS",
                    "Recreational fire smoke",
                    "Smoke exposure, NOS",
                    "Smokehouse smoke",
                    "Tobacco smoke, cigar",
                    "Tobacco smoke, cigarettes",
                    "Tobacco smoke, NOS",
                    "Tobacco smoke, pipe",
                    "Volcanic smoke",
                    "Waste burning smoke",
                    "Wood burning smoke, factory",
                    "Wood burning smoke, NOS",
                    "Work-related smoke, artificial smoke machines",
                    "Work-related smoke, fire fighting",
                    "Work-related smoke, foundry",
                    "Work-related smoke, generators",
                    "Work-related smoke, military",
                    "Work-related smoke, NOS",
                    "Work-related smoke, paint baking",
                    "Work-related smoke, plastics factory",
                    "Work-related smoke, plumbing",
                    "Work-related smoke, soldering/welding",
                    "Unknown",
                ],
                "enumDef": {
                    "Accidental building fire smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced during a building fire that was not caused by deliberate human actions.",
                        "termDef": {
                            "term": "Accidental Building Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164066",
                            "term_id": "C164066",
                            "term_version": "19.12e",
                        },
                    },
                    "Accidental fire smoke, grass": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced during a grass fire that was not caused by deliberate human actions.",
                        "termDef": {
                            "term": "Accidental Grass Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164067",
                            "term_id": "C164067",
                            "term_version": "19.12e",
                        },
                    },
                    "Accidental fire smoke, NOS": {
                        "description": "Environmental exposure to airborne gases and particulates produced during a fire that was not caused by deliberate human actions.",
                        "termDef": {
                            "term": "Accidental Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164059",
                            "term_id": "C164059",
                            "term_version": "19.12e",
                        },
                    },
                    "Accidental forest fire smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced during a forest fire that was not caused by deliberate human actions.",
                        "termDef": {
                            "term": "Accidental Forest Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164068",
                            "term_id": "C164068",
                            "term_version": "19.12e",
                        },
                    },
                    "Accidental vehicle fire smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced during a vehicle fire that was not caused by deliberate human actions.",
                        "termDef": {
                            "term": "Accidental Vehicle Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164069",
                            "term_id": "C164069",
                            "term_version": "19.12e",
                        },
                    },
                    "Aircraft smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced when an aircraft is in operation.",
                        "termDef": {
                            "term": "Aircraft Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164072",
                            "term_id": "C164072",
                            "term_version": "19.12e",
                        },
                    },
                    "Burning tree smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when trees are undergoing combustion.",
                        "termDef": {
                            "term": "Burning Tree Smoke",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164075",
                            "term_id": "C164075",
                            "term_version": "19.12e",
                        },
                    },
                    "Coal smoke, NOS": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when coal is rapidly oxidized via combustion.",
                        "termDef": {
                            "term": "Coal Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164060",
                            "term_id": "C164060",
                            "term_version": "19.12e",
                        },
                    },
                    "Cooking-related smoke, NOS": {
                        "description": "Environmental, occupational or consumer-based exposure to vaporized materials produced when food products are being cooked.",
                        "termDef": {
                            "term": "Cooking-Related Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164061",
                            "term_id": "C164061",
                            "term_version": "19.12e",
                        },
                    },
                    "Electrical fire smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced during an electrical fire.",
                        "termDef": {
                            "term": "Electrical Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164077",
                            "term_id": "C164077",
                            "term_version": "19.12e",
                        },
                    },
                    "Electronic cigarette smoke, NOS": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of an electronic cigarette.",
                        "termDef": {
                            "term": "Electronic Cigarette Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164062",
                            "term_id": "C164062",
                            "term_version": "19.12e",
                        },
                    },
                    "Environmental tobacco smoke": {
                        "description": "Exposure to tobacco smoke products among individuals who do not smoke. This can result from sharing space with a smoker or from placental transfer from mother to fetus.",
                        "termDef": {
                            "term": "Passive Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C17140",
                            "term_id": "C17140",
                            "term_version": "19.12e",
                        },
                    },
                    "Factory smokestack smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates emitted by a factory smokestack.",
                        "termDef": {
                            "term": "Factory Smokestack Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164081",
                            "term_id": "C164081",
                            "term_version": "19.12e",
                        },
                    },
                    "Field burning smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when trees, brush and grass in a field are burning.",
                        "termDef": {
                            "term": "Field Burning Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164082",
                            "term_id": "C164082",
                            "term_version": "19.12e",
                        },
                    },
                    "Fire smoke, NOS": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when materials are rapidly oxidized via combustion.",
                        "termDef": {
                            "term": "Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164058",
                            "term_id": "C164058",
                            "term_version": "19.12e",
                        },
                    },
                    "Furnace or boiler smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates emitted by a boiler or furnace.",
                        "termDef": {
                            "term": "Furnace or Boiler Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164083",
                            "term_id": "C164083",
                            "term_version": "19.12e",
                        },
                    },
                    "Gas burning smoke, propane": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced when propane is rapidly oxidized via combustion.",
                        "termDef": {
                            "term": "Propane Smoke Exposue",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164084",
                            "term_id": "C164084",
                            "term_version": "19.12e",
                        },
                    },
                    "Grease fire smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced during a grease fire.",
                        "termDef": {
                            "term": "Grease Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164085",
                            "term_id": "C164085",
                            "term_version": "19.12e",
                        },
                    },
                    "Grilling smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates emitted by an indoor or outdoor grill used for cooking.",
                        "termDef": {
                            "term": "Grilling Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164086",
                            "term_id": "C164086",
                            "term_version": "19.12e",
                        },
                    },
                    "Hashish smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of a vaporized or combusted product made from cannabis plant resin.",
                        "termDef": {
                            "term": "Hashish Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164087",
                            "term_id": "C164087",
                            "term_version": "19.12e",
                        },
                    },
                    "Indoor stove or fireplace smoke, coal burning": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when coal is subjected to combustion in an indoor stove or fireplace.",
                        "termDef": {
                            "term": "Coal-Burining Indoor Stove or Fireplace Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164088",
                            "term_id": "C164088",
                            "term_version": "19.12e",
                        },
                    },
                    "Indoor stove or fireplace smoke, NOS": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when materials are subjected to combustion in an indoor stove or fireplace.",
                        "termDef": {
                            "term": "Indoor Stove or Fireplace Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164064",
                            "term_id": "C164064",
                            "term_version": "19.12e",
                        },
                    },
                    "Indoor stove or fireplace smoke, wood burning": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when wood is subjected to combustion in an indoor stove or fireplace.",
                        "termDef": {
                            "term": "Wood-Burning Indoor Stove or Fireplace Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164089",
                            "term_id": "C164089",
                            "term_version": "19.12e",
                        },
                    },
                    "Machine smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates through the direct or nearby use of a machine.",
                        "termDef": {
                            "term": "Machine Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164090",
                            "term_id": "C164090",
                            "term_version": "19.12e",
                        },
                    },
                    "Marijuana smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of a vaporized or combusted product made from the leaves and flowers of the cannabis plant.",
                        "termDef": {
                            "term": "Marijuana Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164091",
                            "term_id": "C164091",
                            "term_version": "19.12e",
                        },
                    },
                    "No Smoke Exposure": {
                        "description": "An indication that a subject has no history of smoke exposure from any source.",
                        "termDef": {
                            "term": "No Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164092",
                            "term_id": "C164092",
                            "term_version": "19.12e",
                        },
                    },
                    "Oil burning smoke, Kerosene": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced when kerosene is rapidly oxidized via combustion.",
                        "termDef": {
                            "term": "Kerosene Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164093",
                            "term_id": "C164093",
                            "term_version": "19.12e",
                        },
                    },
                    "Oil burning smoke, NOS": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when oils are rapidly oxidized via combustion.",
                        "termDef": {
                            "term": "Burning Oil Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164063",
                            "term_id": "C164063",
                            "term_version": "19.12e",
                        },
                    },
                    "Recreational fire smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced when materials (usually wood) are burned for recreational purposes.",
                        "termDef": {
                            "term": "Recreational Fire Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164094",
                            "term_id": "C164094",
                            "term_version": "19.12e",
                        },
                    },
                    "Smoke exposure, NOS": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced when materials undergo combustion or thermal decomposition.",
                        "termDef": {
                            "term": "Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164057",
                            "term_id": "C164057",
                            "term_version": "19.12e",
                        },
                    },
                    "Smokehouse smoke": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced during indoor smoke curing of food products.",
                        "termDef": {
                            "term": "Smokehouse Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164095",
                            "term_id": "C164095",
                            "term_version": "19.12e",
                        },
                    },
                    "Tobacco smoke, cigar": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of a cigar.",
                        "termDef": {
                            "term": "Cigar Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164097",
                            "term_id": "C164097",
                            "term_version": "19.12e",
                        },
                    },
                    "Tobacco smoke, cigarettes": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of a cigarette.",
                        "termDef": {
                            "term": "Cigarette Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164098",
                            "term_id": "C164098",
                            "term_version": "19.12e",
                        },
                    },
                    "Tobacco smoke, pipe": {
                        "description": "Environmental, occupational or consumer-based exposure to airborne gases and particulates produced by direct or nearby use of a tobacco pipe.",
                        "termDef": {
                            "term": "Tobacco Pipe Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164099",
                            "term_id": "C164099",
                            "term_version": "19.12e",
                        },
                    },
                    "Volcanic smoke": {
                        "description": "Environmental exposure to airborne gases and particulates produced by a volcanic event.",
                        "termDef": {
                            "term": "Volcanic Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164100",
                            "term_id": "C164100",
                            "term_version": "19.12e",
                        },
                    },
                    "Waste burning smoke": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when trash or waste is burned.",
                        "termDef": {
                            "term": "Burning Waste Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164101",
                            "term_id": "C164101",
                            "term_version": "19.12e",
                        },
                    },
                    "Wood burning smoke, factory": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when wood is burned in a factory setting.",
                        "termDef": {
                            "term": "Wood-Burning Factory Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164102",
                            "term_id": "C164102",
                            "term_version": "19.12e",
                        },
                    },
                    "Wood burning smoke, NOS": {
                        "description": "Environmental or occupational exposure to airborne gases and particulates produced when wood is subjected to combustion.",
                        "termDef": {
                            "term": "Burning Wood Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164065",
                            "term_id": "C164065",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, artificial smoke machines": {
                        "description": "Occupational exposure to airborne gases and particulates during the operation of a machine that produces artificial smoke.",
                        "termDef": {
                            "term": "Occupational Artificial Smoke Machine Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164104",
                            "term_id": "C164104",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, fire fighting": {
                        "description": "Occupational exposure to airborne gases and particulates while preventing, controlling or extinguishing fires.",
                        "termDef": {
                            "term": "Occupational Fire Fighting Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164105",
                            "term_id": "C164105",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, foundry": {
                        "description": "Occupational exposure to airborne gases and particulates during the operation of a foundry.",
                        "termDef": {
                            "term": "Occupational Foundry Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164106",
                            "term_id": "C164106",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, generators": {
                        "description": "Occupational exposure to airborne gases and particulates during the operation of a power generator.",
                        "termDef": {
                            "term": "Occupational Generator Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164107",
                            "term_id": "C164107",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, military": {
                        "description": "Occupational exposure to airborne gases and particulates during a military posting or deployment.",
                        "termDef": {
                            "term": "Occupational Military Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164115",
                            "term_id": "C164115",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, NOS": {
                        "description": "Occupational exposure to airborne gases and particulates produced when materials undergo combustion or thermal decomposition.",
                        "termDef": {
                            "term": "Work-Related Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164103",
                            "term_id": "C164103",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, paint baking": {
                        "description": "Occupational exposure to airborne gases and particulates during the operation of a paint oven.",
                        "termDef": {
                            "term": "Occupational Paint Baking Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164116",
                            "term_id": "C164116",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, plastics factory": {
                        "description": "Occupational exposure to airborne gases and particulates during the manufacturing of plastics.",
                        "termDef": {
                            "term": "Occupational Plastics Factory Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164118",
                            "term_id": "C164118",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, plumbing": {
                        "description": "Occupational exposure to airborne gases and particulates during the installation of plumbing pipes and fixtures.",
                        "termDef": {
                            "term": "Occupational Plumbing Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164119",
                            "term_id": "C164119",
                            "term_version": "19.12e",
                        },
                    },
                    "Work-related smoke, soldering/welding": {
                        "description": "Occupational exposure to airborne gases and particulates during the operation of a soldering iron or welding machine.",
                        "termDef": {
                            "term": "Occupational Soldering/Welding Smoke Exposure",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C164120",
                            "term_id": "C164120",
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
            "type_of_tobacco_used": {
                "description": "The text term used to describe the specific type of tobacco used by the patient.",
                "termDef": {
                    "term": "Person Tobacco Use Type",
                    "source": "caDSR",
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Cigar",
                    "Cigarette",
                    "Electronic Cigarette",
                    "Other",
                    "Pipe",
                    "Smokeless Tobacco",
                ],
                "enumDef": {
                    "Cigar": {
                        "description": "A compact roll of tobacco leaves prepared for smoking.",
                        "termDef": {
                            "term": "Cigar",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C1813",
                            "term_id": "C1813",
                            "term_version": "19.12e",
                        },
                    },
                    "Cigarette": {
                        "description": "Finely cut tobacco encased in a wrapper of thin paper and rolled for smoking.",
                        "termDef": {
                            "term": "Cigarette",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C1802",
                            "term_id": "C1802",
                            "term_version": "19.12e",
                        },
                    },
                    "Electronic Cigarette": {
                        "description": "A battery-powered electronic device designed to atomize a nicotine-containing liquid solution for inhalation in a manner that simulates smoking a tobacco cigarette.",
                        "termDef": {
                            "term": "Electronic Cigarette",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C120482",
                            "term_id": "C120482",
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
                    "Pipe": {
                        "description": "A tube with a small bowl at one end, especially one used for smoking tobacco.",
                        "termDef": {
                            "term": "Pipe",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C86044",
                            "term_id": "C86044",
                            "term_version": "19.12e",
                        },
                    },
                    "Smokeless Tobacco": {
                        "description": "Tobacco that is not smoked but used in another form such as chewing tobacco or snuff.",
                        "termDef": {
                            "term": "Smokeless Tobacco",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C892",
                            "term_id": "C892",
                            "term_version": "19.12e",
                        },
                    },
                },
            },
            "use_per_day": {
                "description": "The average number of times the patient used per day.",
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
            "years_smoked": {
                "description": "Numeric value (or unknown) to represent the number of years a person has been smoking.",
                "termDef": {
                    "term": "Person Smoking Duration Year Count",
                    "source": "caDSR",
                    "cde_id": 3137957,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3137957%20and%20ver_nr=1.0",
                },
                "type": "number",
                "maximum": 89,
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
        return "exposure"

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
                "name": "exposures",
                "src_type": base.Node.get_subclass("annotation"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "exposures",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "exposures",
                "type": base.Node.get_subclass("case"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "cases": {
                "edge_out": "_ExposureDescribesCase_out",
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

    @psqlgraph.pg_property(int)
    def age_at_last_exposure(self, value):
        self._set_property("age_at_last_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def age_at_onset(self, value):
        self._set_property("age_at_onset", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def alcohol_days_per_week(self, value):
        self._set_property("alcohol_days_per_week", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def alcohol_drinks_per_day(self, value):
        self._set_property("alcohol_drinks_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Daily Drinker", "Weekly Drinker"])
    def alcohol_frequency(self, value):
        self._set_property("alcohol_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes", "no", "yes"])
    def alcohol_history(self, value):
        self._set_property("alcohol_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Drinker",
            "Heavy Drinker",
            "Lifelong Non-Drinker",
            "Non-Drinker",
            "Not Reported",
            "Occasional Drinker",
            "Social Drinker",
            "Unknown",
        ],
    )
    def alcohol_intensity(self, value):
        self._set_property("alcohol_intensity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum=["Beer", "Liquor", "Not Reported", "Other", "Unknown", "Wine"]
    )
    def alcohol_type(self, value):
        self._set_property("alcohol_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def asbestos_exposure(self, value):
        self._set_property("asbestos_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Amosite", "Crocidolite"])
    def asbestos_exposure_type(self, value):
        self._set_property("asbestos_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def chemical_exposure_type(self, value):
        self._set_property("chemical_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def cigarettes_per_day(self, value):
        self._set_property("cigarettes_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Unknown", "Yes"])
    def coal_dust_exposure(self, value):
        self._set_property("coal_dust_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Unknown", "Yes"])
    def environmental_tobacco_smoke_exposure(self, value):
        self._set_property("environmental_tobacco_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Not Reported", "Six Weeks or More", "Unknown"])
    def exposure_duration(self, value):
        self._set_property("exposure_duration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def exposure_duration_hrs_per_day(self, value):
        self._set_property("exposure_duration_hrs_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def exposure_duration_years(self, value):
        self._set_property("exposure_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Occupational", "Secondary", "Unknown"])
    def exposure_source(self, value):
        self._set_property("exposure_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Asbestos",
            "Chemical",
            "Coal Dust",
            "Dust, NOS",
            "Marijuana",
            "Radiation",
            "Radon",
            "Respirable Crystalline Silica",
            "Smoke",
            "Smokeless Tobacco",
            "Tobacco",
            "Wood Dust",
        ],
    )
    def exposure_type(self, value):
        self._set_property("exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def occupation_duration_years(self, value):
        self._set_property("occupation_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def occupation_type(self, value):
        self._set_property("occupation_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def pack_years_smoked(self, value):
        self._set_property("pack_years_smoked", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Yes"])
    def parent_with_radiation_exposure(self, value):
        self._set_property("parent_with_radiation_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def radon_exposure(self, value):
        self._set_property("radon_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Unknown", "Yes"])
    def respirable_crystalline_silica_exposure(self, value):
        self._set_property("respirable_crystalline_silica_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["No", "Not Reported", "Unknown", "Yes"])
    def secondhand_smoke_as_child(self, value):
        self._set_property("secondhand_smoke_as_child", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Every day", "Some days", "Unknown"])
    def smoking_frequency(self, value):
        self._set_property("smoking_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "31-60 Minutes",
            "6-30 Minutes",
            "After 60 Minutes",
            "Unknown",
            "Within 5 Minutes",
        ],
    )
    def time_between_waking_and_first_smoke(self, value):
        self._set_property("time_between_waking_and_first_smoke", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def tobacco_smoking_onset_year(self, value):
        self._set_property("tobacco_smoking_onset_year", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def tobacco_smoking_quit_year(self, value):
        self._set_property("tobacco_smoking_quit_year", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "Current Reformed Smoker for < or = 15 yrs",
            "Current Reformed Smoker for > 15 yrs",
            "Current Reformed Smoker, Duration Not Specified",
            "Current Smoker",
            "Lifelong Non-Smoker",
            "Not Allowed To Collect",
            "Not Reported",
            "Smoker at Diagnosis",
            "Smoking history not documented",
            "Unknown",
        ],
    )
    def tobacco_smoking_status(self, value):
        self._set_property("tobacco_smoking_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Accidental building fire smoke",
            "Accidental fire smoke, NOS",
            "Accidental fire smoke, grass",
            "Accidental forest fire smoke",
            "Accidental vehicle fire smoke",
            "Aircraft smoke",
            "Burning tree smoke",
            "Coal smoke, NOS",
            "Cooking-related smoke, NOS",
            "Electrical fire smoke",
            "Electronic cigarette smoke, NOS",
            "Environmental tobacco smoke",
            "Factory smokestack smoke",
            "Field burning smoke",
            "Fire smoke, NOS",
            "Furnace or boiler smoke",
            "Gas burning smoke, propane",
            "Grease fire smoke",
            "Grilling smoke",
            "Hashish smoke",
            "Indoor stove or fireplace smoke, NOS",
            "Indoor stove or fireplace smoke, coal burning",
            "Indoor stove or fireplace smoke, wood burning",
            "Machine smoke",
            "Marijuana smoke",
            "No Smoke Exposure",
            "Oil burning smoke, Kerosene",
            "Oil burning smoke, NOS",
            "Recreational fire smoke",
            "Smoke exposure, NOS",
            "Smokehouse smoke",
            "Tobacco smoke, NOS",
            "Tobacco smoke, cigar",
            "Tobacco smoke, cigarettes",
            "Tobacco smoke, pipe",
            "Unknown",
            "Volcanic smoke",
            "Waste burning smoke",
            "Wood burning smoke, NOS",
            "Wood burning smoke, factory",
            "Work-related smoke, NOS",
            "Work-related smoke, artificial smoke machines",
            "Work-related smoke, fire fighting",
            "Work-related smoke, foundry",
            "Work-related smoke, generators",
            "Work-related smoke, military",
            "Work-related smoke, paint baking",
            "Work-related smoke, plastics factory",
            "Work-related smoke, plumbing",
            "Work-related smoke, soldering/welding",
        ],
    )
    def type_of_smoke_exposure(self, value):
        self._set_property("type_of_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Cigar",
            "Cigarette",
            "Electronic Cigarette",
            "Other",
            "Pipe",
            "Smokeless Tobacco",
        ],
    )
    def type_of_tobacco_used(self, value):
        self._set_property("type_of_tobacco_used", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def use_per_day(self, value):
        self._set_property("use_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def years_smoked(self, value):
        self._set_property("years_smoked", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Exposure)
datetime_hooks.cls_inject_updated_datetime_hook(Exposure)
