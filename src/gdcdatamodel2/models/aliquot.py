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


class Aliquot(base.Node):
    __tablename__: str = "node_aliquot"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {
        "state": "validated",
        "no_matched_normal_low_pass_wgs": False,
        "no_matched_normal_targeted_sequencing": False,
        "no_matched_normal_wgs": False,
        "no_matched_normal_wxs": False,
        "selected_normal_wxs": False,
        "selected_normal_wgs": False,
        "selected_normal_targeted_sequencing": False,
        "selected_normal_low_pass_wgs": False,
    }
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Aliquot",
        "namespace": "https://gdc.cancer.gov",
        "category": "biospecimen",
        "submittable": True,
        "downloadable": False,
        "description": "Pertaining to a portion of the whole; any one of two or more samples of something, of the same volume or weight.",
        "required": ["submitter_id"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "exclusive": True,
                "required": True,
                "subgroup": [
                    {
                        "name": "analytes",
                        "backref": "aliquots",
                        "label": "derived_from",
                        "target_type": "analyte",
                        "multiplicity": "many_to_one",
                        "required": False,
                    },
                    {
                        "name": "samples",
                        "backref": "aliquots",
                        "label": "derived_from",
                        "target_type": "sample",
                        "multiplicity": "many_to_many",
                        "required": False,
                    },
                ],
            },
            {
                "name": "centers",
                "backref": "aliquots",
                "label": "shipped_to",
                "target_type": "center",
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
            "aliquot_quantity": {
                "description": "The quantity in micrograms (ug) of the aliquot(s) derived from the analyte(s) shipped for sequencing and characterization.",
                "termDef": {
                    "term": "Biospecimen Aliquot Quantity",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "aliquot_volume": {
                "description": "The volume in microliters (ul) of the aliquot(s) derived from the analyte(s) shipped for sequencing and characterization.",
                "termDef": {
                    "term": "Biospecimen Aliquot Volume",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
                "minimum": 0,
            },
            "amount": {
                "description": "Weight in grams or volume in mL.",
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
            "analyte_type": {
                "description": "Text term that represents the kind of molecular specimen analyte.",
                "termDef": {
                    "term": "Molecular Specimen Type Text Name",
                    "source": "caDSR",
                    "cde_id": 2513915,
                    "cde_version": 2.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2513915%20and%20ver_nr=2.0",
                },
                "enum": [
                    "cfDNA",
                    "DNA",
                    "EBV Immortalized Normal",
                    "FFPE DNA",
                    "FFPE RNA",
                    "GenomePlex (Rubicon) Amplified DNA",
                    "m6A Enriched RNA",
                    "Nuclei RNA",
                    "Repli-G (Qiagen) DNA",
                    "Repli-G Pooled (Qiagen) DNA",
                    "Repli-G X (Qiagen) DNA",
                    "RNA",
                    "Total RNA",
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
                },
            },
            "analyte_type_id": {
                "description": "A single letter code used to identify a type of molecular analyte.",
                "termDef": {
                    "term": "Molecular Analyte Identification Code",
                    "source": "caDSR",
                    "cde_id": 5432508,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432508%20and%20ver_nr=1.0",
                },
                "enum": ["D", "E", "G", "H", "R", "S", "T", "W", "X", "Y"],
            },
            "concentration": {
                "description": "Numeric value that represents the concentration of an analyte or aliquot extracted from the sample or sample portion, measured in milligrams per milliliter.",
                "termDef": {
                    "term": "Biospecimen Analyte or Aliquot Extracted Concentration Milligram per Milliliter Value",
                    "source": "caDSR",
                    "cde_id": 5432594,
                    "cde_version": 1.0,
                    "term_url": "https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432594%20and%20ver_nr=1.0",
                },
                "type": "number",
                "minimum": 0,
            },
            "no_matched_normal_low_pass_wgs": {
                "description": "There will be no matched normal low pass WGS aliquots for this case that can be used for variant calling purposes. The GDC may elect to use a single tumor calling pipeline to process this data.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "no_matched_normal_targeted_sequencing": {
                "description": "There will be no matched normal Targeted Sequencing aliquots for this case that can be used for variant calling purposes. The GDC may elect to use a single tumor calling pipeline to process this data.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "no_matched_normal_wgs": {
                "description": "There will be no matched normal WGS aliquots for this case that can be used for variant calling purposes. The GDC may elect to use a single tumor calling pipeline to process this data.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "no_matched_normal_wxs": {
                "description": "There will be no matched normal WXS aliquots for this case that can be used for variant calling purposes. The GDC may elect to use a single tumor calling pipeline to process this data.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "source_center": {
                "description": "Name of the center that provided the item.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "string",
            },
            "selected_normal_wxs": {
                "description": "Denotes which WXS normal aliquot the submitter prefers to use for variant calling. Only one normal per experimental strategy per case can be selected.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "selected_normal_wgs": {
                "description": "Denotes which WGS normal aliquot the submitter prefers to use for variant calling. Only one normal per experimental strategy per case can be selected.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "selected_normal_targeted_sequencing": {
                "description": "Denotes which targeted_sequencing normal aliquot the submitter prefers to use for variant calling. Only one normal per experimental strategy per case can be selected.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "selected_normal_low_pass_wgs": {
                "description": "Denotes which low-pass WGS normal aliquot the submitter prefers to use for variant calling. Only one normal per experimental strategy per case can be selected.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "boolean",
                "default": False,
            },
            "analytes": {
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
            "centers": {
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
        return "aliquot"

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
                "name": "aliquots",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "files": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("file"),
            },
            "raw_methylation_arrays": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("raw_methylation_array"),
            },
            "read_groups": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("read_group"),
            },
            "submitted_genotyping_arrays": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_genotyping_array"),
            },
            "submitted_methylation_beta_values": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_methylation_beta_value"),
            },
            "submitted_tangent_copy_number": {
                "name": "aliquots",
                "src_type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "analytes": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("analyte"),
            },
            "annotations": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("annotation"),
            },
            "centers": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("center"),
            },
            "files": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("file"),
            },
            "raw_methylation_arrays": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("raw_methylation_array"),
            },
            "read_groups": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("read_group"),
            },
            "samples": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("sample"),
            },
            "submitted_genotyping_arrays": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_genotyping_array"),
            },
            "submitted_methylation_beta_values": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_methylation_beta_value"),
            },
            "submitted_tangent_copy_number": {
                "backref": "aliquots",
                "type": base.Node.get_subclass("submitted_tangent_copy_number"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "analytes": {
                "edge_out": "_AliquotDerivedFromAnalyte_out",
                "dst_type": base.Node.get_subclass("analyte"),
            },
            "centers": {
                "edge_out": "_AliquotShippedToCenter_out",
                "dst_type": base.Node.get_subclass("center"),
            },
            "samples": {
                "edge_out": "_AliquotDerivedFromSample_out",
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

    @psqlgraph.pg_property(float, int)
    def aliquot_quantity(self, value):
        self._set_property("aliquot_quantity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def aliquot_volume(self, value):
        self._set_property("aliquot_volume", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def amount(self, value):
        self._set_property("amount", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "DNA",
            "EBV Immortalized Normal",
            "FFPE DNA",
            "FFPE RNA",
            "GenomePlex (Rubicon) Amplified DNA",
            "Nuclei RNA",
            "RNA",
            "Repli-G (Qiagen) DNA",
            "Repli-G Pooled (Qiagen) DNA",
            "Repli-G X (Qiagen) DNA",
            "Total RNA",
            "cfDNA",
            "m6A Enriched RNA",
        ],
    )
    def analyte_type(self, value):
        self._set_property("analyte_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["D", "E", "G", "H", "R", "S", "T", "W", "X", "Y"])
    def analyte_type_id(self, value):
        self._set_property("analyte_type_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def concentration(self, value):
        self._set_property("concentration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_low_pass_wgs(self, value):
        self._set_property("no_matched_normal_low_pass_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_targeted_sequencing(self, value):
        self._set_property("no_matched_normal_targeted_sequencing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_wgs(self, value):
        self._set_property("no_matched_normal_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def no_matched_normal_wxs(self, value):
        self._set_property("no_matched_normal_wxs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def source_center(self, value):
        self._set_property("source_center", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_wxs(self, value):
        self._set_property("selected_normal_wxs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_wgs(self, value):
        self._set_property("selected_normal_wgs", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_targeted_sequencing(self, value):
        self._set_property("selected_normal_targeted_sequencing", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def selected_normal_low_pass_wgs(self, value):
        self._set_property("selected_normal_low_pass_wgs", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Aliquot)
datetime_hooks.cls_inject_updated_datetime_hook(Aliquot)
