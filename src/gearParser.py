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
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if "BLACKLISTED" not in data.get("ComponentTags", {}).get("items", []) or "Modes" not in data:
                            weapon_entry = parse_weapon_json(file_path)
                            weapon_dict.update(weapon_entry)
                    
def parse_weapon_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

if __name__ == "__main__":
    result = process_weapon_files(weapon_dir_list)
    pp(result)