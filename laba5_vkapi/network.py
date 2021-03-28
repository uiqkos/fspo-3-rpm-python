from igraph import *
import numpy as np


def plot_graph(edges, vertices=None, label=None, directed=False, **kwargs):
    if vertices is None:
        vertices = list(range(len(edges) + 1))

    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)

    comms = g.community_leading_eigenvector()
    plot(comms, mark_groups=True, inline=False, vertex_label=None)
