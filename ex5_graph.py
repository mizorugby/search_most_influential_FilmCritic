import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd

G = nx.read_edgelist("user_graph.txt", nodetype=str)
plt.figure(figsize=(10, 8))

# 図のレイアウトを決める。kの値が小さい程図が密集する
pos = nx.spring_layout(G, k=0.9)

nx.draw_networkx_edges(G, pos, edge_color='b', alpha=0.3)
nx.draw_networkx_nodes(G, pos, node_color='r', alpha=0.5, node_size=50)

nx.draw_networkx_labels(G, pos, font_size=5,
                        font_family='Hiragino Mincho ProN')
plt.axis('off')
plt.show()
