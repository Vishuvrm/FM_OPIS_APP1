# Copyright information
__author__ = "Vishal Verma"
__copyright__ = "Copyright (C) 2004 Vishal Verma"
__license__ = "Public Domain"
__version__ = "1.5"

import json
import os


def create_metadata_json(dict_, path):
    json_path = os.path.join(path, "monitor.json")
    with open(json_path, "w") as file:
        json.dump(dict_, file, indent=4)
        file.close()


def read_json(add):
    with open(add, "r") as file:
        data = json.load(file)
        file.close()

    return data