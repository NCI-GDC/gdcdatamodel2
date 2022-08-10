from copy import copy

from gdcdatamodel2 import validators


class MockSubmissionEntity(object):
    def __init__(self):
        self.errors = []
        self.node = None
        self.doc = {}

    def record_error(self, message, **kwargs):
        self.errors.append(dict(message=message, **kwargs))


def test_json_validator_with_insufficient_properties():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {"type": "aliquot", "centers": {"submitter_id": "test"}}
    json_validator.record_errors(entities)
    assert entities[0].errors[0]["keys"] == ["submitter_id"]
    assert len(entities[0].errors) == 1


def test_json_validator_with_wrong_node_type():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {"type": "aliquo"}
    json_validator.record_errors(entities)
    assert entities[0].errors[0]["keys"] == ["type"]
    assert len(entities[0].errors) == 1


def test_json_validator_with_wrong_property_type():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {"type": "aliquot", "submitter_id": 1, "centers": {"submitter_id": "test"}}
    json_validator.record_errors(entities)
    assert entities[0].errors[0]["keys"] == ["submitter_id"]
    assert len(entities[0].errors) == 1


def test_json_validator_with_multiple_errors():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {
        "type": "aliquot",
        "submitter_id": 1,
        "test": "test",
        "centers": {"submitter_id": "test"},
    }
    json_validator.record_errors(entities)
    assert len(entities[0].errors) == 2


def test_json_validator_with_nested_error_keys():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {
        "type": "aliquot",
        "submitter_id": "test",
        "centers": {"submitter_id": True},
    }
    json_validator.record_errors(entities)
    assert entities[0].errors[0]["keys"] == ["centers"]


def test_json_validator_with_multiple_entities():
    entities = [MockSubmissionEntity()]
    json_validator = validators.GDCJSONValidator()
    entities[0].doc = {
        "type": "aliquot",
        "submitter_id": 1,
        "test": "test",
        "centers": {"submitter_id": "test"},
    }
    entity = MockSubmissionEntity()
    entity.doc = {"type": "aliquot", "submitter_id": "test", "centers": {"submitter_id": "test"}}
    entities.append(entity)

    json_validator.record_errors(entities)
    assert len(entities[0].errors) == 2
    assert len(entity.errors) == 0


def test_json_validator_with_array_prop():
    entity_doc = {
        "type": "diagnosis",
        "submitter_id": "test",
        "age_at_diagnosis": 10,
        "primary_diagnosis": "Abdominal desmoid",
        "morphology": "8000/0",
        "tissue_or_organ_of_origin": "Abdomen, NOS",
        "site_of_resection_or_biopsy": "Abdomen, NOS",
    }

    def mock_doc(sites_of_involvement):
        mock = MockSubmissionEntity()
        mock.doc = copy(entity_doc)
        mock.doc["sites_of_involvement"] = sites_of_involvement
        return mock

    # Right is invalid value and diagnosis_is_primary_disease is required
    entities = [
        mock_doc(["Right"]),
        mock_doc(["Cervix", "Right"]),
        mock_doc(["Cervix", "Ovary, NOS"]),
    ]

    json_validator = validators.GDCJSONValidator()

    json_validator.record_errors(entities)
    assert len(entities[0].errors) == 2
    assert len(entities[1].errors) == 2
    assert len(entities[2].errors) == 1
    error_keys_zero = sorted(error["keys"][0] for error in entities[0].errors)
    error_keys_one = sorted(error["keys"][0] for error in entities[1].errors)

    assert error_keys_zero == ["diagnosis_is_primary_disease", "sites_of_involvement.0"]
    assert error_keys_one == ["diagnosis_is_primary_disease", "sites_of_involvement.1"]
