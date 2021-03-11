import sys
import numpy as np

class FSProblem:
    def __init__(self, lines):
        self.name = lines[0].rstrip()
        self.jobs_count, self.machines_count = (int(val) for val in lines[1].split())
        self.jobs = []
        for job in lines[2:2+self.jobs_count]:
            machines_times = [int(val) for val in job.split()]
            self.jobs.append(machines_times)


    def __str__(self):
        text =  '{0} {1}\n'.format("dataset", self.name)
        text += '{0:<8} {1}\n'.format("jobs", "machines times")
        text += '-----------------------\n'
        for i, job in enumerate(self.jobs):
            text += '{0:<8} {1}\n'.format(i, job)
        return text


class Operation:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

class Gantt_time:
    def __init__(self, tab, order):
        self.tab = tab
        self.tab_in_order = []
        self.tab_of_operations = []
        for i in range(len(order)):
            self.tab_in_order.append(tab[order[i]])
        print(self.tab_in_order)



def get_file_content():
    try:
        with open(sys.argv[1]) as f:
            return f.readlines()
    except IOError:
        print("There is no such file.")
        exit()


def main():
    lines = get_file_content()
    fs_problem = FSProblem(lines)
    print(fs_problem)

    print(fs_problem.jobs)
    order = [0, 1, 2, 3]
    gantt = Gantt_time(fs_problem.jobs, order)
    gantttab = gantt.tab_in_order
    print(gantttab)

    no_of_machines = fs_problem.machines_count
    list_of_machines = []

    machine1 = np.zeros(shape=(len(order),2))
    begin, end = 0, 0
    op = Operation(begin, end)
    for i in range(len(order)):
        op.end += gantttab[i][0]
        machine1[i] = [op.begin, op.end]
        op.begin += gantttab[i][0]
    print(machine1)
    list_of_machines.append(machine1)

    for j in range(1, no_of_machines):
        machine = np.zeros(shape=(len(order), 2))
        if j == 1:
            begin, end = machine1[0][1], machine1[0][1] + gantttab[0][j]
        else:
            begin, end = list_of_machines[j-1][0][1], list_of_machines[j-1][0][1] + gantttab[0][j]
        op = Operation(begin, end)
        machine[0] = [op.begin, op.end]
        for i in range(1, len(order)):
            if machine[i-1][1] >= list_of_machines[j-1][i][1]:
                op.begin = machine[i-1][1]
            else:
                op.begin = list_of_machines[j-1][i][1]
            op.end = op.begin + gantttab[i][j]

            machine[i] = [op.begin, op.end]

        print(machine)
        list_of_machines.append(machine)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No filename specified.")
    else:
        main()
