# Welcome to gdcdatamodel2

Repo to keep information about the GDC data model design.

<!-- toc -->

# Table of Contents

- [Installation](#Installation)
- [Testing](#Testing)
- [Update models](#Update-models)
  - [Update Plaster](#Update-Plaster)
  - [Update dictionary](#Update-dictionary)
  - [Generate graph models](#Generate-graph-models)
    - [Known Issues:](#Known-Issues:)
- [Visualize Graph](#Visualize-Graph)
- [Repo Visualizer](#Repo-Visualizer)

<!-- tocstop -->

This project is a drop-in replacement to the project
https://github.com/NCI-GDC/gdcdatamodel, without challenges and obscurity associated
with using gdcdatamodel. The resulting code will be readable, pass static and linting
checks, completely remove delays from dictionary load times.

# Requirements

- Python >= 3.6

# Installation

To install the gdcdatamodel library run the setup script:

```bash
python setup.py install
```

# Testing

Install dependencies with:

```bash
pip install --no-deps -r dev-requirements.txt
```

Run test with:

```bash
pytest tests
```

# Update models

Some times we need to add new data types to our graph. Bio team will update the
biodictionary and biodatamodels. The bio team or user service team will helps us update
gdcdictionary. After the gdcditionary is updated and merged, The gdcdatamodel2 should be
automatically updated and released to nexus by gitlab-ci. But we can also manual update
gdcdatamodel2 by following steps.


## Update Plaster
Plaster is the application used to generate gdcdatamodel2. Most of the time,  for date
release, we only need to update gdcdictionary and leave the plaster untouched.

To use a different version of plaster, update the plaster entry in
plaster file in root directory.

## Update dictionary

To use a different version of gdcdictioanry, update the version value of
profile.gdcdictionary in [plaster.toml](plaster.toml).

## Generate graph models

Generate graph with:

```bash
bash plaster
```

### Known Issues:

1. If you see this error:
    ```
    File "/Users/qiaoqiao/gdc/gdcdatamodel2/venv_plaster/lib/python3.8/site-packages/dulwich/refs.py", line 326, in __getitem__
        raise KeyError(name)
    KeyError: b'refs/tags/2.6.6'
   ```
    run the command to remove the cache `rm -rf ~/.gml/git/gdcdictionary`

# Visualize Graph

For interactive visualization, use [gexplorer](https://github.com/ncI-GDC/gexplorer)

Use following code in jupyterlab to visualize your graph.
```python
from IPython.display import display
from gdcdatamodel2 import models
from gdcdatamodel2.viz import create_graphviz

with g.session_scope():
    cases = g.nodes(models.Case).subq_path('samples').limit(1).all()
    case_neighbors = [edge.src for case in cases for edge in case.edges_in]
    samples = [sample for case in cases for sample in case.samples]
    portions = [portion for sample in samples for portion in sample.portions]
    analytes = [analyte for portion in portions for analyte in portion.analytes]
    aliquots = [aliquot for analyte in analytes for aliquot in analyte.aliquots]
    nodes = cases + case_neighbors + samples + portions + analytes + aliquots
    display(create_graphviz(nodes))
```

Example result:
![Visualization of graph](examples/jupyter_example.svg)


# Repo Visualizer

![Visualization of this repo](images/diagram.svg)
