import os
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_armor_files(directories):
    armor_dict = {}
    def process_armor_files(directories):
    armor_dict = {}
    excluded_files = }

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

                        armor_entry = parse_armor_json(file_path, bonuses)                        )

                        armor_dict.update(armor_entry)

    return armor_dict

def parse_armor_json(file_path, bonuses):
    with open(file_path, 'r') as file:
            #print("attempting: ", file_path)
            data = json.load(file)
            armor_name = data.get("Description", {}).get("UIName", "unknown")
            armor_details = {
                "name": armor_name
                "weight_mod": data.get("Custom", {}).get("Weights", {}).get("ArmorFactor", "None"),
                "armor_factor": data.get("Custom", {}).get("ArmorStructureChanges", {}).get("ArmorFactor", "None"),
                "crit_slots": data.get("Custom", {}).get("DynamicSlots", {}).get("ReservedSlots", None),
                "effects": genUtilities.map_details(bonuses, data.get('Custom', {}).get('BonusDescriptions', []), 'Long'),
                "com_content": "Yes" if filepath.contains("Community") else "No",
                "armorID": data.get("Description", {}).get("Id", "N/A")
            }

def format_percentage(decimal: float) -> int:
    

if __name__ == "__main__":
    #print(armor_dir_list)
    armor_directories = armor_dir_list
    processed_list = process_armor_files(armor_directories)