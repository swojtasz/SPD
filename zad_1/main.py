import sys

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No filename specified.")
    else:
        main()