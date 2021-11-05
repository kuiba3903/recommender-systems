#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/4 15:47
# @Author : Xiao Feng
# coding=utf-8
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import gmres
import numpy as np
from numpy import eye
def PersonalRank(G, alpha, root, max_depth):
    rank = {x: 0 for x in G.keys()}
    rank[root] = 1
    for k in range(1,max_depth+1):
        tmp = {x: 0 for x in G.keys()}
        # 取出节点i和他的出边尾节点集合ri
        for i, ri in G.items():
            # 取节点i的出边的尾节点j以及边E(i,j)的权重wij,边的权重都为1，归一化后就是1/len(ri)
            for j, wij in ri.items():
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))
        tmp[root] += (1 - alpha)
        rank = tmp
        if k%20==0:
            print(k)
            lst = sorted(rank.items(), key=lambda x: x[1], reverse=True)
            print(lst)
    for ele in lst:
        print("%s:%.3f, \t" % (ele[0], ele[1]))
    return rank

def matrix_PR(G,alpha,root,table_id):
    data = []
    row = []
    col = []
    for u,u_dict in G.items():
        for v,v_edge in u_dict.items():
            data.append(1/len(u_dict))
            row.append(table_id[u])
            col.append(table_id[v])
    # print(data)
    # 状态矩阵
    M = csc_matrix((data, (row, col)), shape=(len(table_id), len(table_id)))
    # print(M.toarray())
    r0 = [[0] for i in range(len(table_id))]
    r0[table_id[root]][0] = 1
    r0 = np.array(r0)
    # print(r0)
    r = gmres(eye(len(table_id)) - alpha * M.T, (1 - alpha) * r0)  # gmres(A,b),解决稀疏Ax=b的求解问题，
    for key,value in table_id.items():
        print(key,":",list(r[0])[value])
if __name__ == '__main__':
    G = {'A': {'a': 1, 'b': 1,'d':1},
         'B': {'a': 1, 'c': 1,},
         'C': {'b': 1, 'e': 1},
         'D':{'c':1,'d':1,'e':1},
         'a': {'A': 1, 'B': 1},
         'b': {'A': 1,'C':1},
         'c': { 'B': 1, 'D': 1},
         'd': {'A': 1, 'D': 1},
         'e':{'C':1,'D':1}}
    table_id = {'A':0,'B':1,'C':2,'D':3,'a':4,'b':5,'c':6,'d':7,'e':8}
    PersonalRank(G, 0.85, 'A', 100)
    print("______________________")
    # G = {'A': {'a': 1, 'c': 1},
    #      'B': {'a': 1, 'b': 1, 'c': 1, 'd': 1},
    #      'C': {'c': 1, 'd': 1},
    #      'a': {'A': 1, 'B': 1},
    #      'b': {'B': 1},
    #      'c': {'A': 1, 'B': 1, 'C': 1},
    #      'd': {'B': 1, 'C': 1}}
    # PersonalRank(G,0.85,'A',100)
    matrix_PR(G,0.85,'A',table_id)