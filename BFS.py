
import time


class Problem:
    def __init__(self, values, weights, items_count, capacity):
        self.values = values
        self.weights = weights
        self.items_count = items_count
        self.capacity = capacity
  

def getDensity(value : int, weight : int) -> float:
    return value / weight



def sortByDensity(item_count : int, values : list, weights : list) -> list:
    items : list = [(values[index], weights[index], index) for index in range(item_count)]
    
    items.sort(key=lambda x: getDensity(x[0], x[1]), reverse=True)

    values = []
    weights = []
    indexes = []

    for item in items:
        values.append(item[0])
        weights.append(item[1])
        indexes.append(item[2])
    
    return values, weights, indexes


class state:
    def __init__(self, j : int, value : int, capacity: int, optimal : int, taken : list, problem : Problem):
        self.j = j
        self.value = value
        self.capacity = capacity
        self.optimal = optimal
        self.taken = taken.copy()
        self.problem = problem

    def dontChoose(self):
        j = self.j + 1

        if j > self.problem.items_count:
            return None

        problem = self.problem
        taken = self.taken.copy() + [0]
        capacity = self.capacity
        optimal = self.optimal - problem.values[j - 1]
        value = self.value

        
        
        return state(j, value, capacity, optimal, taken, problem)
    
    def choose(self):
        j = self.j + 1
        
        if j > self.problem.items_count or self.capacity < self.problem.weights[j - 1]:
            return None

        problem = self.problem
        taken = self.taken.copy() + [1]
        capacity = self.capacity - problem.weights[j - 1]
        optimal = self.optimal
        value = self.value + problem.values[j - 1]

        if j > problem.items_count:
            return None
    
        return state(j, value, capacity, optimal, taken, problem)
    
    def get_childs(self):
        result = []
        result.append(self.dontChoose())
        result.append(self.choose())
        
        if(result[0] == None):
            result.pop(0)
        if(result[1] == None):
            result.pop(1)

        return result


class NotVisitedNodes:
    def __init__(self):
        self.open = []
        self.lenght = 0
    def insert(self, state : state):
        low = 0
        high = self.lenght - 1
        while low <= high:
            mid = (low + high) // 2
            if self.open[mid].optimal < state.optimal:
                low = mid + 1
            else:
                high = mid - 1

        self.open.insert(low, state)
        self.lenght += 1
    
    def pop(self) -> state:
        self.lenght -= 1
        return self.open.pop()

    
def makeEstimationBetter(result : state, capacity : int, problem : Problem):

    for i in range(result.j, problem.items_count):
        if(problem.weights[i] <= capacity):
            result.taken.append(1)
            result.value += problem.values[i]
            capacity -= problem.weights[i]
        else:
            result.taken.append(0)
    

        

def BFS(problem : Problem, time_limit : int):
    problem.values, problem.weights, indexes = sortByDensity(problem.items_count, problem.values, problem.weights)

    

    Open = NotVisitedNodes()
    Open.insert(state(0, 0, problem.capacity, sum(problem.values), [], problem))


    best_answer : state = None
    complete_answer : state = None

    is_deterministic = True
    start_time = time.time()
    while Open.lenght > 0:
        
        if(time.time() - start_time > time_limit and best_answer != None):
            if(complete_answer == None):
                complete_answer = best_answer
            is_deterministic = False
            break
        current = Open.pop()
        

        for child in current.get_childs():

            if child.j == problem.items_count:
                if best_answer == None or best_answer.value <= child.value:
                    best_answer = child
                    complete_answer = child
            elif best_answer != None and child.optimal <= best_answer.value:
                continue 
            elif child.capacity != 0:
                Open.insert(child)
                if best_answer == None or child.value >= best_answer.value:
                    best_answer = child
            
            elif child.capacity == 0:
                if best_answer == None or child.value >= best_answer.value:
                    best_answer = child
                    complete_answer = child
                
                needed = problem.items_count - child.j
                child.taken += [0] * needed
            
                
    
    if complete_answer == None:
        complete_answer = best_answer
    
    if not is_deterministic:
        makeEstimationBetter(complete_answer, complete_answer.capacity, problem)
    
    new_taken = [0] * problem.items_count
    for i in range(len(complete_answer.taken)):
        if complete_answer.taken[i] == 1:
            new_taken[indexes[i]] = 1

    complete_answer.taken = new_taken


    return is_deterministic, complete_answer


def DoBFS(item_count : int, values : list, weights : list, max_capacity : int, time_limit : int = 1):
    problem = Problem(values, weights, item_count, max_capacity)
    is_deterministic, result = BFS(problem, time_limit)

    value = result.value
    return value, result.taken, is_deterministic
        