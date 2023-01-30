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

    @psqlgraph.pg_property(type(None), int)
    def age_at_index(self, value):
        self._set_property("age_at_index", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(bool)
    def age_is_obfuscated(self, value):
        self._set_property("age_is_obfuscated", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "Spinal Muscular Atrophy",
            "Not Cancer Related",
            "Toxicity",
            "Renal Disorder, NOS",
            "Cancer Related",
            "End-stage Renal Disease",
            "Not Reported",
            "Cardiovascular Disorder, NOS",
            "Surgical Complications",
            "Infection",
        },
    )
    def cause_of_death(self, value):
        self._set_property("cause_of_death", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Medical Record",
            "Unknown",
            "Social Security Death Index",
            "Not Reported",
            "Autopsy",
            "Death Certificate",
        },
    )
    def cause_of_death_source(self, value):
        self._set_property("cause_of_death_source", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Jamaica",
            "Bangladesh",
            "Niger",
            "Mayotte",
            "Tunisia",
            "Uganda",
            "Switzerland",
            "Senegal",
            "State of Palestine",
            "Croatia",
            "Antigua and Barbuda",
            "Lebanon",
            "Russia",
            "El Salvador",
            "Chad",
            "Guadeloupe",
            "Japan",
            "Equatorial Guinea",
            "Botswana",
            "Hungary",
            "Mauritius",
            "Maldives",
            "Guam",
            "Angola",
            "Guernsey",
            "Libya",
            "Serbia",
            "Tajikistan",
            "Austria",
            "South Africa",
            "Wallis and Futuna",
            "Virgin Islands, U.S.",
            "Australia",
            "Slovakia",
            "Indonesia",
            "Fiji",
            "Guinea",
            "Algeria",
            "Tuvalu",
            "Turkmenistan",
            "French Guiana",
            "Gambia",
            "Guinea-Bissau",
            "Timor-Leste",
            "Venezuela",
            "New Zealand",
            "Nepal",
            "Trinidad and Tobago",
            "Lesotho",
            "Mali",
            "Chile",
            "Cote d'Ivoire",
            "Yemen",
            "South Sudan",
            "Kenya",
            "Cape Verde",
            "Burundi",
            "Afghanistan",
            "Benin",
            "Qatar",
            "New Caledonia",
            "Bermuda",
            "Germany",
            "Belize",
            "Brunei",
            "Ethiopia",
            "Macau",
            "North Korea",
            "Nauru",
            "Slovenia",
            "Anguilla",
            "Comoros",
            "Honduras",
            "Samoa",
            "Andorra",
            "Hong Kong",
            "Iran",
            "Zambia",
            "France",
            "Democratic Republic of the Congo",
            "Niue",
            "Palau",
            "Oman",
            "Saint Vincent and the Grenadines",
            "Pakistan",
            "Bahamas",
            "Peru",
            "Albania",
            "Suriname",
            "Malawi",
            "North Macedonia",
            "Bosnia and Herzegovina",
            "Mozambique",
            "Seychelles",
            "Spain",
            "Sierra Leone",
            "United Kingdom",
            "Saint Helena, Ascension and Tristan da Cunha",
            "Uzbekistan",
            "Dominican Republic",
            "Cameroon",
            "Paraguay",
            "Bhutan",
            "China",
            "Faroe Islands",
            "Burkina Faso",
            "Kosovo",
            "Laos",
            "Costa Rica",
            "Cyprus",
            "Mauritania",
            "Ireland",
            "Tonga",
            "Mexico",
            "Singapore",
            "Barbados",
            "Liberia",
            "Northern Mariana Islands",
            "Sweden",
            "Bahrain",
            "Estonia",
            "Kiribati",
            "Ukraine",
            "Montserrat",
            "Denmark",
            "Sri Lanka",
            "Bolivia",
            "San Marino",
            "Martinique",
            "Aruba",
            "Norway",
            "Montenegro",
            "Togo",
            "Iceland",
            "Azerbaijan",
            "Namibia",
            "Papua New Guinea",
            "Nigeria",
            "Marshall Islands",
            "Italy",
            "Svalbard & Jan Mayen Islands",
            "Canada",
            "Argentina",
            "Saudi Arabia",
            "Poland",
            "Ghana",
            "Monaco",
            "Curacao",
            "French Polynesia",
            "Syria",
            "Cayman Islands",
            "Uruguay",
            "Egypt",
            "Eswatini",
            "Solomon Islands",
            "Zimbabwe",
            "Cambodia",
            "Turkey",
            "South Korea",
            "Tokelau",
            "Iraq",
            "Myanmar",
            "Vanuatu",
            "Belgium",
            "Belarus",
            "Saint Lucia",
            "Eritrea",
            "Georgia",
            "Tanzania",
            "Virgin Islands, British",
            "Falkland Islands (Malvinas)",
            "Panama",
            "Malta",
            "Western Sahara",
            "Djibouti",
            "Israel",
            "Guyana",
            "Taiwan",
            "Armenia",
            "Sudan",
            "Cook Islands",
            "Finland",
            "Isle of Man",
            "Reunion",
            "Vietnam",
            "Kuwait",
            "Kyrgyzstan",
            "Dominica",
            "Latvia",
            "Haiti",
            "Ecuador",
            "Jordan",
            "Sao Tome and Principe",
            "Moldova",
            "Gibraltar",
            "India",
            "Netherlands",
            "Thailand",
            "Portugal",
            "Morocco",
            "Nicaragua",
            "Liechtenstein",
            "United Arab Emirates",
            "Gabon",
            "United States",
            "Brazil",
            "Rwanda",
            "Philippines",
            "Romania",
            "Bulgaria",
            "Lithuania",
            "Luxembourg",
            "Greenland",
            "Holy See",
            "Mongolia",
            "Somalia",
            "Colombia",
            "Saint Pierre and Miquelon",
            "Greece",
            "Guatemala",
            "Czech Republic (Czechia)",
            "Madagascar",
            "Malaysia",
            "Kazakhstan",
            "Congo",
            "Grenada",
            "Cuba",
            "Puerto Rico",
            "Federated States of Micronesia",
            "Central African Republic",
            "Jersey",
            "Saint Kitts and Nevis",
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
            "Unknown",
            "unknown",
            "not allowed to collect",
            "hispanic or latino",
            "not hispanic or latino",
            "not reported",
        },
    )
    def ethnicity(self, value):
        self._set_property("ethnicity", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str, enum={"unknown", "male", "female", "unspecified", "not reported"}
    )
    def gender(self, value):
        self._set_property("gender", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def occupation_duration_years(self, value):
        self._set_property("occupation_duration_years", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "No", "Not Reported", "Yes"})
    def premature_at_birth(self, value):
        self._set_property("premature_at_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(
        str,
        enum={
            "Unknown",
            "white",
            "native hawaiian or other pacific islander",
            "unknown",
            "black or african american",
            "american indian or alaska native",
            "asian",
            "not reported",
            "other",
            "not allowed to collect",
        },
    )
    def race(self, value):
        self._set_property("race", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(str, enum={"Unknown", "Alive", "Dead", "Not Reported"})
    def vital_status(self, value):
        self._set_property("vital_status", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(float, int)
    def weeks_gestation_at_birth(self, value):
        self._set_property("weeks_gestation_at_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(type(None), int)
    def year_of_birth(self, value):
        self._set_property("year_of_birth", value)  # type: ignore  # inherited from CommonBase

    @psqlgraph.pg_property(int)
    def year_of_death(self, value):
        self._set_property("year_of_death", value)  # type: ignore  # inherited from CommonBase


datetime_hooks.cls_inject_created_datetime_hook(Demographic)
datetime_hooks.cls_inject_updated_datetime_hook(Demographic)
