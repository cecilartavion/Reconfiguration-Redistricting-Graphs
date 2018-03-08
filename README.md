# Reconfiguration Redistricting Graphs

The programs in this folder are those used for visualizing the various projects I am working on related to redistricting and gerrymandering.

## graves-original-altered.py

Code was originally by Christine Graves, a graduate student from Princeton. This code has been modified to produce histograms for the number of seats that the Yellow party would win given a random walk through the state space. The graph used is always a 10 by 10 grid, though this may need to be generalized in the future.

There is an initial vote made by each vertex of the 10 by 10 grid (Cartesian product of two paths of length 10). 

A random walk is performed so that at each time step, a vertex is taken from one part and given to another part of the partition so that the the number of vertices in each partition is 9, 10, or 11, and the induced subgraph on each part is connected.

The program will print out some of the redistrictings in the middle of the program, the number of districtings that were allowed out of the 10,000 simulations made, and a histogram for the number of votes alloted to the Yellow party out of 10 possible seats. Note that ties go to the Yellow party. 
This can easily be switched so that Yellow only gets 1/2 a seat.

## no_diagonals_redistricting_10_by_10_colums.py

This code was also heavily based on code from Christine Graves but has been modified so that districts connected by diagonal squares do not count. The graph used is always a 10 by 10 grid, though this may need to be generalized in the future. 

There is an initial vote made by each vertex of the 10 by 10 grid (Cartesian product of two paths of length 10). The initial districting are just the columns. 

A random walk is performed so that at each time step, a vertex is taken from one part and given to another part of the partition so that the the number of vertices in each partition is 9, 10, or 11, and the induced subgraph on each part is connected.

The program will print out the last several redistrictings, the number of districtings that were allowed out of the 10,000 simulations made, and a histogram for the number of votes alloted to the Yellow party out of 10 possible seats. Note that ties go to the Yellow party. This can easily be switched so that Yellow only gets 1/2 a seat.

## 1d_hist_generator.py

This program will build all the possible ways to redistrict a one-dimensional map into 5 districts given an initial vote made by the various precincts. The output for this graph is a histogram with the number of seats won by the Yellow party. Note that 1/2 votes are given in the event of ties. 

## build_graphs.py

This program build the k-reconfiguration redistring graph RRG. That is, given a base graph G, each vertex of the k-RRG of G is represented by a subgraph of G with k components so that each component is an induced subgraph of G. Given two such subgraphs of G, say G_1 and G_2, we say there is an edge in the RRG of G between the vertices represented by G_1 and G_2 if there is an edge xy in G that joins two components C_1,C_2 in G_1 and simply deleting y from C_2 and adding y to C_1 and all the adjacencies between y and vertices in C_1 that appear in G forms G_2. 

## elections_2016GA_new_test.py

This program was created in collaboration with Andrew Penland. We created a web scraping tool that would grab all of the voting data for Georgia from https://results.enr.clarityelections.com/GA/.

All data will be exported into an xls format. This file is highly dependent on where it is placed in the file system as it is grabing information from another file. 
