class Process:
    def __init__(self, pid: int, name: str, cpu: float, memoryInfo: float, date:str):
        self.pid = pid
        self.name = name
        self.cpu = cpu
        self.memoryInfo = memoryInfo
        self.date = date
        self.count = 1

    def update(self, cpu: float, memoryInfo: float, date: str):
        self.cpu += cpu
        self.memoryInfo += memoryInfo
        self.count += 1
        self.date = date

    def calc_avg(self):
        avg_cpu = self.cpu / self.count
        avg_mem = self.memoryInfo / self.count
        return  avg_cpu,avg_mem
