import networkx as nx
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import random
from operator import itemgetter
import copy

# csvファイルの読み込み
Data = pd.read_csv('ratings.csv')

Data.drop("timestamp", axis=1, inplace=True)

movieId = set()  # ここにmovieIdのすべての値を格納する
for i in range(1, len(Data)):
    movieId.add(Data.loc[i, 'movieId'])  # movieIdを重複なしで格納


userId = set()  # ここにuserIdのすべての値を格納する
for i in range(1, len(Data)):
    userId.add(Data.loc[i, 'userId'])  # userIdを重複なしで格納

df_list = []  # ここにグラフのもとになるデータセットを格納

for i in movieId:
    for j in range(1, 5):
        new_df = Data[(Data['movieId'] == i) & (Data['rating'] == j)]
        # movieIdがiで評価がjのものを取り出し、そのuserIdをlistに変換
        list_a = new_df.loc[:, 'userId'].values.tolist()
        for i in range(len(list_a) - 1):  # ある映画に同じ評価をつけたuserをlistの要素として格納する。
            add_list = [list_a[i], list_a[i + 1]]
            df_list.append(add_list)

df_weight = copy.copy(df_list)

"""
df_list = list(map(list, set(map(tuple, df_list))))  # 同じ要素を削除
df_list.sort(key=itemgetter(0))
df = pd.DataFrame(df_list)
df.to_csv('user_graph.csv')  # 重みなしグラフ
"""

df_weight.sort(key=itemgetter(0))
weight_list = []
saw_list = []
for u in df_weight:
    if not (u in saw_list):
        saw_list.append(u)
        a = copy.copy(u)
        a.append(df_weight.count(a))
        weight_list.append(a)
df_p_weight = pd.DataFrame(weight_list)
df_p_weight.to_csv('weight_graph.csv')
