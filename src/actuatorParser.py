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
    excluded_files = {"Gear_Actuator_LifterClamp.json", "Gear_Actuator_Backhoe.json", "Gear_Actuator_LiftHoist.json"}

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
    
    actuator_dict = dict(sorted(actuator_dict.items(), key=lambda item: item[1]['location']))
    return actuator_dict

def parse_actuator_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        actuator_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        location = get_part_category(data)
        part = get_part_category(data)
        allowed = data.get("AllowedLocations", "unknown")
        salvageable = "No" if "no_salvage" in data.get("Custom").get("Flags", []) else "Yes"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        #remove_effects = {"Initiative", "Health", "IsCockpit", "IsSensorsB", "IsSensorsA", "TorsoMount"}
        #effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        actuator_details = {
            "name": actuator_name,
            "weight": weight,
            "slots": slots,
            "location": location,
            "allowed": allowed,
            "salvageable": salvageable,
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "actuator_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(actuator_details)
    return {actuator_name: actuator_details}

def get_part_category(data):
    categories = data.get("Custom", {}).get("Category", [])

    for category in categories:
        category_id = category.get("CategoryID", "")

        if "Leg" in category_id or "Arm" in category_id:
            result = category_id.replace("Actuator", "")

            # Transform combined names
            replacements = {
                "ArmUpper": "Upper Arm",
                "ArmLower": "Lower Arm",
                "LegUpper": "Upper Leg",
                "LegLower": "Lower Leg",
            }

            for old, new in replacements.items():
                result = result.replace(old, new)

            # Remove Arm/Leg unless Upper or Lower exists
            if "Upper" not in result and "Lower" not in result:
                result = result.replace("Leg", "", 1)
                result = result.replace("Arm", "", 1)

            return result.strip()

    return None

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