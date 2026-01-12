import os
import sys
import json
from pprint import pp
import genUtilities
from collections import defaultdict
from settings import *

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
                            #or "Modes" in data
                        ):
                            weapon_entry = parse_weapon_json(file_path)
                            weapon_dict.update(weapon_entry)
    return weapon_dict
                    
def parse_weapon_json(file_path):
    descriptions = genUtilities.transform_settings_to_descriptions(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json")
    with open(file_path, 'r') as file:
        #print("attempting: ", file_path)
        data = json.load(file)
        weapon_name = data.get("Description", {}).get("UIName", "unknown")
        weapon_details = {
            "filepath": os.path.basename(file_path),
            "name": data.get("Description", {}).get("UIName", "unknown"),
            "category": genUtilities.extract_weapon_category(data) or data.get("weaponCategoryID"),
            "ammo": data.get("AmmoCategory"),
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
            "accuracy": data.get("AccuracyModifier"),
            "evasionignored": data.get("EvasivePipsIgnored"),
            "bonuscritchance": (lambda v: "0" if v == 1 else f"{int((v-1)*100):+d}%")(data.get("CriticalChanceMultiplier", 1)),
            "rangemin": data.get("MinRange"),
            "rangeshort": (data.get("RangeSplit") or [0, 0, 0])[0],
            "rangemedium": (data.get("RangeSplit") or [0, 0, 0])[1],
            "rangelong": (data.get("RangeSplit") or [0, 0, 0])[2],
            "rangemax": data.get("MaxRange"),
            "firesinmelee": "No" if data.get("MinRange", 0) != 0 or data.get("AOECapable") else "Yes",
            "additionalinfo": genUtilities.map_bonus_descriptions(descriptions, data.get("Custom", {}).get("BonusDescriptions", []))
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
    pp(result)
    #pp(processed_list)
    #print("\n".join(c if c is not None else "uncategorized" for c in result))
    #print("\n".join((c if c is not None else "uncategorized").capitalize() for c in result))


