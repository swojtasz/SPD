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
    parser.add_argument('--brutal', nargs='?', const=True, default=False, help='number of processes utilized for bruteforce method')
    parser.add_argument('--workers', type=int, default=1, help='number of processes utilized for bruteforce method')
    return parser.parse_args()


def main():
    args = parse_arguments()
    t = Timer()
    for path in args.filepaths:
        rpq_problem = RPQProblem(get_file_content(path))
        # print('R P Q')
        # for i in range(rpq_problem.jobs_count):
        #     print(rpq_problem.jobs[i].r, rpq_problem.jobs[i].p, rpq_problem.jobs[i].q)
        t.start()
        cmax1, pi = rpq_problem.SchrageWithoutQueue()
        s1 = t.stop()
        t.start()
        cmax2, pi = rpq_problem.Schrage()
        s2 = t.stop()

        print("file:", path)
        print("normal:", s1)
        print("queue:", s2)
        # print("PI - order:")
        # for i in range(rpq_problem.jobs_count):
        #     print(pi[i].r, pi[i].p, pi[i].q)
        print("==============================")
        print("CMAX:", cmax1)
        print("CMAX pmtn:", cmax2)


if __name__ == "__main__":
    main()
