# Welcome to gdcdatamodel2

> [!NOTE]
> The code in this repository has been made public as-is for informational purposes. The repository may use private resources for the building and execution of the code. For example, private registries may be used for dependency resolution.
>
> The documentation may refer to restricted URLs.

Repo to keep information about the GDC data model design.

<!-- toc -->

# Table of Contents

- [Testing](#Testing)
  - [Prerequistes](#Prerequistes)
  - [Execution](#Execution)
- [Repo Visualizer](#Repo-Visualizer)

<!-- tocstop -->

This project replaces [gdcdatamodel](https://github.com/NCI-GDC/gdcdatamodel)
to overcome the challenges and obscurity associated
with using gdcdatamodel. The resulting code is readable, passes static and linting
checks, and completely removes delays from dictionary load times.

# Requirements

- Python >= 3.10

# Testing

> At this time the dependencies: [gdcdictionary](https://github.com/NCI-GDC/gdcdictionary) and [psqlgraph](https://github.com/NCI-GDC/psqlgraph/) will have to be independenty assembled as they are not available for download from the public pypi repository.

## Prerequistes

- Python >= 3.9 environment
- `tox` installed e.g., `pip install tox`

## Execution

Run tests with:

```bash
tox
```

# Repo Visualizer

![Visualization of this repo](images/diagram.svg)
