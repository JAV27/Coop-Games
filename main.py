# Question: Can't we just compute W? Am I correct as to what it represents
# What exactly is J? Why does it go  to n-1?
import numpy as np
from wvg import wvg

# Generates the dynamic programming table required in order to 
# compute the Shapley value in weighted voting games.

# The returned table is of dimensions n-1 x w(N) x n-1
# where the X[j][w][s] entry has the number of sets of size s 
# contained in {0,...,j} and whose weight is w.

# n: Int - Number of players 
# weights: [Int] - Weights associated with each player
# W: Int - w(N)
def create_DP_table(n, weights,W):

    # Create table with all zeroes
    table = np.zeros((n-1,W+1,n))

    for j in range(n-1):
        table[j][0][0] = 1

    table[0][weights[0]][1] = 1

    for j in range(1, n-1):
        for w in range(W+1):
            for s in range(1,n):
                if (w >= weights[j]):
                    table[j][w][s] = table[j-1][w][s] + table[j-1][w-weights[j]][s-1]
                else:
                    table[j][w][s] = table[j-1][w][s]

    return table

# What exactly is this doing? I got the jist but want to be more clear so I can document
def get_num_of_permutations_last(wvg):
    W = 0

    for i in range(wvg.get_num_players()):
        W += wvg.get_weights[i]

    table = create_DP_table(wvg.get_num_players(), wvg.get_weights(), W)

    num_of_permutations = []

    for w in range(W+1):
        num_of_permutations[w] = 0

        for s in range(wvg.get_num_players()):
            num_of_permutations[w] += table[wvg.get_num_players()-2][w][s]*np.math.factorial(s)*np.math.factorial(wvg.get_num_players()-s-1)
    
    # Why is there a big for loop? do I need it?
    del table

    return num_of_permutations