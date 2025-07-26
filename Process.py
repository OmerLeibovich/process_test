class Process:
    """
    A class to represent a monitored process and store its resource usage over time.
    """

    def __init__(self, pid: int, name: str, cpu: float, memoryInfo: float, date: str):
        """
        Initializes a new Process object.

        Args:
            pid (int): Process ID.
            name (str): Name of the process.
            cpu (float): Initial CPU usage percentage.
            memoryInfo (float): Initial memory usage in MB.
            date (str): Timestamp of the measurement.
        """
        self.pid: int = pid
        self.name: str = name
        self.cpu: float = cpu
        self.memoryInfo: float = memoryInfo
        self.date: str = date
        self.count: int = 1  # Number of samples aggregated

    def update(self, cpu: float, memoryInfo: float, date: str) -> None:
        """
        Updates the process statistics with a new measurement.

        Args:
            cpu (float): Additional CPU usage to add.
            memoryInfo (float): Additional memory usage to add.
            date (str): Timestamp of the latest update.
        """
        self.cpu += cpu
        self.memoryInfo += memoryInfo
        self.count += 1
        self.date = date

    def calc_avg(self) -> tuple[float, float]:
        """
        Calculates the average CPU and memory usage.

        Returns:
            tuple[float, float]: A tuple containing:
                - avg_cpu (float): Average CPU usage.
                - avg_mem (float): Average memory usage in MB.
        """
        avg_cpu: float = self.cpu / self.count
        avg_mem: float = self.memoryInfo / self.count
        return avg_cpu, avg_mem

