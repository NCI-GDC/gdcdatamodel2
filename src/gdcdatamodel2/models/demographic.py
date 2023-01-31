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


class Demographic(base.Node):
    __tablename__: str = "node_demographic"

    # this field contains values of uniqueProperties
    __pg_secondary_keys: List[List[str]] = [["project_id", "submitter_id"]]

    # _defaults: default value for specified fields in the dictionary
    _defaults: Dict[str, Union[bool, float, int, str]] = {"state": "validated"}
    _dictionary: Dict[str, Union[bool, str, List[str]]] = {
        "title": "Demographic",
        "namespace": "https://gdc.cancer.gov",
        "category": "clinical",
        "submittable": True,
        "downloadable": False,
        "description": "Data for the characterization of the patient by means of segmenting the population (e.g., characterization by age, sex, or race).",
        "required": ["submitter_id", "ethnicity", "gender", "race", "vital_status"],
        "project": "*",
        "program": "*",
        "previous_version_downloadable": False,
    }

    _pg_backrefs: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_edges: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None
    _pg_links: Optional[Dict[str, Dict[str, Union[str, psqlgraph.Node]]]] = None

    @classmethod
    def get_label(cls) -> str:
        return "demographic"

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
                "name": "demographics",
                "src_type": base.Node.get_subclass("annotation"),
            },
        }

    @classmethod
    def populate_pg_edges(cls) -> None:
        """_pg_edges are all edges, links to AND from other types."""
        cls._pg_edges = {
            "annotations": {
                "backref": "demographics",
                "type": base.Node.get_subclass("annotation"),
            },
            "cases": {
                "backref": "demographics",
                "type": base.Node.get_subclass("case"),
            },
        }

    @classmethod
    def populate_pg_links(cls) -> None:
        """_pg_links are out_edges, links TO other types."""
        cls._pg_links = {
            "cases": {
                "edge_out": "_DemographicDescribesCase_out",
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

    @psqlgraph.pg_property(int, type(None))
    def age_at_index(self, value):
        self._set_property("age_at_index", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def age_is_obfuscated(self, value):
        self._set_property("age_is_obfuscated", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Not Cancer Related",
            "Unknown",
            "End-stage Renal Disease",
            "Cardiovascular Disorder, NOS",
            "Spinal Muscular Atrophy",
            "Renal Disorder, NOS",
            "Infection",
            "Toxicity",
            "Not Reported",
            "Cancer Related",
            "Surgical Complications",
        },
    )
    def cause_of_death(self, value):
        self._set_property("cause_of_death", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Social Security Death Index",
            "Death Certificate",
            "Unknown",
            "Not Reported",
            "Medical Record",
            "Autopsy",
        },
    )
    def cause_of_death_source(self, value):
        self._set_property("cause_of_death_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Monaco",
            "Tanzania",
            "Somalia",
            "Czech Republic (Czechia)",
            "Martinique",
            "Nigeria",
            "Aruba",
            "Cape Verde",
            "Costa Rica",
            "Anguilla",
            "Jordan",
            "Turkmenistan",
            "Samoa",
            "Gibraltar",
            "Belarus",
            "Armenia",
            "Bangladesh",
            "Chad",
            "Maldives",
            "Malaysia",
            "Georgia",
            "Switzerland",
            "Curacao",
            "Virgin Islands, U.S.",
            "Macau",
            "Saint Helena, Ascension and Tristan da Cunha",
            "Panama",
            "Eritrea",
            "Finland",
            "Botswana",
            "Argentina",
            "San Marino",
            "Uzbekistan",
            "Antigua and Barbuda",
            "Equatorial Guinea",
            "Italy",
            "Jersey",
            "United Kingdom",
            "New Caledonia",
            "Madagascar",
            "Jamaica",
            "Kuwait",
            "Cambodia",
            "India",
            "Saint Lucia",
            "Lesotho",
            "Iceland",
            "French Polynesia",
            "Bahamas",
            "South Sudan",
            "Kazakhstan",
            "Bermuda",
            "Bulgaria",
            "Suriname",
            "Zimbabwe",
            "Cameroon",
            "Japan",
            "Paraguay",
            "North Korea",
            "French Guiana",
            "Guinea-Bissau",
            "Moldova",
            "Mayotte",
            "Ghana",
            "Rwanda",
            "Qatar",
            "Nicaragua",
            "Venezuela",
            "Malawi",
            "Gabon",
            "Nepal",
            "Peru",
            "Tuvalu",
            "Niue",
            "Cyprus",
            "Mauritius",
            "Netherlands",
            "Northern Mariana Islands",
            "Pakistan",
            "Colombia",
            "South Korea",
            "Mali",
            "Zambia",
            "Morocco",
            "Barbados",
            "Singapore",
            "Cook Islands",
            "Tunisia",
            "Chile",
            "Vanuatu",
            "Dominica",
            "Saudi Arabia",
            "Svalbard & Jan Mayen Islands",
            "Federated States of Micronesia",
            "Mongolia",
            "United States",
            "Cayman Islands",
            "Dominican Republic",
            "Greece",
            "Sudan",
            "Montenegro",
            "Bhutan",
            "Tokelau",
            "Yemen",
            "Malta",
            "Taiwan",
            "Falkland Islands (Malvinas)",
            "Uruguay",
            "Russia",
            "Western Sahara",
            "Mauritania",
            "Lebanon",
            "Guadeloupe",
            "Timor-Leste",
            "Mexico",
            "Togo",
            "Guyana",
            "Oman",
            "Cuba",
            "Saint Kitts and Nevis",
            "Afghanistan",
            "Australia",
            "Algeria",
            "Azerbaijan",
            "Ethiopia",
            "Iran",
            "United Arab Emirates",
            "Bahrain",
            "Virgin Islands, British",
            "Ukraine",
            "Israel",
            "Philippines",
            "Vietnam",
            "Portugal",
            "Kosovo",
            "Belize",
            "Marshall Islands",
            "Gambia",
            "Laos",
            "Saint Pierre and Miquelon",
            "Wallis and Futuna",
            "Romania",
            "Democratic Republic of the Congo",
            "Haiti",
            "Sweden",
            "Faroe Islands",
            "Trinidad and Tobago",
            "Saint Vincent and the Grenadines",
            "Seychelles",
            "Canada",
            "Lithuania",
            "Bolivia",
            "Thailand",
            "Germany",
            "Poland",
            "Mozambique",
            "Slovenia",
            "Isle of Man",
            "Kenya",
            "North Macedonia",
            "El Salvador",
            "Austria",
            "Myanmar",
            "Andorra",
            "Hungary",
            "Latvia",
            "Senegal",
            "Kiribati",
            "Cote d'Ivoire",
            "Grenada",
            "Brunei",
            "State of Palestine",
            "Reunion",
            "Uganda",
            "Sri Lanka",
            "Guatemala",
            "Brazil",
            "Norway",
            "Tajikistan",
            "Central African Republic",
            "Palau",
            "Liechtenstein",
            "Sao Tome and Principe",
            "Syria",
            "China",
            "Angola",
            "Guinea",
            "Holy See",
            "Bosnia and Herzegovina",
            "Estonia",
            "South Africa",
            "Luxembourg",
            "Denmark",
            "Fiji",
            "Guernsey",
            "Slovakia",
            "Congo",
            "France",
            "Montserrat",
            "Albania",
            "Ireland",
            "Guam",
            "Indonesia",
            "New Zealand",
            "Sierra Leone",
            "Tonga",
            "Eswatini",
            "Comoros",
            "Hong Kong",
            "Libya",
            "Puerto Rico",
            "Belgium",
            "Turkey",
            "Greenland",
            "Ecuador",
            "Liberia",
            "Benin",
            "Egypt",
            "Burundi",
            "Serbia",
            "Iraq",
            "Solomon Islands",
            "Spain",
            "Niger",
            "Honduras",
            "Nauru",
            "Namibia",
            "Djibouti",
            "Croatia",
            "Papua New Guinea",
            "Burkina Faso",
            "Kyrgyzstan",
        },
    )
    def country_of_residence_at_enrollment(self, value):
        self._set_property("country_of_residence_at_enrollment", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_birth(self, value):
        self._set_property("days_to_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def days_to_death(self, value):
        self._set_property("days_to_death", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "not allowed to collect",
            "hispanic or latino",
            "Unknown",
            "not hispanic or latino",
            "not reported",
            "unknown",
        },
    )
    def ethnicity(self, value):
        self._set_property("ethnicity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"male", "unspecified", "female", "not reported", "unknown"})
    def gender(self, value):
        self._set_property("gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def occupation_duration_years(self, value):
        self._set_property("occupation_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Yes", "No", "Unknown", "Not Reported"})
    def premature_at_birth(self, value):
        self._set_property("premature_at_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "native hawaiian or other pacific islander",
            "asian",
            "black or african american",
            "american indian or alaska native",
            "white",
            "not allowed to collect",
            "other",
            "not reported",
            "unknown",
        },
    )
    def race(self, value):
        self._set_property("race", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Not Reported", "Dead", "Alive"})
    def vital_status(self, value):
        self._set_property("vital_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, float)
    def weeks_gestation_at_birth(self, value):
        self._set_property("weeks_gestation_at_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int, type(None))
    def year_of_birth(self, value):
        self._set_property("year_of_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def year_of_death(self, value):
        self._set_property("year_of_death", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Demographic)
datetime_hooks.cls_inject_updated_datetime_hook(Demographic)
