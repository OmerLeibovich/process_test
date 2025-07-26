import csv
import os
import unittest
from typing import List, Optional
from unittest.mock import MagicMock, patch
import psutil
from datetime import datetime
from Process import Process
from ProcessMonitor import ProcessMonitor


class TestProcesses(unittest.TestCase):
    """
      Unit tests for the ProcessMonitor class and related functionality.
      """

    def create_process(self, pid=3210, name="test", cpu=0.13, memory=98.3) -> Process:
        """
        Helper method to create a Process object for testing purposes.

        Args:
            pid (int, optional): Process ID. Defaults to 3210.
            name (str, optional): Process name. Defaults to "test".
            cpu (float, optional): CPU usage percentage. Defaults to 0.13.
            memory (float, optional): Memory usage in MB. Defaults to 98.3.

        Returns:
            Process: A Process instance with the provided values and current timestamp.
        """
        testProcess = Process(pid=pid, name=name, cpu=cpu, memoryInfo=memory, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return testProcess

    def test_process_update(self):
        """
         Test that the update() method correctly accumulates CPU and memory usage,
         increments the sample count, and updates the timestamp.
         """
        testProcess = self.create_process()
        testProcess.update(0.42, 11.3, "2025-01-01 12:00:00")
        self.assertEqual(testProcess.cpu, 0.55)
        self.assertEqual(testProcess.memoryInfo, 109.6)
        self.assertEqual(testProcess.count, 2)
        self.assertEqual(testProcess.date, "2025-01-01 12:00:00")

    def create_process_monitor(self, interval=5, duration=5,exclude: Optional[List[str]] = None) -> ProcessMonitor:
        """
        Helper method to create a ProcessMonitor instance for testing.

        Args:
            interval (int, optional): Time in seconds between measurements. Defaults to 5.
            duration (int, optional): Total monitoring duration in seconds. Defaults to 5.
            exclude (Optional[List[str]], optional): List of process names to exclude. Defaults to None.

        Returns:
            ProcessMonitor: A configured ProcessMonitor instance.
        """
        monitor = ProcessMonitor(interval=interval,duration=duration,exclude=exclude)
        return monitor

    def create_mock_processes(self) -> List[MagicMock]:
        """
        Creates a list of mocked psutil.Process-like objects for testing purposes.
        Also resets the monitor instance and clears its internal data dictionary.

        Returns:
            List[MagicMock]: A list of mocked process objects with preset values.
        """
        self.monitor = self.create_process_monitor()
        # Mock for process 1
        mock_proc1 = MagicMock()
        mock_proc1.info = {'pid': 1, 'name': 'test_proc_name_1'}
        mock_proc1.pid = 1
        mock_proc1.name = MagicMock(return_value='test_proc_name_1')
        mock_proc1.cpu_percent = MagicMock(return_value=0.0)
        mock_proc1.memory_info.return_value.rss = 93.9 * 1024 * 1024

        # Mock for process 2
        mock_proc2 = MagicMock()
        mock_proc2.info = {'pid': 2, 'name': 'test_proc_name_2'}
        mock_proc2.pid = 2
        mock_proc2.name = MagicMock(return_value='test_proc_name_2')
        mock_proc2.cpu_percent = MagicMock(return_value=1.30)
        mock_proc2.memory_info.return_value.rss = 38.2 * 1024 * 1024

        # Mock for process 3
        mock_proc3 = MagicMock()
        mock_proc3.info = {'pid': 3, 'name': 'test_proc_name_3'}
        mock_proc3.pid = 3
        mock_proc3.name = MagicMock(return_value='test_proc_name_3')
        mock_proc3.cpu_percent = MagicMock(return_value=1.0)
        mock_proc3.memory_info.return_value.rss = 21.5 * 1024 * 1024
        self.monitor.data_dict.clear()

        return [mock_proc1, mock_proc2, mock_proc3]

    def setUp(self) -> None:
        """
        Set up the test environment before each test method.

        - Defines the path to a temporary CSV file.
        - Creates mock processes with predefined CPU and memory usage.
        - Calls cpu_percent() once to initialize CPU tracking.
        - Runs the monitoring logic on the mocked processes and writes to the CSV.
        """
        self.csvFilename: str = "test.csv"
        self.processes = self.create_mock_processes()

        # Initialize CPU tracking
        for proc in self.processes:
            proc.cpu_percent()

        # Run one full monitoring cycle with mock data
        self.monitor.run_monitoring(self.csvFilename, delete=True, processes=self.processes)

    def test_process_monitor_existCsv(self) -> None:
        """
        Test that the CSV file is created after monitoring.
        """
        self.assertTrue(os.path.exists(self.csvFilename))

    def test_process_monitor_checkCsvFile(self) -> None:
        """
        Test that the CSV file contains the correct process data as recorded by run_monitoring.
        """
        with open(self.csvFilename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            for i in range(len(reader)):
                self.assertEqual(int(reader[i]['pid']), self.processes[i].pid)
                self.assertEqual(str(reader[i]['name']), self.processes[i].name())
                self.assertEqual(
                    float(reader[i]['cpu']),
                                 self.processes[i].cpu_percent() / psutil.cpu_count(logical=True))
                self.assertEqual(
                    float(reader[i]['memoryInfo']),
                                 self.processes[i].memory_info().rss / (1024 * 1024))

                parsed_date = datetime.strptime(reader[i]['date'], "%Y-%m-%d %H:%M:%S")
                self.assertIsInstance(parsed_date, datetime)

    def test_exclude_items(self) -> None:
        """
        Test that processes with names in the exclusion list are not included in the monitoring results.
        """
        excluded_name = 'test_proc_name_1'
        monitor = ProcessMonitor(5, 5, [excluded_name])
        mock_processes = self.create_mock_processes()

        processes_info = monitor.get_process_info(mock_processes)

        for proc in processes_info:
            self.assertNotEqual(proc.name, excluded_name)



if __name__ == '__main__':
    unittest.main()
