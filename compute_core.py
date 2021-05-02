import numpy as np
from compute_sv import get_all_subsets
from scipy.optimize import minimize

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

# What we are trying to minimize. The sum of the players
# Takes in: value function of a game fun, possible payout vector x [1,5,8,6,...]
# Returns sum of all payoffs to players 
def objective(x):
    return np.sum(x)

# Creates all the linear constraints for optimization
# Takes in: value function of a game fun, number of players n
# Returns: List of constraints 
def create_constraints(fun, n):
    # All the constraints
    cons = []

    # Get all subsets
    all_subsets = []
    for i in range(n+1):
        all_subsets_i = get_all_subsets(list(range(n)), i)
        for j in all_subsets_i:
            all_subsets.append(j)
    
    # For every subset
    for S in all_subsets:
        
        # Create constraint of form sum(payoff to players in set) - v(players in set) >= 0
        def constraint(x,S=S):
            player_sum = 0
            for i in S:
                player_sum += x[i]

            return player_sum - fun(S)
            
        con = {'type': 'ineq', 'fun': constraint}
        cons.append(con)

    return cons

# Takes in: value function of a game fun, and number of players n, optimization method opt (default is SLSQP)
# Returns: tuple of form (core exists, payoffs)
def compute_core_general(fun, n, opt='SLSQP'):
    # All the constraints
    cons = create_constraints(fun, n)

    # All the bounds
    b = (0,None)
    bounds = (b,)*n

    # Initial guess
    all_players = []
    for i in range(n):
        all_players.append(i)

    x0 = np.array([fun(all_players)/n]*n)
    
    sol = minimize(objective, x0, method=opt, bounds=bounds, constraints=cons)
    
    core_exists = False
    if round(sol.fun) <= fun(all_players):
        core_exists = True

    return (core_exists, sol.x)