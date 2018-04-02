#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import pdb

# 70 nodes, 280 edges random graph
G = nx.gnm_random_graph(70,280)

# giving edges attributes 'len','risk' randomly
# and initialize edges' attribute 'f' as 0
for (u,v,w) in G.edges(data=True):
    w['len'] = random.randint(10,100)
    w['risk'] = random.randint(0,10)
    w['f'] = 0

# just showing graph
pos = nx.shell_layout(G)
nx.draw_networkx(G)
plt.show()

# setting s_source node & t_target node
s = 36
t = 51

# S_set of paths from s to t
S = []

# Pl_shortest "LEN" path from s to t
# Pu_shortest "RISK" path from s to t
# x-coordinate : len / y-coordinate : risk
# then, Pl pointed at "LOWER" position
# and PU pointed at "UPPER" position
Pl = list(nx.dijkstra_path(G,s,t,weight='len'))
Pu = list(nx.dijkstra_path(G,s,t,weight='risk'))

S += [Pl]
S += [Pu]

def sum_rec(Pl, Pu, S):
    print('function called')
    rPl = 0; lPl = 0; rPu = 0; lPu = 0
    for i in range(len(Pu)-1):
            rPu += G[i][i+1]['risk']
            lPu += G[i][i+1]['len']
    for j in range(len(Pl)-1):
            rPl += G[j][j+1]['risk']
            lPl += G[j][j+1]['len']
    pm = (rPu-rPl)/(lPu-lPl)
    for (u,v,w) in G.edges(data=True):
            w['f']=w['risk']-pm*w['len']
    Pi = list(nx.dijkstra_path(G,s,v,weight='f'))
    if Pi!=Pl and Pi!=Pu:
            S = S+[Pi]
            sum_rec(Pu, Pi, S)
            sum_rec(Pi, Pl, S)
    print('function return')

pdb.set_trace()
sum_rec(Pl, Pu, S)

