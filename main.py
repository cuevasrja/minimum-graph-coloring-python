import igraph as ig
import matplotlib.pyplot as plt
import random

visual_style = {
    "edge_width": 0.3,
    "vertex_size": 15,
    "palette": "heat",
    "layout": "fruchterman_reingold"
}

random.seed(1)
gs = [ig.Graph.Barabasi(n=30, m=1) for i in range(4)]

betweenness = [g.betweenness() for g in gs]
colors = [[int(i * 255 / max(btw)) for i in btw] for btw in betweenness]

fig, axs = plt.subplots(2, 2)
axs = axs.ravel()
for g, color, ax in zip(gs, colors, axs):
    ig.plot(g, target=ax, vertex_color=color, **visual_style)
plt.show()
