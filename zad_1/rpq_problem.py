import math
from queue import Queue

class RPQ:
    r = 0
    q = 0
    p = 0

    def __init__(self, r, p, q):
        self.r = r
        self.p = p
        self.q = q

    def __str__(self):
        return f"{self.r} {self.p} {self.q}"

class RPQProblem:
    def __init__(self, lines):
        self.jobs_count, self.parametres_count = (int(val) for val in lines[0].split())

        self.jobs = []
        for job in lines[1:1 + self.jobs_count]:
            r, p, q = (int(val) for val in job.split())
            rpq = RPQ(int(r), int(p), int(q))
            self.jobs.append(rpq)

    def minR(self, jobs):
        minR = math.inf
        for job in jobs:
            if (job.r < minR):
                minR = job.r
        return minR

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

    def SchrageWithoutQueue(self):
        G = []
        N = self.jobs.copy()
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

    def SchragePMTNWithoutQueue(self):
        G = []
        N = self.jobs.copy()
        t = 0
        l = RPQ(N[0].r, N[0].p, N[0].q)
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