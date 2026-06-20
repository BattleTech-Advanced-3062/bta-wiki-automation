import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined


import genUtilities

if not "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
    bta_dir = "../../BattleTech-Advanced/"
    jinja_dir = "../templates/"
elif "GITHUB_ACTIONS" in os.environ:
    bta_dir = "/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/bta/"
    jinja_dir = "/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/wiki-gen/templates/"

environment = Environment(loader=FileSystemLoader(jinja_dir), undefined=StrictUndefined)

csv_dir_list = [bta_dir + "DynamicShops/", bta_dir + "Community Content/", bta_dir + "Flashpoint Unit Module/",
    bta_dir + "Heavy Metal Unit Module/", bta_dir + "Urban Warfare Unit Module/"]

pilot_dir_list = [bta_dir + "BT Advanced Core/StreamingAssets/data/pilot/", bta_dir + "BT Advanced Pilots/pilot/",
    bta_dir + "Community Content/pilot/", bta_dir + "BT Advanced Events/pilot/"]

weapon_dir_list = [bta_dir + "BT Advanced Clan Gear/", bta_dir + "BT Advanced Gear/", 
    bta_dir + "BT Advanced Sanctuary Worlds Equipment/", bta_dir + "Heavy Metal Equipment Module/"]

armor_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/internals/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/internals/", 
    bta_dir + "BT Advanced Clan Gear/internals/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/upgrade/", bta_dir + "Community Content/upgrade/"]

cc_weapon_dir_list = [bta_dir + "Community Content/weapon/"]

ability_dir_list = [bta_dir + "Abilifier/abilities/", bta_dir + "BT Advanced Core/StreamingAssets/data/abilities/",
    bta_dir + "CustomUnits/ability/"]

cockpit_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/cockpitMods/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/internals/", 
    bta_dir + "BT Advanced Gear/upgrade/cockpit/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/upgrade/", bta_dir + "Community Content/upgrade/", bta_dir + "BT Advanced Quad Mechs/upgrade/"]

actuator_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/actuators/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/actuators/", 
    bta_dir + "BT Advanced Gear/upgrade/actuators/", bta_dir + "BT Advanced Unique Mechs/upgrade/", bta_dir + "Community Content/upgrade/", bta_dir + "BT Advanced Quad Mechs/upgrade/"]

cooling_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/heatsinks/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/"]

kit_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/", bta_dir + "BT Advanced Clan Gear/engines/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/",
    bta_dir + "Community Content/heatsink/"]

sink_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/", bta_dir + "BT Advanced Clan Gear/engines/", 
    bta_dir + "Community Content/heatsink/"]

engine_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/engine_parts/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/",
    bta_dir + "BT Advanced Clan Gear/engines/", bta_dir + "Community Content/heatsink/"]

api_url = "https://www.bta3062.com/api.php"
