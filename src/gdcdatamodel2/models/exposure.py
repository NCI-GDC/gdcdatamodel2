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

    @psqlgraph.pg_property(str, enum={"Weekly Drinker", "Daily Drinker"})
    def alcohol_frequency(self, value):
        self._set_property("alcohol_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Amosite", "Crocidolite"})
    def asbestos_exposure_type(self, value):
        self._set_property("asbestos_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def age_at_last_exposure(self, value):
        self._set_property("age_at_last_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def age_at_onset(self, value):
        self._set_property("age_at_onset", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def alcohol_days_per_week(self, value):
        self._set_property("alcohol_days_per_week", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def alcohol_drinks_per_day(self, value):
        self._set_property("alcohol_drinks_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "Unknown", "Not Reported", "no", "No", "yes"})
    def alcohol_history(self, value):
        self._set_property("alcohol_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Drinker",
            "Lifelong Non-Drinker",
            "Non-Drinker",
            "Occasional Drinker",
            "Heavy Drinker",
            "Not Reported",
            "Social Drinker",
        },
    )
    def alcohol_intensity(self, value):
        self._set_property("alcohol_intensity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Beer", "Unknown", "Not Reported", "Other", "Liquor", "Wine"}
    )
    def alcohol_type(self, value):
        self._set_property("alcohol_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def asbestos_exposure(self, value):
        self._set_property("asbestos_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def chemical_exposure_type(self, value):
        self._set_property("chemical_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def cigarettes_per_day(self, value):
        self._set_property("cigarettes_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown"})
    def coal_dust_exposure(self, value):
        self._set_property("coal_dust_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown"})
    def environmental_tobacco_smoke_exposure(self, value):
        self._set_property("environmental_tobacco_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Unknown", "Six Weeks or More"})
    def exposure_duration(self, value):
        self._set_property("exposure_duration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def exposure_duration_years(self, value):
        self._set_property("exposure_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Secondary", "Unknown", "Occupational"})
    def exposure_source(self, value):
        self._set_property("exposure_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Smokeless Tobacco",
            "Chemical",
            "Smoke",
            "Marijuana",
            "Radon",
            "Coal Dust",
            "Radiation",
            "Tobacco",
            "Asbestos",
            "Respirable Crystalline Silica",
            "Wood Dust",
        },
    )
    def exposure_type(self, value):
        self._set_property("exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def occupation_duration_years(self, value):
        self._set_property("occupation_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def occupation_type(self, value):
        self._set_property("occupation_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def pack_years_smoked(self, value):
        self._set_property("pack_years_smoked", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Not Reported"})
    def parent_with_radiation_exposure(self, value):
        self._set_property("parent_with_radiation_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def radon_exposure(self, value):
        self._set_property("radon_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown"})
    def respirable_crystalline_silica_exposure(self, value):
        self._set_property("respirable_crystalline_silica_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def secondhand_smoke_as_child(self, value):
        self._set_property("secondhand_smoke_as_child", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Every day", "Unknown", "Some days"})
    def smoking_frequency(self, value):
        self._set_property("smoking_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Within 5 Minutes",
            "Unknown",
            "6-30 Minutes",
            "After 60 Minutes",
            "31-60 Minutes",
        },
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
        enum={
            "Current Reformed Smoker, Duration Not Specified",
            "Smoker at Diagnosis",
            "Current Reformed Smoker for < or = 15 yrs",
            "Current Smoker",
            "Lifelong Non-Smoker",
            "2",
            "Smoking history not documented",
            "3",
            "Current Reformed Smoker for > 15 yrs",
            "7",
            "Unknown",
            "6",
            "5",
            "Not Reported",
            "1",
            "Not Allowed To Collect",
            "4",
        },
    )
    def tobacco_smoking_status(self, value):
        self._set_property("tobacco_smoking_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Accidental vehicle fire smoke",
            "Tobacco smoke, pipe",
            "Cooking-related smoke, NOS",
            "Grilling smoke",
            "Work-related smoke, plumbing",
            "Electronic cigarette smoke, NOS",
            "Oil burning smoke, NOS",
            "Field burning smoke",
            "Work-related smoke, fire fighting",
            "Work-related smoke, soldering/welding",
            "Accidental fire smoke, NOS",
            "Indoor stove or fireplace smoke, coal burning",
            "Coal smoke, NOS",
            "Marijuana smoke",
            "Smokehouse smoke",
            "Work-related smoke, generators",
            "Work-related smoke, military",
            "Unknown",
            "Tobacco smoke, cigar",
            "No Smoke Exposure",
            "Work-related smoke, plastics factory",
            "Tobacco smoke, NOS",
            "Gas burning smoke, propane",
            "Work-related smoke, foundry",
            "Recreational fire smoke",
            "Hashish smoke",
            "Machine smoke",
            "Indoor stove or fireplace smoke, NOS",
            "Work-related smoke, paint baking",
            "Furnace or boiler smoke",
            "Accidental forest fire smoke",
            "Aircraft smoke",
            "Grease fire smoke",
            "Electrical fire smoke",
            "Wood burning smoke, NOS",
            "Tobacco smoke, cigarettes",
            "Oil burning smoke, Kerosene",
            "Waste burning smoke",
            "Work-related smoke, NOS",
            "Work-related smoke, artificial smoke machines",
            "Accidental fire smoke, grass",
            "Accidental building fire smoke",
            "Volcanic smoke",
            "Indoor stove or fireplace smoke, wood burning",
            "Environmental tobacco smoke",
            "Burning tree smoke",
            "Factory smokestack smoke",
            "Fire smoke, NOS",
            "Wood burning smoke, factory",
            "Smoke exposure, NOS",
        },
    )
    def type_of_smoke_exposure(self, value):
        self._set_property("type_of_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Pipe",
            "Smokeless Tobacco",
            "Cigarette",
            "Other",
            "Cigar",
            "Electronic Cigarette",
        },
    )
    def type_of_tobacco_used(self, value):
        self._set_property("type_of_tobacco_used", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def use_per_day(self, value):
        self._set_property("use_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def years_smoked(self, value):
        self._set_property("years_smoked", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Exposure)
datetime_hooks.cls_inject_updated_datetime_hook(Exposure)
