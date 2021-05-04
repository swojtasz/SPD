class Queue:
    def __init__(self):
        self.data = []
        self.jobs = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return ((2 * i) + 1)

    def right_child(self, i):
        return ((2 * i) + 2)
        
    def shift_up(self, i):
        while (i > 0 and self.data[self.parent(i)] < self.data[i]):
            self.swap(self.parent(i), i)
            i = self.parent(i)
            
    def shift_down(self, i):
        maxIndex = i
        size = len(self.data)

        l = self.left_child(i)
        if (l <= size-1 and self.data[l] > self.data[maxIndex]):
            maxIndex = l

        r = self.right_child(i)
        if (r <= size-1 and self.data[r] > self.data[maxIndex]):
            maxIndex = r
        
        if (i != maxIndex):
            self.swap(i, maxIndex)
            self.shift_down(maxIndex)

    def insert(self, job, p):
        self.data.append(p)
        self.jobs.append(job)
        size = len(self.data)
        self.shift_up(size-1)

    def pop(self):
        result = self.jobs[0]
        size = len(self.data)
        self.data[0] = self.data[size-1]
        self.jobs[0] = self.jobs[size-1]
        self.data.pop(size-1)
        self.jobs.pop(size-1)
        self.shift_down(0)
        return result

    def changePriority(self, i, p):
        oldp = self.data[i]
        self.data[i] = p
        if (p > oldp):
            self.shift_up(i)
        else:
            self.shift_down(i)

    def get_root_r(self):
        return self.jobs[0].r  

    def swap(self, i, j):
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp

        temp = self.jobs[i]
        self.jobs[i] = self.jobs[j]
        self.jobs[j] = temp
