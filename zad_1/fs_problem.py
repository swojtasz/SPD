import numpy as np
import matplotlib.pyplot as plt
import itertools
import multiprocessing as mp


class Operation:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        

class FSProblem:
    from johnson import johnson
    from neh import neh
    from tabu import tabu
    
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
        matrix = np.zeros(shape=(len(jobs_in_order) + 1, self.machines_count + 1))
        for i, val in enumerate(matrix):
            if i == 0:
                continue
            else:
                for j, val in enumerate(val):
                    if j == 0:
                        continue
                    else:
                        matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1]) + jobs_in_order[i - 1][j - 1]
        return matrix

    def get_critical_path(self, endings_matrix, order):
        jobs_in_order = []
        for i in range(len(order)):
            jobs_in_order.append(self.jobs[order[i]])
        i, j = endings_matrix.shape[0] - 1, endings_matrix.shape[1] - 1
        critical_path = []
        critical_path.insert(0, (i - 1, j - 1, jobs_in_order[i - 1][j - 1]))
        while i != 1 or j != 1:
            if endings_matrix[i][j - 1] > endings_matrix[i - 1][j]:
                critical_path.insert(0, (i - 1, j - 1 - 1, jobs_in_order[i - 1][j - 1 - 1]))
                j -= 1
            else:
                critical_path.insert(0, (i - 1 - 1, j - 1, jobs_in_order[i - 1 - 1][j - 1]))
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
                if not self.neh_correct_order[i] == order[i] + 1:
                    print("Incorrect NEH order. Correct:", self.neh_correct_order, end="\n\n")
                    return
            print("Correct NEH order.", end="\n\n")

    def createFSProblem(self, order):
        foo_lines = []
        foo_lines.append([len(order), self.machines_count])
        foo_lines[0] = " ".join(str(r) for r in foo_lines[0])
        for b in range(0, len(order)):
            foo_lines.append([])
            for a in range(self.machines_count):
                foo_lines[b + 1].append(self.jobs[order[b]][a])
            foo_lines[b + 1] = " ".join(str(f) for f in foo_lines[b + 1])
        return FSProblem(foo_lines)
