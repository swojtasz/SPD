import time
import argparse
import random
from fs_problem import FSProblem
import neh
import tabu

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
        fs_problem = FSProblem(get_file_content(path))
        print(fs_problem)

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
        neh_order, neh_c_max = fs_problem.neh()
        neh_exec_time = t.stop()
        neh_schedule = fs_problem.get_machines_schedule(neh_order)
        fs_problem.check_answer("neh", neh_order, neh_c_max)

        t.start()
        neh_mod1_order, neh_mod1_c_max = fs_problem.neh(mod=1)
        neh_mod1_exec_time = t.stop()
        neh_mod1_schedule = fs_problem.get_machines_schedule(neh_mod1_order)

        t.start()
        neh_mod2_order, neh_mod2_c_max = fs_problem.neh(mod=2)
        neh_mod2_exec_time = t.stop()
        neh_mod3_schedule = fs_problem.get_machines_schedule(neh_mod2_order)

        t.start()
        neh_mod3_order, neh_mod3_c_max = fs_problem.neh(mod=3)
        neh_mod3_exec_time = t.stop()
        neh_mod3_schedule = fs_problem.get_machines_schedule(neh_mod3_order)

        t.start()
        # tabu_order, tabu_cmax = fs_problem.tabu(init=[1,2,3], stop=('timeout', 4))
        tabu_order, tabu_cmax = fs_problem.tabu(init='neh', stop=('iter', 50000))
        # tabu_order, tabu_cmax = fs_problem.tabu(init='random', stop=('improvement', 1000))
        tabu_exec_time = t.stop()
        tabu_schedule = fs_problem.get_machines_schedule(tabu_order)

        print('{0:<20}{1:<10}{2:<14}{3}'.format("algorithm/data", "c_max", "exec time", "order"))
        print(*['-'] * 50)
        if args.brutal:
            print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Bruteforce", optimal_c_max, optimal_exec_time, optimal_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Johnson", johnson_c_max, johnson_exec_time, johnson_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH", neh_c_max, neh_exec_time, neh_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 1", neh_mod1_c_max, neh_mod1_exec_time, neh_mod1_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 2", neh_mod2_c_max, neh_mod2_exec_time, neh_mod2_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 3", neh_mod3_c_max, neh_mod3_exec_time, neh_mod3_order))
        print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Tabu Search", tabu_cmax, tabu_exec_time, tabu_order))

        # fs_problem.display_gantt_chart(optimal_schedule, optimal_order)
        # fs_problem.display_gantt_chart(johnson_schedule, johnson_order)
        # fs_problem.display_gantt_chart(neh_schedule, neh_order)

if __name__ == "__main__":
    main()
