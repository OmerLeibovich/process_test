import csv
import logging
import os
from datetime import datetime
import time
from typing import List, Dict, Optional
import psutil
from Process import Process

class ProcessMonitor:
        def __init__(self, interval: int, duration: int, exclude: Optional[List[str]] = None):
            """
            Initializes the ProcessMonitor instance.

            Args:
                interval (int): Number of seconds between each process snapshot.
                duration (int): Total duration in seconds to run the monitoring.
                exclude (Optional[List[str]]): A list of process names to exclude from monitoring.
            """
            self.interval: int = interval
            self.duration: int = duration
            self.exclude: List[str] = exclude if exclude is not None else []
            self.data_dict: Dict[int, Process] = {}


        def get_process_info(self, processes: Optional[List[psutil.Process]] = None) -> List[Process]:
            """
            Collects information about running OS processes: PID, name, CPU %, memory usage, and timestamp.
            It first initializes CPU usage measurement, waits, and then collects data.

            If a process with the same PID was previously monitored, its data is updated.

            Args:
                processes (Optional[List[psutil.Process]]): A list of processes to monitor.
                    If None, uses psutil to get all current system processes.

            Returns:
                List[Process]: A list of Process objects containing the collected data.
            """
            initialized_processes = []

            if processes is None:
                processes = psutil.process_iter(['pid', 'name', 'memory_info'])

            for proc in processes:
                try:
                    if proc.info['name'] in self.exclude:
                        continue
                    proc.cpu_percent()  # initialize CPU tracking
                    initialized_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logging.error(f"Process access error during initialization: {e}")
                    continue

            time.sleep(1)  # Wait for CPU measurements to stabilize

            for proc in initialized_processes:
                try:
                    pid: int = proc.pid
                    name: str = proc.name()
                    cpu: float = proc.cpu_percent() / psutil.cpu_count(logical=True)
                    memory: float = proc.memory_info().rss / (1024 * 1024)  # MB
                    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if pid in self.data_dict:
                        self.data_dict[pid].update(cpu, memory, timestamp)
                    else:
                        self.data_dict[pid] = Process(pid, name, cpu, memory, timestamp)
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logging.error(f"Process access error during data collection: {e}")
                    continue

            return list(self.data_dict.values())


        def run_monitoring(self,csvFilename: str,delete: bool,processes: Optional[List[object]] = None,debug: bool = False) -> None:
            """
            Runs the monitoring loop: periodically collects process data and writes it to a CSV file.

            Args:
                csvFilename (str): Path to the CSV file for storing process data.
                delete (bool): Whether to delete the CSV file before starting.
                processes (Optional[List[object]]): Optional list of mocked or real psutil.Process objects.
                debug (bool): Whether to print debug information to the console.

            Notes:
                - This function collects CPU/memory info every `self.interval` seconds for a total of `self.duration`.
                - Each snapshot is written as a row in the CSV file.
                - Uses self.get_process_info to retrieve updated process metrics.
                - Updates are logged to file (and optionally printed if debug=True).
            """
            try:
                if delete and os.path.exists(csvFilename):
                    os.remove(csvFilename)

                file_exists = os.path.exists(csvFilename)

                with open(csvFilename, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['pid', 'name', 'cpu', 'memoryInfo', 'date'])
                    if not file_exists:
                        writer.writeheader()

                    iterations = self.duration // self.interval
                    for i in range(iterations):
                        try:
                            if(debug):
                                print(f"Monitoring iteration {i + 1} started")
                            logging.info(f"Monitoring iteration {i + 1} started")
                            processes_data = self.get_process_info(processes)
                            for item in processes_data:
                                writer.writerow({'pid': item.pid,'name': item.name,'cpu': item.cpu,
                                    'memoryInfo': item.memoryInfo,'date': item.date})
                            if (debug):
                                print(f"Monitoring iteration {i + 1} ended")
                            logging.info(f"Monitoring complete, total  {len(processes_data)} processes")
                        except Exception as e:
                            logging.error(f"Failed to collect or write process data: {e}")
            except Exception as e:
                logging.critical(f"Critical failure in run_monitoring: {e}")


        def get_data_dict(self) -> Dict[int, Process]:
            """
            Returns the internal data dictionary that maps process IDs to Process objects.

            Returns:
                Dict[int, Process]: A dictionary where each key is a process ID (PID)
                and each value is a Process object containing monitoring data.
            """
            return self.data_dict