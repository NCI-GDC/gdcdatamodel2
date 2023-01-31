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
        enum={
            "validating",
            "suppressed",
            "live",
            "submitted",
            "error",
            "validated",
            "md5summing",
            "uploaded",
            "uploading",
            "released",
            "md5summed",
            "redacted",
            "invalid",
        },
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
        enum={
            "Nephew",
            "Natural Father",
            "Paternal Great Aunt",
            "Son-in-law",
            "Paternal Half Brother",
            "Half Sister",
            "Foster Son",
            "Child",
            "Identical Twin Brother",
            "Mother",
            "Mother-in-law",
            "Sister-in-law",
            "Grandson",
            "Grandparent",
            "Adopted Daughter",
            "Unknown",
            "Half Brother",
            "Niece Second Degree Relative",
            "Grandfather",
            "Maternal Grandparent",
            "Paternal Grandfather",
            "Legal Guardian",
            "Foster Father",
            "Unrelated",
            "Identical Twin Sibling",
            "Ward",
            "Parent",
            "Great Grandchild",
            "Fraternal Twin Sibling",
            "Uncle",
            "Foster Mother",
            "Twin Sibling",
            "Adopted Sister",
            "Maternal First Cousin Once Removed",
            "Natural Parent",
            "Maternal Grandfather",
            "Niece",
            "Stepmother",
            "Maternal Half Brother",
            "Son",
            "Stepfather",
            "Adoptive Mother",
            "Daughter",
            "Fraternal Twin Sister",
            "Stepsister",
            "Paternal Grandparent",
            "Maternal First Cousin",
            "Maternal Grandmother",
            "Natural Child",
            "Natural Grandfather",
            "Stepbrother",
            "Maternal Uncle",
            "Grand Niece",
            "Paternal Grandmother",
            "Not Reported",
            "Maternal Great Aunt",
            "Husband",
            "Paternal First Cousin",
            "Natural Mother",
            "Adopted Brother",
            "Stepson",
            "Natural Sibling",
            "Paternal Half Sister",
            "Father-in-law",
            "Step Sibling",
            "Female Cousin",
            "Natural Grandmother",
            "Adoptive Father",
            "Sister",
            "Granddaughter",
            "Other",
            "Foster Sister",
            "Sibling",
            "Cousin",
            "Paternal Half Sibling",
            "Full Brother",
            "Natural Sister",
            "Male Sibling of Adopted Child",
            "Maternal Great Grandparent",
            "Wife",
            "Aunt",
            "Step Child",
            "Paternal Uncle",
            "Maternal Half Sister",
            "Identical Twin Sister",
            "Grandmother",
            "Grand Nephew",
            "Maternal Half Sibling",
            "Fraternal Twin Brother",
            "Daughter-in-law",
            "First Cousin Once Removed",
            "Father",
            "Stepdaughter",
            "Paternal First Cousin Once Removed",
            "Natural Son",
            "Maternal Aunt",
            "Grandchild",
            "Natural Grandchild",
            "Paternal Great Grandparent",
            "Foster Brother",
            "Maternal Great Uncle",
            "Natural Grandparent",
            "Half Sibling",
            "Paternal Great Uncle",
            "Female Sibling of Adopted Child",
            "Paternal Aunt",
            "Natural Daughter",
            "Natural Brother",
            "Brother",
            "Brother-in-law",
            "First Degree Relative, NOS",
            "Spouse",
            "Domestic Partner",
            "Male Cousin",
            "Adopted Son",
            "First Cousin",
            "Full Sister",
            "Foster Daughter",
        },
    )
    def relationship_type(self, value):
        self._set_property("relationship_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"male", "unspecified", "female", "not reported", "unknown"})
    def relationship_gender(self, value):
        self._set_property("relationship_gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def relationship_age_at_diagnosis(self, value):
        self._set_property("relationship_age_at_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Skin Cancer",
            "Brain Cancer",
            "Kidney Cancer",
            "Kaposi Sarcoma",
            "Head and Neck Cancer",
            "Rectal Cancer",
            "Multiple Myeloma",
            "Bile Duct Cancer",
            "Liver Cancer",
            "Ovarian Cancer",
            "Unknown",
            "Lymph Node Cancer",
            "Lymphoma",
            "Bladder Cancer",
            "Spleen Cancer",
            "Colorectal Cancer",
            "Tonsillar Cancer",
            "Chondrosarcoma",
            "Osteosarcoma",
            "Neuroblastoma",
            "Adrenal Gland Cancer",
            "Throat Cancer",
            "Esophageal Cancer",
            "Gastric Cancer",
            "Pancreas Cancer",
            "Glioblastoma",
            "Pediatric Liver Cancer",
            "Cervical Cancer",
            "Sarcoma",
            "Basal Cell Cancer",
            "Rhabdomyosarcoma",
            "Breast Cancer",
            "Laryngeal Cancer",
            "Lung Cancer",
            "CNS Cancer",
            "Uterine Cancer",
            "Blood Cancer",
            "Testicular Cancer",
            "Cancer",
            "Hematologic Cancer",
            "Mesothelioma",
            "Ewing Sarcoma",
            "Thyroid Cancer",
            "Leukemia",
            "Tongue Cancer",
            "Gynecologic Cancer",
            "Wilms Tumor",
            "Not Reported",
            "Bone Cancer",
            "Prostate Cancer",
            "Gallbladder Cancer",
            "Melanoma",
        },
    )
    def relationship_primary_diagnosis(self, value):
        self._set_property("relationship_primary_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"yes", "not reported", "unknown", "no"})
    def relative_with_cancer_history(self, value):
        self._set_property("relative_with_cancer_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def relatives_with_cancer_history_count(self, value):
        self._set_property("relatives_with_cancer_history_count", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FamilyHistory)
datetime_hooks.cls_inject_updated_datetime_hook(FamilyHistory)
