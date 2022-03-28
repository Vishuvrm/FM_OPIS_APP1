# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"

from file_monitor import Monitor
import multiprocessing

monitor = Monitor()

def start(meta_data, main_pid):
    app_related = meta_data["app_related"]
    log_file = app_related["log_file"]
    PID = app_related["PID"]
    events = meta_data["events"]

    start_process = multiprocessing.Process(
        target=monitor.start, args=(meta_data["active_folder"],
                                    events["on_create"], events["on_delete"], events["on_modify"],
                                    events["on_move"], meta_data["pattern"], meta_data["ign_pattern"],
                                    meta_data["ignore_dir"], meta_data["case_sensitive"],
                                    meta_data['refresh_rate'], meta_data["show_logs"],
                                    meta_data["auto_start"], log_file, main_pid
                                    ))
    start_process.start()

