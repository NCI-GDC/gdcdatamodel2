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


class AlignedReads(base.Node):
    __tablename__: str = "node_alignedreads"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {
        "state": "validated",
        "file_state": "registered",
    }
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Aligned Reads",
        "namespace": "https://gdc.cancer.gov",
        "category": "data_file",
        "submittable": False,
        "downloadable": True,
        "description": "Data file containing aligned reads that are generated internally by the GDC.",
        "required": [
            "submitter_id",
            "file_name",
            "file_size",
            "md5sum",
            "data_category",
            "data_format",
            "data_type",
            "experimental_strategy",
            "platform",
        ],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
        "links": [
            {
                "exclusive": True,
                "required": True,
                "subgroup": [
                    {
                        "name": "alignment_cocleaning_workflows",
                        "backref": "aligned_reads_files",
                        "label": "data_from",
                        "target_type": "alignment_cocleaning_workflow",
                        "multiplicity": "many_to_one",
                        "required": False,
                    },
                    {
                        "name": "alignment_workflows",
                        "backref": "aligned_reads_files",
                        "label": "data_from",
                        "target_type": "alignment_workflow",
                        "multiplicity": "many_to_one",
                        "required": False,
                    },
                ],
            },
            {
                "exclusive": True,
                "required": False,
                "subgroup": [
                    {
                        "name": "submitted_unaligned_reads_files",
                        "backref": "aligned_reads_files",
                        "label": "matched_to",
                        "target_type": "submitted_unaligned_reads",
                        "multiplicity": "one_to_many",
                        "required": False,
                    },
                    {
                        "name": "submitted_aligned_reads_files",
                        "backref": "aligned_reads_files",
                        "label": "matched_to",
                        "target_type": "submitted_aligned_reads",
                        "multiplicity": "one_to_one",
                        "required": False,
                    },
                ],
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
            "file_name": {
                "common": {
                    "description": "The name (or part of a name) of a file (of any type).",
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
            "file_size": {
                "common": {
                    "description": "The size of the data file (object) in bytes.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "type": "integer",
            },
            "md5sum": {
                "common": {
                    "description": "The 128-bit hash value expressed as a 32 digit hexadecimal number (in lower case) used as a file's digital fingerprint.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "type": "string",
                "pattern": "^[a-f0-9]{32}$",
            },
            "file_state": {
                "common": {
                    "description": "The current state of the data file object.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "default": "registered",
                "enum": [
                    "registered",
                    "uploading",
                    "uploaded",
                    "validating",
                    "validated",
                    "submitted",
                    "processing",
                    "processed",
                    "released",
                    "error",
                    "deleted",
                ],
            },
            "error_type": {
                "common": {
                    "description": "Type of error for the data file object.",
                    "termDef": {
                        "term": None,
                        "source": None,
                        "cde_id": None,
                        "cde_version": None,
                        "term_url": None,
                    },
                },
                "enum": ["file_size", "file_format", "md5sum"],
            },
            "state_comment": {
                "description": "Optional comment about why the file is in the current state, mainly for invalid state.",
                "type": "string",
            },
            "average_base_quality": {
                "description": "Average base quality collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "average_insert_size": {
                "description": "Average insert size collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
            },
            "average_read_length": {
                "description": "Average read length collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
            },
            "contamination": {
                "description": "Fraction of reads coming from cross-sample contamination collected from GATK4.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "contamination_error": {
                "description": "Estimation error of cross-sample contamination collected from GATK4.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "data_category": {
                "description": "Broad categorization of the contents of the data file.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Sequencing Reads"],
            },
            "data_type": {
                "description": "Specific content type of the data file.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["Aligned Reads"],
            },
            "data_format": {
                "description": "Format of the data files.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": ["BAM"],
            },
            "experimental_strategy": {
                "description": "The sequencing strategy used to generate the data file.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "ATAC-Seq",
                    "Bisulfite-Seq",
                    "ChIP-Seq",
                    "HiChIP",
                    "m6A MeRIP-Seq",
                    "miRNA-Seq",
                    "RNA-Seq",
                    "scATAC-Seq",
                    "scRNA-Seq",
                    "Targeted Sequencing",
                    "Validation",
                    "WGS",
                    "WXS",
                ],
                "enumDef": {
                    "Targeted Sequencing": {
                        "description": "A technique that determines the nucleotide sequence of a pre-specified region of DNA or RNA by using primers that are specific for that region.",
                        "termDef": {
                            "term": "Next Generation Targeted Sequencing",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C130177",
                            "term_id": "C130177",
                            "term_version": "20.10d",
                        },
                    },
                    "WGS": {
                        "description": "A procedure that can determine the DNA sequence for nearly the entire genome of an individual.",
                        "termDef": {
                            "term": "Whole Genome Sequencing",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C101294",
                            "term_id": "C101294",
                            "term_version": "20.10d",
                        },
                    },
                    "WXS": {
                        "description": "A procedure that can determine the DNA sequence for all of the exons in an individual.",
                        "termDef": {
                            "term": "Whole Exome Sequencing",
                            "source": "NCIt",
                            "cde_id": None,
                            "cde_version": None,
                            "term_url": "https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C101295",
                            "term_id": "C101295",
                            "term_version": "20.10d",
                        },
                    },
                },
            },
            "mean_coverage": {
                "description": "Mean coverage for whole genome sequencing, or mean target coverage for whole exome and targeted sequencing, collected from Picard Tools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "msi_status": {
                "description": "MSIsensor determination of either microsatellite stability or instability.",
                "enum": ["MSI", "MSS"],
            },
            "msi_score": {
                "description": "Numeric score denoting the aligned reads file's MSI score from MSIsensor.",
                "type": "number",
            },
            "pairs_on_diff_chr": {
                "description": "Pairs on different chromosomes collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
            },
            "platform": {
                "description": "Name of the platform used to obtain data.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "enum": [
                    "Complete Genomics",
                    "Illumina",
                    "Ion Torrent",
                    "LS454",
                    "Other",
                    "PacBio",
                    "SOLiD",
                ],
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
                    }
                },
            },
            "proportion_base_mismatch": {
                "description": "Proportion of mismatched bases collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "proportion_coverage_10x": {
                "description": "Proportion of all reference bases for whole genome sequencing, or targeted bases for whole exome and targeted sequencing, that achieves 10X or greater coverage from Picard Tools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "proportion_coverage_30x": {
                "description": "Proportion of all reference bases for whole genome sequencing, or targeted bases for whole exome and targeted sequencing, that achieves 30X or greater coverage from Picard Tools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "proportion_reads_duplicated": {
                "description": "Proportion of duplicated reads collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "proportion_reads_mapped": {
                "description": "Proportion of mapped reads collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "proportion_targets_no_coverage": {
                "description": "Proportion of targets that did not reach 1X coverage over any base from Picard Tools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "tumor_ploidy": {
                "description": "Numeric value used to describe the number of sets of chromosomes in a cell or an organism. For example, haploid means one set and diploid means two sets.",
                "termDef": {
                    "term": "Tumor Ploidy Value",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "tumor_purity": {
                "description": "Numeric value used to describe the ratio of tumor cells compared to total cells present in a sample.",
                "termDef": {
                    "term": "Tumor Purity Ratio",
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "number",
            },
            "total_reads": {
                "description": "Total number of reads collected from samtools.",
                "termDef": {
                    "term": None,
                    "source": None,
                    "cde_id": None,
                    "cde_version": None,
                    "term_url": None,
                },
                "type": "integer",
            },
            "alignment_cocleaning_workflows": {
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
            "alignment_workflows": {
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
            "submitted_unaligned_reads_files": {
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
            "submitted_aligned_reads_files": {
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
        return "aligned_reads"

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
            "aligned_reads_indexes": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("aligned_reads_index"),
            },
            "annotations": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "germline_mutation_calling_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("germline_mutation_calling_workflow"),
            },
            "mirna_expression_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("mirna_expression_workflow"),
            },
            "rna_expression_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("rna_expression_workflow"),
            },
            "somatic_copy_number_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("somatic_copy_number_workflow"),
            },
            "somatic_mutation_calling_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("somatic_mutation_calling_workflow"),
            },
            "structural_variant_calling_workflows": {
                "name": "aligned_reads_files",
                "src_type": base.Node.get_subclass("structural_variant_calling_workflow"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "aligned_reads_indexes": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("aligned_reads_index"),
            },
            "alignment_cocleaning_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("alignment_cocleaning_workflow"),
            },
            "alignment_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("alignment_workflow"),
            },
            "annotations": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("annotation"),
            },
            "germline_mutation_calling_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("germline_mutation_calling_workflow"),
            },
            "mirna_expression_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("mirna_expression_workflow"),
            },
            "rna_expression_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("rna_expression_workflow"),
            },
            "somatic_copy_number_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("somatic_copy_number_workflow"),
            },
            "somatic_mutation_calling_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("somatic_mutation_calling_workflow"),
            },
            "structural_variant_calling_workflows": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("structural_variant_calling_workflow"),
            },
            "submitted_aligned_reads_files": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("submitted_aligned_reads"),
            },
            "submitted_unaligned_reads_files": {
                "backref": "aligned_reads_files",
                "type": base.Node.get_subclass("submitted_unaligned_reads"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "alignment_cocleaning_workflows": {
                "edge_out": "_AlignedReadsDataFromAlignmentCocleaningWorkflow_out",
                "dst_type": base.Node.get_subclass("alignment_cocleaning_workflow"),
            },
            "alignment_workflows": {
                "edge_out": "_AlignedReadsDataFromAlignmentWorkflow_out",
                "dst_type": base.Node.get_subclass("alignment_workflow"),
            },
            "submitted_aligned_reads_files": {
                "edge_out": "_AlignedReadsMatchedToSubmittedAlignedReads_out",
                "dst_type": base.Node.get_subclass("submitted_aligned_reads"),
            },
            "submitted_unaligned_reads_files": {
                "edge_out": "_AlignedReadsMatchedToSubmittedUnalignedReads_out",
                "dst_type": base.Node.get_subclass("submitted_unaligned_reads"),
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

    @psqlgraph.pg_property(str)
    def file_name(self, value):
        self._set_property("file_name", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def file_size(self, value):
        self._set_property("file_size", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def md5sum(self, value):
        self._set_property("md5sum", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "deleted",
            "error",
            "processed",
            "processing",
            "registered",
            "released",
            "submitted",
            "uploaded",
            "uploading",
            "validated",
            "validating",
        ],
    )
    def file_state(self, value):
        self._set_property("file_state", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["file_format", "file_size", "md5sum"])
    def error_type(self, value):
        self._set_property("error_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def state_comment(self, value):
        self._set_property("state_comment", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def average_base_quality(self, value):
        self._set_property("average_base_quality", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def average_insert_size(self, value):
        self._set_property("average_insert_size", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def average_read_length(self, value):
        self._set_property("average_read_length", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def contamination(self, value):
        self._set_property("contamination", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def contamination_error(self, value):
        self._set_property("contamination_error", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Sequencing Reads"])
    def data_category(self, value):
        self._set_property("data_category", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["BAM"])
    def data_format(self, value):
        self._set_property("data_format", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["Aligned Reads"])
    def data_type(self, value):
        self._set_property("data_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "ATAC-Seq",
            "Bisulfite-Seq",
            "ChIP-Seq",
            "HiChIP",
            "RNA-Seq",
            "Targeted Sequencing",
            "Validation",
            "WGS",
            "WXS",
            "m6A MeRIP-Seq",
            "miRNA-Seq",
            "scATAC-Seq",
            "scRNA-Seq",
        ],
    )
    def experimental_strategy(self, value):
        self._set_property("experimental_strategy", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def mean_coverage(self, value):
        self._set_property("mean_coverage", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def msi_score(self, value):
        self._set_property("msi_score", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum=["MSI", "MSS"])
    def msi_status(self, value):
        self._set_property("msi_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def pairs_on_diff_chr(self, value):
        self._set_property("pairs_on_diff_chr", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=[
            "Complete Genomics",
            "Illumina",
            "Ion Torrent",
            "LS454",
            "Other",
            "PacBio",
            "SOLiD",
        ],
    )
    def platform(self, value):
        self._set_property("platform", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_base_mismatch(self, value):
        self._set_property("proportion_base_mismatch", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_coverage_10x(self, value):
        self._set_property("proportion_coverage_10x", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_coverage_30x(self, value):
        self._set_property("proportion_coverage_30x", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_reads_duplicated(self, value):
        self._set_property("proportion_reads_duplicated", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_reads_mapped(self, value):
        self._set_property("proportion_reads_mapped", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def proportion_targets_no_coverage(self, value):
        self._set_property("proportion_targets_no_coverage", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def total_reads(self, value):
        self._set_property("total_reads", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_ploidy(self, value):
        self._set_property("tumor_ploidy", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def tumor_purity(self, value):
        self._set_property("tumor_purity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum=["0x-10x", "10x-25x", "150x+", "25x-150x", "Not Applicable", "Unknown"],
    )
    def wgs_coverage(self, value):
        self._set_property("wgs_coverage", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(AlignedReads)
datetime_hooks.cls_inject_updated_datetime_hook(AlignedReads)
