import os
import sys
import json
from pprint import pp
import genUtilities

prefixes = ["itemCollection_", "ItemCollection_", "BTA_"]

def process_files(primary_path):
    factory_dict = {}
    csv_files_index = genUtilities.index_csv_files(["/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/bta/DynamicShops/", "/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/bta/Community Content/"])
    #csv_files_index = genUtilities.index_csv_files(["../DynamicShops/", "../Community Content/"])
    # Iterate through files in primary path and process each
    for file_name in os.listdir(primary_path):
        full_path = os.path.join(primary_path, file_name)
        if os.path.isfile(full_path):
            #file_dict[file_name] = []
            if file_name.startswith("factories"):
                process_Factory_Collections(full_path, factory_dict)
    for location, data in factory_dict.items():
        collection_name = data.get("item_list")
        if "items" in data:
            data["items"] = add_factory_contents(collection_name, csv_files_index, data["items"], factory_dict, prefixes)

    return factory_dict

def process_Factory_Collections(full_path, factory_dict):
    with open(full_path, "r") as json_file:
        data = json.load(json_file)
        #print("this is the data:\r\n", data)
        for block in data:
            #print("this is the block:\r\n", block)
            name = block.get('name')  # Safely fetch 'name'
            if name:  # Proceed only if 'name' exists
                conditions = block.get('conditions', {})
                factory_dict[name] = {
                    "owner": conditions.get("owner", None),
                    "rep": conditions.get("rep", None),
                    "item_list": block.get("items", None),  # Safely fetch 'items'
                    "items": []
                }
                #print("this is the factory dict:\r\n", factory_dict)
            #print("this is the factory dict:\r\n", factory_dict)
            #pp(factory_dict)
 
    #pp(factory_dict)
    return factory_dict

def add_factory_contents(collection_name, csv_files_index, item_collection_list, factory_dict, prefixes):
        # Read file and get its contents
        csv_files_index[collection_name]
        with open(csv_files_index[collection_name], 'r') as file:
            lines = file.readlines()
        # Skip the first line
        lines = lines[1:]
        # Iterate over the lines in the file
        for line in lines:
            line = line.split(",")
            if line[0].startswith(tuple(prefixes)):
                add_factory_contents(line[0], csv_files_index, item_collection_list, factory_dict, prefixes)
            else: 
                item_collection_list.append(line[0])
        return item_collection_list

if __name__ == "__main__":
    result = process_files(sys.argv[1])
    #pp(result)
    """get rid of this for now   
    for item_name, entries in matched_entries.items():
        print(f"Processing {item_name} list:")
        for entry in entries:
            print(entry) """

