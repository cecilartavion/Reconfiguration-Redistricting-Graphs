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
    graph created is an n by n grid.

    Arguments:
    ----------
    n: int instance
        the dimensions of the n by n grid. There are n**2 vertices.

    RETURNS:
    ----------
    G: networkx graph instance
        graph of the n by n grid.
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
        if(my_row>0):
            G.add_edge(i,north)
        if(my_row<(n-1)):
            G.add_edge(i,south)
        if(my_column>0):
            G.add_edge(i,west)
        if(my_column<(n-1)):
            G.add_edge(i,east)
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
    for i in range(n**2):
        my_column=i%n
        districting[i]=my_column
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
            r2=random.randint(0,1)
            edge=all_edges[r]
            r_a=edge[0]
            r_b=edge[1]
            if(districting[r_a]!=districting[r_b]):
                conflicted_edge_not_found=False
        if r2==0:
            proposed_districting[r_a]=districting[r_b]
        else:
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
            if(len(district)<n-1 or len(district)>n+1):
                proposed_plan_valid=False
        if(proposed_plan_valid):
            # When we are near the end of this for loop, plot the last few
            # districtings for examination purposes.
            if(k>num_proposals-5):
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
        for k in range(num_plans):
            for i in range(n**2):
                my_party=party_assignment[i]
                my_district=districtings[k][i]
                party_counts[k,my_district]+=my_party
            for j in range(n):
                if party_counts[k,j]>n/2: #if n=10, ties go to the yellow, (make an example with n=9 or 11?)
                    num_yellow_seats[k]+=1
#        Print the number of districtings that we found that worked.
        print(len(num_yellow_seats))
#        plt.ylim(ymin=0, ymax =3)
        bins = np.arange(0,5,0.5)-.175
        width=0.7*(bins[1]-bins[0])
        plt.ylabel('Frequency')
        plt.xlabel('Number of districts (out of 10) for Yellow party')
#        plt.yticks(range(0,3))
        plt.hist(num_yellow_seats,bins=bins,width=width) # the histogram it makes is ugly, but you get the idea
##        If we want to print the histogram, run the following line of code.
#        plt.savefig('redistricting_graph_hist1.png', format='png', dpi=1000)
        plt.show()