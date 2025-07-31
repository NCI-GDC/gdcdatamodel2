# Welcome to gdcdatamodel2

Repo to keep information about the GDC data model design.

<!-- toc -->

# Table of Contents

- [Testing](#Testing)
  - [Prerequistes](#Prerequistes)
  - [Execution](#Execution)
- [Update models](#Update-models)
  - [Update dictionary](#Update-dictionary)
  - [Generate graph models](#Generate-graph-models)
- [Visualize Graph](#Visualize-Graph)
- [Repo Visualizer](#Repo-Visualizer)

<!-- tocstop -->

This project replaces [gdcdatamodel](https://github.com/NCI-GDC/gdcdatamodel)
to overcome the challenges and obscurity associated
with using gdcdatamodel. The resulting code is readable, passes static and linting
checks, completely remove delays from dictionary load times.

# Requirements

- Python >= 3.9

# Testing

## Prerequistes

- Python >= 3.9 environment
- Running postgres database natively or with docker
- `tox` installed e.g., `pip install tox`

## Execution

Run tests with:

```bash
tox
```

# Update models

Updating models happens are part of the GDC CI/CD process.
The classes generated from the gdcdictionary are commited to this repository.
Setting up an environment to execute `plaster` is not covered as part of this README.

## Update dictionary

To use a different version of gdcdictioanry, update the version value of
profile.gdcdictionary in [plaster.toml](plaster.toml).

## Generate graph models

Generate graph with:

```bash
bash plaster
```

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
