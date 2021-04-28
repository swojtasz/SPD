import math

class RPQ:
    r = 0
    q = 0
    p = 0

    def __init__(self, r, p, q):
        self.r = r
        self.p = p
        self.q = q

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
        N = self.jobs
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
            elif (G != 0):
                max_index = self.maxQindex(G)
                pi.append(G[max_index])
                t += G[max_index].p
                cmax = max(cmax, t + G[max_index].q)
                G.remove(G[max_index])
        return cmax, pi



