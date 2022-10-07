import networkx as nx
import math
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import collections
import copy

ppr = {'1': 1, '2': 2, '3': 3}
new_ppr = dict()
for ppr_key in ppr.keys():
    new_ppr[int(ppr_key)] = ppr[ppr_key]

val = 0
for u in range(1, 4):
    val = new_ppr[u] + val
print(val)
