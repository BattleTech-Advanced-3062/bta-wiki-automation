import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")

def process_thermalgear_files(directories):
    thermalgear_dict = {}
    excluded_files = {""}
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        thermalgear_entry = parse_thermalgear_json(file_path, bonuses)
                        thermalgear_dict.update(thermalgear_entry)
    
    thermalgear_dict = dict(sorted(thermalgear_dict.items(), key=lambda item: item[1]['weight']))
    return thermalgear_dict

def parse_thermalgear_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        thermalgear_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        explosion = genUtilities.get_explosion_damage(data)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Activatable"}
        effects_list_cleaned = [ x for x in effects_list if not any(effect in str(x) for effect in remove_effects)]
        thermalgear_details = {
            "name": thermalgear_name,
            "weight": weight,
            "slots": slots,
            "explosion": explosion,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ID": data.get("Description", {}).get("Id", "N/A")
        }
        ##pp(ecooling_details)
    return {thermalgear_name: thermalgear_details}

if __name__ == "__main__":
    processed_list = process_thermalgear_files(thermal_dir_list)
    pp(processed_list)