import os
import sys
import json
from pprint import pp
import genUtilities
from collections import defaultdict
from settings import *

bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
categories = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/categories/Categories_Weapons.json",
                                                                      "Settings", "Name")

def process_weapon_files(directories):
    weapon_dict = {}
    excluded_files = {"Weapon_DFAAttack.json", "Weapon_MeleeAttack.json", "Weapon_MeleeAttackEx.json", "Weapon_Laser_AI_Imaginary.json"}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if (
                    file.startswith("Weapon_")
                    and file.endswith(".json")
                    and file not in excluded_files
                ):
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                        weapon_entry = parse_weapon_json(
                            file_path, bonuses, categories
                        )
                        weapon_dict.update(weapon_entry)

    return weapon_dict
                    
def parse_weapon_json(file_path, bonuses, categories):
    with open(file_path, 'r') as file:
        #print("attempting: ", file_path)
        data = json.load(file)
        weapon_name = data.get("Description", {}).get("UIName", "unknown")
        weapon_details = {
            "filepath": os.path.splitext(os.path.basename(file_path))[0],
            "name": data.get("Description", {}).get("UIName", "unknown"),
            "category": genUtilities.map_categories(categories, data.get("Custom", {}).get("Category"), "DisplayName"),# or data.get("weaponCategoryID"),
            "ammo": "None" if data.get("AmmoCategory") == "NotSet" else data.get("AmmoCategory"),
            "hardpoint": data.get("weaponCategoryID", data.get("Category")),
            "tonnage": data.get("Tonnage"),
            "slots": data.get("InventorySize"),
            "damage": data.get("Damage"),
            "heatdamage": data.get("HeatDamage"),
            "instability": data.get("Instability"),
            "shots": data.get("ShotsWhenFired"),
            "projectiles": data.get("ProjectilesPerShot"),
            "heat": data.get("HeatGenerated"),
            "recoil": data.get("RefireModifier"),
            "accuracy": data.get('AccuracyModifier'),
            "evasionignored": data.get("EvasivePipsIgnored"),
            "bonuscritchance": genUtilities.format_crit_chance(data.get('CriticalChanceMultiplier', 1)),
            "rangemin": data.get("MinRange"),
            "rangeshort": (data.get("RangeSplit") or [0, 0, 0])[0],
            "rangemedium": (data.get("RangeSplit") or [0, 0, 0])[1],
            "rangelong": (data.get("RangeSplit") or [0, 0, 0])[2],
            "rangemax": data.get("MaxRange"),
            "firesinmelee": "No" if data.get("MinRange", 0) != 0 or data.get("AOECapable") else "Yes",
            "additionalinfo": genUtilities.map_details(bonuses, data.get('Custom', {}).get('BonusDescriptions', []), 'Full'),
            "modes": genUtilities.normalize_modes(data.get("Modes"))
        }
    # print(weapon_details)
    return {weapon_name: weapon_details}

def group_by_category(data: dict) -> dict:
    grouped = defaultdict(dict)

    for name, attrs in data.items():
        category = attrs.get("category")

        if isinstance(category, str):
            category = category.replace("Small ", "")

        grouped[category][name] = attrs

    return dict(sorted(grouped.items()))

'''
def split_modes(grouped: dict) -> dict:
    result = {}

    for category, weapons in grouped.items():
        non_modes = {}
        modes = {}

        for name, attrs in weapons.items():
            if attrs.get("modes"):
                modes[name] = attrs
            else:
                non_modes[name] = attrs

        result[category] = {
            "non_modes": non_modes,
            "modes": modes,
        }

    return result
'''
def split_modes(grouped: dict) -> dict:
    result = {}

    for category, weapons in grouped.items():
        non_modes = {}
        modes = defaultdict(dict)

        for name, attrs in weapons.items():
            weapon_modes = attrs.get("modes")

            if not weapon_modes:
                non_modes[name] = attrs
                continue

            for mode_name, mode_data in weapon_modes.items():
                modes[mode_name][name] = {
                    **attrs,
                    "active_mode": mode_data
                }

        result[category] = {
            "non_modes": non_modes,
            "modes": dict(sorted(modes.items())),
        }

    return result

def print_categories(grouped: dict, label: str = "uncategorized") -> None:
    for category, items in grouped.items():
        if category == label:
            print(f'{label}: {", ".join(items)}')
        else:
            print(category)

def get_modes(directories):
    weapon_dict = {}
    mode_keys = set()

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("Weapon_") and file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []):
                            continue

                        # Collect mode keys
                        for mode in data.get("Modes", []):
                            if isinstance(mode, dict):
                                mode_keys.update(mode.keys())

                        # Normal weapon processing
                        weapon_entry = parse_weapon_json(file_path, bonuses, categories)
                        weapon_dict.update(weapon_entry)

    return sorted(mode_keys)

if __name__ == "__main__":
    #print(weapon_dir_list)
    weapon_directories = weapon_dir_list
    processed_list = process_weapon_files(weapon_directories)
    grouped = group_by_category(processed_list)
    result = split_modes(grouped)
    modes = get_modes(weapon_directories)
    pp(grouped)
    #cats = print_categories(grouped)
    #print(cats)
    #pp(modes)
    #pp(result)
    #pp(processed_list)
    #print("\n".join(c if c is not None else "uncategorized" for c in result))
    #print("\n".join((c if c is not None else "uncategorized").capitalize() for c in result))


