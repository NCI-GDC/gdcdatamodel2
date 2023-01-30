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
            "validated",
            "error",
            "md5summing",
            "released",
            "invalid",
            "live",
            "submitted",
            "md5summed",
            "uploading",
            "validating",
            "redacted",
            "uploaded",
            "suppressed",
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
            "Maternal First Cousin Once Removed",
            "Grandchild",
            "Natural Grandchild",
            "Son",
            "Paternal Half Brother",
            "Niece",
            "Niece Second Degree Relative",
            "Domestic Partner",
            "First Cousin",
            "Paternal Grandparent",
            "Female Sibling of Adopted Child",
            "Stepdaughter",
            "Cousin",
            "Maternal Great Aunt",
            "Foster Sister",
            "Child",
            "Natural Sibling",
            "Stepmother",
            "Foster Son",
            "Nephew",
            "Sibling",
            "Half Sister",
            "Natural Child",
            "First Degree Relative, NOS",
            "Grandfather",
            "Unknown",
            "Adopted Daughter",
            "Full Brother",
            "Paternal First Cousin Once Removed",
            "Wife",
            "Ward",
            "Adoptive Father",
            "Uncle",
            "Maternal Grandmother",
            "Parent",
            "Stepbrother",
            "Half Sibling",
            "Aunt",
            "Stepfather",
            "Natural Grandfather",
            "Paternal First Cousin",
            "Foster Brother",
            "Identical Twin Sister",
            "Sister",
            "Unrelated",
            "Foster Father",
            "Maternal Grandparent",
            "Fraternal Twin Sister",
            "Identical Twin Brother",
            "Grandparent",
            "Grandmother",
            "Brother",
            "Natural Brother",
            "Adopted Son",
            "Mother",
            "Maternal Uncle",
            "Fraternal Twin Sibling",
            "Stepsister",
            "Son-in-law",
            "Natural Mother",
            "Paternal Great Uncle",
            "Twin Sibling",
            "Male Sibling of Adopted Child",
            "Adopted Brother",
            "Half Brother",
            "Not Reported",
            "Maternal Half Sister",
            "Step Sibling",
            "Natural Father",
            "Foster Mother",
            "Paternal Grandmother",
            "Maternal Great Grandparent",
            "Natural Daughter",
            "First Cousin Once Removed",
            "Maternal Aunt",
            "Paternal Uncle",
            "Natural Son",
            "Foster Daughter",
            "Paternal Aunt",
            "Grand Niece",
            "Granddaughter",
            "Mother-in-law",
            "Paternal Great Grandparent",
            "Paternal Half Sister",
            "Identical Twin Sibling",
            "Maternal Half Sibling",
            "Grand Nephew",
            "Other",
            "Maternal First Cousin",
            "Maternal Great Uncle",
            "Natural Parent",
            "Paternal Half Sibling",
            "Spouse",
            "Full Sister",
            "Paternal Great Aunt",
            "Adoptive Mother",
            "Natural Grandmother",
            "Natural Sister",
            "Maternal Grandfather",
            "Paternal Grandfather",
            "Stepson",
            "Adopted Sister",
            "Sister-in-law",
            "Maternal Half Brother",
            "Brother-in-law",
            "Daughter",
            "Father-in-law",
            "Natural Grandparent",
            "Fraternal Twin Brother",
            "Daughter-in-law",
            "Grandson",
            "Father",
            "Male Cousin",
            "Legal Guardian",
            "Step Child",
            "Female Cousin",
            "Husband",
            "Great Grandchild",
        },
    )
    def relationship_type(self, value):
        self._set_property("relationship_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"unknown", "male", "female", "unspecified", "not reported"}
    )
    def relationship_gender(self, value):
        self._set_property("relationship_gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def relationship_age_at_diagnosis(self, value):
        self._set_property("relationship_age_at_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Tongue Cancer",
            "Cervical Cancer",
            "Testicular Cancer",
            "Multiple Myeloma",
            "Leukemia",
            "Wilms Tumor",
            "Gastric Cancer",
            "Head and Neck Cancer",
            "Not Reported",
            "Prostate Cancer",
            "Bone Cancer",
            "Hematologic Cancer",
            "Tonsillar Cancer",
            "Spleen Cancer",
            "Throat Cancer",
            "Pediatric Liver Cancer",
            "Brain Cancer",
            "Lung Cancer",
            "Liver Cancer",
            "Bile Duct Cancer",
            "Lymphoma",
            "Ovarian Cancer",
            "Thyroid Cancer",
            "Bladder Cancer",
            "Colorectal Cancer",
            "Unknown",
            "Kaposi Sarcoma",
            "Esophageal Cancer",
            "CNS Cancer",
            "Melanoma",
            "Cancer",
            "Gynecologic Cancer",
            "Lymph Node Cancer",
            "Chondrosarcoma",
            "Osteosarcoma",
            "Adrenal Gland Cancer",
            "Basal Cell Cancer",
            "Blood Cancer",
            "Mesothelioma",
            "Neuroblastoma",
            "Rhabdomyosarcoma",
            "Pancreas Cancer",
            "Sarcoma",
            "Ewing Sarcoma",
            "Rectal Cancer",
            "Laryngeal Cancer",
            "Breast Cancer",
            "Gallbladder Cancer",
            "Skin Cancer",
            "Uterine Cancer",
            "Kidney Cancer",
            "Glioblastoma",
        },
    )
    def relationship_primary_diagnosis(self, value):
        self._set_property("relationship_primary_diagnosis", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"yes", "unknown", "no", "not reported"})
    def relative_with_cancer_history(self, value):
        self._set_property("relative_with_cancer_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def relatives_with_cancer_history_count(self, value):
        self._set_property("relatives_with_cancer_history_count", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(FamilyHistory)
datetime_hooks.cls_inject_updated_datetime_hook(FamilyHistory)
