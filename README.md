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

## Update Plaster

To use a different version of plaster, update the `extras_require.plaster` entry in
[setup.cfg](setup.cfg).

## Update dictionary

To use a different version of gdcdictioanry, update the version value of
profile.gdcdictionary in [plaster.toml](plaster.toml).

## Generate graph models

Generate graph with:

```bash
bash plaster
```

# Repo Visualizer

![Visualization of this repo](images/diagram.svg)
