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


class Tag(base.Node):
    __tablename__: str = "node_tag"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["name"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Tag",
        "namespace": "https://gdc.cancer.gov",
        "category": "TBD",
        "submittable": False,
        "downloadable": False,
        "description": "Any comment or other information about an entity (deprecated).",
        "required": ["name"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "tag"

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
            "files": {
                "name": "tags",
                "src_type": base.Node.get_subclass("file"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "files": {
                "backref": "tags",
                "type": base.Node.get_subclass("file"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {}

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

    @psqlgraph.pg_property(
        str,
        enum={
            "original",
            "Paired_LogR",
            "segmentation",
            "Delta_B_Allele_Freq",
            "DGE",
            "batch_effect_removed",
            "Unpaired_LogR",
            "portion",
            "normalized",
            "gene",
            "germline",
            "MSI",
            "slide",
            "B_Allele_Freq",
            "hg18",
            "Tag",
            "coverage",
            "sv",
            "nocnv",
            "aliquot",
            "diagnostic_slides",
            "hg19",
            "snv",
            "alleleSpecificCN",
            "indel",
            "sample",
            "cgh",
            "meth",
            "seg",
            "miRNA",
            "exon",
            "v1",
            "qc",
            "omf",
            "pairedcn",
            "patient",
            "sif",
            "allcnv",
            "LOH",
            "cqcf",
            "isoform",
            "control",
            "harmonized",
            "hpv",
            "PilotAnalysisPipeline2",
            "FIRMA",
            "cnv",
            "nte",
            "Normal_LogR",
            "radiation",
            "segmented",
            "auxiliary",
            "BioSizing",
            "ismpolish",
            "junction",
            "follow_up",
            "QA",
            "tr",
            "image",
            "summary",
            "byallele",
            "cov",
            "analyte",
            "lowess_normalized_smoothed",
            "bisulfite",
            "tangent",
            "drug",
            "msi",
            "raw",
            "protocol",
            "segnormal",
            "OptionAnalysisPipeline2",
            "v2",
            "Genotypes",
            "unnormalized",
            "somatic",
        },
    )
    def name(self, value):
        self._set_property("name", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Tag)
datetime_hooks.cls_inject_updated_datetime_hook(Tag)
