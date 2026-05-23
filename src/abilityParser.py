import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

def process_ability_files(directories):
    ability_dict = {}
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("AbilityDef") and file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    #pp(file_path)
                    ability_entry = parse_ability_json(file_path)
                    #pp(ability_entry)
                    ability_dict.update(ability_entry)
    
    return ability_dict

def parse_ability_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    ability_id = data.get("Description", {}).get("Id", "unknown")
    ability_id = ability_id.replace("AbilityDef", "")
    ability_name = data.get("Description", {}).get("Name", "unknown")
    ability_name = ability_name.title()
    ability_details = data.get("Description", {}).get("Details", "unknown")
    ability_details = genUtilities.strip_color_tags(ability_details)
    ability_icon = data.get("Description", {}).get("Icon", "unknown")
    ability_entry = {
        "path": file_path,
        "id": ability_id,
        "name": ability_name,
        "details": ability_details,
        "icon": ability_icon
    }
    return {ability_id: ability_entry }

if __name__ == "__main__":
    processed_list = process_ability_files(ability_dir_list)
    pp(processed_list)