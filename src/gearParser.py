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
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("Weapon_") and file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if not (
                            "BLACKLISTED" in data.get("ComponentTags", {}).get("items", [])
                            or "Modes" in data
                        ):
                            weapon_entry = parse_weapon_json(file_path, bonuses, categories)
                            weapon_dict.update(weapon_entry)
    return weapon_dict
                    
def parse_weapon_json(file_path, bonuses, categories):
    with open(file_path, 'r') as file:
        #print("attempting: ", file_path)
        data = json.load(file)
        weapon_name = data.get("Description", {}).get("UIName", "unknown")
        weapon_details = {
            "filepath": os.path.basename(file_path),
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
            "accuracy": f" {data.get('AccuracyModifier')}",
            "evasionignored": data.get("EvasivePipsIgnored"),
            "bonuscritchance": f" {genUtilities.format_crit_chance(data.get('CriticalChanceMultiplier', 1))}",
            "rangemin": data.get("MinRange"),
            "rangeshort": (data.get("RangeSplit") or [0, 0, 0])[0],
            "rangemedium": (data.get("RangeSplit") or [0, 0, 0])[1],
            "rangelong": (data.get("RangeSplit") or [0, 0, 0])[2],
            "rangemax": data.get("MaxRange"),
            "firesinmelee": "No" if data.get("MinRange", 0) != 0 or data.get("AOECapable") else "Yes",
            "additionalinfo": f" {genUtilities.map_details(bonuses, data.get('Custom', {}).get('BonusDescriptions', []), 'Full')}"
        }
    # print(weapon_details)
    return {weapon_name: weapon_details}

def group_by_category(data: dict) -> dict:
    grouped = defaultdict(dict)

    for name, attrs in data.items():
        category = attrs.get("category")
        grouped[category][name] = attrs

    return dict(grouped)

def print_categories(grouped: dict, label: str = "uncategorized") -> None:
    for category, items in grouped.items():
        if category == label:
            print(f'{label}: {", ".join(items)}')
        else:
            print(category)

if __name__ == "__main__":
    #print(weapon_dir_list)
    weapon_directories = weapon_dir_list
    processed_list = process_weapon_files(weapon_directories)
    result = group_by_category(processed_list)
    print(result)
    #pp(result)
    #pp(processed_list)
    #print("\n".join(c if c is not None else "uncategorized" for c in result))
    #print("\n".join((c if c is not None else "uncategorized").capitalize() for c in result))


