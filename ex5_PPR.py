import networkx as nx
import math
import numpy as np
import pprint

G = nx.read_edgelist("user_graph.txt", nodetype=str)
# G = nx.read_edgelist("test.txt", nodetype=int)

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


scan_communities(G, eps, mu)
length_list = []
for u in all_cluster:
    length_list.append(len(u))  # 各クラスタの長さを格納
length_list.sort(reverse=True)
big_cluster_len = length_list[0]  # クラスタの中で最も要素数が多いクラスタの長さ

for u in all_cluster:
    if (len(u) == big_cluster_len):
        target_cluster = u  # target_clusterに最も要素数が多いクラスタを格納


#G = nx.read_edgelist("user_graph.txt", nodetype=str)
G = nx.read_weighted_edgelist('weight_graph.txt', nodetype=str)
Personalization_Dict = dict()

PPR_val = dict()
for u in target_cluster:
    u = int(u)
    PPR_val.setdefault(u, 0)
PPR_KeyInt = dict()
for v in target_cluster:
    for u in G.nodes():
        if (u == v):
            Personalization_Dict[u] = 1
        else:
            Personalization_Dict[u] = 0

    result_pagerank = nx.pagerank(
        G, alpha=0.9, personalization=Personalization_Dict, weight='weight')  # 対象のノードがvのPPRを求める

    for PPR_key in result_pagerank.keys():
        PPR_KeyInt[int(PPR_key)] = result_pagerank[PPR_key]

    for k in target_cluster:
        k = int(k)
        PPR_val[k] = PPR_val[k] + PPR_KeyInt[k]

    sort_PPR_val = sorted(PPR_val.items(),
                          key=lambda x: x[1], reverse=True)[0:10]


pprint.pprint(sort_PPR_val)
