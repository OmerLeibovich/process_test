import logging
from db import insert
from ProcessMonitor import ProcessMonitor
import json
from initLog import init_log


with open("config.json", "r") as details:
    config = json.load(details)
    interval = config["monitoring_interval"]
    duration = config["monitoring_duration"]
    csvFilename = config["output_file"]
    delete_database_table = config["delete_database_table"]
    delete_csv_file = config["delete_csv_file"]
    exclude = config["exclude_processes"]
    debug = config["debug_mode"]
    db_config = config["database"]

init_log()

if(debug):
    print("script start")
logging.info("script start")
monitor = ProcessMonitor(interval, duration, exclude)
monitor.run_monitoring(csvFilename,delete_csv_file,debug=debug)
processes = list(monitor.get_data_dict().values())
insert(processes, db_config, delete_database_table)
if(debug):
    print("script end")
logging.info("script end")






