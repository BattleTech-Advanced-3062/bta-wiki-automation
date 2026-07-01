import os
import math
import sys
import json
import re
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_jumpjet_files(directories):
    jumpjet_dict = {}
    excluded_files = {"Gear_Gyro_Generic_Standard.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Jump")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        jumpjet_entry = parse_jumpjet_json(file_path, bonuses)
                        jumpjet_dict.update(jumpjet_entry)

    jumpjet_dict = dict(sorted(jumpjet_dict.items(), key=lambda item: item[1]['min_tons']))
    return jumpjet_dict

def parse_jumpjet_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        jumpjet_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "None")
        slots = data.get("InventorySize", "None")
        capacity = data.get("JumpCapacity", "None")
        min_tons = data.get("MinTonnage", "None")
        max_tons = data.get("MaxTonnage", "None")
        salvageable = "No" if "no_salvage" in data.get("Custom").get("Flags", []) else "Yes"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        heat = get_jump_heat(effects_list)
        # Jump Jets per Hex: more understandable than MaxCountJJ
        jjph = get_mountable(effects_list)
        remove_effects = {"JumpCapacity", "JumpHeat", "MinWeightJJ", "MaxWeightJJ", "MaxCountJJ"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        jumpjet_details = {
            "name": jumpjet_name,
            "weight": weight,
            "slots": slots,
            "capacity": capacity,
            "heat": heat,
            "min_tons": min_tons,
            "max_tons": max_tons,
            "jjph": jjph,
            "salvageable": salvageable,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "jumpjet_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(jumpjet_details)
    return {jumpjet_name: jumpjet_details}

def get_jump_heat(effects_list):
    for entry in effects_list:
        if entry.startswith("JumpHeat:"):
            return entry.split(":", 1)[1].strip()

    return None

def get_mountable(effects_list):
    for entry in effects_list:
        if entry.startswith("MaxCountJJ:"):
            return entry.split(":", 1)[1].strip()

    return None

if __name__ == "__main__":
    jumpjet_directories = jumpjet_dir_list
    processed_list = process_jumpjet_files(jumpjet_directories)
    pp(processed_list)