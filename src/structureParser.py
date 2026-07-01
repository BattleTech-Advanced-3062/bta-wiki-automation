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
                                                            
def process_structure_files(directories):
    structure_dict = {}
    excluded_files = {"emod_structureslots_endo_standard_hybrid.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("emod_structure")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        structure_entry = parse_structure_json(file_path, bonuses)
                        structure_dict.update(structure_entry)

    structure_dict = dict(sorted(structure_dict.items(), key=lambda item: item[1]['name']))
    return structure_dict

def parse_structure_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        structure_name = data.get("Description", {}).get("Name", "unknown")
        weight_string = data.get("Custom", {}).get("Weights", {}).get("StructureFactor", "None")
        formatted_weight = "None" if weight_string == "None" else format_percentage(weight_string)
        structure_string = data.get("Custom", {}).get("ArmorStructureChanges", {}).get("StructureFactor", "None")
        formatted_structure = "None" if structure_string == "None" else format_percentage(structure_string)
        slots = data.get("Custom", {}).get("DynamicSlots", {}).get("ReservedSlots", None)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"StructureFactor", "StructureProtection", "ReservedSlots", "AirdropRange", "AirdropBARange", "AirdropBACount", "RequiresOmni"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        structure_details = {
            "name": structure_name,
            "weight_mod": formatted_weight,
            "structure_factor": formatted_structure,
            "slots": slots,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "structure_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(structure_details)
    return {structure_name: structure_details}

def format_percentage(x):
    return f"{(float(x) - 1) * 100:+.0f}%"

if __name__ == "__main__":
    structure_directories = structure_dir_list
    processed_list = process_structure_files(structure_directories)
    pp(processed_list)