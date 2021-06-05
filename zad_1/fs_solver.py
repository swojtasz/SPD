import time
import collections
from fs_problem import FSProblem

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


def solve_fs_with_solver(instance: FSProblem):
    from ortools.sat.python import cp_model # importujemy model CP z biblioteki or-tools

    model = cp_model.CpModel() # inicjalizacja modelu - przechowa nasze zmienne oraz ograniczenia naszego problemu

    variable_max_value = 0 # póki co
    variable_min_value = 0 # nic nie jest ujemne w naszym wypadku

    for job in instance.jobs:
        variable_max_value += sum(job) # suma czasow wsystkich zadan, overkill

    model_start_vars = collections.defaultdict(list) # tutaj będą czasy rozpoczęć operacji kazdego zadania
    model_ends_vars = collections.defaultdict(list) # tutaj będą czasy zakończeń operacji kazdego zadania
    model_interval_vars = collections.defaultdict(list) # tutaj będą przechowywane zmienne odpowiedzialne za zmienne interwałowe kadej maszyny

    for job_id, job in enumerate(instance.jobs):
        for machine, duration in enumerate(job):
            suffix = f"_{job_id}_{machine}"
            start_var = model.NewIntVar(0, variable_max_value, 'start' + suffix)
            end_var = model.NewIntVar(0, variable_max_value, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval' + suffix)

            model_start_vars[job_id].append(start_var)
            model_ends_vars[job_id].append(end_var)
            model_interval_vars[machine].append(interval_var)

    for key in model_interval_vars:
        model.AddNoOverlap(model_interval_vars[key]) # operacje nie mogą się nakładać na zadnej z maszyn
    
    for job_id, job in enumerate(instance.jobs):
        for task_id in range(len(job) - 1):
            model.Add(model_start_vars[job_id][task_id + 1] >= model_ends_vars[job_id][task_id]) # kolejna operacja zadania nie moze sie zacząc przed koncem poprzedniej

    # minimalizujemy cmax
    cmax_optimalization_objective = model.NewIntVar(variable_min_value, variable_max_value, 'cmax_makespan')
    model.AddMaxEquality(cmax_optimalization_objective,
    [
        model_ends_vars[job_id][instance.machines_count - 1] for job_id, job in enumerate(instance.jobs)
    ])
    model.Minimize(cmax_optimalization_objective)

    # Inicjalizujemy solver, który spróbuje znaleźć rozwiązanie w ramach naszego modelu:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0 # dodatkowo ograniczmy czas wykonywania obliczeń do maksymalnie 5 min

    # Wszystkie ograniczenia dodane! pora odpalić solver!
    status = solver.Solve(model) # solver zwróci status, ale jako typ wyliczeniowy, więc troche nieczytelnie dla nas

    if (status is not cp_model.OPTIMAL): # sprawdzamy status, aby określić czy solver znalazł rozwiązanie optymalne
        status_readable = "not optimal solution :("
    else:
        status_readable = "optimum found!"

    # sprawdzamy rozpoczecie pierwszej operacji kazdego zadania:
    # Tworzymy listę z parami: (numer zadania, czas rozpoczęcia), sortujemy po tej drugiej wartości.
    pi_order = []
    for job_id, job in enumerate(instance.jobs):
        pi_order.append((job_id, solver.Value(model_start_vars[job_id][0])))
    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order] # modyfikujemy naszą listę, aby przechowywać tylko numer zadań, bez czasów rozpoczęć

    return solver.ObjectiveValue(), pi_order, status_readable # zwracamy cmax, kolejność wykonywania zadań oraz informacje czy znaleźliśmy optimum


def solver(fs_problem: FSProblem):

    t = Timer()
    t.start()
    cmax, pi_order, status = solve_fs_with_solver(fs_problem)
    s = t.stop()

    return f"CMAX SOLVER: {cmax}, order: {pi_order}\nis optimal? {status}", s, pi_order
