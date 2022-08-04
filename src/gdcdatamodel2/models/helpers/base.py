from psqlgraph import ext

# namespace needed for multiple dictionaries to work at same time(graphmanager)
namespace = None

# the register_base_class is needed for edge.get_node_class to work
Node, Edge = ext.register_base_class(namespace)
