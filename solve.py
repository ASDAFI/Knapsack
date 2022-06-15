import DP
import BFS

def solve(count_of_items : int, values : list, weights : list, max_capacity : int):
    if(count_of_items * max_capacity > 10**8):
            total_value, taken, is_deterministic = BFS.DoBFS(count_of_items , values , weights  , max_capacity, time_limit = 1)
    else:
        total_value, taken, is_deterministic = DP.doDP(count_of_items , max_capacity , values , weights )
    

    # total value is our maximized value
    # taken is a list of 1s and 0s indicating which items were taken
    # is_deterministic is a boolean indicating whether the algorithm was deterministic or not
    return total_value, taken, is_deterministic

