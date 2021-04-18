import random
import time
import math
import numpy as np

'''###
init:
    - 'neh'
    - 'random'
    - order (as list of ints)
generate:
    - 'swap'
    - 'insert'
    - 'inverse'
stop:
    - ('timeout', seconds)
    - ('iter', number_of_iterations)
    - ('improvement', number_of_iterations)
###'''


def inverse(order, neighbourhood_size):
    candidates = []
    inverses = []
    # iterate over number of required neighbours
    for i in range(neighbourhood_size):
        # get copy of a given order
        neighbour = order.copy()
        left = random.randrange(0, len(neighbour))
        right = random.randrange(left, len(neighbour))
        while (right-left < 3) or ([left, right] in inverses):
            left = random.randrange(0, len(neighbour))
            right = random.randrange(left, len(neighbour))
        neighbour[left:right] = neighbour[left:right][::-1]
        inverses.append([left, right])
        candidates.append(neighbour)
    return candidates


def swap(order, neighbourhood_size):
    candidates = []
    swaps = []
    # iterate over number of required neighbours
    for i in range(neighbourhood_size):
        # get copy of a given order
        neighbour = order.copy()
        # pick to numbers to swap
        x1 = random.randrange(len(neighbour))
        x2 = random.randrange(len(neighbour))
        # neighbours need to be different
        while ([x1, x2] in swaps) or ([x2, x1] in swaps) or (x1 == x2):
            x1 = random.randrange(len(neighbour))
            x2 = random.randrange(len(neighbour))
        swaps.append([x1, x2])
        # swap two
        neighbour[x1], neighbour[x2] = neighbour[x2], neighbour[x1]
        candidates.append(neighbour)

    return candidates


def insert(order, neighbourhood_size):
    candidates = []
    inserts = []
    # iterate over number of required neighbours
    for i in range(neighbourhood_size):
        neighbour = order.copy()
        while neighbour == order:
            # get copy of a given order
            neighbour_may = order.copy()
            # pick place and element to insert
            xplace = random.randrange(len(neighbour_may))
            xinsert = random.randrange(len(neighbour_may))
            # neighbours need to be different
            while [xplace, xinsert] in inserts:
                xplace = random.randrange(len(neighbour_may))
                xinsert = random.randrange(len(neighbour_may))
            # pop and insert at index
            popped = neighbour_may.pop(xinsert)
            neighbour_may.insert(xplace, popped)
            neighbour = neighbour_may.copy()
            # if its different from a given order, proceed
            if neighbour != order:
                inserts.append([xplace, xinsert])
        candidates.append(neighbour)

    return candidates


def tabu(self, init=None, generate=None, stop=None, neighbourhood_size=5, tabu_list_size=10):

    # determine initialization 
    if init == 'neh':
        order, c_max = self.neh()
    elif init == 'random':
        order = random.sample(range(self.jobs_count), self.jobs_count)
        c_max = self.get_machines_schedule(order)[-1][-1][-1]
    elif isinstance(init, list):
        order = init
        c_max = self.get_machines_schedule(order)[-1][-1][-1]
    else:
        return

    # determine stop condition
    if stop:
        if stop[0] == 'timeout':
            start_time = time.time()
            duration = stop[1]
            # not used
            iterations = 0
            max_iterations = math.inf
        elif stop[0] == 'iter' or 'improvement':
            iterations = 0
            max_iterations = stop[1]
            # not used
            start_time = time.time()
            duration = math.inf
        else:
            return
    else:
        return

    tabu_list = [None] * tabu_list_size
    improved = False
    best_cmax = c_max
    best_order = order
    
    while iterations < max_iterations and time.time() - start_time < duration:
        if generate == 'swap':
            candidates = swap(order, neighbourhood_size)
        elif generate == 'insert':
            candidates = insert(order, neighbourhood_size)
        elif generate == 'inverse':
            candidates = inverse(order, neighbourhood_size)
        else:
            print("Tabu Search: Generate method not specified. Returning early.")
            return
        
        cmax_of_candidates = [ val[-1][-1][-1] for val in list(map(self.get_machines_schedule, candidates))]

        # choose best candidate that is not in tabu list
        for i in range(len(candidates)):
            index = np.argmin(cmax_of_candidates)
            best_candidate = candidates[index]
            if best_candidate in tabu_list:
                cmax_of_candidates.pop(index)
                continue
            else:
                order = best_candidate
                cmax = cmax_of_candidates[index]
                break
        
        # update tabu list
        tabu_list.pop(0)
        tabu_list.append(best_candidate)

        # update best stats
        if cmax < best_cmax:
            best_cmax = cmax
            best_order = order
            improved = True
        else:
            improved = False

        
        if stop[0] == 'improvement':
            if improved:
                iterations = 0
            else:
                iterations += 1
        else:
            iterations += 1

    return best_order, best_cmax