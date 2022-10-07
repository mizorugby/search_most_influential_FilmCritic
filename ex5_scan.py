import networkx as nx
import math
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np
import pprint

G = nx.read_edgelist("user_graph.txt", nodetype=str)
# G = nx.read_edgelist("test.txt", nodetype=int)
"""
Commu_list = list(greedy_modularity_communities(G))
print(Commu_list)
"""

nodes_list = G.nodes()
all_cluster = []
mu = 2
eps = 0.4


def sigma(u, v):  # シグマを計算する関数
    G_n = set(G.adj[u])
    G_n.add(u)
    G_m = set(G.adj[v])
    G_m.add(v)
    len_and = len(G_n & G_m)
    sqrt = math.sqrt(len(G_n) * len(G_m))
    sigma_val = len_and / sqrt
    return sigma_val


saw_nodes = set()


def Community(u):  # 資料のアルゴリズム1~3を実装する関数
    if u in saw_nodes:  # すでに見たノードは見ない
        _set = set()
        return _set

    saw_nodes.add(u)  # 見たノードに自分を追加
    sigma_set = set()
    for v in set(G.adj[u]):
        if sigma(u, v) >= eps:
            sigma_set.add(v)  # sigmaがepsを超えているノードを集める

    if len(sigma_set) >= mu:  # coreだったら
        true_cluster = set()
        true_cluster = sigma_set.copy()
        true_cluster.add(u)  # 自分を追加
        for v in sigma_set:
            _set = set()
            # 自分とepsを超えてるノード、その中のノードの再帰の返り値の和集合
            true_cluster |= Community(v)
        return (true_cluster)

    else:  # 上記の条件に当てはまらないノードの場合
        _set = set()
        return _set


def scan_communities(G, eps, mu):
    hub_Outliers_set = set(G.nodes())  # ここに外れ値とハブを格納

    for u in nodes_list:
        community_set = set()
        community_set = Community(u)  # uが含まれるクラスター

        if len(community_set) != 0:  # community_setの空set判定
            all_cluster.append(community_set)  # 空setでなければクラスタなので追加

        for v in nodes_list:  # すべてのノードを見て
            if v in community_set:
                hub_Outliers_set.discard(v)  # クラスターに含まれるノードを削除

    hub_set = set()  # hubをここに格納
    list_cluster = list(all_cluster)  # クラスタをリスト化
    for u in hub_Outliers_set:  # ハブか外れ値のどっちかのノード
        count = 0  # つながっているクラスタの数
        u_connect = list(G.adj[u])  # uにつながっているノードのリスト
        for t in range(len(u_connect)):
            for v in list_cluster:  # 一つのクラスタ
                if (u_connect[t] in v):  # uにつながっているノードリストのうちt番目のものがクラスタに含まれているか
                    count = count + 1  # 含まれていたらcountを1プラス
        if (count >= 2):  # countが2以上ならhubとしてhub_setに追加
            hub_set.add(u)

    Outliers_set = set()  # 外れ値をここに格納
    Outliers_set = hub_Outliers_set - hub_set  # hoge

    for u in hub_Outliers_set:
        hoge = set()
        hoge.add(u)
        all_cluster.append(hoge)  # 外れ値、ハブを最終結果に追加


scan_communities(G, eps, mu)

G = nx.read_edgelist("user_graph.txt", nodetype=str)
pos = nx.spring_layout(G, k=0.9)  # posが各ノードの位置が格納
color_list = ['green', 'black', 'red', 'yellow',
              'sienna', 'orange', 'blue', 'hotpink', 'lime', 'purple', ]


nodes_count = 0
for u in all_cluster:
    for i in u:
        if (len(u) == 1):
            G.nodes[i]['group'] = 100
        else:
            G.nodes[i]['group'] = nodes_count  # ノードにクラスタ番号の属性値を追加
    nodes_count = nodes_count + 1

for u in G.nodes():
    if (G.nodes[u]['group'] == 100):
        x = 0
        y = 0
        local = np.array([x, y])
        pos[u] = local  # ノードを(x, y)だけ移動する
    else:
        x = 5 * math.sin(G.nodes[u]['group'] * 50)
        y = 3 * math.cos(G.nodes[u]['group'] * 50)
        local = np.array([x, y])
        pos[u] = pos[u] + local  # ノードを(x, y)だけ移動する


color_count = 2
for u in all_cluster:
    for i in u:
        if (len(u) == 1):
            G.nodes[i]['color'] = color_list[1]
        else:
            G.nodes[i]['color'] = color_list[(
                color_count % 10)]  # ノードに色の属性値を追加
    color_count = color_count + 1


plt.figure(figsize=(13, 10))  # image is 10 x 8 inches
color = [G.nodes[i]['color'] for i in G.nodes]  # colorにノードのカラー属性に格納されている色を格納する
nx.draw_networkx_nodes(G, pos, node_size=15, node_color=color)
nx.draw_networkx_edges(G, pos, alpha=0.5, width=0.08)
plt.axis('off')
plt.show()
