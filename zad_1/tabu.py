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

def tabu(self, init=None, generate=None, stop=None, neighbourhood_size=5, tabu_list_size=10):

    # determine initialization 
    if init == 'neh':
        best_order, best_cmax = self.neh()
    elif init == 'random':
        best_order = random.sample(range(self.jobs_count), self.jobs_count)
        best_cmax = self.get_machines_schedule(best_order)[-1][-1][-1]
    elif isinstance(init, list):
        best_order = init
        best_cmax = self.get_machines_schedule(best_order)[-1][-1][-1]
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
    
    while iterations < max_iterations and time.time() - start_time < duration:
        if generate == 'swap':
            # candidates = swap(order, neighbourhood_size)
            pass
        elif generate == 'insert':
            # candidates = insert(order, neighbourhood_size)
            pass
        elif generate == 'inverse':
            # candidates = inverse(order, neighbourhood_size)
            pass
        
        # temporary candidates, nedd to implement above ^^^
        dummy_candidates = [[0,1,2,3], [1,2,3,0], [0,2,3,1]]
        cmax_of_candidates = [ val[-1][-1][-1] for val in list(map(self.get_machines_schedule, dummy_candidates))]

        # choose best candidate that is not in tabu list
        for i in range(len(dummy_candidates)):
            index = np.argmin(cmax_of_candidates)
            best_candidate = dummy_candidates[index]
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