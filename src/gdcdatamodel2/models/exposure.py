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

    @psqlgraph.pg_property(str, enum={"Weekly Drinker", "Daily Drinker"})
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

    @psqlgraph.pg_property(str, enum={"Unknown", "no", "Yes", "yes", "No", "Not Reported"})
    def alcohol_history(self, value):
        self._set_property("alcohol_history", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Social Drinker",
            "Heavy Drinker",
            "Non-Drinker",
            "Occasional Drinker",
            "Not Reported",
            "Lifelong Non-Drinker",
            "Drinker",
        },
    )
    def alcohol_intensity(self, value):
        self._set_property("alcohol_intensity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"Unknown", "Liquor", "Not Reported", "Beer", "Wine", "Other"}
    )
    def alcohol_type(self, value):
        self._set_property("alcohol_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def asbestos_exposure(self, value):
        self._set_property("asbestos_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(list)
    def chemical_exposure_type(self, value):
        self._set_property("chemical_exposure_type", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def cigarettes_per_day(self, value):
        self._set_property("cigarettes_per_day", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Yes"})
    def coal_dust_exposure(self, value):
        self._set_property("coal_dust_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Yes"})
    def environmental_tobacco_smoke_exposure(self, value):
        self._set_property("environmental_tobacco_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Six Weeks or More"})
    def exposure_duration(self, value):
        self._set_property("exposure_duration", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def exposure_duration_years(self, value):
        self._set_property("exposure_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Secondary", "Occupational"})
    def exposure_source(self, value):
        self._set_property("exposure_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Marijuana",
            "Asbestos",
            "Smoke",
            "Tobacco",
            "Smokeless Tobacco",
            "Wood Dust",
            "Respirable Crystalline Silica",
            "Radon",
            "Coal Dust",
            "Chemical",
            "Radiation",
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

    @psqlgraph.pg_property(str, enum={"Not Reported", "No", "Yes"})
    def parent_with_radiation_exposure(self, value):
        self._set_property("parent_with_radiation_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def radon_exposure(self, value):
        self._set_property("radon_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Yes"})
    def respirable_crystalline_silica_exposure(self, value):
        self._set_property("respirable_crystalline_silica_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def secondhand_smoke_as_child(self, value):
        self._set_property("secondhand_smoke_as_child", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Some days", "Every day", "Unknown"})
    def smoking_frequency(self, value):
        self._set_property("smoking_frequency", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "6-30 Minutes",
            "After 60 Minutes",
            "31-60 Minutes",
            "Within 5 Minutes",
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
            "Unknown",
            "6",
            "Lifelong Non-Smoker",
            "2",
            "3",
            "Not Allowed To Collect",
            "Not Reported",
            "5",
            "Current Smoker",
            "Smoking history not documented",
            "Current Reformed Smoker, Duration Not Specified",
            "Current Reformed Smoker for < or = 15 yrs",
            "4",
            "7",
            "Current Reformed Smoker for > 15 yrs",
            "Smoker at Diagnosis",
            "1",
        },
    )
    def tobacco_smoking_status(self, value):
        self._set_property("tobacco_smoking_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Smokehouse smoke",
            "No Smoke Exposure",
            "Smoke exposure, NOS",
            "Work-related smoke, fire fighting",
            "Cooking-related smoke, NOS",
            "Recreational fire smoke",
            "Accidental building fire smoke",
            "Aircraft smoke",
            "Indoor stove or fireplace smoke, wood burning",
            "Tobacco smoke, cigar",
            "Tobacco smoke, pipe",
            "Work-related smoke, paint baking",
            "Oil burning smoke, Kerosene",
            "Gas burning smoke, propane",
            "Grilling smoke",
            "Waste burning smoke",
            "Accidental forest fire smoke",
            "Furnace or boiler smoke",
            "Electrical fire smoke",
            "Work-related smoke, soldering/welding",
            "Grease fire smoke",
            "Machine smoke",
            "Marijuana smoke",
            "Electronic cigarette smoke, NOS",
            "Hashish smoke",
            "Wood burning smoke, factory",
            "Unknown",
            "Work-related smoke, NOS",
            "Work-related smoke, generators",
            "Work-related smoke, artificial smoke machines",
            "Coal smoke, NOS",
            "Oil burning smoke, NOS",
            "Accidental fire smoke, grass",
            "Tobacco smoke, NOS",
            "Work-related smoke, military",
            "Tobacco smoke, cigarettes",
            "Field burning smoke",
            "Wood burning smoke, NOS",
            "Environmental tobacco smoke",
            "Indoor stove or fireplace smoke, coal burning",
            "Burning tree smoke",
            "Work-related smoke, plumbing",
            "Volcanic smoke",
            "Indoor stove or fireplace smoke, NOS",
            "Work-related smoke, foundry",
            "Accidental vehicle fire smoke",
            "Fire smoke, NOS",
            "Factory smokestack smoke",
            "Work-related smoke, plastics factory",
            "Accidental fire smoke, NOS",
        },
    )
    def type_of_smoke_exposure(self, value):
        self._set_property("type_of_smoke_exposure", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Cigar",
            "Cigarette",
            "Pipe",
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
