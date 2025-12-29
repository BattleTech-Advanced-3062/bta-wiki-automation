import os
import sys
import json
from pprint import pp
import genUtilities
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
                        if "BLACKLISTED" not in data.get("ComponentTags", {}).get("items", []) or "Modes" not in data:
                            weapon_entry = parse_weapon_json(file_path)
                            weapon_dict.update(weapon_entry)
    return weapon_dict
                    
def parse_weapon_json(file_path):
    descriptions = genUtilities.transform_settings_to_descriptions(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json")
    with open(file_path, 'r') as file:
        data = json.load(file)
        weapon_name = data.get("Description", {}).get("UIName", "unknown")
        weapon_details = {
            "name": data.get("Description", {}).get("UIName", "unknown"),
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



if __name__ == "__main__":
    weapon_dir_list = bta_dir + "BT Advanced Gear"
    result = process_weapon_files(weapon_dir_list)
    pp(result)