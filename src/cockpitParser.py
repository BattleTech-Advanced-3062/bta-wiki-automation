import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_cockpit_files(directories):
    cockpit_dict = {}
    excluded_files = {"Gear_Cockpit_SensorsTC_Standard.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Cockpit")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        cockpit_entry = parse_cockpit_json(file_path, bonuses)
                        cockpit_dict.update(cockpit_entry)

    return cockpit_dict

def parse_cockpit_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        cockpit_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        location = data.get("AllowedLocations", "unknown")
        fixed = "Yes" if "no_salvage" in data.get("Custom").get("Flags", []) else "No"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        init = next((x.split(":", 1)[1].strip() for x in effects_list if x.startswith("Initiative:")), "0")
        injuries = next((x.split(":", 1)[1].strip() for x in effects_list if x.startswith("Health:")), "0")
        remove_effects = {"Initiative", "Health", "IsCockpit", "IsSensorsB", "IsSensorsA", "TorsoMount"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        cockpit_details = {
            "name": cockpit_name,
            "weight": weight,
            "slots": slots,
            "location": location,
            "fixed": fixed,
            "init": init,
            "injuries": injuries,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "cockpit_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(cockpit_details)
    return {cockpit_name: cockpit_details}
  

if __name__ == "__main__":
    #print(cockpit_dir_list)
    cockpit_directories = cockpit_dir_list
    processed_list = process_cockpit_files(cockpit_directories)
    pp(processed_list)