import os.path

from gdcdatamodel2.partial_schema import utils


def test_partial_schema():
    data_path = os.path.dirname(__file__) + "/data"
    test_schema = utils.get_partial_schema(data_path)
    assert "aggregated_somatic_mutation" in test_schema["schema"]
    assert "alignment_cocleaning_workflow" in test_schema["schema"]

    partial_schema = utils.get_partial_schema()
    assert "case" in partial_schema["schema"]
