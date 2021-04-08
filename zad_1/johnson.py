def johnson(self):
    jobs = list(self.jobs)

    if self.machines_count > 2:
        i = 0
        mid = int(self.machines_count / 2)
        for job in jobs:
            machine_time1 = 0
            machine_time2 = 0
            machine1_it = 0
            machine2_it = mid

            while machine1_it <= mid:
                machine_time1 = machine_time1 + job[machine1_it]
                machine1_it += 1

            while machine2_it < self.machines_count:
                machine_time2 = machine_time2 + job[machine2_it]
                machine2_it += 1

            job = job[:2]
            job[0] = machine_time1
            job[1] = machine_time2
            jobs[i] = job
            i = i + 1

    johnson_order = [-1] * len(jobs)
    front = 0
    back = len(jobs) - 1
    for x in range(len(jobs)):
        lowest_value = 10000
        i_best = -1
        j_best = -1
        for i in range(len(jobs)):
            for j in range(len(jobs[i])):
                if jobs[i][j] < lowest_value:
                    lowest_value = jobs[i][j]
                    i_best = i
                    j_best = j
        if j_best == 1:
            johnson_order[back] = i_best
            back = back - 1
            jobs[i_best] = [10000, 10000]
        if j_best == 0:
            johnson_order[front] = i_best
            front = front + 1
            jobs[i_best] = [10000, 10000]
    return johnson_order
