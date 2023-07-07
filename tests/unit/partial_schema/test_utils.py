import os.path

from gdcdatamodel2.partial_dictionary import utils


def test_partial_schema():
    data_path = os.path.dirname(__file__) + "/data"
    test_schema = utils.get_partial_dictionary(data_path).schema
    assert "aggregated_somatic_mutation" in test_schema
    assert "alignment_cocleaning_workflow" in test_schema

    partial_schema = utils.get_partial_dictionary().schema
    assert "case" in partial_schema
