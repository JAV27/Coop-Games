import numpy as np
from wvg import wvg
from itertools import combinations
import math

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

    if wvg.get_quota() == 0:
        return 1/wvg.get_num_players()

    # Instantiated DP table
    table = create_DP_table(wvg.get_weights())

    num_of_permutations = np.zeros((wvg.get_quota()), dtype=np.float128)

    # How many permutations where player is pivotal and weight of other players is w
    # For every weight from q-w_of_last_player to q-1
    for w in range(max(0,wvg.get_quota()-wvg.get_weights()[wvg.get_num_players()-1]), wvg.get_quota()):
        num_of_permutations[w] = 0

        # for every subset size
        for s in range(wvg.get_num_players()):
            # Look at table for 2nd to last player at all w and s
            # Multiply by amount of combinations of that group of players
            num_of_permutations[w] += float(table[wvg.get_num_players()-2][w][s])*float(np.math.factorial(s))*float(np.math.factorial(wvg.get_num_players()-s-1))
    
    del table

    return num_of_permutations

def get_num_of_permutation(wvg, i):

    if i >= wvg.get_num_players():
        raise IndexError("i is larger than number of players")

    a = wvg.get_weights()[i]
    weights = wvg.get_weights()

    # Swap the last player with the ith player
    weights[i] = weights[wvg.get_num_players()-1]
    weights[wvg.get_num_players()-1] = a

    wvg.set_weights(weights)

    # Compute with new player as last
    num_of_permutations = get_num_of_permutations_last(wvg)

    # Swap back to original 
    a = wvg.get_weights()[i]
    weights = wvg.get_weights()

    weights[i] = weights[wvg.get_num_players()-1]
    weights[wvg.get_num_players()-1] = a

    return num_of_permutations

def compute_shapley_value(wvg, i):
    return np.sum(get_num_of_permutation(wvg, i))/float(np.math.factorial(wvg.get_num_players()))

# arr: Set of items
# k: size of the subsets to take
# returns: Set of total sums for each subsets
def get_all_subset_weights(arr, k):
    all_subsets = np.array(list(combinations(arr, k)))
    all_weights = [np.sum(arr) for arr in all_subsets]
    
    return all_weights

# Computes the Shapley value of player i in wvg
def brute_force_sv(wvg, i):

    shapley_value = 0
    quota = wvg.get_quota()
    n = wvg.get_num_players()
    player_value = wvg.get_weights()[i]
    set_minus_i = wvg.get_weights()[:i] + wvg.get_weights()[i+1:]

    # All numbers of subsets from 0 to n-1. Player is anywhere from first to last
    for k in range(n):
        inside_value = 0
        # Every permutation of subset k
        all_sums = get_all_subset_weights(set_minus_i, k)

        for set_sum in all_sums:
            if(set_sum < quota and set_sum + player_value >= quota):
                inside_value += 1

        inside_value = round(inside_value / math.comb(n-1, k), 3)
        shapley_value += inside_value

    return (shapley_value/n)


total = 0
for i in range(25):
    total += compute_shapley_value(wvg([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25], 20), i)

print("Total: " + str(total))

total = 0
for i in range(20):
    total += brute_force_sv(wvg([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 30), i)

print("Total: " + str(round(total, 3)))