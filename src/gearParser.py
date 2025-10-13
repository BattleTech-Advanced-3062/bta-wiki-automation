import os
import sys
import json
from pprint import pp
import genUtilities
from settings import *

def process_weapon_files(directories):
    weapon_dict = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("Weapon_") and file.endswith(".json"):


if __name__ == "__main__":
    result = process_weapon_files(weapon_dir_list)
    pp(result)