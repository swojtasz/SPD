import time
import argparse
import random
from fs_problem import FSProblem
import neh
import tabu
from rpq_problem import RPQProblem


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
        rpq_problem = RPQProblem(get_file_content(path))
        rpq_problem2 = RPQProblem(get_file_content(path))
        # print('R P Q')
        # for i in range(rpq_problem.jobs_count):
        #     print(rpq_problem.jobs[i].r, rpq_problem.jobs[i].p, rpq_problem.jobs[i].q)

        cmax, pi = rpq_problem.SchrageWithoutQueue()
        cmaxprzerwania = rpq_problem2.SchragePMTN()
        print("PI - order:")
        for i in range(rpq_problem.jobs_count):
            print(pi[i].r, pi[i].p, pi[i].q)
        print("==============================")
        print("CMAX:" + str(cmax))
        print("CMAX pmtn:" + str(cmaxprzerwania))


    # args = parse_arguments()
    # t = Timer()
    # for path in args.filepaths:
    #     fs_problem = FSProblem(get_file_content(path))
    #     print(fs_problem)
    #
    #     # if args.brutal:
    #     #     t.start()
    #     #     optimal_order = fs_problem.bruteforce(args.workers)
    #     #     optimal_exec_time = t.stop()
    #     #     optimal_schedule = fs_problem.get_machines_schedule(optimal_order)
    #     #     optimal_c_max = optimal_schedule[-1][-1][-1]
    #
    #     t.start()
    #     johnson_order = fs_problem.johnson()
    #     johnson_exec_time = t.stop()
    #     johnson_schedule = fs_problem.get_machines_schedule(johnson_order)
    #     johnson_c_max = johnson_schedule[-1][-1][-1]
    #
    #     t.start()
    #     neh_order, neh_c_max = fs_problem.neh()
    #     neh_exec_time = t.stop()
    #     # fs_problem.check_answer("neh", neh_order, neh_c_max)
    #
    #     t.start()
    #     neh_mod1_order, neh_mod1_c_max = fs_problem.neh(mod=1)
    #     neh_mod1_exec_time = t.stop()
    #
    #     t.start()
    #     neh_mod2_order, neh_mod2_c_max = fs_problem.neh(mod=2)
    #     neh_mod2_exec_time = t.stop()
    #
    #     t.start()
    #     neh_mod3_order, neh_mod3_c_max = fs_problem.neh(mod=3)
    #     neh_mod3_exec_time = t.stop()
    #
    #     # all random, different generation, 20s timeout
    #     t.start()
    #     tabu_1_order, tabu_1_cmax = fs_problem.tabu(init='random', generate='swap', stop=('timeout', 20))
    #     tabu_1_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_2_order, tabu_2_cmax = fs_problem.tabu(init='random', generate='insert', stop=('timeout', 20))
    #     tabu_2_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_3_order, tabu_3_cmax = fs_problem.tabu(init='random', generate='inverse', stop=('timeout', 20))
    #     tabu_3_exec_time = t.stop()
    #
    #     # all neh, different generation, 20s timeout
    #     t.start()
    #     tabu_4_order, tabu_4_cmax = fs_problem.tabu(init='neh', generate='swap', stop=('timeout', 20))
    #     tabu_4_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_5_order, tabu_5_cmax = fs_problem.tabu(init='neh', generate='insert', stop=('timeout', 20))
    #     tabu_5_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_6_order, tabu_6_cmax = fs_problem.tabu(init='neh', generate='inverse', stop=('timeout', 20))
    #     tabu_6_exec_time = t.stop()
    #
    #     # all neh, all swap generation, 10k iterations improvement, different neighbourhood size
    #     t.start()
    #     tabu_7_order, tabu_7_cmax = fs_problem.tabu(init='neh', generate='swap', stop=('improvement', 10000), neighbourhood_size=5)
    #     tabu_7_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_8_order, tabu_8_cmax = fs_problem.tabu(init='neh', generate='swap', stop=('improvement', 10000), neighbourhood_size=10)
    #     tabu_8_exec_time = t.stop()
    #
    #     t.start()
    #     tabu_9_order, tabu_9_cmax = fs_problem.tabu(init='neh', generate='swap', stop=('improvement', 10000), neighbourhood_size=15)
    #     tabu_9_exec_time = t.stop()
    #
    #     print('{0:<20}{1:<10}{2:<14}{3}'.format("algorithm/data", "c_max", "exec time", "order"))
    #     print(*['-'] * 50)
    #     # if args.brutal:
    #         # print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Bruteforce", optimal_c_max, optimal_exec_time, optimal_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("Johnson", johnson_c_max, johnson_exec_time, johnson_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH", neh_c_max, neh_exec_time, neh_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 1", neh_mod1_c_max, neh_mod1_exec_time, neh_mod1_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 2", neh_mod2_c_max, neh_mod2_exec_time, neh_mod2_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("NEH MOD 3", neh_mod3_c_max, neh_mod3_exec_time, neh_mod3_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS rdm swp 5", tabu_1_cmax, tabu_1_exec_time, tabu_1_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS rdm ins 5", tabu_2_cmax, tabu_2_exec_time, tabu_2_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS rdm inv 5", tabu_3_cmax, tabu_3_exec_time, tabu_3_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh swp 5", tabu_4_cmax, tabu_4_exec_time, tabu_4_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh ins 5", tabu_5_cmax, tabu_5_exec_time, tabu_5_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh inv 5", tabu_6_cmax, tabu_6_exec_time, tabu_6_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh swp 5", tabu_7_cmax, tabu_7_exec_time, tabu_7_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh swp 10", tabu_8_cmax, tabu_8_exec_time, tabu_8_order))
    #     print('{0:<20}{1:<10}{2:<14.6f}{3}'.format("TS neh swp 15", tabu_9_cmax, tabu_9_exec_time, tabu_9_order))
    #
    #
    #     # fs_problem.display_gantt_chart(optimal_schedule, optimal_order)
    #     # fs_problem.display_gantt_chart(johnson_schedule, johnson_order)
    #     # fs_problem.display_gantt_chart(neh_schedule, neh_order)

if __name__ == "__main__":
    main()
