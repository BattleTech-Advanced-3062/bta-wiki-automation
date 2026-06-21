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
                                                            
def process_airdrop_files(directories):
    airdrop_dict = {}
    excluded_files = {"Gear_Airdrop_Beacon_BA.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Airdrop")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        airdrop_entry = parse_airdrop_json(file_path, bonuses)
                        airdrop_dict.update(airdrop_entry)

    airdrop_dict = dict(sorted(airdrop_dict.items(), key=lambda item: item[1]['name']))
    return airdrop_dict

def parse_airdrop_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        airdrop_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "None")
        slots = data.get("InventorySize", "None")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        #pp(effects_list)
        resolve = genUtilities.extract_bonus_value(effects_list, "AbilityResolveCost")
        cbills = genUtilities.extract_bonus_value(effects_list, "AbilityCBillCost")
        range = disambiguate_range(effects_list, "AirdropRange")
        drops = disambiguate_drops(effects_list, "AirdropCount")
        remove_effects = {"AbilityResolveCost", "AbilityCBillCost", "AirdropCount", "AirdropRange", "AirdropBARange", "AirdropBACount", "RequiresOmni"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        airdrop_details = {
            "name": airdrop_name,
            "weight": weight,
            "slots": slots,
            "resolve": resolve,
            "cbills": cbills,
            "range": range,
            "drops": drops,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "airdrop_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(airdrop_details)
    return {airdrop_name: airdrop_details}

def disambiguate_range(list, value):

    for entry in list:
        if entry.startswith("AirdropRange"):
            return genUtilities.extract_bonus_value(list, "AirdropRange")

    for entry in list:
        if entry.startswith("AirdropBARange"):
            return genUtilities.extract_bonus_value(list, "AirdropBARange")

    return None

def disambiguate_drops(list, value):

    for entry in list:
        if entry.startswith("AirdropCount"):
            return genUtilities.extract_bonus_value(list, "AirdropCount")

    for entry in list:
        if entry.startswith("AirdropBACount"):
            return genUtilities.extract_bonus_value(list, "AirdropBACount")

    return None

if __name__ == "__main__":
    airdrop_directories = airdrop_dir_list
    processed_list = process_airdrop_files(airdrop_directories)
   # pp(processed_list)