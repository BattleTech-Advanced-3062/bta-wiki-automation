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
                                                            
def process_gyro_files(directories):
    gyro_dict = {}
    excluded_files = {"Gear_Gyro_Generic_Standard.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Gyro")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        gyro_entry = parse_gyro_json(file_path, bonuses)
                        gyro_dict.update(gyro_entry)

    gyro_dict = dict(sorted(gyro_dict.items(), key=lambda item: item[1]['name']))
    return gyro_dict

def parse_gyro_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        gyro_name = data.get("Description", {}).get("Name", "unknown")
        weight_type = get_weight_type(data)
        weight_value = get_weight_value(data)
        slots = data.get("InventorySize", "None")
        salvageable = "No" if "no_salvage" in data.get("Custom").get("Flags", []) else "Yes"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"EngineWeight", "EngineReserved", "Omni", "IsGyro"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        gyro_details = {
            "name": gyro_name,
            "weight_type": weight_type,
            "weight_value": weight_value,
            "slots": slots,
            "salvageable": salvageable,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "gyro_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(gyro_details)
    return {gyro_name: gyro_details}

def get_weight_type(data):
    weights = data.get("Custom", {}).get("Weights", {})

    if "StructureFactor" in weights:
        return "Chassis Weight"

    if data.get("Tonnage", 0) == 0:
        return "N/A"

    return "Flat Weight"

def get_weight_value(data):
    structure_factor = (
        data.get("Custom", {})
            .get("Weights", {})
            .get("StructureFactor")
    )

    tonnage = data.get("Tonnage")

    if structure_factor is not None:
        return format_percentage(structure_factor)

    if structure_factor is None and tonnage == 0:
        return "N/A"
    
    return str(data.get("Tonnage"))

def format_percentage(x):
    return f"{(float(x) - 1) * 100:+.0f}%"

if __name__ == "__main__":
    gyro_directories = gyro_dir_list
    processed_list = process_gyro_files(gyro_directories)
    #pp(processed_list)