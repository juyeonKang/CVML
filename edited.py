#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import pdb


###### G[i][i+1]['  '] -> G[Pu[i]][Pu[i+1]]['   ']
###### sum_rec(Pl, Pu, S) -> sum_rec(Pu, Pl, S)
def sum_rec(Pu, Pl,S):
    print('function called')
    rPl = 0; lPl = 0; rPu = 0; lPu = 0
    for i in range(len(Pu)-1):
            rPu += G[Pu[i]][Pu[i+1]]['risk']
            lPu += G[Pu[i]][Pu[i+1]]['len']
    for j in range(len(Pl)-1):
            rPl += G[Pl[j]][Pl[j+1]]['risk']
            lPl += G[Pl[j]][Pl[j+1]]['len']
    if lPu == lPl : 
        if lPl not in S : 
            S = S+[Pl]
        return 
    pm = (rPu-rPl)/(lPu-lPl)
    print('rPu:',rPu,'lPu:', lPu,'rPl:', rPl, 'lPl:',lPl,'pm:', pm)
    for (u,v,w) in G.edges(data=True):
            w['f']=w['risk']-pm*w['len']
    ### 여기에서 'f'값을 기준으로 Pi를 뽑을 건데,
    ### 그 Pi가 Pl보다는 위에 있고 Pu보다는 아래에 존재한다는 "확신"을 'f'값이 주지 못하는 상태
    ### G의 subG로 Pl,Pu가 만드는 사각형 안에 존재하는 P의 합(?)을 두고,
    ### 전달 인자로 S말고 subG를 줘야 할 듯..>?
    Pi = list(nx.dijkstra_path(G,s,v,weight='f'))
    if Pi not in S:
            S = S+[Pi]
            sum_rec(Pu, Pi,S)
            sum_rec(Pi, Pl,S)
    print('function return')
    return



# 70 nodes, 280 edges random graph
G = nx.gnm_random_graph(10,40)

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
s = int(input())
t = int(input())

# S_set of paths from s to t
S = []

# Pl_shortest "LEN" path from s to t
# Pu_shortest "RISK" path from s to t
# x-coordinate : len / y-coordinate : risk
# then, Pl pointed at "LOWER" position
# and PU pointed at "UPPER" position
##### Pl = len, Pu = risk -> Pl = risk, Pu = len
Pl_ = list(nx.dijkstra_path(G,s,t,weight='len')) #shortest path
Pr_ = list(nx.dijkstra_path(G,s,t,weight='risk')) #safest path

S += [Pl_]
if Pl_ != Pr_ : 
    S += [Pr_]
    sum_rec(Pl_, Pr_, S)

#pdb.set_trace()

