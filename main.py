# Future thing to do: Test cases? Good way to test whats happening. Might need help coming up with test cases though
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
# TODO:
# Remove n and W
# Check if w-weights[j] < 0
# Create test case file
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
# Computes raw shapley value
# Gets how many permutations the last player is pivotal in
def get_num_of_permutations_last(wvg):
    W = 0

    # Computes w(N)
    for i in range(wvg.get_num_players()):
        W += wvg.get_weights[i]

    # Instantiated DP tablee
    table = create_DP_table(wvg.get_num_players(), wvg.get_weights(), W)

    num_of_permutations = []

    # How many permutations where player is pivotal and weight of other players is w
    for w in range(wvg.get_quote()-wvg.get_weights[wvg.get_num_players()], wvg.get_quota()):
        num_of_permutations[w] = 0

        # S is subsets of size s
        for s in range(wvg.get_num_players()):
            # Look at 2nd to last player and all sets of different sizes and weights
            num_of_permutations[w] += table[wvg.get_num_players()-2][w][s]*np.math.factorial(s)*np.math.factorial(wvg.get_num_players()-s-1)
    
    # Why is there a big for loop? do I need it?
    # Todo: check out del
    del table

    return num_of_permutations