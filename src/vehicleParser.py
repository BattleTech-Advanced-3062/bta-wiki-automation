import os
import sys
import json
import re
from pprint import pp
import genUtilities
import math
from settings import *

def add_vehicle_inventory(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        item_name = data[0].get("items")
        print("item_name")
        #if not "" in item_name 

def calc_speed(engine, tonnage):

    if engine is None or tonnage is None:
        return "4/6"
    try:
        a = float(engine)
        b = float(tonnage)
        walk = math.ceil(a / b)
        run = walk + math.ceil(walk * 0.5)
        return f"{walk}/{run}"
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except ValueError:
        return "Error: Inputs must be numbers or numeric strings."

def remove_unwanted_components(data):
    keywords = ['slots', 'HeatSink', 'Tank', 'Tracked', 'Hover', 'Wheeled']
    filtered_data = {}
    for filename, components in data.items():
        filtered_components = [
            comp for comp in components
            if 'ComponentDefID' in comp and not any(keyword in comp['ComponentDefID'] for keyword in keywords)
        ]
        filtered_data[filename] = filtered_components
    return filtered_data

def extract_component_ids(data):
    return {
        'Components': [component['ComponentDefID'] for component in data.get('Components', [])]
    }

def extract_engine_size(components):
    for comp in components:
        comp_id = comp.get("ComponentDefID", "")
        match = re.match(r"emod_engine_(\d+)", comp_id)
        if match:
            return int(match.group(1))
    return None

def extract_engine_type(components):
    for comp in components:
        comp_id = comp.get("ComponentDefID", "")
        match = re.search(r'emod_engineslots_(\w+)_center', comp_id)
        if match:
            return match.group(1)
    return None

def process_vehicle_files(directory):
    vehicle_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("vehicledef_") and file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if "unit_controllableTank" in data["VehicleTags"]["items"]:

                        uiname = data["Description"].get("UIName")
                        vehicle_dict[uiname] = {
                            "Components": {}
                        }
                        vehicle_dict[uiname]["Components"] = data["inventory"]
                        vehicle_dict[uiname] = remove_unwanted_components(vehicle_dict[uiname])
                        vehicle_dict[uiname] = extract_component_ids(vehicle_dict[uiname])
                        chassisfilename = data["ChassisID"] + ".json"
                        #print(chassisfilename)
                        
                        for chassisroot, _, chassisfiles in os.walk(directory):
                            for chassisfile in chassisfiles:
                                if chassisfile.startswith(chassisfilename):
                                    chassisfile_path = os.path.join(chassisroot, chassisfile)
                                    with open(chassisfile_path, 'r') as cf:
                                        cdata = json.load(cf)
                                        vehicle_dict[uiname]["Tonnage"] = cdata.get("Tonnage")
                                        vehicle_dict[uiname]["Propulsion"] = clean_vehicle_pathing(cdata.get("PathingCapDefID"))
                                        armorvalues = {}
                                        total_armor = 0
                                        total_structure = 0
                                        for loc in cdata.get("Locations", []):
                                            location_name = loc.get("Location")
                                            max_armor = int(loc.get("MaxArmor", 0))
                                            internal_structure = int(loc.get("InternalStructure", 0))
                                            total_armor += max_armor
                                            total_structure += internal_structure
                                            key = f"{location_name}Armor"
                                            value = f"{max_armor}/{internal_structure}"
                                            armorvalues[key] = value
                                        vehicle_dict[uiname]["ArmorValues"] = armorvalues
                                        vehicle_dict[uiname]["TotalArmor"] = total_armor
                                        vehicle_dict[uiname]["TotalStructure"] = total_structure
                        core_size = extract_engine_size(data["inventory"])
                        core_type = extract_engine_type(data["inventory"])
                        tonnage = vehicle_dict[uiname]["Tonnage"]
                        vehicle_dict[uiname]["CoreSize"] = core_size
                        vehicle_dict[uiname]["CoreType"] = core_type
                        vehicle_dict[uiname]["Speed"] = calc_speed(core_size, tonnage)
                        vehicle_dict[uiname]["Icon"] = data["Description"]["Icon"]                     

    #pp(vehicle_dict)
    return vehicle_dict

if __name__ == "__main__":
    #result = process_vehicle_files(vehicle_dir_list)
    result = process_vehicle_files(bta_dir + "/VIPAdvanced")
    #pp(result)