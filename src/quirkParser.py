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

def process_quirk_files(directories):
    quirk_dict = {}
    excluded_patterns = {"", ""}
    extra_files = []

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

                        if "DEPRECATED" in json.dumps(data):
                                continue
                        # Awaiting mass update from BD
                        #categories = data.get("Custom", {}).get("Category", [])
                        #if isinstance(categories, dict):
                        #    categories = [categories]
                        #elif categories is None:
                        #    categories = []
                        #if any(category.get("CategoryID") == "ECM" for category in categories):
                        quirk_entry = parse_quirk_json(file_path, bonuses)
                        quirk_dict.update(quirk_entry)

    for extra_file in extra_files:
        extra_entry = parse_quirk_json(extra_file, bonuses)
        quirk_dict.update(extra_entry)
    quirk_dict = dict(sorted(quirk_dict.items(), key=lambda item: item[1]['name']))
    return quirk_dict

def parse_quirk_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        quirk_name = data.get("Description", {}).get("UIName", "unknown")
        remove = ["Gear", "Quirk", "Attachment", "_", "/"]
        for x in remove: quirk_name = quirk_name.replace(x, "")
        title = quirk_name.replace(" ", "")
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"IsGyro", "GyroStab", "Omni", "BAMounts"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        quirk_details = {
            "name": quirk_name,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, "Long") or "None",
            "title": title
        }
        #pp(quirk_details)
    return {quirk_name: quirk_details}

if __name__ == "__main__":
    processed_list = process_quirk_files(quirk_dir_list)
    pp(processed_list)