# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"

import json
import os
# import win32api

# To get desktop location in any computer with windows

conf = {
  "meta_folder_path": "D:\\PROS_DATA_BKP\\MonitorData", #__meta_folder_path
  "PROD_Master_path": "D:\\PPSS\\Data\\Inbound",
  "SCRIPT": {
              "Inbound_SFG": r"",
              "Delete_Rack_Staging": r"",
              "OPIS_Post_Process": r"",
              "RACK_IF_LOAD": r"",
              "OPIS_MI_Load_1": r"",
              "OPIS_MI_Load_2": r"",
              "OPIS_MI_Load_3": r"",
              "OPIS_MI_Load_4": r"",
              "Signal_path": ""
            }
}

try:
    meta_folder_path = conf['meta_folder_path']
    if not os.path.exists(meta_folder_path):
        os.makedirs(meta_folder_path)

except PermissionError:
    # drives = win32api.GetLogicalDriveStrings()
    # drives = drives.split('\000')[:-1]
    user = os.environ["USERPROFILE"]
    meta_folder_path = os.path.join(user, "Desktop", "PROS_DATA_BKP", "MonitorData")
    conf['meta_folder_path'] = meta_folder_path
    if not os.path.exists(meta_folder_path):
        os.makedirs(meta_folder_path)

except FileNotFoundError:
    # drives = win32api.GetLogicalDriveStrings()
    # drives = drives.split('\000')[:-1]
    user = os.environ["USERPROFILE"]
    meta_folder_path = os.path.join(user, "Desktop", "PROS_DATA_BKP", "MonitorData")
    conf['meta_folder_path'] = meta_folder_path
    if not os.path.exists(meta_folder_path):
        os.makedirs(meta_folder_path)

if not os.path.exists(os.path.join(meta_folder_path, "config.json")):
    with open(os.path.join(meta_folder_path,"config.json"), "w") as file:
        json.dump(conf, file, indent=4)
        file.close()