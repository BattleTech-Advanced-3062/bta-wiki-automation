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

def process_all_callins():
    list_of_dicts = {}
    airdrops = {"airdrops": process_airdrop_files(callin_dir_list)}
    list_of_dicts.update(airdrops)
    contracts = {"contracts": process_contract_files(contract_dir_list)}
    list_of_dicts.update(contracts)
    battlearmors = {"battlearmors": process_ba_files(callin_dir_list)}
    list_of_dicts.update(battlearmors)

    return list_of_dicts

def process_airdrop_files(directories):
    airdrop_dict = {}
    excluded_patterns = {"Gear_Airdrop_Beacon_BA*", "Gear_Airdrop_Beacon_Tank_UrbanAmbush*"}
    extra_file = bta_dir + "StrategicOperations/upgrade/Gear_Airdrop_Beacon_BA.json"

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith(("Gear_Airdrop_Beacon", "Gear_Strafing"))
                    and file.endswith(".json")
                    and not any(fnmatch(file, pattern) for pattern in excluded_patterns)
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        airdrop_entry = parse_airdrop_json(file_path, bonuses)
                        airdrop_dict.update(airdrop_entry)

    extra_entry = parse_airdrop_json(extra_file, bonuses)
    airdrop_dict.update(extra_entry)
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
        cbills = (genUtilities.extract_bonus_value(effects_list, "AbilityCBillCost") or genUtilities.extract_bonus_value(effects_list, "StrafingRunCBillCost"))
        range = disambiguate_range(effects_list, "AirdropRange") 
        drops = (disambiguate_drops(effects_list, "AirdropCount") or genUtilities.extract_bonus_value(effects_list, "StrafeCount"))
        remove_effects = {"AbilityResolveCost", "AbilityCBillCost", "AirdropCount", "AirdropRange", "AirdropBARange", "AirdropBACount", "RequiresOmni", "StrafingRunCBillCost", "AirdropTank", "Airdrop", "AirdropMech", "AirdropBA", "AirdropTurret", "AirdropDrone", "Strafe", "StrafeCount"}
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
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Full') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "airdrop_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(airdrop_details)
    return {airdrop_name: airdrop_details}

def process_ba_files(directories):
    ba_dict = {}
    excluded_files = {"Gear_Airdrop_Beacon_BA.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Airdrop_Beacon_BA")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        ba_entry = parse_ba_json(file_path, bonuses)
                        ba_dict.update(ba_entry)

    ba_dict = dict(sorted(ba_dict.items(), key=lambda item: item[1]['name']))
    return ba_dict

def parse_ba_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        ba_name = data.get("Description", {}).get("UIName", "unknown")
        weight = data.get("Tonnage", "None")
        slots = data.get("InventorySize", "None")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        #pp(effects_list)
        resolve = genUtilities.extract_bonus_value(effects_list, "AbilityResolveCost")
        cbills = genUtilities.extract_bonus_value(effects_list, "AbilityCBillCost")
        range = disambiguate_range(effects_list, "airdropRange")
        drops = disambiguate_drops(effects_list, "airdropCount")
        remove_effects = {"AbilityResolveCost", "AbilityCBillCost", "baCount", "AirdropRange", "AirdropBARange", "AirdropBACount", "AirdropTank", "RequiresOmni", "BASquad", "AirdropBA"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        ba_details = {
            "name": ba_name,
            "weight": weight,
            "slots": slots,
            "resolve": resolve,
            "cbills": cbills,
            "range": range,
            "drops": drops,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "ba_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(ba_details)
    return {ba_name: ba_details}

def process_contract_files(directories):
    contract_dict = {}
    excluded_files = {""}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Gear_Contract")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)
                    #pp(file_path)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        contract_entry = parse_contract_json(file_path, bonuses)
                        contract_dict.update(contract_entry)

    contract_dict = dict(sorted(contract_dict.items(), key=lambda item: item[1]['name']))
    return contract_dict

def parse_contract_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        contract_name = data.get("Description", {}).get("UIName", "unknown")
        contract_type = data.get("Description", {}).get("Model", "unknown")
        single_use = "Yes" if "ConsumeOnUse" in data.get("ComponentTags", {}).get("items",[]) else "No"
        contract_details = {
            "name": contract_name,
            "type": contract_type,
            "single_use": single_use,
            "com_content": "Yes" if "Community" in file_path else "No",
            "contract_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(contract_details)
    return {contract_name: contract_details}

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
    processed_list = process_all_callins()
    pp(processed_list)