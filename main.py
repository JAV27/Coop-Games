import computesv
from wvg import wvg
from ttg import ttg

test_ttg = ttg([1,2,3,4,5], [(10,2), (10,1)])
test_wvg = wvg([1,2,3,4,5], 10)
sv = computesv.compute_shapley_value_ttg(test_ttg, 2)
sv2 = computesv.compute_shapley_value(test_wvg, 2)
print(sv)
print(sv2)