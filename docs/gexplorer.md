> The intended audience of this document GDC developers

<!-- toc -->

- [Visualize Graph](#visualize-graph)

<!-- tocstop -->

# Visualize Graph

For interactive visualization, use [gexplorer](https://github.com/NCI-GDC/gexplorer)

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
