import sys
import numpy as np
import matplotlib.pyplot as plt

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

    def get_machines_schedule(self, order):
        jobs_in_order = []
        for i in range(len(order)):
            jobs_in_order.append(self.jobs[order[i]])

        list_of_machines = []
        machine1 = np.zeros(shape=(len(order),2))
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
                begin, end = list_of_machines[j-1][0][1], list_of_machines[j-1][0][1] + jobs_in_order[0][j]
            op = Operation(begin, end)
            machine[0] = [op.begin, op.end]
            for i in range(1, len(order)):
                if machine[i-1][1] >= list_of_machines[j-1][i][1]:
                    op.begin = machine[i-1][1]
                else:
                    op.begin = list_of_machines[j-1][i][1]
                op.end = op.begin + jobs_in_order[i][j]
                machine[i] = [op.begin, op.end]
            list_of_machines.append(machine)
        
        return list_of_machines

    def display_gantt_chart(self, machines_schedule):
        rect_height = 5
        max_y_position = len(machines_schedule) * (2*rect_height) - rect_height
        fig, ax = plt.subplots()
        ax.set_ylim(0, max_y_position + 2*rect_height)
        ax.set_xlim(0, np.max(machines_schedule))
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
                ax.text(x=operation[0]+operation[1]/2,
                        y=rect_position_y+rect_height/2,
                        s="J"+str(i),
                        ha='center',
                        va='center',
                        color='black')
        plt.show()


class Operation:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        

def get_file_content():
    try:
        with open(sys.argv[1]) as f:
            return f.readlines()
    except IOError:
        print("There is no such file.")
        exit()

def main():
    fs_problem = FSProblem(get_file_content())
    print(fs_problem)

    order = list(range(fs_problem.jobs_count))
    machines_schedule = fs_problem.get_machines_schedule(order)
    fs_problem.display_gantt_chart(machines_schedule)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No filename specified.")
    else:
        main()
