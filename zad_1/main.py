from copy import deepcopy
import time
import argparse

from fs_problem import FSProblem
from rpq_problem import RPQProblem
import rpq_solver
import fs_solver


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
    parser.add_argument('--brutal', nargs='?', const=True, default=False,
                        help='number of processes utilized for bruteforce method')
    parser.add_argument('--workers', type=int, default=1, help='number of processes utilized for bruteforce method')
    return parser.parse_args()


def main():
    args = parse_arguments()
    t = Timer()
    for path in args.filepaths:

        if "in" in path:
            rpq_problem = RPQProblem(get_file_content(path))
            print("file:", path)
            print("=========== SCHRAGE ===========")

            t.start()
            cmax1, pi1 = rpq_problem.SchrageWithoutQueue()
            s1 = t.stop()
            t.start()
            cmax2, pi2 = rpq_problem.Schrage()
            s2 = t.stop()
            t.start()
            cmax3 = rpq_problem.SchragePMTNWithoutQueue()
            s3 = t.stop()
            t.start()
            cmax4 = rpq_problem.SchragePMTN()
            s4 = t.stop()

            print("CMAX", cmax1, s1)
            print("CMAX queue:", cmax2, s2)
            print("CMAX pmtn:", cmax3, s3)
            print("CMAX pmtn queue:", cmax4, s4)

            print("=========== CARLIER ===========")

            t.start()
            cmax = rpq_problem.CarlierWithoutQueue(deepcopy(rpq_problem.jobs))
            s1 = t.stop()

            t.start()
            cmax_q = rpq_problem.Carlier(deepcopy(rpq_problem.jobs))
            s2 = t.stop()

            print("CMAX Carlier:", cmax, s1)
            print("CMAX Carlier queue:", cmax_q, s2)

            print("============ TABU =============")

            t.start()
            order, cmax = rpq_problem.tabu(init='schrage',  generate='insert', stop=('timeout', 10))
            s1 = t.stop()
            print("CMAX tabu:", cmax, s1)

            print("=========== SOLVER ============")

            info, s = rpq_solver.solver(path)
            print(info, s)

        if "data_" in path:
            print("=========== SOLVER ============")

            fs_problem = FSProblem(get_file_content(path))
            info, s, order = fs_solver.solver(fs_problem)
            print(info, s)
            schdl = fs_problem.get_machines_schedule(order)
            fs_problem.display_gantt_chart(schdl, order)

if __name__ == "__main__":
    main()
