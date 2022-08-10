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
