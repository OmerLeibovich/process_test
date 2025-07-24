from db import insert
from ProcessMonitor import ProcessMonitor
import json

with open("config.json", "r") as details:
    config = json.load(details)
    interval = config["monitoring_interval"]
    duration = config["monitoring_duration"]
    csvFilename = config["output_file"]
    delete_database_table = config["delete_database_table"]
    delete_csv_file = config["delete_csv_file"]
    exclude = config["exclude_processes"]
    db_config = config["database"]

monitor = ProcessMonitor(interval, duration, exclude)
monitor.run_monitoring(csvFilename,delete_csv_file)
processes = list(monitor.get_data_dict().values())
insert(processes,db_config,delete_database_table)






