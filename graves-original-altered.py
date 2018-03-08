#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
10 by 10 toy example for Moon
Code is general enough to work for any n by n grid with n districts
of n members, but need to write a function similar to
'create_party_assignment_n_10()' to get the vote tallies.

Note: it might be a good idea to use 9 or 11 instead of 10 so there are no ties.

"""

import networkx as nx
import math
import numpy as np
import copy
import random
import matplotlib.pyplot as plt # only used for the histogram at the end

def create_graph_n_by_n(n):
    '''
    create_graph_n_by_n, creates the base graph from which we will creating a 
    subgraph by partitioning the vertex into k components so that the 
    induced subgraph on those vertices is connected. In particular, the base
    graph created is an n by n grid with diagonal edges, i.e. the strong 
    product between two paths of length n.

    Arguments:
    ----------
    n: int instance
        the dimensions of the n by n grid with diagonal edges. There are n**2 vertices.

    RETURNS:
    ----------
    G: networkx graph instance
        graph of the n by n grid with diagonal edges.
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
        northwest=i-n-1
        northeast=i-n+1
        southwest=i+n-1
        southeast=i+n+1
        if(my_row>0):
            G.add_edge(i,north)
        if(my_row<(n-1)):
            G.add_edge(i,south)
        if(my_column>0):
            G.add_edge(i,west)
        if(my_column<(n-1)):
            G.add_edge(i,east)
        if(my_row>0 and my_column>0):
            G.add_edge(i,northwest)
        if(my_row>0 and my_column<(n-1)):
            G.add_edge(i,northeast)
        if(my_row<(n-1) and my_column>0):
            G.add_edge(i,southwest)
        if(my_row<(n-1) and my_column<(n-1)):
            G.add_edge(i,southeast)
    return G
    
def create_initial_districting(n):
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
    districting=np.zeros(n**2,dtype=np.int)
    for i in [1,2,3,4,5,6,7,8,11,12]:
    	districting[i-1]=0
    for i in [9,10,20,29,30,36,37,38,39,40]:
        districting[i-1]=1
    for i in [13,14,15,16,17,18,19,26,27,28]:
        districting[i-1]=2
    for i in [21,22,23,24,25,31,32,33,34,35]:
        districting[i-1]=3
    for i in [41,42,51,52,61,62,71,72,81,82]:
        districting[i-1]=4
    for i in [43,44,45,46,47,48,49,59,53,54]:
        districting[i-1]=5
    for i in [50,60,69,70,79,80,89,90,99,100]:
        districting[i-1]=6
    for i in [55,63,64,65,73,74,75,83,84,85]:
        districting[i-1]=7
    for i in [56,57,58,66,67,68,77,78,88,98]:
        districting[i-1]=8
    for i in [76,86,87,91,92,93,94,95,96,97]:
        districting[i-1]=9
    return districting
    
def create_party_assignment_n_10():
    '''
    create_party_assignment_n_10, each vertex in the base graph represents
    a precinct in our map. Each vertex has voted for either the Yellow party (1)
    or the Green party (0). This function will build the vote for each vertex.

    Arguments:
    ----------
    
    RETURNS:
    ----------
    party_assignment: list instance
        This n**2 list represents the vote for each vertex in the n by n grid.
        In the future, this should be randomized with a fixed seed.
    '''
    party_assignment=np.zeros(n**2,dtype=np.int)
    yellow_list=[2,3,4,5,6,7,19,20,22,23,24,28,29,31,32,35,36,37,40,41,47,49,50,54,59,60,62,63,64,66,70,72,79,80,84,85,89,93,98,99]
    for i in range(len(yellow_list)):
        party_assignment[yellow_list[i]]=1
    return party_assignment


if __name__ == '__main__':
    num_proposals=10000 # number of proposal steps to try
    n=10 # length/width of grid
    G=create_graph_n_by_n(n)
    all_edges=list(G.edges())
    m=len(all_edges) # number of edges

    districtings=[] # array where each row is a districting plan
    districting=create_initial_districting(n) # gets an initial districting plan
    districtings.append(districting)
    
    for k in range(num_proposals):
        # 'districting' is the current districting plan
        proposed_districting=copy.deepcopy(districting)
        # propose a change to the current districting
        # What I am doing here is choosing a random edge until I find a
        # conflicted edge, then I swap the districts of the 2 nodes.
        conflicted_edge_not_found=True
        while(conflicted_edge_not_found):
            r=random.randint(0,m-1)
            edge=all_edges[r]
            r_a=edge[0]
            r_b=edge[1]
            if(districting[r_a]!=districting[r_b]):
                conflicted_edge_not_found=False
        proposed_districting[r_a]=districting[r_b]
        proposed_districting[r_b]=districting[r_a]          
        
        
        # What I am doing here is for each proposed districting plan, I make a
        # copy of the full adjacency graph G and I delete the conflicted edges.
        # Then I ask networkx to find the connected components of this new
        # graph, G2. If each of the connected components has n members, the
        # plan is valid, so then it is added to the array 'districtings', and
        # then my current 'districting' is overwritten by this valid 
        # 'proposed_districting'. Making a copy of G is extremely inefficient,
        # but easier than keeping track of which edges change whether they are
        # conflicted or not.
        G2=G.copy()
        G2_edges=list(G2.edges())
        for edge in G2_edges:
            a=edge[0]
            b=edge[1]
            if proposed_districting[a]!=proposed_districting[b]:
                G2.remove_edge(edge[0],edge[1])
        proposed_districts=list(nx.connected_components(G2))
        proposed_plan_valid=True
        # This will print the last 4 graphs representing the redistrictings.
        for district in proposed_districts:
            if(len(district)!=n):
                proposed_plan_valid=False
        if(proposed_plan_valid):
            # When we are in the middle this for loop, plot the 9 of the 
            # districtings for examination purposes.
            if(len(districtings)<1000 and len(districtings)>990):
                plt.figure(k)
                nx.draw(G2,pos=nx.spring_layout(G,dim=2,iterations=100),with_labels=True,node_size=10)
            districting=proposed_districting
            districtings.append(districting)
##    If we want to print the graphs we found, run the following line of code.
#    plt.savefig('redistricting_graph.svg', format='svg', dpi=1000)
    plt.show()
            
    if(n==10):
        num_plans=len(districtings)
        # party_counts gives the number of yellow nodes in each districting
        # for each plan in the ensemble 'districtings'
        party_counts=np.zeros((num_plans,n),dtype=np.int)
        party_assignment=create_party_assignment_n_10()
        num_yellow_seats=np.zeros(num_plans,dtype=np.int)
#        print(districtings)
        for k in range(num_plans):
            for i in range(n**2):
                my_party=party_assignment[i]
                my_district=districtings[k][i]
                party_counts[k,my_district]+=my_party
            for j in range(n):
                if party_counts[k,j]>n/2: #if n=10, ties go to the yellow, (make an example with n=9 or 11?)
                    num_yellow_seats[k]+=1
                    
        print(len(num_yellow_seats))
#        plt.ylim(ymin=0, ymax =3)
        bins = np.arange(0,5,0.5)-.175
        width=0.7*(bins[1]-bins[0])
        plt.ylabel('Frequency')
        plt.xlabel('Number of districts (out of 10) for Yellow party')
#        plt.yticks(range(0,3))
        plt.hist(num_yellow_seats,bins=bins,width=width) # the histogram it makes is ugly, but you get the idea
#        plt.savefig('redistricting_graph_hist1.png', format='png', dpi=1000)
        plt.show()