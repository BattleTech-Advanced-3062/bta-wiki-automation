import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_actuator_files(directories):
    actuator_dict = {}
    excluded_files = {"Gear_Actuator_LifterClamp.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Actuator")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        actuator_entry = parse_actuator_json(file_path, bonuses)
                        actuator_dict.update(actuator_entry)

    return actuator_dict

def parse_actuator_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        actuator_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        location = data.get("BonusValueB", "unknown")
        part = find_actuator_type(data)
        allowed = data.get("AllowedLocations", "unknown")
        fixed = "Yes" if "no_salvage" in data.get("Custom").get("Flags", []) else "No"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Initiative", "Health", "IsCockpit", "IsSensorsB", "IsSensorsA", "TorsoMount"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        actuator_details = {
            "name": actuator_name,
            "weight": weight,
            "slots": slots,
            "location": location,
            "bvb": location,
            "part": part,
            "allowed": allowed,
            "fixed": fixed,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "actuator_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(actuator_details)
    return {actuator_name: actuator_details}

def find_actuator_type(data):
    custom = data.get("Custom", {})

    for key, value in custom.items():
        if "Actuator" in key and isinstance(value, dict):
            t = value.get("Type")
            if isinstance(t, str):
                return t.replace("Part", "", 1)

    return ""

if __name__ == "__main__":
    #print(actuator_dir_list)
    actuator_directories = actuator_dir_list
    processed_list = process_actuator_files(actuator_directories)
    pp(processed_list)