from more_itertools import set_partitions 
from wvg import wvg
from ttg import ttg

def find_best_initial_coalition_struct(n, fun):
    players = list(range(n))
    second_two_levels = list(set_partitions(players, 2))
    second_two_levels.append([players])
    max_val = 0
    max_coalition = []

    for partition in second_two_levels:
        partition_val = 0
        for player_set in partition:
            partition_val += fun(player_set)
        

        if partition_val > max_val:
            max_val = partition_val
            max_coalition = partition

    return (max_val, max_coalition)


test_ttg = ttg([3,4,5], [(7,500), (9,750), (11,1000)])

ans = find_best_initial_coalition_struct(test_ttg.get_num_players(), test_ttg.v)
print(ans)