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
                                                            
def process_engine_files(directories):
    engine_dict = {}
    excluded_files = {"Gear_Cockpit_SensorsTC_Standard.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("emod_engineslots")
                    and file.endswith(".json")
                    and "size" not in file
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        engine_entry = parse_engine_json(file_path, bonuses)
                        engine_dict.update(engine_entry)

    engine_dict = dict(sorted(engine_dict.items(), key=lambda item: item[1]['name']))
    return engine_dict

def parse_engine_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        engine_name = data.get("Description", {}).get("Name", "unknown")
        weight_factor = get_weight_factor(data)
        ct_slots = data.get("InventorySize", "None")
        st_slots = get_engine_slot_size(data)
        fixed = "Yes" if "no_salvage" in data.get("Custom").get("Flags", []) else "No"
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"EngineWeight", "EngineReserved", "IsCockpit", "IsSensorsB", "IsSensorsA", "TorsoMount"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        engine_details = {
            "name": engine_name,
            "weight_factor": weight_factor,
            "ct_slots": ct_slots,
            "rt_slots": st_slots,
            "lt_slots": st_slots,
            "fixed": fixed,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "engine_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(engine_details)
    return {engine_name: engine_details}

def get_weight_factor(data):
    weight_factor = data.get('Custom', {}).get('Weights', {}).get('EngineFactor')
    return format_percentage(weight_factor) if weight_factor is not None else "N/A"

def format_percentage(x):
    return f"{(float(x) - 1) * 100:+.0f}%"

def get_engine_slot_size(data):
    links = data.get("Custom", {}).get("Linked", {}).get("Links", [])

    for link in links:
        component_id = link.get("ComponentDefId", "")
        match = re.search(r"emod_engineslots_size(\d+)$", component_id)
        if match:
            return match.group(1)

    return "N/A"

if __name__ == "__main__":
    engine_directories = engine_dir_list
    processed_list = process_engine_files(engine_directories)
    pp(processed_list)