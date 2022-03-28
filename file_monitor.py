# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"


# Monitor file system changes

# Import relevant libraries
import os
import time
import multiprocessing

import pywintypes

from powershell import *
from wait_for_task import wait_for_task

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import re
from tkinter import messagebox as msgt
from tkinter import *
import logging
from datetime import datetime
from app_data import create_metadata_json
import json
import config
import pythoncom



__config_file = open(r"{0}".format(os.path.join(config.meta_folder_path,"config.json")), "r")
try:
    meta_data = json.load(__config_file)
except json.decoder.JSONDecodeError:
    msgt.showerror("json error", "config.json file is creating issue. Please clear it and restart the application.")
    exit()

meta_folder_path = meta_data["meta_folder_path"]
__config_file.close()

class Monitor:
    def __init__(self):
        self.root = None
        self.files_to_monitor = set()
        self.__show_logs = None
        self.logbox = None
        self.logger = None
        self.log_file = None
        self.__on_modify = None
        self.__on_move = None
        self.__on_delete = None
        self.__on_create = None
        self.__active_folder = None
        self.obs = None
        self.event = None
        self.__patterns: list = None  # File patterns we want to handle(* means all files)
        self.__ignore_patterns: list = None  # File patterns we want to ignore
        self.__ignore_directories: bool = False  # If True, it will ignore directories in the file system. If will only notify for the new files added and not the new directories added
        self.__case_sensitive: bool = True  # Matches the files with the exact pattern we have chosen
        self.__refresh_rate = None  # Time after which scanning occurs
        self.__auto_start = None  # Auto start the application with the previous configuration as soon as the computer starts.
        self.__meta_data = None

    def create_log_window(self, show_logs):
        if not os.path.exists(self.log_file):
            file = open(self.log_file, "w")
            file.close()
        if show_logs:
            # Create log window
            self.root = Tk()
            self.root.geometry("500x500")
            self.root.title("log window(Live)")

            def disable_event():
                event = msgt.askokcancel("Process still running",
                                         "The process is still running in the background.\n"
                                         "To end the process, go to task manager")
                if event:
                    self.root.destroy()

            if self.__auto_start: # and not psutil.pid_exists(self.main_pid):
                self.root.protocol("WM_DELETE_WINDOW", disable_event)
            scrollbar = Scrollbar(self.root)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.logbox = Text(self.root, yscrollcommand=scrollbar.set)
            self.logbox.pack(fill=BOTH, expand=True)

            # Getting previous data from the logs and inserting into the logbox
            with open(self.log_file, 'r') as file:
                self.logbox.insert(END, file.read())
                file.close()
            self.logbox.yview(END)

            self.logbox.configure(state="disabled")
            scrollbar.config(command=self.logbox.yview())

            # root.main =loop is at the end of all the processes.

    def create_logger(self):
        self.logger = logging.getLogger(__name__)

        # Creating handlers
        if not self.log_file:
            self.log_file = "monitor.log"
        f_handler = logging.FileHandler(self.log_file, mode="a")
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        f_format = logging.Formatter("@ %(asctime)s --> %(message)s", datefmt="%d-%b-%y::%H:%M:%S")
        f_handler.setFormatter(f_format)

        # Add handlers to logger
        self.logger.addHandler(f_handler)

    def run_powershell(self):
        # num_processes = len(meta_data["SCRIPT"])
        if self.__show_logs:
            try:
                self.logbox.configure(state="normal")
                self.logbox.insert(END, "\n############# POWERSHELL RUNNING... ##############\n")
                self.logbox.configure(state="disabled")
            except RuntimeError:
                pass

        refresh_rate = self.modified_refresh_rate(self.__refresh_rate)
        # for i, name in zip(range(num_processes), meta_data["SCRIPT"]):
        while True:
            __config_file = open(r"{0}".format(os.path.join(config.meta_folder_path, "config.json")), "r")
            try:
                meta_data = json.load(__config_file)
            except json.decoder.JSONDecodeError:
                msgt.showerror("json error",
                               "config.json file is creating issue. Please clear it and restart the application.")
                exit()
            num_processes = len(meta_data["SCRIPT"])

            for i, name in zip(range(num_processes), meta_data["SCRIPT"]):

                pythoncom.CoInitialize()
                # task = exec(f"task{i}", globals())
                # task = globals()[f"task{i}"]
                if name != "Signal_path":
                    if self.__show_logs:
                        try:
                            self.logbox.configure(state='normal')

                            self.logbox.insert(END, f"\nRunning the powershell script: {name}")
                            self.logbox.configure(state='disabled')
                        except RuntimeError:
                            pass
                    try:
                        task(name)
                        wait_for_task(name, refresh_rate, self.logger)
                    except KeyError as e:
                        if self.__show_logs:
                            self.logbox.configure(state='normal')
                            self.logbox.insert(END, f": Couldn't find the powershell script: {name}\n")
                            self.logbox.configure(state='disabled')
                        break

                    except pywintypes.com_error:
                        self.logger.exception(f"\n\nReconnecting to {name}...\n")

                    except Exception as e:
                        self.logger.exception(f"\n\nAn unexpected error has occured for {name}!\n")
                        if self.__show_logs:
                            self.logbox.configure(state="normal")
                            self.logbox.insert(END, f"\n\nAn unexpected error has occured for {name}!\n")
                            self.logbox.insert(END, str(e))
                            self.logbox.insert(END, "\n\n Process is ending now...\n\n")
                            self.logbox.configure(state="disabled")
                            return
                        # msgt.showinfo("Config file changed", "Config file has changed! Do you want to continue?")
                        # task(name,raise_key_error=True)
                elif name == "Signal_path":
                    try:
                        send_signal()
                        if self.__show_logs:
                            self.logbox.configure(state='normal')
                            self.logbox.insert(END,
                                               f"\nCreated signal file in {name}\nLoc: {meta_data['SCRIPT'][name]}")
                            self.logbox.configure(state='disabled')
                    except KeyError as e:
                        if self.__show_logs:
                            self.logbox.configure(state='normal')
                            self.logbox.insert(END,
                                               f"\n\nCouldn't create signal file: {name} is missing from config.json file.\n")
                            self.logbox.configure(state='disabled')
                        break
                    except Exception as e:
                        self.logger.exception(f"\n\nAn unexpected error has occured for {name}!\n")
                        if self.__show_logs:
                            self.logbox.configure(state="normal")
                            self.logbox.insert(END, f"\n\nAn unexpected error has occured for {name}!\n")
                            self.logbox.insert(END, str(e))
                            self.logbox.configure(state="disabled")
                            self.logbox.insert(END, "\n\n Process is ending now...\n\n")
                            self.logbox.configure(state="disabled")
                            return
            else:
                break
            # pythoncom.CoUnInitialized()
            # p1 = multiprocessing.Process(target=task, args=())
            # p1.start()
            # p1.join()

        # Print final log message
        if self.__show_logs:
            try:
                self.logbox.configure(state="normal")
                self.logbox.insert(END, "\n############# POWERSHELL PROCESS COMPLETED ##############\n\n")
                self.logbox.configure(state="disabled")
            except RuntimeError:
                pass

        self.files_to_monitor.clear()

        # Clear the logs
        with open(os.path.join(meta_folder_path, "monitor.log"), "w") as file:
            file.close()
            if self.__show_logs:
                try:
                    self.logbox.configure(state="normal")
                    self.logbox.insert(END, "\n############# Log file cleared!!! ##############\n\n")
                    self.logbox.configure(state="disabled")
                except RuntimeError:
                    pass

    # Handle all events
    def on_created(self, event, on_created_api):
        message = f"{event.src_path} has been created!"
        self.logger.warning(message)
        self.files_to_monitor.add(event.src_path)
        if self.__show_logs:
            try:
                self.logbox.configure(state='normal')
                self.logbox.insert(END, f"@ {datetime.now()}, {message}" + "\n")
                self.logbox.configure(state='disabled')
            except RuntimeError:
                pass
                # print("You closed the log window!")
        if len(self.files_to_monitor) == 2:
            self.run_powershell()

    def on_deleted(self, event, on_deleted_api):
        message = f"{event.src_path} has been deleted!"
        self.logger.warning(message)
        if self.__show_logs:
            try:
                self.logbox.configure(state='normal')
                self.logbox.insert(END, f"@ {datetime.now()}, {message}" + "\n")
                self.logbox.configure(state='disabled')
            except RuntimeError:
                pass
                # print("You closed the log window!")

    def on_modified(self, event, on_modified_api):
        message = f"{event.src_path} has been modified!"
        self.logger.warning(message)
        if self.__show_logs:
            try:
                self.logbox.configure(state='normal')
                self.logbox.insert(END, f"@ {datetime.now()}, {message}" + "\n")
                self.logbox.configure(state='disabled')
            except RuntimeError:
                pass
                # print("You closed the log window!")

    def on_moved(self, event, on_moved_api):
        message = f"{event.src_path} moved to {event.dest_path}"
        self.logger.warning(message)
        if self.__show_logs:
            try:
                self.logbox.configure(state='normal')
                self.logbox.insert(END, f"@ {datetime.now()}, {message}" + "\n")
                self.logbox.configure(state='disabled')
            except RuntimeError:
                pass
                # print("You closed the log window!")

    def observer(self, event_handler):
        # Create an observer: To monitor our filesystem, looking for any changes which will be handled by the event handler
        path = self.__active_folder
        if not path:
            path = "."
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(event_handler=event_handler, path=path, recursive=go_recursively)
        return my_observer

    def event_handler(self):
        # Binding the functions to the events
        my_event_handler = PatternMatchingEventHandler(self.__patterns, self.__ignore_patterns,
                                                       self.__ignore_directories, self.__case_sensitive)
        if self.__on_create == 1:
            my_event_handler.on_created = lambda e: self.on_created(e, "hello")
        if self.__on_delete == 1:
            my_event_handler.on_deleted = lambda e: self.on_deleted(e, "hello")
        if self.__on_modify == 1:
            my_event_handler.on_modified = lambda e: self.on_modified(e, "hello")
        if self.__on_move == 1:
            my_event_handler.on_moved = lambda e: self.on_moved(e, "hello")
        return my_event_handler

    def modified_refresh_rate(self, rate):
        time_units = {"sec", "min", "hr", "day", "week", "mo", "yr"}

        unit = re.findall(r"[a-z]+", rate)[0]
        digit = float(re.findall(r"[\d]+", rate)[0])

        if unit in time_units:
            if unit == "sec":
                return digit
            elif unit == "min":
                return 60 * digit
            elif unit == "hr":
                return 60 * 60 * digit
            elif unit == "day":
                return 24 * 60 * 60 * digit
            elif unit == "week":
                return 7 * 24 * 60 * 60 * digit
            elif unit == "mo":
                msgt.showwarning("incorrect units",
                                 message="Sorry, we are currently working on month(mo) and year(yr). Please choose any unit from sec(seconds), min(minutes), hr(hour), day(day), week(week).\nWe are stopping the program for now..PLease restart it.")
                self.stop()
                return
            elif unit == "yr":
                msgt.showwarning("incorrect units",
                                 message="Sorry, we are currently working on month(mo) and year(yr). Please choose any unit from sec(seconds), min(minutes), hr(hour), day(day), week(week).\nWe are stopping the program for now..PLease restart it.")
                self.stop()
                return
        else:
            msgt.showwarning("No units mentioned",
                             message="Please mention any unit from sec(seconds), min(minutes), hr(hour), day(day), week(week).\nAplpication is stopping now..Please restart it.")
            self.stop()
            return

    def start(self, active_folder, on_create, on_delete, on_modify, on_move, pattern, ign_pattern, ignore_dir,
              case_sensitive, refresh_rate, show_logs, auto_start, log_file, main_pid):
        # Initialize some variables
        self.__active_folder = active_folder
        self.__on_create = on_create
        self.__on_delete = on_delete
        self.__on_modify = on_modify
        self.__on_move = on_move

        if type(pattern) is list:
            self.__patterns = pattern
        else:
            self.__patterns = re.split(",", re.sub(r"(\s*,\s*)", r",", pattern))

        if type(ign_pattern) is list:
            self.__ignore_patterns = ign_pattern
        else:
            self.__ignore_patterns = re.split(",", re.sub(r"(\s*,\s*)", r",", ign_pattern))
        self.__ignore_directories = bool(ignore_dir)
        self.__case_sensitive = bool(case_sensitive)
        self.__refresh_rate = refresh_rate
        self.__show_logs = show_logs
        self.__auto_start = auto_start
        self.log_file = log_file

        self.create_log_window(self.__show_logs)

        # Creating JSON data
        if self.__auto_start:
            meta_data = {"events": {
                "on_create": self.__on_create,
                "on_delete": self.__on_delete,
                "on_modify": self.__on_modify,
                "on_move": self.__on_move,
            },
                "active_folder": self.__active_folder,
                "pattern": self.__patterns,
                "ign_pattern": self.__ignore_patterns,
                "ignore_dir": self.__ignore_directories,
                "case_sensitive": self.__case_sensitive,
                "refresh_rate": self.__refresh_rate,
                "show_logs": self.__show_logs,
                "auto_start": self.__auto_start,
                "app_related": {"log_file": self.log_file,
                                "PID": main_pid}}

            create_metadata_json(meta_data, meta_folder_path)

        self.event = self.event_handler()  # Start the event handler
        self.obs = self.observer(event_handler=self.event)
        self.obs.start()  # Start the file observer
        self.create_logger()  # Start the logging process

        if self.__show_logs:
            self.root.mainloop()

        try:
            while True:
                delay_seconds = self.modified_refresh_rate(self.__refresh_rate)
                time.sleep(delay_seconds)
        except KeyboardInterrupt:
            self.obs.stop()
            self.obs.join()
            try:
                print("Application still alive?:", self.obs.isAlive())
            except:
                print("Application is dead!")

    def stop(self):
        self.obs.stop()
        self.obs.join()
        try:
            pass
            # print("Application still alive?:", self.obs.isAlive())
        except:
            pass
            # print("Application is dead!")

        finally:
            exit()


if __name__ == "__main__":
    file_monitor = Monitor()
    file_monitor.start()
