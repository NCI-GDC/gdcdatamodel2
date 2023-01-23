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
            "validated",
            "md5summing",
            "redacted",
            "invalid",
            "submitted",
            "uploading",
            "released",
            "error",
            "uploaded",
            "md5summed",
        },
    )
    def state(self, value):
        self._set_property("state", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str)
    def project_id(self, value):
        self._set_property("project_id", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), str)
    def created_datetime(self, value):
        self._set_property("created_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), str)
    def updated_datetime(self, value):
        self._set_property("updated_datetime", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Daughter",
            "Grandparent",
            "Father-in-law",
            "Paternal Grandfather",
            "Brother-in-law",
            "Unrelated",
            "Daughter-in-law",
            "Stepdaughter",
            "Step Sibling",
            "Paternal Great Grandparent",
            "Niece",
            "Maternal Great Aunt",
            "Ward",
            "Identical Twin Sister",
            "Sibling",
            "Male Sibling of Adopted Child",
            "Fraternal Twin Sibling",
            "Foster Mother",
            "Natural Parent",
            "Full Sister",
            "Grandson",
            "Full Brother",
            "Paternal First Cousin Once Removed",
            "Maternal Great Uncle",
            "Father",
            "Half Brother",
            "Natural Sibling",
            "Natural Father",
            "Paternal Half Sibling",
            "Natural Grandfather",
            "Paternal Grandmother",
            "Maternal Grandfather",
            "Paternal Aunt",
            "Half Sibling",
            "Foster Son",
            "Maternal First Cousin",
            "Other",
            "Spouse",
            "Grandfather",
            "Stepsister",
            "Foster Daughter",
            "Domestic Partner",
            "Maternal Grandparent",
            "Stepson",
            "Sister",
            "Child",
            "Step Child",
            "Grand Niece",
            "Natural Sister",
            "Paternal Half Sister",
            "Natural Daughter",
            "Nephew",
            "Natural Son",
            "Grandchild",
            "Maternal Grandmother",
            "Identical Twin Brother",
            "Maternal Half Sister",
            "Paternal Half Brother",
            "Adopted Daughter",
            "Cousin",
            "Stepfather",
            "Maternal Half Brother",
            "Natural Grandchild",
            "Maternal Half Sibling",
            "Natural Grandmother",
            "First Cousin",
            "Granddaughter",
            "Twin Sibling",
            "First Cousin Once Removed",
            "Foster Sister",
            "Mother-in-law",
            "Half Sister",
            "Paternal Great Uncle",
            "Identical Twin Sibling",
            "Sister-in-law",
            "Great Grandchild",
            "Adopted Son",
            "Grandmother",
            "Legal Guardian",
            "Natural Child",
            "Niece Second Degree Relative",
            "Wife",
            "Natural Grandparent",
            "Not Reported",
            "Parent",
            "First Degree Relative, NOS",
            "Maternal First Cousin Once Removed",
            "Uncle",
            "Paternal Grandparent",
            "Adopted Brother",
            "Adopted Sister",
            "Natural Brother",
            "Adoptive Father",
            "Adoptive Mother",
            "Maternal Aunt",
            "Husband",
            "Paternal Great Aunt",
            "Stepbrother",
            "Grand Nephew",
            "Mother",
            "Fraternal Twin Sister",
            "Unknown",
            "Foster Father",
            "Paternal Uncle",
            "Female Cousin",
            "Maternal Uncle",
            "Maternal Great Grandparent",
            "Foster Brother",
            "Brother",
            "Stepmother",
            "Male Cousin",
            "Son-in-law",
            "Natural Mother",
            "Female Sibling of Adopted Child",
            "Son",
            "Aunt",
            "Fraternal Twin Brother",
            "Paternal First Cousin",
        },
    )
    def relationship_type(self, value):
        self._set_property("relationship_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"unspecified", "female", "not reported", "unknown", "male"})
    def relationship_gender(self, value):
        self._set_property("relationship_gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def relationship_age_at_diagnosis(self, value):
        self._set_property("relationship_age_at_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Gynecologic Cancer",
            "Lymph Node Cancer",
            "Thyroid Cancer",
            "Glioblastoma",
            "Basal Cell Cancer",
            "Osteosarcoma",
            "Tonsillar Cancer",
            "Bladder Cancer",
            "Gallbladder Cancer",
            "Head and Neck Cancer",
            "Lymphoma",
            "Not Reported",
            "Ewing Sarcoma",
            "Sarcoma",
            "Blood Cancer",
            "Wilms Tumor",
            "Chondrosarcoma",
            "Esophageal Cancer",
            "Pediatric Liver Cancer",
            "CNS Cancer",
            "Spleen Cancer",
            "Brain Cancer",
            "Hematologic Cancer",
            "Cervical Cancer",
            "Breast Cancer",
            "Melanoma",
            "Neuroblastoma",
            "Rectal Cancer",
            "Tongue Cancer",
            "Pancreas Cancer",
            "Cancer",
            "Throat Cancer",
            "Kaposi Sarcoma",
            "Liver Cancer",
            "Mesothelioma",
            "Unknown",
            "Prostate Cancer",
            "Bile Duct Cancer",
            "Laryngeal Cancer",
            "Rhabdomyosarcoma",
            "Testicular Cancer",
            "Kidney Cancer",
            "Multiple Myeloma",
            "Colorectal Cancer",
            "Bone Cancer",
            "Skin Cancer",
            "Leukemia",
            "Gastric Cancer",
            "Ovarian Cancer",
            "Adrenal Gland Cancer",
            "Uterine Cancer",
            "Lung Cancer",
        },
    )
    def relationship_primary_diagnosis(self, value):
        self._set_property("relationship_primary_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"unknown", "yes", "not reported", "no"})
    def relative_with_cancer_history(self, value):
        self._set_property("relative_with_cancer_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def relatives_with_cancer_history_count(self, value):
        self._set_property("relatives_with_cancer_history_count", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FamilyHistory)
datetime_hooks.cls_inject_updated_datetime_hook(FamilyHistory)
