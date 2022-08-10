from typing import Any, Dict, List, Optional, Union

import psqlgraph
from sqlalchemy.ext import hybrid

from .helpers import base, datetime_hooks, indexes, related_cases, versioning


class DataSubtype(base.Node):
    __tablename__: str = "node_datasubtype"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["name"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Data Subtype",
        "namespace": "https://gdc.cancer.gov",
        "category": "TBD",
        "submittable": False,
        "downloadable": False,
        "description": "Data subtype of a legacy file (deprecated).",
        "required": ["name", "data_types"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "data_subtype"

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
                "name": "data_subtypes",
                "src_type": base.Node.get_subclass("file"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "data_types": {
                "backref": "data_subtypes",
                "type": base.Node.get_subclass("data_type"),
            },
            "files": {
                "backref": "data_subtypes",
                "type": base.Node.get_subclass("file"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "data_types": {
                "edge_out": "_DataSubtypeMemberOfDataType_out",
                "dst_type": base.Node.get_subclass("data_type"),
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
    def _secondary_keys(self):
        vals = []
        for keys in self.__pg_secondary_keys:
            vals.append(tuple(getattr(self, key) for key in keys))
        return tuple(vals)

    @_secondary_keys.comparator
    def _secondary_keys(cls):
        return indexes.SecondaryKeyComparator(cls)

    # Set this attribute so psqlgraph doesn't treat it as a property
    _secondary_keys._is_pg_property = False

    @psqlgraph.pg_property(str)
    def name(self, value):
        self._set_property("name", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(DataSubtype)
datetime_hooks.cls_inject_updated_datetime_hook(DataSubtype)
