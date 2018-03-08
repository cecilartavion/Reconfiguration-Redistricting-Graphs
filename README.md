# Reconfiguration Redistricting Graphs

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

## build_graphs.py

## elections_2016GA_new_test.py
