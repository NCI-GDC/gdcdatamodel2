import functools
import os
import pathlib
from typing import Dict, Optional

import yaml


@functools.lru_cache(None)
def get_partial_schema(path: Optional[str] = None) -> Dict[str, Dict]:
    partial_schema = {"schema": {}}

    if not path:
        path = os.path.dirname(__file__)

    for file in pathlib.Path(path).glob("*.yml"):
        with open(file) as fp:
            dictionary = yaml.safe_load(fp)
            if "schema" in dictionary:
                dictionary = dictionary["schema"]
            partial_schema["schema"].update(dictionary)

    return partial_schema
