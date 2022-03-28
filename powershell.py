# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"

import subprocess
import json
import config
import os
from tkinter import messagebox as msgt
from tkinter import *
import config

class NoScriptFound(Exception):
    pass

# import subprocess
#
# # os.system("powershell -command 'Set-ExecutionPolicy Unrestricted'") # Run this in command prompt
# # OR
# # os.system("powershell -command 'start-process PowerShell -verb runas'") # Run this in powershell
# os.system(r"powershell -command C:\Users\INTEL\Desktop\echo.ps1")
# # os.system("powershell -command 'Set-ExecutionPolicy restricted'")
#
# # p = subprocess.Popen(["powershell.exe", "start-process PowerShell -verb runas"])
# # p = subprocess.Popen(["powershell.exe",r"C:\Users\INTEL\Desktop\powersh1.ps1"])
# # p.communicate()

# define the tasks here
def get_json_data():
    __config_file = open(r"{0}".format(os.path.join(config.meta_folder_path,"config.json")), "r")
    data = json.load(__config_file)
    __config_file.close()
    return data

def task(task_name):
    global data
    global root
    root = Tk()
    root.withdraw()
    while True:
        try:
            # if raise_key_error:
            #     msgt.showwarning("Config file modified",
            #                      "You have modified the config.json file. Do you want to continue?")
            #     raise_key_error=False
            data = get_json_data()
            path = data["SCRIPT"][task_name]
            if path == "":
                raise NoScriptFound(f"Please add location for {task_name} in the config.json file")
            subprocess.check_call(["powershell.exe", path])
            # subprocess.call(["powershell.exe", path])
            break

        except NoScriptFound as e:
            msgt.showwarning("Location not mentioned!", e)
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])

        except subprocess.CalledProcessError:
            # subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])
            msgt.showwarning("File not found", f"File location for {task_name} is incorrect.\n"
                                               "Please change its location in the config.json file.")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])

        except FileNotFoundError as e:
            # subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path,"config.json")])
            msgt.showwarning("File not found", f"File location for {task_name} is incorrect.\n"
                                               "Please change its location in the config.json file.")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])
        except json.decoder.JSONDecodeError:
            msgt.showerror("Incorrect format", r"Hint: May be try using double backslash(\\) in location")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])

def send_signal():
    global data
    while True:
        try:
            data = get_json_data()
            path = data["SCRIPT"]["Signal_path"]
            if path == "":
                raise NoScriptFound("Please add location for Sterling_shared_path in the config.json file0")
            # subprocess.check_call(["powershell.exe", path])
            # subprocess.call(["powershell.exe", path])

            # Create a signal file
            signal_path = os.path.join(path, "FileMonitor_signal.txt")
            signal = open(signal_path, "w")
            signal.write("Run next server")
            signal.close()
            break

        except NoScriptFound as e:
            # subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path,"config.json")])
            msgt.showwarning("File not found", "File location for Sterling_shared_path is incorrect.\n"
                                               "Please change its location in the config.json file.")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])

        except FileNotFoundError as e:
            # subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path,"config.json")])
            msgt.showwarning("File not found", "File location for Sterling_shared_path is incorrect.\n"
                                               "Please change its location in the config.json file.")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])

        except json.decoder.JSONDecodeError:
            msgt.showerror("Incorrect format", r"Hint: May be try using double backslash(\\) in location")
            subprocess.Popen(["notepad.exe", os.path.join(config.meta_folder_path, "config.json")])