import math
import numpy as np

def neh(self, mod=None):
    # get total time of jobs on all machines
    jobs_time_sum = [0] * self.jobs_count
    for i in range(self.jobs_count):
        for j in range(self.machines_count):
            jobs_time_sum[i] += self.jobs[i][j]

    # get order of jobs to insert
    job_order = len(jobs_time_sum) - 1 - np.argsort(jobs_time_sum[::-1], kind='stable')[::-1]
    list_of_elements = [job_order[0]]

    # main loop, i iterates over elements to insert
    for i in range(0, len(job_order)):
        cmax = math.inf
        looked_x = -1

        # x iterates over possible places to insert
        for x in range(0, len(list_of_elements) + 1):
            # inside loop all operations on a copy
            list_copy = list_of_elements.copy()
            # skip first time
            if i > 0:
                list_copy.insert(x, job_order[i])

            # create new FSProblem, in format same as loaded from file
            flowshop = self.createFSProblem(list_copy)

            # get cmax of this instance
            schdl = []
            for s in range(len(list_copy)):
                schdl.append(s)
            schedule = flowshop.get_machines_schedule(schdl)
            local_cmax = schedule[-1][-1][-1]

            # if it is better, remember
            if local_cmax < cmax:
                cmax = local_cmax
                looked_x = x

        # insert element in a place where cmax best best
        if i > 0:
            list_of_elements.insert(looked_x, job_order[i])

        if i > 0:
            if mod in (1, 2, 3):
                cmax_mod = math.inf

                critical_path_mod = self.get_critical_path(self.get_endings_matrix(list_of_elements),
                                                                 list_of_elements)
                mod_time = 0

                critical_path = [list(ele) for ele in critical_path_mod]

                index = 0
                for cp in critical_path:
                    if index != cp[0]:
                        index += 1
                    cp[0] = list_of_elements[index]

                if mod == 1:
                    for paths in critical_path:
                        if mod_time < paths[2]:
                            mod_time = paths[2]
                            mod_job_number = paths[0]

                if mod == 2:
                    mod_jobs_in_cp = {}
                    for paths in critical_path:
                        check = mod_jobs_in_cp.get(paths[0], "Not")
                        if check == "Not":
                            mod_jobs_in_cp[paths[0]] = 0
                        else:
                            number = mod_jobs_in_cp[paths[0]]
                            mod_jobs_in_cp[paths[0]] = number + paths[2]
                    mod_job_number = max(mod_jobs_in_cp, key=mod_jobs_in_cp.get)

                if mod == 3:
                    mod_jobs_in_cp = {}
                    for paths in critical_path:
                        check = mod_jobs_in_cp.get(paths[0], "Not")
                        if check == "Not":
                            mod_jobs_in_cp[paths[0]] = 0
                        else:
                            number = mod_jobs_in_cp[paths[0]]
                            mod_jobs_in_cp[paths[0]] = number + 1
                    mod_job_number = max(mod_jobs_in_cp, key=mod_jobs_in_cp.get)
                poppedElement = -1

                if mod_job_number != list_of_elements[looked_x]:
                    for y in range(len(list_of_elements)):
                        if list_of_elements[y] == mod_job_number:
                            poppedElement = list_of_elements.pop(y)
                            break

                    # x iterates over possible places to insert
                    for x in range(0, len(list_of_elements) + 1):
                        list_copy_mod = list_of_elements.copy()
                        list_copy_mod.insert(x, poppedElement)

                        # create new FSProblem, in format same as loaded from file
                        flowshop = self.createFSProblem(list_copy_mod)

                        # get cmax of this instance
                        schdl = []
                        for s in range(len(list_copy_mod)):
                            schdl.append(s)
                        schedule = flowshop.get_machines_schedule(schdl)
                        local_cmax = schedule[-1][-1][-1]

                        # if it is better, remember
                        if local_cmax < cmax_mod:
                            cmax_mod = local_cmax
                            looked_x = x

                    # insert element in a place where cmax best best
                    if i > 0:
                        list_of_elements.insert(looked_x, poppedElement)

    return list_of_elements, cmax
