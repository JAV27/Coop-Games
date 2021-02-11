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
def create_DP_table(weights):

    # Number of players
    n = len(weights)

    # Get w(N)
    W = 0
    for i in range(len(weights)):
        W += weights[i]

    # Create table with all zeroes
    table = np.zeros((n-1,W+1,n), dtype=int)

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

# Computes raw shapley value
# Gets how many permutations the last player is pivotal in
def get_num_of_permutations_last(wvg):

    # Instantiated DP table
    table = create_DP_table(wvg.get_weights())

    num_of_permutations = []

    # How many permutations where player is pivotal and weight of other players is w
    # For every weight from q-w_of_last_player to q-1
    for w in range(wvg.get_quota()-wvg.get_weights[wvg.get_num_players()], wvg.get_quota()):
        num_of_permutations[w] = 0

        # for every subset size
        for s in range(wvg.get_num_players()):
            # Look at table for 2nd to last player at all w and s
            # Multiply by amount of combinations of that group of players
            num_of_permutations[w] += table[wvg.get_num_players()-2][w][s]*np.math.factorial(s)*np.math.factorial(wvg.get_num_players()-s-1)
    
    del table

    return num_of_permutations