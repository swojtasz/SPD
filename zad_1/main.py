import sys
import time
import itertools
import argparse
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.shape_base import block


class FSProblem:
    def __init__(self, lines):
        self.name = lines[0].rstrip()
        self.jobs_count, self.machines_count = (int(val) for val in lines[1].split())
        self.jobs = []
        for job in lines[2:2 + self.jobs_count]:
            machines_times = [int(val) for val in job.split()]
            self.jobs.append(machines_times)

    def __str__(self):
        text = '{0} {1}\n'.format("dataset", self.name)
        text += '{0:<8} {1}\n'.format("jobs", "machines times")
        text += '-----------------------\n'
        for i, job in enumerate(self.jobs):
            text += '{0:<8} {1}\n'.format(i, job)
        return text

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
        c_max = np.min(results)
        optimal_order = permu[np.argmin(results)]
        print("Best time equals: ", c_max, "For order: ", optimal_order)
        return c_max, optimal_order

    def bruteforce_worker(self, order):
        machines_schedule = self.get_machines_schedule(order)
        return machines_schedule[-1][-1][-1]  # last machine, last row, endtime

    def jackson2(self):
        jobs = list(self.jobs)
        jackson2_order = [-1] * len(jobs)
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
                jackson2_order[back] = i_best
                back = back - 1
                jobs[i_best] = [10000, 10000]
            if j_best == 0:
                jackson2_order[front] = i_best
                front = front + 1
                jobs[i_best] = [10000, 10000]
        return jackson2_order

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


class Operation:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end


class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = 0
        print(f"Elapsed time: {elapsed_time:0.6f} seconds")


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
    parser.add_argument('--workers', type=int, default=1, help='number of processes utilized for bruteforce method')
    return parser.parse_args()

def main():
    args = parse_arguments()
    print(args)
    for path in args.filepaths:
        fs_problem = FSProblem(get_file_content(path))
        print(fs_problem)

        t = Timer()
        t.start()
        c_max, optimal_order = fs_problem.bruteforce(args.workers)
        t.stop()
        
        jackson_order = fs_problem.jackson2()
        print("Jackson order is: ", jackson_order)

        schedule = fs_problem.get_machines_schedule(optimal_order)
        fs_problem.display_gantt_chart(schedule, optimal_order)

if __name__ == "__main__":
    main()
