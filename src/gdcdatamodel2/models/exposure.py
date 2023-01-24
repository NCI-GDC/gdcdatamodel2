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

    @psqlgraph.pg_property(str, enum={"Daily Drinker", "Weekly Drinker"})
    def alcohol_frequency(self, value):
        self._set_property("alcohol_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Crocidolite", "Amosite"})
    def asbestos_exposure_type(self, value):
        self._set_property("asbestos_exposure_type", value)  # type: ignore  # inherited from CommonBase

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

    @psqlgraph.pg_property(str, enum={"Yes", "yes", "no", "Unknown", "Not Reported", "No"})
    def alcohol_history(self, value):
        self._set_property("alcohol_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Heavy Drinker",
            "Drinker",
            "Social Drinker",
            "Occasional Drinker",
            "Not Reported",
            "Lifelong Non-Drinker",
            "Non-Drinker",
            "Unknown",
        },
    )
    def alcohol_intensity(self, value):
        self._set_property("alcohol_intensity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Wine", "Beer", "Other", "Liquor", "Not Reported"}
    )
    def alcohol_type(self, value):
        self._set_property("alcohol_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def asbestos_exposure(self, value):
        self._set_property("asbestos_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def chemical_exposure_type(self, value):
        self._set_property("chemical_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def cigarettes_per_day(self, value):
        self._set_property("cigarettes_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Yes", "No"})
    def coal_dust_exposure(self, value):
        self._set_property("coal_dust_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Yes", "No"})
    def environmental_tobacco_smoke_exposure(self, value):
        self._set_property("environmental_tobacco_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Six Weeks or More", "Unknown"})
    def exposure_duration(self, value):
        self._set_property("exposure_duration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def exposure_duration_years(self, value):
        self._set_property("exposure_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Secondary", "Occupational", "Unknown"})
    def exposure_source(self, value):
        self._set_property("exposure_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Smoke",
            "Respirable Crystalline Silica",
            "Coal Dust",
            "Smokeless Tobacco",
            "Chemical",
            "Asbestos",
            "Radiation",
            "Wood Dust",
            "Tobacco",
            "Marijuana",
            "Radon",
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

    @psqlgraph.pg_property(float, int)
    def pack_years_smoked(self, value):
        self._set_property("pack_years_smoked", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Not Reported", "Yes", "No"})
    def parent_with_radiation_exposure(self, value):
        self._set_property("parent_with_radiation_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def radon_exposure(self, value):
        self._set_property("radon_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Yes", "No"})
    def respirable_crystalline_silica_exposure(self, value):
        self._set_property("respirable_crystalline_silica_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Yes", "No"})
    def secondhand_smoke_as_child(self, value):
        self._set_property("secondhand_smoke_as_child", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Every day", "Some days", "Unknown"})
    def smoking_frequency(self, value):
        self._set_property("smoking_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "31-60 Minutes",
            "After 60 Minutes",
            "Within 5 Minutes",
            "6-30 Minutes",
            "Unknown",
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
            "1",
            "Lifelong Non-Smoker",
            "3",
            "2",
            "Current Smoker",
            "Unknown",
            "Current Reformed Smoker for < or = 15 yrs",
            "6",
            "7",
            "Current Reformed Smoker, Duration Not Specified",
            "Not Allowed To Collect",
            "Smoker at Diagnosis",
            "Not Reported",
            "Current Reformed Smoker for > 15 yrs",
            "4",
            "5",
            "Smoking history not documented",
        },
    )
    def tobacco_smoking_status(self, value):
        self._set_property("tobacco_smoking_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Smokehouse smoke",
            "Tobacco smoke, cigar",
            "Recreational fire smoke",
            "Work-related smoke, plumbing",
            "Indoor stove or fireplace smoke, NOS",
            "Accidental fire smoke, grass",
            "Field burning smoke",
            "Marijuana smoke",
            "Electronic cigarette smoke, NOS",
            "Work-related smoke, fire fighting",
            "Fire smoke, NOS",
            "Wood burning smoke, factory",
            "No Smoke Exposure",
            "Work-related smoke, military",
            "Machine smoke",
            "Tobacco smoke, cigarettes",
            "Hashish smoke",
            "Oil burning smoke, NOS",
            "Factory smokestack smoke",
            "Tobacco smoke, pipe",
            "Work-related smoke, plastics factory",
            "Wood burning smoke, NOS",
            "Work-related smoke, soldering/welding",
            "Burning tree smoke",
            "Tobacco smoke, NOS",
            "Indoor stove or fireplace smoke, coal burning",
            "Work-related smoke, paint baking",
            "Waste burning smoke",
            "Accidental forest fire smoke",
            "Aircraft smoke",
            "Accidental fire smoke, NOS",
            "Cooking-related smoke, NOS",
            "Smoke exposure, NOS",
            "Accidental vehicle fire smoke",
            "Unknown",
            "Volcanic smoke",
            "Work-related smoke, artificial smoke machines",
            "Furnace or boiler smoke",
            "Grease fire smoke",
            "Grilling smoke",
            "Environmental tobacco smoke",
            "Coal smoke, NOS",
            "Gas burning smoke, propane",
            "Work-related smoke, NOS",
            "Work-related smoke, generators",
            "Indoor stove or fireplace smoke, wood burning",
            "Work-related smoke, foundry",
            "Electrical fire smoke",
            "Oil burning smoke, Kerosene",
            "Accidental building fire smoke",
        },
    )
    def type_of_smoke_exposure(self, value):
        self._set_property("type_of_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Pipe",
            "Cigarette",
            "Cigar",
            "Electronic Cigarette",
            "Smokeless Tobacco",
            "Other",
        },
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
