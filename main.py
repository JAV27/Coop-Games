import compute_sv
import compute_core
from wvg import wvg
from ttg import ttg
import numpy as np

test_ttg = ttg([1,2,3,4,5], [(10,1)])
test_wvg = wvg([1,2,3,4,5], 10)
sv = compute_sv.brute_force_sv(test_ttg.v, 2, 5)
sv2 = compute_sv.brute_force_sv(test_wvg.v, 2, 5)
print(sv)
print(sv2)

# Example from textbook. Example 2.2
ttg = ttg([3,4,5], [(7,500), (9,750), (11,1000)])
sol = compute_core.compute_core_general(ttg.v, ttg.get_num_players())
print(sol)