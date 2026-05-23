import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_armor_files(directories):
    armor_dict = {}
    excluded_files = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("emod_armor")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        armor_entry = parse_armor_json(file_path, bonuses)
                        #pp(armor_entry)
                        armor_dict.update(armor_entry)

    return armor_dict

def parse_armor_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        #print("attempting: ", file_path)
        data = json.load(file)
        #pp(data)
        armor_name = data.get("Description", {}).get("Name", "unknown")
        #print(armor_name)
        weight_string = data.get("Custom", {}).get("Weights", {}).get("ArmorFactor", "None")
        formatted_weight = "None" if weight_string == "None" else format_percentage(weight_string)
        armor_string = data.get("Custom", {}).get("ArmorStructureChanges", {}).get("ArmorFactor", "None")
        formatted_armor = "None" if armor_string == "None" else format_percentage(armor_string)
        effects_list = dedupe_effects(data.get('Custom', {}).get('BonusDescriptions', []))
        #pp(effects_list)
        armor_details = {
            "name": armor_name,
            "weight_mod": formatted_weight,
            "armor_factor": formatted_armor,
            "crit_slots": data.get("Custom", {}).get("DynamicSlots", {}).get("ReservedSlots", None),
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "armor_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(armor_details)
    return {armor_name: armor_details}
        
def format_percentage(x):
    return f"{(float(x) - 1) * 100:+.0f}%"

def dedupe_effects(effects):
    duplicates = ("ArmorFactor", "ReservedSlots", "ArmorProtection")
    return [x for x in effects if not any(u in x for u in duplicates)]

    

if __name__ == "__main__":
    #print(armor_dir_list)
    armor_directories = armor_dir_list
    processed_list = process_armor_files(armor_directories)
    pp(processed_list)