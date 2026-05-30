import os
import math
import sys
import json
from pprint import pp
import genUtilities
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")

def process_all_cooling():
    list_of_dicts = {}
    ecoolings = {"ecoolings": process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")}
    list_of_dicts.update(ecoolings)
    exchangers = {"exchangers": process_exchanger_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/heatsinks/")}
    list_of_dicts.update(exchangers)
    kits = {"kits": process_kit_files(kit_dir_list)}
    list_of_dicts.update(kits)
    banks = {"banks": process_bank_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/heatsinks/")}
    list_of_dicts.update(banks)
    heatsinks = {"heatsinks": process_heatsink_files(sink_dir_list)}
    list_of_dicts.update(heatsinks)
    
    return list_of_dicts

def process_ecooling_files(directory):
    ecooling_dict = {}
    excluded_files = {"emod_engine_cooling_7.json"}
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("emod_engine_cooling")
                and file.endswith(".json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                ##pp(file_path)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                        continue

                    ecooling_entry = parse_ecooling_json(file_path, bonuses)
                    ecooling_dict.update(ecooling_entry)
    
    ecooling_dict = dict(sorted(ecooling_dict.items(), key=lambda item: item[1]['weight']))
    return ecooling_dict

def process_exchanger_files(directory):
    exchanger_dict = {}
    excluded_files = {}
    extra_file = bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/Gear_HeatSink_Heat_Controller.json"
    ##pp(extra_file)
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("Gear_HeatSink_Generic_Thermal-Exchanger")
                and file.endswith(".json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                #pp(file_path)

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
                    ##pp(file_path)

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
    ##pp(extra_file)
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.startswith("Gear_HeatSink_Generic_")
                and file.endswith("Bank.json")
                and file not in excluded_files
            ):
                file_path = os.path.join(root, file)
                #pp(file_path)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                        continue

                    bank_entry = parse_bank_json(file_path, bonuses)
                    bank_dict.update(bank_entry)
    
    bank_dict = dict(sorted(bank_dict.items(), key=lambda item: item[1]['weight']))
    extra_entry = parse_bank_json(extra_file, bonuses)
    bank_dict.update(extra_entry)
    return bank_dict

def process_heatsink_files(directories):
    heatsink_dict = {}
    excluded_files = {}
    extra_file = bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/Gear_HeatSink_Generic_SanctuaryWorlds.json"
    ##pp(extra_file)
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_HeatSink")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    ##pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        heatsink_entry = parse_heatsink_json(file_path, bonuses)
                        heatsink_dict.update(heatsink_entry)
    
    extra_entry = parse_heatsink_json(extra_file, bonuses)
    heatsink_dict.update(extra_entry)
    heatsink_dict = dict(sorted(heatsink_dict.items(), key=lambda item: item[1]['name']))
    return heatsink_dict

def parse_ecooling_json(file_path, bonuses):
    engine_size_mapping = {
        "emod_engine_cooling_1": "275",
        "emod_engine_cooling_2": "300",
        "emod_engine_cooling_2_laser": "300",
        "emod_engine_cooling_3": "325",
        "emod_engine_cooling_4": "350",
        "emod_engine_cooling_5": "375",
        "emod_engine_cooling_6": "400"
    }
    with open(file_path, 'r') as file:
        data = json.load(file)
        ecooling_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Whitespace"}
        effects_list_cleaned = [ x for x in effects_list if not any(effect in str(x) for effect in remove_effects)]
        ecooling_ID = data.get("Description", {}).get("Id", "N/A")
        engine_size = engine_size_mapping.get(ecooling_ID)
        ecooling_details = {
            "name": ecooling_name,
            "weight": weight,
            "engine_size": engine_size,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Full') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ID": ecooling_ID
        }
        ##pp(ecooling_details)
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
            "ID": data.get("Description", {}).get("Id", "N/A")
        }
        ##pp(ecooling_details)
    return {exchanger_name: exchanger_details}

def parse_kit_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        kit_name = data.get("Description", {}).get("UIName", "unknown")
        ##pp(file_path)        
        explosion = genUtilities.get_explosion_damage(data)
        validity = get_valid_hs(data.get("Custom", {}).get("Cooling", {}).get("HeatSinkDefId", "unknown"), file_path)
        explosion = genUtilities.get_explosion_damage(data)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"CoolingSystem", "Boom", "FreezerHeatSink"}
        effects_list_cleaned = [ x for x in effects_list if not any(effect in str(x) for effect in remove_effects)]
        kit_details = {
            "name": kit_name,
            "validity": validity,
            "explosion": explosion,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ID": data.get("Description", {}).get("Id", "N/A")
        }
        ##pp(kit_details)
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
            "ID": data.get("Description", {}).get("Id", "N/A")
        }
        ##pp(ecooling_details)
    return {bank_name: bank_details}

def parse_heatsink_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        heatsink_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "0")
        slots = data.get("InventorySize", "1")
        dissipation = data.get("DissipationCapacity", "0")
        explosion = genUtilities.get_explosion_damage(data)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Dissipation", "FreezerHeatSink"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        heatsink_details = {
            "name": heatsink_name,
            "weight": weight,
            "slots": slots,
            "dissipation": dissipation,
            "explosion": explosion,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ID": data.get("Description", {}).get("Id", "N/A")
        }
    return {heatsink_name: heatsink_details}

def get_valid_hs(heatsink, filepath):
    dir_path = os.path.dirname(filepath)
    filename = dir_path + "/" + heatsink + ".json"
    with open(filename, 'r') as file:
        data = json.load(file)
        hs_name = data.get("Custom", {}).get("EngineHeatSink", {}).get("FullName", "unknown")
    
    return hs_name

if __name__ == "__main__":
    #processed_list = process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    #processed_list = process_exchanger_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/heatsinks/")
    #processed_list = process_heatsink_files(sink_dir_list)
    processed_list = process_all_cooling()

    #pp(processed_list)