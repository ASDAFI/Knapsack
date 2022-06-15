def getDensity(value : int, weight : int) -> float:
    return value / weight


def sortByDensity(item_count : int, values : list, weights : list) -> list:
    items : list = [(values[index], weights[index], index) for index in range(item_count)]
    
    items.sort(key=lambda x: getDensity(x[0], x[1]), reverse=True)

    values = []
    weights = []

    for item in items:
        values.append(item[0])
        weights.append(item[1])
    
    return values, weights

def DP(item_count : int, max_capacity : int, values : list, weights : list):
    dp = [[0] * (item_count + 1) for i in range(max_capacity + 1)]

    for i in range(max_capacity + 1):
        for j in range(item_count + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0

            elif(i >= weights[j - 1]):
                dp[i][j] = max(values[j - 1] + dp[i - weights[j - 1]][j - 1], dp[i][j - 1])
            else:
                dp[i][j] = dp[i][j - 1]
        
    return dp               


def doDP(item_count : int, max_capacity : int, values : list, weights : list) -> list:
    dp_table = DP(item_count, max_capacity, values, weights)

    taken : list = []
    i, j = max_capacity, item_count

    while j > 0:
        if dp_table[i][j] == dp_table[i][j-1]:
            taken.append(0)
        else:
            taken.append(1)
            i -= weights[j-1]
        j -= 1
    
    taken.reverse()
    return  dp_table[max_capacity][item_count], taken, 1
                
