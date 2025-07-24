import unittest
from unittest.mock import MagicMock, patch
import psutil
import psycopg2
from datetime import datetime
from db import insert
from Process import Process
from main import monitor


class TestProcesses(unittest.TestCase):

    def create_process(self, pid=3210, name="test", cpu=0.13, memory=98.3):
        testProcess = Process(pid=pid, name=name, cpu=cpu, memoryInfo=memory, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return testProcess

    def test_create_process(self):
        testProcess = self.create_process()
        self.assertEqual(testProcess.pid,3210)
        self.assertEqual(testProcess.name,"test")
        self.assertEqual(testProcess.cpu,0.13)
        self.assertEqual(testProcess.memoryInfo,98.3)
        self.assertEqual(testProcess.date,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_process_update(self):
        testProcess = self.create_process()
        testProcess.update(0.42, 11.3, "2025-01-01 12:00:00")
        self.assertEqual(testProcess.cpu, 0.55)
        self.assertEqual(testProcess.memoryInfo, 109.6)
        self.assertEqual(testProcess.count, 2)
        self.assertEqual(testProcess.date, "2025-01-01 12:00:00")

    def test_process_monitor(self):
        mock_proc1 = MagicMock()
        mock_proc1.pid = 1
        mock_proc1.name = MagicMock(return_value='other_proc')
        mock_proc1.cpu_percent = MagicMock(side_effect=[None, 0.0])
        mock_proc1.memory_info.return_value.rss = 93.9 * 1024 * 1024

        mock_proc2 = MagicMock()
        mock_proc2.pid = 2
        mock_proc2.name = MagicMock(return_value='test_proc_name')
        mock_proc2.cpu_percent = MagicMock(side_effect=[None, 1.30])
        mock_proc2.memory_info.return_value.rss = 38.2 * 1024 * 1024

        mock_proc3 = MagicMock()
        mock_proc3.pid = 3
        mock_proc3.name = MagicMock(return_value='test_proc_name')
        mock_proc3.cpu_percent = MagicMock(side_effect=[None, 1.0])
        mock_proc3.memory_info.return_value.rss = 21.5 * 1024 * 1024
        monitor.data_dict.clear()

        with patch('ProcessMonitor.psutil.process_iter', return_value=[mock_proc1, mock_proc2, mock_proc3]):
            processes = monitor.get_process_info()

            self.assertEqual(len(processes), 3)

            names = [p.name for p in processes]
            self.assertIn('test_proc_name', names)
            for proc in processes:
                self.assertIsInstance(proc, Process)


if __name__ == '__main__':
    unittest.main()
