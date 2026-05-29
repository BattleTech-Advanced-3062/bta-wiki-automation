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

def process_exchanger_files(directory):
    exchanger_dict = {}
    excluded_files = {}
    extra_file = bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/Gear_HeatSink_Heat_Controller.json"
    pp(extra_file)
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("Gear_HeatSink_Generic_Thermal-Exchanger")
                and file.endswith(".json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                pp(file_path)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                        continue

                    exchanger_entry = parse_exchanger_json(file_path, bonuses)
                    exchanger_dict.update(exchanger_entry)
    
    extra_entry = parse_exchanger_json(extra_file, bonuses)
    exchanger_dict.update(extra_entry)
    #ecooling_dict = dict(sorted(ecooling_dict.items(), key=lambda item: item[1]['location']))
    return exchanger_dict

def process_kit_files(directories):
    kit_dict = {}
    excluded_files = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("emod_kit")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        kit_entry = parse_kit_json(file_path, bonuses)
                        kit_dict.update(kit_entry)
    
    #kit_dict = dict(sorted(kit_dict.items(), key=lambda item: item[1]['location']))
    return kit_dict

def process_bank_files(directory):
    bank_dict = {}
    excluded_files = {}
    extra_file = bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/Gear_HeatSink_Heat_Negator.json"
    pp(extra_file)
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("Gear_HeatSink_Generic_")
                and file.endswith("Bank.json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                pp(file_path)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                        continue

                    bank_entry = parse_bank_json(file_path, bonuses)
                    bank_dict.update(bank_entry)
    
    extra_entry = parse_bank_json(extra_file, bonuses)
    bank_dict.update(extra_entry)
    #ecooling_dict = dict(sorted(ecooling_dict.items(), key=lambda item: item[1]['location']))
    return bank_dict

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

def parse_exchanger_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        exchanger_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        exchanger_details = {
            "name": exchanger_name,
            "weight": weight,
            "slots": slots,
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ecooling_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(ecooling_details)
    return {exchanger_name: exchanger_details}

def parse_kit_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        kit_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")        
        validity = get_valid_hs(data.get("Custom", {}).get("Cooling", {}).("HeatSinkDefID", "unknown"), file_path)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        kit_details = {
            "name": kit_name,
            "weight": weight,
            "validity": validity
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "kit_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(kit_details)
    return {kit_name: kit_details}

def parse_bank_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        bank_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        bank_details = {
            "name": bank_name,
            "weight": weight,
            "slots": slots,
            "effects": genUtilities.map_details(bonuses, effects_list, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ecooling_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(ecooling_details)
    return {bank_name: bank_details}

def get_valid_hs(heatsink, filepath):
    dir_path = os.path.dirname(file_path)
    filename = dir_path + heatsink + ".json"
    with open(filename, 'r') as file:
        data = json.load(file)
        hs_name = data.get("Custom", {}).get("EngineHeatSink", {}).get("FullName", "unknown")
    
    return hs_name

if __name__ == "__main__":
    #processed_list = process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    processed_list = process_exchanger_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/heatsinks/")

    pp(processed_list)