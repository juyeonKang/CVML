#!/usr/bin/python3

import sys
import random
import networkx as nx

if len(sys.argv)==4:
	dim = int(sys.argv[1])
	node = int(sys.argv[2])
	edge = int(sys.argv[3])
else:
	dim = 2
	node = int(sys.argv[1])
	edge = int(sys.argv[2])

G = nx.gnm_random_graph(node,edge)

for (u,v,w) in G.edges(data=True):
	w['len'] = random.randint(50,300)
	w['risk'] = random.randint(0,20)
	w['f'] = 0
	if dim == 3:
		w['new'] = random.randint(20,100)

filename = str(dim)+"D_Graph_"+str(node)+"_"+str(edge)+".gpickle"
nx.write_gpickle(G,filename)
