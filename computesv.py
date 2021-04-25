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

    # Get w(N)
    W = 0
    for i in range(len(wvg.get_weights())):
        W += wvg.get_weights()[i]

    if wvg.get_quota() == 0:
        return 1/wvg.get_num_players()
    elif  wvg.get_quota() > W:
        return 0

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

def get_total_marginal_value_last(ttg):
    # Get w(N)
    W = 0
    for i in range(len(ttg.get_weights())):
        W += ttg.get_weights()[i]
    
    # Instantiated DP table
    table = create_DP_table(ttg.get_weights())
    
    total_values = np.zeros((W), dtype=np.float128)

    # How many permutations where player is pivotal and weight of other players is w
    # For every weight from q-w_of_last_player to q-1
    for w in range(W):
        total_values[w] = 0

        # for every subset size
        for s in range(ttg.get_num_players()):
            # Look at table for 2nd to last player at all w and s
            # Multiply by amount of combinations of that group of players
            
            total_weight_without_i = w
            total_weight_with_i = w+ttg.get_weights()[ttg.get_num_players()-1]

            total_values[w] += (ttg.v_with_total_weight(total_weight_with_i)-ttg.v_with_total_weight(total_weight_without_i))*float(table[ttg.get_num_players()-2][w][s])*float(np.math.factorial(s))*float(np.math.factorial(ttg.get_num_players()-s-1))
    
    del table

    return total_values

def get_total_marginal_value(ttg, i):
    if i >= ttg.get_num_players():
        raise IndexError("i is larger than number of players")
    
    a = ttg.get_weights()[i]
    weights = ttg.get_weights()

    # Swap the last player with the ith player
    weights[i] = weights[ttg.get_num_players()-1]
    weights[ttg.get_num_players()-1] = a

    ttg.set_weights(weights)

    # Compute with new player as last
    total_values = get_total_marginal_value_last(ttg)

    # Swap back to original 
    a = ttg.get_weights()[i]
    weights = ttg.get_weights()

    weights[i] = weights[ttg.get_num_players()-1]
    weights[ttg.get_num_players()-1] = a

    return total_values

def compute_shapley_value(wvg, i):
    return np.sum(get_num_of_permutation(wvg, i))/float(np.math.factorial(wvg.get_num_players()))

def compute_shapley_value_ttg(ttg, i):
    return np.sum(get_total_marginal_value(ttg, i))/float(np.math.factorial(ttg.get_num_players()))

# arr: Set of items
# k: size of the subsets to take
# returns: Set of all subsets
def get_all_subsets(arr, k):
    all_subsets = np.array(list(combinations(arr, k)), dtype=int)
    
    return all_subsets

# Computes the Shapley value of player i in wvg
# Takes in
# fun: function that takes in set of players and returns value oof that coalitino
# i: player to compute (int)
# n: number of players in game (int)
def brute_force_sv(fun, i, n):

    shapley_value = 0
    set_minus_i = list(range(i)) + list(range(i+1,n))

    # All numbers of subse  ts from 0 to n-1. Player is anywhere from first to last
    for k in range(n):
        inside_value = 0
        # Every permutation of subset k
        all_subsets = get_all_subsets(set_minus_i, k)

        for indiv_set in all_subsets:
            inside_value += ( fun(np.append(indiv_set, [i])) - fun(indiv_set) )

        inside_value = round(inside_value / math.comb(n-1, k), 3)
        shapley_value += inside_value

    return (shapley_value/n)

def compute_shapley_value_induced_subgraph(matrix, i):
    #Make sure matrix is mxm
    m = 0 
    n = 0

    if type(matrix) is list:
        matrix = np.array(matrix)

    if len(matrix.shape) != 2:
        raise Exception("Matrix must have 2 dimensions")

    
    m = matrix.shape[0]
    n = matrix.shape[1]
    
    if m != n:
        raise Exception("Matrix must have same number of rows and cols")

    total = np.sum(matrix[i])

    return total/2

# Checks to see if player i is a veto player in wvg
def check_if_veto_player_wvg(wvg, i):
    
    n = wvg.get_num_players()

    if i >= n:
        raise Exception("I is too large")

    set_minus_i = list(range(i)) + list(range(i+1,n))
    print(set_minus_i)
    
    for k in range(n):
        all_subsets = get_all_subsets(set_minus_i, k)
        for sub in all_subsets:
            if wvg.v(sub) == 1:
                return False

    return True

# Takes in: A WVG
# Returns: Tuple that includes if the core exists [0] and who the veto players are [1]
def core_exists_wvg(wvg):
    n = wvg.get_num_players()
    exists = False
    veto_players = []
    
    for i in range(n):
        if check_if_veto_player_wvg(wvg, i):
            exists = True
            veto_players.append(i)

    return (exists, veto_players)

