import time
import itertools
import argparse
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import math

class FSProblem:
    def __init__(self, lines):
      #  self.name = lines[0].rstrip()
        self.jobs_count, self.machines_count = (int(val) for val in lines[0].split())
        self.jobs = []
        self.neh_correct_order = []
        for job in lines[1:1 + self.jobs_count]:
            machines_times = [int(val) for val in job.split()]
            self.jobs.append(machines_times)
        if len(lines) > 1 + self.jobs_count and lines[1 + self.jobs_count + 1].rstrip() == "neh:":
            self.neh_correct_c_max = int(lines[1 + self.jobs_count + 2])
            for order_line in lines[1 + self.jobs_count + 3:]:
                self.neh_correct_order += [int(val) for val in order_line.split()]

    def __str__(self):
   #     text = '{0} {1}\n'.format("dataset", self.name)
        text = '{0:<8} {1}\n'.format("jobs", "machines times")
        text += '- - - - - - - - - - - -\n'
        for i, job in enumerate(self.jobs):
            text += '{0:<8} {1}\n'.format(i, job)
        return text

    def get_endings_matrix(self, order):
        jobs_in_order = []
        for i in range(len(order)):
            jobs_in_order.append(self.jobs[order[i]])
        matrix = np.zeros(shape=(len(jobs_in_order)+1, self.machines_count+1))
        for i, val in enumerate(matrix):
            if i == 0:
                continue
            else:
                for j, val in enumerate(val):
                    if j == 0:
                        continue
                    else:
                        matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1]) + jobs_in_order[i-1][j-1]
        return matrix

    def get_critical_path(self, endings_matrix, order):
        jobs_in_order = []
        for i in range(len(order)):
            jobs_in_order.append(self.jobs[order[i]])
        print(jobs_in_order)
        i, j = endings_matrix.shape[0]-1 , endings_matrix.shape[1]-1
        critical_path = []
        critical_path.insert(0, (i-1, j-1, jobs_in_order[i-1][j-1]))
        while i != 1 or j != 1:
            if endings_matrix[i][j-1] > endings_matrix[i-1][j]:
                critical_path.insert(0, (i-1, j-1-1, jobs_in_order[i-1][j-1-1]))
                j -= 1
            else:
                critical_path.insert(0, (i-1-1, j-1, jobs_in_order[i-1-1][j-1]))
                i -= 1
        return critical_path

    def get_machines_schedule(self, order):
        jobs_in_order = []
        for i in range(len(order)):
            jobs_in_order.append(self.jobs[order[i]])

        list_of_machines = []
        machine1 = np.zeros(shape=(len(order), 2))
        begin, end = 0, 0
        op = Operation(begin, end)
        for i in range(len(order)):
            op.end += jobs_in_order[i][0]
            machine1[i] = [op.begin, op.end]
            op.begin += jobs_in_order[i][0]
        list_of_machines.append(machine1)

        for j in range(1, self.machines_count):
            machine = np.zeros(shape=(len(order), 2))
            if j == 1:
                begin, end = machine1[0][1], machine1[0][1] + jobs_in_order[0][j]
            else:
                begin, end = list_of_machines[j - 1][0][1], list_of_machines[j - 1][0][1] + jobs_in_order[0][j]
            op = Operation(begin, end)
            machine[0] = [op.begin, op.end]
            for i in range(1, len(order)):
                if machine[i - 1][1] >= list_of_machines[j - 1][i][1]:
                    op.begin = machine[i - 1][1]
                else:
                    op.begin = list_of_machines[j - 1][i][1]
                op.end = op.begin + jobs_in_order[i][j]
                machine[i] = [op.begin, op.end]
            list_of_machines.append(machine)

        return list_of_machines

    def bruteforce(self, workers):
        # permutation
        permu = list(itertools.permutations(list(range(self.jobs_count))))
        with mp.Pool(workers) as pool:
            results = np.array(pool.map(self.bruteforce_worker, permu))
        optimal_order = permu[np.argmin(results)]
        return list(optimal_order)

    def bruteforce_worker(self, order):
        machines_schedule = self.get_machines_schedule(order)
        return machines_schedule[-1][-1][-1]  # last machine, last row, endtime

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

    def display_gantt_chart(self, machines_schedule, order):
        rect_height = 5
        max_y_position = len(machines_schedule) * (2 * rect_height) - rect_height
        fig, ax = plt.subplots()
        ax.set_ylim(0, max_y_position + 2 * rect_height)
        ax.set_xlim(0, machines_schedule[-1][-1][-1])
        ax.set_xlabel('Time units')
        ax.set_yticks(np.linspace(rect_height, max_y_position, num=len(machines_schedule)))
        ax.set_yticklabels(["Machine " + str(i) for i in range(len(machines_schedule), 0, -1)])
        ax.grid(True)
        facecolors = ['tomato', 'skyblue', 'lightgreen', 'orange', 'crimson', 'tan', 'plum', 'cornflowerblue']

        # convert from [begin, end] to [begin, duration]
        for i, machine in enumerate(machines_schedule):
            for operation in machine:
                operation[1] = operation[1] - operation[0]

        for i, machine in enumerate(machines_schedule):
            rect_position_y = max_y_position - (i * 10)
            ax.broken_barh(machine, (rect_position_y, rect_height), facecolors=facecolors)
            for i, operation in enumerate(machine):
                ax.text(x=operation[0] + operation[1] / 2,
                        y=rect_position_y + rect_height / 2,
                        s="J" + str(order[i]),
                        ha='center',
                        va='center',
                        color='black')
        plt.show()
    
    def check_answer(self, algo_type, order, c_max):
        if algo_type == "neh":
            if self.neh_correct_c_max == int(c_max):
                print("Correct NEH c_max.")
            else:
                print("Incorrect NEH c_max. Correct:", self.neh_correct_c_max)

            for i in range(len(order)):
                if not self.neh_correct_order[i] == order[i]+1:
                    print("Incorrect NEH order. Correct:", self.neh_correct_order, end="\n\n")
                    return
            print("Correct NEH order.", end="\n\n")


