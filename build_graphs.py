# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:35:32 2018

@author: jasplund
"""

import networkx as nx
import math
import numpy as np
import copy
import random
import matplotlib.pyplot as plt # only used for the histogram at the end
#from copy import deepcopy

def create_base_graph_n_by_n(n):
    '''
    create_initial_districting, build the initial districting by making each
    column of the n by n grid its own district.

    Arguments:
    ----------
    n: int instance
        the dimensions of the n by n grid. There are n**2 vertices in this 
        grid.

    RETURNS:
    ----------
    districting: list of lists instance
        Each sub-list represents the vertices in a district
    '''
    G=nx.Graph()
    for i in range(n**2):
        # compute index of my neighbor in each direction (north, northeast, etc.)
        # the nodes are indexed by row first (1st row is indices 0 through 9, 2nd row is indices 10 through 19, etc.)
        my_row=int(math.floor(i/n))
        my_column=i%n
        west=i-1
        east=i+1
        north=i-n
        south=i+n
#        northwest=i-n-1
#        northeast=i-n+1
#        southwest=i+n-1
#        southeast=i+n+1
        if(my_row>0):
            G.add_edge(i,north)
        if(my_row<(n-1)):
            G.add_edge(i,south)
        if(my_column>0):
            G.add_edge(i,west)
        if(my_column<(n-1)):
            G.add_edge(i,east)
    return G

def create_all_subgraphs_from_graph(G,k):
    '''
    create_all_subgraphs_from_graph, build all of the subgraphs that are formed
    by partitioning the vertex set of G into k parts where the induced subgraph 
    of each part is a connected graph. This part of the program is extremely
    computationally intensive. 

    Arguments:
    ----------
    G: networkx graph instance
        This is the base graph we are going to partition into k parts.
    k: int instance
        This is the number of parts in the partition of G.

    RETURNS:
    ----------
    induced_subgraphs_of_G: list of lists of tuples instance
        Each list in induced_subgraphs_of_G contains tuples that represent the 
        edges of an admissible subgraph of G which is a disconnected subgraph 
        of G with k components.
    '''
    temp_vertex_set = []
    induced_subgraphs_of_G = []    
    #create set of vertices we still have to add to rrg_graph
    vert_left = [item for item in nx.nodes(G)] 
    
    if not nx.is_connected(G):
        return print('Graph is not connected')

    temp_induced_sub_G1 = []
    temp_induced_sub_G2 = [[]]
    #While we have not gone through all of the vertices, continue building subgraphs.
    while len(vert_left)>0:
        temp_vert = vert_left[0]
        '''
        This while loop will perform the following task. For each incident 
        edge, take all of the subgraphs created so far and add the incident 
        edge to each subgraph as long as the number of connected components 
        is not less than k after adding the edge.
        '''
#        temp_induced_sub_G2 = [subg + [incident_edge] for incident_edge in G.subgraph(temp_vertex_set + [temp_vert]).edges(temp_vert) for subg in induced_subgraphs_of_G if nx.number_connected_components(nx.Graph(subg+incident_edge))<k+1]
        for incident_edge in G.subgraph(temp_vertex_set + [temp_vert]).edges(temp_vert):
            temp_induced_sub_G1 = temp_induced_sub_G2.copy()
            for subg in temp_induced_sub_G1:
                isolates_g1 = [val for val in G.nodes() if val not in (nx.Graph(subg + [incident_edge])).nodes()]
                temp_graph = nx.Graph(subg+[incident_edge])
                temp_graph.add_nodes_from(isolates_g1)
                # If the number of components is large enough still, 
                # continue to check if the number of components is exactly k.
                if nx.number_connected_components(temp_graph)> k-1:
                    temp_induced_sub_G2.append(subg + [incident_edge])
                    # If the number of components is actually k,
                    # add this subgraph to our list of subgraphs
                    if nx.number_connected_components(temp_graph)==k:
                        tmp_comps1 = list(nx.connected_components(temp_graph))
                        temp_set1 = [list((G.subgraph(list(tmp_comps1[num_comp]))).edges()) for num_comp in range(len(tmp_comps1)) if len(list((G.subgraph(list(tmp_comps1[num_comp]))).edges()))!= 0 ]
                        our_edge_set1 = [item for sublist in temp_set1 for item in sublist]
                        induced_subgraphs_of_G.append(our_edge_set1)
            if len(temp_induced_sub_G2)==0:
                temp_induced_sub_G2.append([incident_edge])
        vert_left.remove(temp_vert)
        temp_vertex_set.append(temp_vert)
    return induced_subgraphs_of_G
   
def create_rrg_from_graph(induced_subgraphs_of_G,G,k):
    '''
    create_rrg_from_graph, using all the induced_subgraphs_of_G, G, and the
    number of components k, build the reconfiguration redistricting graph.

    Arguments:
    ----------
    induced_subgraphs_of_G: list of lists of tuples instance
        This is the list of all the subgraphs of G with k components such that
        each component is an induced subgraph of G. The subgraph is given
        by listing all of the edges in the graph. 
    G: networkx graph instance
        This is the base graph we are going to partition into k parts.
    k: int instance
        This is the number of parts in the partition of G.

    RETURNS:
    ----------
    rrg_edge_set: list of tuples
        Each tuple represents an edge in the graph. 
    '''
    rrg_edge_set = []
    vi = 0
    for one_induced_subg_edges in induced_subgraphs_of_G:
        #Make graph representing one of the vertices in RRG
        G1=nx.Graph(one_induced_subg_edges)
        #Make set of all isolated vertices
        isolates_g1 = [set([val]) for val in G.nodes() if val not in G1.nodes()]
        if len(isolates_g1)>0:
            #make component list if there are isolated vertices
            comp_all_g1 = list(nx.connected_components(G1)) + isolates_g1
        else:
            comp_all_g1 = list(nx.connected_components(G1))
         
        vj = 0
        # Build the edge set of G
        for one_induced_subg_edges2 in induced_subgraphs_of_G:
            #check the two connected_components against each other to see if they differ by 1.
            if one_induced_subg_edges2 != one_induced_subg_edges:
                G2 = nx.Graph(one_induced_subg_edges2)
                isolates_g2 = [set([val]) for val in G.nodes() if val not in G2.nodes()]
                if len(isolates_g1)>0:
                    #make component list if there are isolated vertices
                    comp_all_g2 = list(nx.connected_components(G2)) + isolates_g2
                else:
                    comp_all_g2 = list(nx.connected_components(G2))
                xor_g1_g2 = xor_lofl(comp_all_g1,comp_all_g2)
                g1_comp = intersect_lofl(comp_all_g1,xor_g1_g2)
                g2_comp = intersect_lofl(comp_all_g2,xor_g1_g2)
                if (len(xor_g1_g2)==4) and (len(g1_comp)==2 and len(g2_comp)==2):
                    # Check if the two components differ in exactly one vertex.
                    if (len(set(g1_comp[0])^set(g2_comp[0]))==1) and len(set(g1_comp[1])^set(g2_comp[1]))==1:
                        # test if the difference between the two components is the same number
                        # and whether there is an edge there.
                        neighbors_of_x = set(G.neighbors(list(set(g1_comp[0])^set(g2_comp[0]))[0]))
                        if (set(g1_comp[0])^set(g2_comp[0])) == (set(g1_comp[1])^set(g2_comp[1])) and (len(neighbors_of_x & set(g1_comp[0]))>0) and (len(neighbors_of_x & set(g1_comp[1]))>0):
                            #put an edge in edge set of rrg
                            rrg_edge_set.append((vi,vj))
                    elif (len(set(g1_comp[0])^set(g2_comp[1]))==1) and len(set(g1_comp[1])^set(g2_comp[0]))==1:
                        # test if the difference between the two components is the same number
                        # and whether there is an edge there.
                        neighbors_of_x = set(G.neighbors(list(set(g1_comp[0])^set(g2_comp[1]))[0]))
                        if (set(g1_comp[0])^set(g2_comp[1])) == (set(g1_comp[1])^set(g2_comp[0])) and (len(neighbors_of_x & set(g1_comp[0]))>0) and (len(neighbors_of_x & set(g1_comp[1]))>0):
                            #put an edge in edge set of rrg
                            rrg_edge_set.append((vi,vj))
#                            print(comp_all_g1)
#                            print(comp_all_g2)
#                            print('')
            vj += 1
        vi += 1        
    return rrg_edge_set

# In[]:
    
#if __name__ == '__main__':
n=2 # length/width of grid
k = 2 #number of components in the graph.
G=create_base_graph_n_by_n(n)
#G = nx.complete_graph(5)

# Define the intersection between to lists.
def intersect(a, b):
    return list(set(a) & set(b))

#define the intersection between two lists of lists.
def intersect_lofl(a,b):
    temp_lst1 = set(tuple(x) for x in a)
    temp_lst2 = set(tuple(x) for x in b)
    temp_inter = temp_lst1 & temp_lst2
    return [list(x) for x in temp_inter]

# Define the xor between two lists of lists. 
def xor_lofl(a,b):
    temp_lst1 = set(tuple(x) for x in a)
    temp_lst2 = set(tuple(x) for x in b)
    temp_xor = temp_lst1 ^ temp_lst2
    return [list(x) for x in temp_xor]

# Create the list of all subgraphs of G of the required type.
indu_sub = create_all_subgraphs_from_graph(G,k)

# Build the reconfiguration redistricting graph from the the list of all 
# subgraphs of G of the required type.
G1 = nx.Graph(create_rrg_from_graph(indu_sub,G,k))
print('Number of vertices:',len(G1.nodes()))
print('Number of edges:',len(G1.edges()))


# In[]:

#Display the graph.
nx.draw(G1,pos=nx.spring_layout(G1,dim=2,iterations=100),
        with_labels=True,node_size=10)
plt.show()
# In[]:

## Display some parameters of the RRG.
#dmax=max(nx.degree(G1))
#print(dmax)
#print(indu_sub[0])
#print(indu_sub[44])