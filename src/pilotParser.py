import os
import sys
import json
from pprint import pp
import genUtilities
from settings import *

def process_pilot_files(directories):
    pilot_dict = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith("pilot_") and file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if data.get("IsRonin", False):
                            pilot_entry = parse_pilot_json(file_path)
                            pilot_dict.update(pilot_entry)

    return pilot_dict

def lookup_unique_ability(ability):
    abilifier_dir = bta_dir + "Abilifier/abilities/"
    file_path = os.path.join(abilifier_dir, f"{ability}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                name = data.get("Description", {}).get("Name")
                details = data.get("Description", {}).get("Details")
                return name, details 
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading {file_path}: {e}")
    return None

def lookup_unique_affinity(affinity):
    abilifier_dir = bta_dir + "MechAffinity/AffinityDefs/"
    for filename in os.listdir(abilifier_dir):
        if filename.endswith(".json"):  # Assuming files are JSON
            file_path = os.path.join(abilifier_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    #print(data)
                    if data.get("affinityData", {}).get("tag") == affinity:
                        print("missions:", data.get("affinityData", {}).get("affinityLevels", [{}])[0].get("missionsRequired", None))

                    if data.get("affinityData", {}).get("tag") == affinity:
                        affinity_chassis_names = data.get("affinityData", {}).get("chassisNames", None)
                        affinity_missions = data.get("affinityData", {}).get("affinityLevels", [{}])[0].get("missionsRequired", None)
                        affinity_name = data.get("affinityData", {}).get("affinityLevels", [{}])[0].get("levelName", None)
                        affinity_description = data.get("affinityData", {}).get("affinityLevels", [{}])[0].get("decription", None)
                        return affinity_chassis_names, affinity_missions, affinity_name, affinity_description

                        """
                        affinity_chassis_names = data.get("affinityData", {}).get("chassisNames")
                        affinity_missions = data.get("affinityData", {}).get("affinityLevels[0]", {}).get("missionsRequired")
                        affinity_name = data.get("affinityData", {}).get("affinityLevels[0]", {}).get("levelName", None)
                        affinity_description = data.get("affinityData", {}).get("affinityLevels[0]", {}).get("description", None)
                        print(affinity_chassis_names, affinity_missions, affinity_name, affinity_description)
                        return affinity_chassis_names, affinity_missions, affinity_name, affinity_description
                        """
                        
                except json.JSONDecodeError:
                    print(f"Error reading JSON file: {filename}")
    
    return None  # Return None if no matching file is found


def parse_pilot_json(file_path):
    ability_mapping = {
        "AbilityDefG5": "multitarget",
        "AbilityDefG5a": "battlelord",
        "AbilityDefG8": "precisionmaster",
        "AbilityDefG8b": "ballisticmaster",
        "AbilityDefG8a": "energymaster",
        "AbilityDefG8c": "missilemaster",
        "AbilityDefG10a": "stonecold",
        "AbilityDefP5": "surefooting",
        "AbilityDefP5a": "phantom",
        "AbilityDefP10": "acepilot",
        "AbilityDefP8a": "sprinter",
        "AbilityDefGu5": "bulwark",
        "AbilityDefGu5a": "shieldedstance",
        "AbilityDefGu8": "juggernaut",
        "AbilityDefGu8a": "brawler",
        "AbilityDefGu10a": "defensiveformation",
        "AbilityDefT5A": "sensorlock",
        "AbilityDefT5Aa": "targetprediction",
        "AbilityDefT8A": "mastertactician",
        "AbilityDefT8Aa": "knifefighter",
        "AbilityDefT10Aa": "eagleeye",
        "AbilityDefG5T": "intensifyfirepower",
        "AbilityDefG8T": "perfecttargeting",
        "AbilityDefG10T": "overwhelmingaggression",
        "AbilityDefP5T": "sideslip",
        "AbilityDefGu8T": "streetracer",
        "AbilityDefP10T": "spotter",
        "AbilityDefGu5T": "redundantcomponents",
        "AbilityDefP8T": "bruteforce",
        "AbilityDefGu10T": "hulldown",
        "AbilityDefT8T": "sensorsweep",
        "AbilityDefT5T": "targetpainting",
        "AbilityDefT10T": "commandandcontrol"
    }

    excluded_pilot_tags = {
        "pilot_kurita",
        "pilot_liao",
        "pilot_davion",
        "pilot_marik",
        "pilot_steiner",
        "pilot_backer",
        "pilot_periphery",
        "pilot_magistracy",
        "pilot_taurian",
        "pilot_comstar",
        "pilot_vehicle_crew",
        "pilot_mechwarrior",
        "pilot_starter"
    }

    affinity_mech_mapping = {
        "chrPrfMech_commandoBase-001_25": "Commando",
        "chrPrfMech_kingcrabBase-001_100": "King Crab",
        "chrPrfMech_archerBase-001_70": "Archer",
        "chrPrfMech_cataphractBase-001_70": "Cataphract",
        "ValkyrieII_60": "Valkyrie II",
        "Hatchetman_45": "Hatchetman",
        "Corsair_55": "Corsair (55t)",
        "Corsair_75": "Corsair (75t)",
        "Corsair_95": "Corsair (95t)",
        "GreatTurtle_100": "Great Turtle",
        "Mackie_100": "Mackie",
        "MackieII_105": "Mackie II",
        "chrPrfMech_crabBase-001_50": "Crab",
        "NightChanter_45": "Night Chanter"
    }

    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the Description.Callsign as the key
    callsign = data.get("Description", {}).get("Callsign", "Unknown")

    # Map the required fields to their respective values
    pilot_details = {
        "callsign": data.get("Description", {}).get("Callsign"),
        "firstname": data.get("Description", {}).get("FirstName"),
        "lastname": data.get("Description", {}).get("LastName"),
        "age": data.get("Description", {}).get("Age"),
        "gender": data.get("Description", {}).get("Gender"),
        "faction": data.get("Description", {}).get("Faction"),
        "biography": data.get("Description", {}).get("Details"),
        "health": data.get("Health"),
        "gunnery": data.get("BaseGunnery"),
        "piloting": data.get("BasePiloting"),
        "guts": data.get("BaseGuts"),
        "tactics": data.get("BaseTactics"),
    }

    # Check for abilities and add them to pilot details
    ability_def_names = data.get("abilityDefNames", [])
    for ability in ability_def_names:
        if ability.startswith("AbilityDef") and ability not in ability_mapping:
            custom_ability_name, custom_ability_details = lookup_unique_ability(ability)
            pilot_details["custom_ability_name"] = custom_ability_name
            pilot_details["custom_ability_details"] = custom_ability_details
        if ability in ability_mapping:
            pilot_details[ability_mapping[ability]] = ability_mapping[ability]
    
    
    # Process pilot tags
    pilot_tags = data.get("PilotTags", {}).get("items", [])
    print(pilot_tags)
    
    affinity_tag = None
    for tag in pilot_tags:
        if tag.startswith("Affinity_"):
            affinity_tag = tag
            break
            
    print("Affinity Tag: ", affinity_tag)
    if affinity_tag is not None:
        #result = lookup_unique_affinity(affinity_tag)
        #print("Result:", result)
        affinity_chassis_names, affinity_missions, affinity_name, affinity_description = lookup_unique_affinity(affinity_tag)
        if len(affinity_chassis_names) > 1:
            affinity_chassis_names = [affinity_mech_mapping.get(chassis, "None") for chassis in affinity_chassis_names]
            affinity_chassis_names = "/".join(map(str, affinity_chassis_names))
        else:
            affinity_chassis_names = affinity_chassis_names[0]
            affinity_chassis_names = affinity_mech_mapping.get(affinity_chassis_names, "None")  

        if affinity_name:
            pilot_details["custom_affinity_name"] = affinity_name
            pilot_details["custom_affinity_details"] = affinity_description
            pilot_details["custom_affinity_mech"] = affinity_chassis_names
            pilot_details["custom_affinity_missions"] = affinity_missions
            pilot_details["custom_affinity_mech"] = affinity_chassis_names
    

    tag_counter = 1
    for tag in pilot_tags:
        if "pilot_starter" in tag:
            pilot_details["availability"] = "Part of the <b>Original Adventurers</b> character origins starting option. Can also be found as a random starting pilot or in hiring halls."
        elif "pilot_btateam" in tag:
            pilot_details["availability"] = "Part of the <b>Pioneering Comrades</b> character origins starting option. Can also be found as a random starting pilot or in hiring halls."
        elif "pilot_radio" in tag:
            pilot_details["availability"] = "Part of the <b>Radio Crew</b> character origins starting option. Can also be found as a random starting pilot or in hiring halls."
        elif tag.startswith("pilot_") and tag not in excluded_pilot_tags:
            formatted_tag = tag.replace("pilot_", "").capitalize()
            pilot_details[f"pilottag{tag_counter}"] = formatted_tag
            tag_counter += 1

    return {callsign: pilot_details}

if __name__ == "__main__":
    result = process_pilot_files(pilot_dir_list)
    #result = parse_pilot_json(sys.argv[1])
    pp(result)

