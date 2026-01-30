import os
import sys
import json
from pprint import pp
import genUtilities
from collections import defaultdict
from settings import *
import math
import re
import copy

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

                        weapon_entry = expand_coil_modes(weapon_entry)
                        #weapon_entry = sort_coil_modes(weapon_entry)

                        weapon_dict.update(weapon_entry)

    return weapon_dict


def sort_coil_modes(entry: dict) -> dict:
    """
    Accepts a single-entry dict:
    { "<weapon_key>": { weapon_data } }

    Sorts weapon["modes"] numerically by pip count.
    Returns the entry.
    """

    weapon = next(iter(entry.values()))
    if weapon.get("name") != "COIL":
        return entry

    modes = weapon.get("modes")

    if not isinstance(modes, dict):
        return entry

    def sort_key(item):
        key, mode = item

        # Off (or anything without pips) comes first
        if "Id" not in mode:
            return (0, 0)

        m = re.search(r"(On|Over):\s*(\d+)\s*Pips", mode["Id"])
        if not m:
            return (0, 0)

        mode_type, pips = m.groups()

        # Order: Off -> On -> Over
        type_order = {"On": 1, "Over": 2}

        return (type_order.get(mode_type, 0), int(pips))

    weapon["modes"] = dict(sorted(modes.items(), key=sort_key))

    return entry

def expand_coil_modes(entry: dict) -> dict:
    """
    Accepts a single-entry dict:
    { "<weapon_key>": { weapon_data } }

    If weapon is COIL, returns TWO entries:
      - "COIL - On"
      - "COIL - Over"

    Otherwise, returns the entry unchanged.
    """

    # Single-entry dict by contract
    weapon_key, weapon = next(iter(entry.items()))

    if weapon.get("name") != "COIL":
        return entry

    base_damage = weapon.get("damage", 30)
    base_heat = weapon.get("heat", 30)

    results = {}

    # -------- ON VARIANT --------
    on_weapon = copy.deepcopy(weapon)
    on_weapon["name"] = "COIL - On"
    on_weapon["modes"] = {}

    for n in range(1, 13):
        on_weapon["modes"][n] = {
            "Id": n,
            "isBaseMode": False,
            "DamagePerShot": round((base_damage * (n ** 0.75)) - base_damage, 2),
            "HeatGenerated": round((base_heat * (n ** 0.80)) - base_heat, 2),
        }

    results["COIL - On"] = on_weapon

    # -------- OVER VARIANT --------
    over_weapon = copy.deepcopy(weapon)
    over_weapon["name"] = "COIL - Over"
    over_weapon["modes"] = {}

    for n in range(1, 13):
        over_weapon["modes"][n] = {
            "Id": n,
            "isBaseMode": False,
            "DamagePerShot": round((base_damage * (n ** 1.1)) - base_damage, 2),
            "HeatGenerated": round((base_heat * (n ** 1.15)) - base_heat, 2),
        }

    results["COIL - Over"] = over_weapon
    #pp(results)
    return results


"""
def expand_coil_modes(entry: dict) -> dict:
    
    Accepts a single-entry dict:
    { "<weapon_key>": { weapon_data } }

    Mutates COIL modes in place.
    Always returns the entry.
    

    # Single-entry dict by contract
    weapon = next(iter(entry.values()))

    if weapon.get("name") != "COIL":
        return entry

    base_damage = weapon.get("damage", 30)
    base_heat = weapon.get("heat", 30)

    # Ensure modes is a dict
    modes = weapon.get("modes") or {}
    weapon["modes"] = modes

    # Remove existing scalar modes
    modes.pop("On", None)
    modes.pop("Over", None)

    for n in range(1, 13):
        # ON modes
        modes[f"{n} Pips (On)"] = {
            "Id": f"On: {n} pips",
            "isBaseMode": False,
            "DamagePerShot": round((base_damage * (n ** 0.75)) - base_damage, 2),
            "HeatGenerated": round((base_heat * (n ** 0.80)) - base_heat, 2),
        }

        # OVER modes
        modes[f"Over: {n} Pips"] = {
            "Id": f"Over: {n} pips",
            "isBaseMode": False,
            "DamagePerShot": round((base_damage * (n ** 1.1)) - base_damage, 2),
            "HeatGenerated": round((base_heat * (n ** 1.15)) - base_heat, 2),
        }

    return entry
"""
                   

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

        # Special-case COIL variants
        if attrs.get("name") in ("COIL", "COIL - On", "COIL - Over"):
            category = "Superweapon - COIL"

        # Special-case Experimental Assault Gauss
        elif attrs.get("name") == "Experimental Assault Gauss":
            category = "Superweapon - Experimental Assault Gauss"

        elif isinstance(category, str):
            category = category.replace("Small ", "")

        grouped[category][name] = attrs

    # Return sorted by category name
    return dict(sorted(grouped.items()))

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
            "modes": dict(
                sorted(
                    modes.items(),
                    key=lambda kv: (
                        0 if isinstance(kv[0], int) else 1,
                        kv[0]
                    )
                )
            ),

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
    pp(result)
    #cats = print_categories(grouped)
    #print(cats)
    #pp(modes)
    #pp(result)
    #pp(processed_list)
    #print("\n".join(c if c is not None else "uncategorized" for c in result))
    #print("\n".join((c if c is not None else "uncategorized").capitalize() for c in result))


