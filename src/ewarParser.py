import os
import math
import sys
import json
import re
from pprint import pp
import genUtilities
from settings import *
from fnmatch import fnmatch

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")

def process_all_ewar():
    list_of_dicts = {}
    ecms = {"ecms": process_ecm_files(ecm_dir_list)}
    list_of_dicts.update(ecms)
    probes = {"probes": process_probe_files(probe_dir_list)}
    list_of_dicts.update(probes)

    return list_of_dicts

def process_ecm_files(directories):
    ecm_dict = {}
    excluded_patterns = {"", ""}
    extra_files = [bta_dir + "BT Advanced Gear/upgrade/general/Gear_Sensors_StealthField.json", bta_dir + "BT Advanced Gear/upgrade/general/Gear_Guardian_ECM_SLDF.json", bta_dir + "BT Advanced Unique Mechs/upgrade/Gear_Blackbeard_Raven.json"]

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith(("Gear"))
                    and file.endswith(".json")
                    #and not any(fnmatch(file, pattern) for pattern in excluded_patterns)
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                                continue
                        
                        categories = data.get("Custom", {}).get("Category", [])
                        if isinstance(categories, dict):
                            categories = [categories]
                        elif categories is None:
                            categories = []
                        if any(category.get("CategoryID") == "ECM" for category in categories):
                            ecm_entry = parse_ecm_json(file_path, bonuses)
                            ecm_dict.update(ecm_entry)

    for extra_file in extra_files:
        extra_entry = parse_ecm_json(extra_file, bonuses)
        ecm_dict.update(extra_entry)
    ecm_dict = dict(sorted(ecm_dict.items(), key=lambda item: item[1]['name']))
    return ecm_dict

def parse_ecm_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        ecm_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "None")
        slots = data.get("InventorySize", "None")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        salvageable = "No" if "no_salvage" in data.get("Custom").get("Flags", []) else "Yes"
        remove_effects = {"C3Jamming"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        # Auras too complicated to try parsing for limited pay off
        #auras = extract_aura_effects(data)
        ecm_details = {
            "name": ecm_name,
            "weight": weight,
            "slots": slots,
            "salvageable": salvageable,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, "Long") or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ecm_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(ecm_details)
    return {ecm_name: ecm_details}

# def extract_aura_effects(data):
#     results = []

#     for aura in data.get("Auras", []):
#         aura_data = {
#             "name": aura.get("Name"),
#             "range": aura.get("Range"),
#             "statusEffects": []
#         }

#         for effect in aura.get("statusEffects", []):
#             description = effect.get("Description", {})
#             statistic_data = effect.get("statisticData", {})

#             aura_data["statusEffects"].append({
#                 "descriptionId": description.get("Id"),
#                 "details": description.get("Details"),
#                 "statName": statistic_data.get("statName"),
#                 "operation": statistic_data.get("operation"),
#                 "modValue": statistic_data.get("modValue")
#             })

#         results.append(aura_data)

#     return results

def process_probe_files(directories):
    probe_dict = {}
    excluded_patterns = {"", ""}
    extra_files = [bta_dir + "BT Advanced Unique Mechs/upgrade/Gear_Blackbeard_Raven.json"]

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith(("Gear"))
                    and file.endswith(".json")
                    #and not any(fnmatch(file, pattern) for pattern in excluded_patterns)
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                                continue
                        
                        categories = data.get("Custom", {}).get("Category", [])
                        if isinstance(categories, dict):
                            categories = [categories]
                        elif categories is None:
                            categories = []
                        if any(category.get("CategoryID") == "Probe" for category in categories):
                            probe_entry = parse_probe_json(file_path, bonuses)
                            probe_dict.update(probe_entry)
    for extra_file in extra_files:
        extra_entry = parse_probe_json(extra_file, bonuses)
        probe_dict.update(extra_entry)
    probe_dict = dict(sorted(probe_dict.items(), key=lambda item: item[1]['name']))
    return probe_dict

def parse_probe_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        probe_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "None")
        slots = data.get("InventorySize", "None")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        sensor_range = genUtilities.extract_bonus_value(effects_list, "Sensors")
        sight_range = genUtilities.extract_bonus_value(effects_list, "Sight")
        probe_heat = genUtilities.extract_bonus_value(effects_list, "ProbeHeat")
        probe_bubble = genUtilities.extract_bonus_value(effects_list, "ProbeBubble")
        salvageable = "No" if "no_salvage" in data.get("Custom").get("Flags", []) else "Yes"
        remove_effects = {"Sensors", "Sight", "ProbeHeat", "ProbeBubble"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        #auras = extract_aura_effects(data)
        probe_details = {
            "name": probe_name,
            "weight": weight,
            "slots": slots,
            "sensor_range": sensor_range,
            "sight_range": sight_range,
            "probe_heat": probe_heat,
            "probe_bubble": probe_bubble,
            "salvageable": salvageable,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, "Long") or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "probe_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(probe_details)
    return {probe_name: probe_details}    

if __name__ == "__main__":
    processed_list = process_all_ewar()
    pp(processed_list)