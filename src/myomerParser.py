import os
import json
from pprint import pp
import genUtilities
from settings import *
import csv

prefixes = ["itemCollection_", "ItemCollection_", "BTA_"]
csv_files_index = genUtilities.index_csv_files(csv_dir_list)
bonuses = genUtilities.transform_settings_to_details(bta_dir + "BT Advanced Core/settings/bonusDescriptions/BonusDescriptions_MechEngineer.json", 
                                                                   "Settings", "Bonus")
          
def process_all_speed():
    list_of_dicts = {}
    myomers = {"myomers": process_myomer_files(myomer_dir_list)}
    list_of_dicts.update(myomers)
    superchargers = {"superchargers": process_supercharger_files(myomer_dir_list)}
    list_of_dicts.update(superchargers)
    #battlearmors = {"battlearmors": process_ba_files(callin_dir_list)}
    #list_of_dicts.update(battlearmors)

    return list_of_dicts

def process_myomer_files(directories):
    myomer_dict = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                    categories = data.get("Custom", {}).get("Category", [])
                    #print(type(categories), categories)
                    if isinstance(categories, dict):
                        categories = [categories]
                    elif categories is None:
                        categories = []
                    if any(category.get("CategoryID") == "Myomer" for category in categories):
                        myomer_entry = parse_myomer_json(file_path, bonuses)
                        myomer_dict.update(myomer_entry)
    myomer_dict = dict(sorted(myomer_dict.items(), key=lambda item: item[1]['name']))
    return myomer_dict

def parse_myomer_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        myomer_name = data.get("Description", {}).get("Name", "unknown")
        myomer_UIname = data.get("Description", {}).get("UIName", "unknown")
        id = data.get("Description", {}).get("Id", "N/A")
        parents = build_parent_index(csv_files_index)
        faction_collection = find_collection_by_type(id, parents, "faction")
        faction_id_lookup = look_up_collection(faction_collection) if faction_collection else None
        #factory_collection = find_collection_by_type(id, parents, "factory")
        #factory_id_lookup = look_up_collection(factory_collection) if factory_collection else None
        #print(f"Found {id} in {facttory_id_lookup}")
        #pp(factory_collection)
        #id_lookup = look_up_collection(collection) if collection else None
        #pp(id_lookup)
        slots = data.get('Custom', {}).get('DynamicSlots', {}).get('ReservedSlots', 0)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Dynamic", "SetReservedSlotsFullBody"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        myomer_details = {
            "name": myomer_name,
            "UIname": myomer_UIname,
            "slots": slots,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Long') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "myomer_ID": id,
            "faction_store": faction_id_lookup
        }
        #pp(myomer_details)
    return {myomer_name: myomer_details}

def process_supercharger_files(directories):
    supercharger_dict = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "BLACKLISTED" in data.get("ComponentTags", {}).get("items", []) or "DEPRECATED" in json.dumps(data):
                            continue

                    categories = data.get("Custom", {}).get("Category", [])
                    #print(type(categories), categories)
                    if isinstance(categories, dict):
                        categories = [categories]
                    elif categories is None:
                        categories = []
                    if any(category.get("CategoryID") == "Supercharger" for category in categories):
                        supercharger_entry = parse_supercharger_json(file_path, bonuses)
                        supercharger_dict.update(supercharger_entry)
    supercharger_dict = dict(sorted(supercharger_dict.items(), key=lambda item: item[1]['name']))
    return supercharger_dict

def parse_supercharger_json(file_path, bonuses):
    with open(file_path, 'r') as file:
        data = json.load(file)
        supercharger_name = data.get("Description", {}).get("UIName", "unknown")
        slots = data.get('Custom', {}).get('DynamicSlots', {}).get('ReservedSlots', 0)
        locations = data.get("AllowedLocations", "unknown")
        slot_locations = genUtilities.get_linked_location_counts(data)
        explosions = genUtilities.get_explosion_damage(data)
        effects_list = data.get('Custom', {}).get('BonusDescriptions', [])
        remove_effects = {"Dynamic", "SetReservedSlotsFullBody"}
        effects_list_cleaned = [x for x in effects_list if x.split(":", 1)[0] not in remove_effects]
        #pp(effects_list_cleaned)
        supercharger_details = {
            "name": supercharger_name,
            "slots": slots,
            "locations": locations.replace(", ", "</br>"),
            "slot_locations": slot_locations,
            "explosions": explosions,
            "effects": genUtilities.map_details(bonuses, effects_list_cleaned, 'Full') or "None",
            "com_content": "Yes" if "Community" in file_path else "No",
            "supercharger_ID": data.get("Description", {}).get("Id", "N/A")
        }
        #pp(supercharger_details)
    return {supercharger_name: supercharger_details}


def build_parent_index(collection_files):
    """
    Returns a mapping of child collection/item -> collections that contain it.
    """
    parents = {}

    for collection_name, files in collection_files.items():
        for file_path in files:
            with open(file_path, newline="") as f:
                reader = csv.reader(f)

                for row in reader:
                    if not row:
                        continue

                    child = row[0]  # adjust if your CSV uses another column

                    parents.setdefault(child, []).append(collection_name)

    return parents

def find_collection_by_type(item, parents, store_type):
    """
    Walks upward from an item until it finds a collection containing 'faction'.
    """
    visited = set()

    def search(current):
        if current in visited:
            return None

        visited.add(current)

        for parent in parents.get(current, []):
            if store_type in parent.lower():
                return parent

            result = search(parent)
            print(f"Searching for {item} in {parent} of store type {store_type}")
            if result:
                print(f"Found {item} in {parent}")
                return result

        return None

    return search(item)

def look_up_collection(collection):
    faction = ""
    factory = ""
    if "faction" in collection:
        store = "faction"
        bta_dir + "DynamicShops/fshops/"
        faction = get_faction(bta_dir + "DynamicShops/fshops/", collection)
        print(f"Found {collection} in {faction} store")
        return faction
    elif "factory" in collection:
        store = "factory"
        for root, _, files in os.walk(bta_dir + "DynamicShops/factories/"):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    data = json.load(f)
                    factory = data[0].get("factory", "None")
        return factory
    
def get_faction(directory, item_collection):
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(root, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            # Expecting a list of faction entries
            if isinstance(data, list):
                for entry in data:
                    if entry.get("items") == item_collection:
                        return entry.get("factions")

    return None

if __name__ == "__main__":
    #print(myomer_dir_list)
    processed_list = process_all_speed()
    #pp(processed_list)
    #csv_files_index = genUtilities.index_csv_files(csv_dir_list)
    #parents = build_parent_index(csv_files_index)
    #pp(thing)
    #collection = find_collection_by_type("Gear_Airdrop_Beacon_BA_Gnome", parents)
    #pp(collection)

