import csv
import os
from datetime import datetime
import time
from typing import List, Dict

import psutil

from Process import Process

class ProcessMonitor:
    def __init__(self, interval: int, duration: int, exclude: List[str] = []):
        """
        Initialize the process monitor.
        Args:
            interval (int): Number of seconds between measurements.
            duration (int): Total duration of monitoring in seconds.
            exclude (List[str]): Process names to exclude.
        """
        self.interval = interval
        self.duration = duration
        self.exclude = exclude
        self.data_dict: Dict[int, Process] = {}

    def get_process_info(self) -> list[Process]:
        """
        Efficient CPU measurement: initialize, wait, and then measure all at once.
        """
        initialization_processes = []

        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'] in self.exclude:
                    continue
                proc.cpu_percent()
                initialization_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


        time.sleep(1)


        for init_process in initialization_processes:
            try:
                pid = init_process.pid
                name = init_process.name()
                cpu = init_process.cpu_percent() / psutil.cpu_count(logical=True)
                memory = init_process.memory_info().rss / (1024 * 1024)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                if pid in self.data_dict:
                    self.data_dict[pid].update(cpu, memory, timestamp)
                else:
                    self.data_dict[pid] = Process(pid, name, cpu, memory, timestamp)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return list(self.data_dict.values())

    def run_monitoring(self,csvFilename,delete):
        """
        Run monitoring loop.
        """
        if delete:
            if os.path.exists(csvFilename):
                os.remove(csvFilename)

        file_exists = os.path.exists(csvFilename)

        with open(csvFilename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['pid', 'name', 'cpu', 'memoryInfo', 'date'])
            if not file_exists:
                writer.writeheader()

            iterations = self.duration // self.interval
            for i in range(iterations):
                processes_data = self.get_process_info()
                for item in processes_data:
                    writer.writerow({'pid': item.pid,'name': item.name,'cpu': item.cpu,'memoryInfo': item.memoryInfo,'date': item.date})

    def get_data_dict(self) -> Dict[int, Process]:
        """
        Returns the internal data dictionary.
        """
        return self.data_dict
