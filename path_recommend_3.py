#!/usr/bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import random
import pdb


###### G[i][i+1]['  '] -> G[Pu[i]][Pu[i+1]]['   ']
###### sum_rec(Pl, Pu, S) -> sum_rec(Pu, Pl, S)
def sum_rec(Pu, Pl,S, p1, p2):
    print('function called')
    print("now S is ",S)
    rPl = 0; lPl = 0; rPu = 0; lPu = 0
    for i in range(len(Pu)-1):
            rPu += G[Pu[i]][Pu[i+1]][p1]
            lPu += G[Pu[i]][Pu[i+1]][p2]
    for j in range(len(Pl)-1):
            rPl += G[Pl[j]][Pl[j+1]][p1]
            lPl += G[Pl[j]][Pl[j+1]][p2]
    if lPu == lPl : 
        if lPl not in S : 
            S = S+[Pl]
        return S
    pm = (rPu-rPl)/(lPu-lPl)
    print('rPu:',rPu,'lPu:', lPu,'rPl:', rPl, 'lPl:',lPl,'pm:', pm)
    for (u,v,w) in G.edges(data=True):
            w['f']=w[p1]-pm*w[p2]
    ### 여기에서 'f'값을 기준으로 Pi를 뽑을 건데,
    ### 그 Pi가 Pl보다는 위에 있고 Pu보다는 아래에 존재한다는 "확신"을 'f'값이 주지 못하는 상태
    ### G의 subG로 Pl,Pu가 만드는 사각형 안에 존재하는 P의 합(?)을 두고,
    ### 전달 인자로 S말고 subG를 줘야 할 듯..>?
    Pi = list(nx.dijkstra_path(G,s,t,weight='f'))
    print('Pi = ',Pi)
    if Pi not in S:
            #print("before insert Pi, S = ",S)
            S = S+[Pi]
            #print("after insert Pi, S = ",S)
            S = sum_rec(Pu, Pi,S,p1,p2)
            S = sum_rec(Pi, Pl,S,p1,p2)
    print('function return')
    return S



# 70 nodes, 280 edges random graph
G = nx.read_gpickle("Graph_80_300.gpickle")

# setting s_source node & t_target node
s = int(input("sorce:"))
t = int(input("target:")) 

# S_set of paths from s to t
S = []

# Pl_shortest "LEN" path from s to t
# Pu_shortest "RISK" path from s to t
# x-coordinate : len / y-coordinate : risk
# then, Pl pointed at "LOWER" position
# and PU pointed at "UPPER" position
##### Pl = len, Pu = risk -> Pl = risk, Pu = len
Pl_ = nx.dijkstra_path(G,s,t,weight='len') #shortest path
print("Pl_ = ",Pl_)
Pr_ = nx.dijkstra_path(G,s,t,weight='risk') #safest path
print("Pr_ = ",Pr_)
Pn_ = nx.dijkstra_path(G,s,t,weight='new') #best path according to 'new'
print("Pn_ = ",Pn_)

S += [Pl_]
if Pl_ != Pr_ : 
    S += [Pr_]
    S = sum_rec(Pl_, Pr_, S, 'risk', 'len')

if Pn_ != Pr_ : 
    if Pn_ not in S :
        S += [Pn_]
    S = sum_rec(Pn_, Pr_, S, 'risk', 'new')

if Pn_ != Pl_ : 
    if Pn_ not in S :
        S += [Pn_]
    S = sum_rec(Pl_, Pn_, S, 'len', 'new')


#pdb.set_trace()
print(len(S))
print("Final result S : ",S)
