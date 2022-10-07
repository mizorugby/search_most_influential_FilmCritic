import networkx as nx
import math
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import pprint

G = nx.read_edgelist("user_graph.txt", nodetype=str)

Commu_list = list(greedy_modularity_communities(G))

for u in Commu_list:
    print(u)
