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
