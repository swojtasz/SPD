import math
from queue_rpq import Queue
from copy import deepcopy
class RPQ:
    r = 0
    q = 0
    p = 0
    C = 0

    def __init__(self, r, p, q, C):
        self.r = r
        self.p = p
        self.q = q
        self.C = C

    def __str__(self):
        return f"{self.r} {self.p} {self.q}"

class RPQProblem:
    def __init__(self, lines):
        self.jobs_count, self.parametres_count = (int(val) for val in lines[0].split())

        self.jobs = []
        for job in lines[1:1 + self.jobs_count]:
            r, p, q = (int(val) for val in job.split())
            C = 0
            rpq = RPQ(int(r), int(p), int(q), C)
            self.jobs.append(rpq)
        self.UB = math.inf

    def minR(self, jobs):
        minR = math.inf
        for job in jobs:
            if (job.r < minR):
                minR = job.r
        return minR

    def minQ(self, jobs):
        minQ = math.inf
        for job in jobs:
            if (job.q < minQ):
                minQ = job.q
        return minQ

    def sumP(self, jobs):
        sumP = 0
        for job in jobs:
            sumP += job.p
        return sumP

    def minRindex(self, jobs):
        minR = math.inf
        minRind = 0
        for i in range(len(jobs)):
            if (jobs[i].r < minR):
                minR = jobs[i].r
                minRind = i
        return minRind

    def maxQindex(self, jobs):
        maxQ = 0
        maxQind = 0
        for i in range(len(jobs)):
            if (jobs[i].q > maxQ):
                maxQ = jobs[i].q
                maxQind = i
        return maxQind

    def SchrageWithoutQueue(self, given_order=None):
        G = []
        N = self.jobs.copy()
        if given_order is not None:
            N = given_order
        t = self.minR(N)
        cmax = 0
        pi = []

        while(len(G) != 0 or len(N) != 0):
            while(len(N) !=0 and self.minR(N) <= t):
                min_index = self.minRindex(N)
                G.append(N[min_index])
                N.remove(N[min_index])
            if(len(G) == 0):
                t = self.minR(N)
            else:
            # elif (G != 0):
                max_index = self.maxQindex(G)
                pi.append(G[max_index])
                t += G[max_index].p
                cmax = max(cmax, t + G[max_index].q)
                G[max_index].C = t
                G.remove(G[max_index])
        return cmax, pi

    def Schrage(self):
        G = Queue()
        N = Queue()
        for j in self.jobs:
            N.insert(j, -j.r)
        t = N.get_root_r()
        cmax = 0
        pi = []

        while(len(G.jobs) != 0 or len(N.jobs) != 0):
            while(len(N.jobs) !=0 and N.get_root_r() <= t):
                min_r_job = N.pop()
                G.insert(min_r_job, min_r_job.q)
            if(len(G.jobs) == 0):
                t = N.get_root_r()
            else:
                max_q_job = G.pop()
                pi.append(max_q_job)
                t += max_q_job.p
                cmax = max(cmax, t + max_q_job.q)
        return cmax, pi

    def SchragePMTNWithoutQueue(self, given_order=None):
        G = []
        N = self.jobs.copy()
        if given_order is not None:
            N = given_order
        t = 0
        l = RPQ(N[0].r, N[0].p, N[0].q, 0)
        l.q = math.inf
        cmax = 0

        while(len(G) != 0 or len(N) != 0):
            while(len(N) !=0 and self.minR(N) <= t):
                min_index = self.minRindex(N)
                G.append(N[min_index])
                N.remove(N[min_index])
                if G[-1].q > l.q:
                    l.p = t - G[-1].r
                    t = G[-1].r
                    if l.p > 0:
                        G.append(l)
            if(len(G) == 0):
                t = self.minR(N)
            else:
                max_index = self.maxQindex(G)
                t += G[max_index].p
                cmax = max(cmax, t + G[max_index].q)
                foo = G.copy()
                l = foo[max_index]
                G.remove(G[max_index])
        return cmax

    def findb(self, jobs, cmax):
        for job in jobs:
            if cmax == job.C + job.q:
                b = job
        return b

    def finda(self, jobs, cmax, b):
        b_index = jobs.index(b)
        for a_index in range(0, b_index+1):
            sum_a = 0
            for i in range(a_index, b_index+1):
                sum_a += jobs[i].p
            if cmax == jobs[a_index].r + sum_a + b.q:
                return jobs[a_index]

    def findc(self, jobs, cmax, a, b):
        c_index = -1
        for i in range(jobs.index(b), jobs.index(a), -1):
            if jobs[i].q < b.q:
                c_index = i
                break
        if c_index > 0:
            return jobs[c_index]
        else:
            return c_index

    def Carlier(self, pi_given):
        U, pi = RPQProblem.SchrageWithoutQueue(self, pi_given)
        if U < self.UB:
            self.UB = U
            pi_star = pi
        b = self.findb(pi, U)
        a = self.finda(pi, U, b)
        c = self.findc(pi, U, a, b)
        if c == -1:
            return self.UB
        K = pi[pi.index(c)+1:pi.index(b)+1]
        el_K = RPQ(0, 0, 0, 0)
        el_K.r = self.minR(K)
        el_K.q = self.minQ(K)
        el_K.p = self.sumP(K)

        c_index = pi.index(c)
        r_c = pi[c_index].r
        pi[pi.index(c)].r = max(pi[pi.index(c)].r, el_K.r + el_K.p)
        LB = RPQProblem.SchragePMTNWithoutQueue(self, deepcopy(pi))
        if LB < self.UB:
            self.Carlier(deepcopy(pi))
        pi[c_index].r = r_c

        c_index = pi.index(c)
        q_c = pi[c_index].q
        pi[pi.index(c)].q = max(pi[pi.index(c)].q, el_K.q + el_K.p)
        LB = RPQProblem.SchragePMTNWithoutQueue(self, deepcopy(pi))
        if LB < self.UB:
            self.Carlier(deepcopy(pi))
        pi[c_index].q = q_c
        return self.UB
