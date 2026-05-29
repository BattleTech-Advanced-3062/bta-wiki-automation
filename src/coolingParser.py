import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
                                                            
def process_ecooling_files(directory):
    ecooling_dict = {}
    excluded_files = {}
    pp(directory)
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("emod_engine_cooling")
                and file.endswith(".json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                pp(file_path)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                        continue

                    ecooling_entry = parse_ecooling_json(file_path, bonuses)
                    ecooling_dict.update(ecooling_entry)
    
    #ecooling_dict = dict(sorted(ecooling_dict.items(), key=lambda item: item[1]['location']))
    return ecooling_dict

def parse_ecooling_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        ecooling_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        ecooling_details = {
            "name": ecooling_name,
            "weight": weight,
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ecooling_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(ecooling_details)
    return {ecooling_name: ecooling_details}



if __name__ == "__main__":
    processed_list = process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    pp(processed_list)