class Operation:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end


class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self, verbose=False):
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = 0
        if verbose:
            print(f"Elapsed time: {elapsed_time:0.6f} seconds")
        return elapsed_time


def get_file_content(filepath):
    try:
        with open(filepath) as f:
            return f.readlines()
    except IOError:
        print(f"There is no file named {filepath} .")
        exit()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepaths', metavar='filepaths', nargs='+', help='list of data filepaths to be processed')
    parser.add_argument('--brutal', nargs='?', const=True, default=False, help='number of processes utilized for bruteforce method')
    parser.add_argument('--workers', type=int, default=1, help='number of processes utilized for bruteforce method')
    return parser.parse_args()


def neh(fs_problem, mod=None):

    # get total time of jobs on all machines
    jobs_time_sum = [0]*fs_problem.jobs_count
    for i in range(fs_problem.jobs_count):
        for j in range(fs_problem.machines_count):
            jobs_time_sum[i] += fs_problem.jobs[i][j]

    # get order of jobs to insert
    job_order = len(jobs_time_sum) - 1 - np.argsort(jobs_time_sum[::-1], kind='stable')[::-1]
    list_of_elements = [job_order[0]]

    # main loop, i iterates over elements to insert
    for i in range(0, len(job_order)):
        cmax = math.inf
        looked_x = -1

        # x iterates over possible places to insert
        for x in range(0, len(list_of_elements)+1):
            # inside loop all operations on a copy
            list_copy = list_of_elements.copy()
            # skip first time
            if i > 0:
                list_copy.insert(x, job_order[i])

            # create new FSProblem, in format same as loaded from file
            foo_lines = []
            foo_lines.append([len(list_copy), fs_problem.machines_count])
            foo_lines[0] = " ".join(str(r) for r in foo_lines[0])
            for b in range(0, len(list_copy)):
                foo_lines.append([])
                for a in range(fs_problem.machines_count):
                    foo_lines[b+1].append(fs_problem.jobs[list_copy[b]][a])
                foo_lines[b+1] = " ".join(str(f) for f in foo_lines[b+1])
            flowshop = FSProblem(foo_lines)

            # get cmax of this instance
            schdl=[]
            for s in range(len(list_copy)):
                schdl.append(s)
            schedule = flowshop.get_machines_schedule(schdl)
            local_cmax = schedule[-1][-1][-1]

            if mod == 1:
                # tutaj chyba implenentacja kroku 5. by poszla dla reguły 1
                pass 

            # if it is better, remember
            if local_cmax < cmax:
                cmax = local_cmax
                looked_x = x

        # insert element in a place where cmax best best
        if i > 0:
            list_of_elements.insert(looked_x, job_order[i])

    return list_of_elements, cmax


def main():
    args = parse_arguments()
    t = Timer()
    for path in args.filepaths:
        fs_problem = FSProblem(get_file_content(path))
        print(fs_problem)
        m = fs_problem.get_endings_matrix([0,3,2,1])
        print(fs_problem.get_critical_path(m, [0,3,2,1]))


        if args.brutal:
            t.start()
            optimal_order = fs_problem.bruteforce(args.workers)
            optimal_exec_time = t.stop()
            optimal_schedule = fs_problem.get_machines_schedule(optimal_order)
            optimal_c_max = optimal_schedule[-1][-1][-1]

        t.start()
        johnson_order = fs_problem.johnson()
        johnson_exec_time = t.stop()
        johnson_schedule = fs_problem.get_machines_schedule(johnson_order)
        johnson_c_max = johnson_schedule[-1][-1][-1]

        t.start()
        neh_order, neh_c_max = neh(fs_problem)
        neh_exec_time = t.stop()
        neh_schedule = fs_problem.get_machines_schedule(neh_order)
        fs_problem.check_answer("neh", neh_order, neh_c_max)

        # t.start()
        # neh_mod1_order, neh_mod1_c_max = neh(fs_problem, mod=1)
        # neh_mod1_exec_time = t.stop()
        # neh_mod1_schedule = fs_problem.get_machines_schedule(neh_mod1_order)
        # fs_problem.check_answer("neh", neh_mod1_order, neh_mod1_c_max)

        print('{0:<20}{1:<10}{2:<14}{3}'.format("algorithm/data", "c_max", "exec time", "order"))
        print(*['-'] * 50)
        if args.brutal:
            print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Bruteforce", optimal_c_max, optimal_exec_time, optimal_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Johnson", johnson_c_max, johnson_exec_time, johnson_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH", neh_c_max, neh_exec_time, neh_order))
        # print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 1", neh_mod1_c_max, neh_mod1_exec_time, neh_mod1_order))


        # fs_problem.display_gantt_chart(optimal_schedule, optimal_order)
        # fs_problem.display_gantt_chart(johnson_schedule, johnson_order)
        # fs_problem.display_gantt_chart(neh_schedule, neh_order)



if __name__ == "__main__":
    main()
