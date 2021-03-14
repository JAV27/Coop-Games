import computesv
from wvg import wvg
import time

test_arr = [1,2,3,4,5]
for i in range(6,30):
    test_arr.append(i)
    test_wvg = wvg(test_arr, 10+i)

    start = time.time()
    computesv.compute_shapley_value(test_wvg, 3)
    end = time.time()
    print("DP Solution Time with " +  str(i) + " players: " + str(end-start))

    start = time.time()
    computesv.brute_force_sv(test_wvg.v, 3, test_wvg.get_num_players())
    end = time.time()
    print("BF Solution Time with " +  str(i) + " players: " + str(end-start))

    print("\n")
    





