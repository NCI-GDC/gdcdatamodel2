from typing import Any, Dict, List, Tuple, Union, Optional

import psqlgraph
from sqlalchemy.ext import hybrid
from sqlalchemy.orm import query, Session

from .helpers import (
    base,
    datetime_hooks,
    indexes,
    related_cases,
    versioning,
    versioned_nodes,
)


class TissueSourceSite(base.Node):
    __tablename__: str = "node_tissuesourcesite"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["code"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Tissue Source Site",
        "namespace": "https://gdc.cancer.gov",
        "category": "administrative",
        "submittable": False,
        "downloadable": False,
        "description": "A clinical site that collects and provides patient samples and clinical metadata for research use. (NCIt C103264)",
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "tissue_source_site"

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
                "name": "tissue_source_sites",
                "src_type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "name": "tissue_source_sites",
                "src_type": base.Node.get_subclass("case"),
            },
            "samples": {
                "name": "tissue_source_sites",
                "src_type": base.Node.get_subclass("sample"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "tissue_source_sites",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "tissue_source_sites",
                "type": base.Node.get_subclass("case"),
            },
            "samples": {
                "backref": "tissue_source_sites",
                "type": base.Node.get_subclass("sample"),
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

    @psqlgraph.pg_property(str)
    def name(self, value):
        self._set_property("name", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def code(self, value):
        self._set_property("code", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def project(self, value):
        self._set_property("project", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def bcr_id(self, value):
        self._set_property("bcr_id", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(TissueSourceSite)
datetime_hooks.cls_inject_updated_datetime_hook(TissueSourceSite)
