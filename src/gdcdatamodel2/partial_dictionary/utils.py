import functools
import os
import pathlib
from typing import Dict, Optional

import yaml


class PartialDictionary:
    def __init__(self):
        self.schema = {}


@functools.lru_cache(maxsize=3)
def get_partial_dictionary(path: Optional[str] = None) -> Dict[str, Dict]:
    partial_dictionary = PartialDictionary()

    if not path:
        path = os.path.dirname(__file__)

    for file in pathlib.Path(path).glob("*.yml"):
        with open(file) as fp:
            dictionary = yaml.safe_load(fp)
        if "schema" in dictionary:
            dictionary = dictionary["schema"]
        partial_dictionary.schema.update(dictionary)

    return partial_dictionary
