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

engine_dir_list = [bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/engine_parts/", 
    bta_dir + "BT Advanced Sanctuary Worlds Equipment/heatsink/", bta_dir + "BT Advanced Clan Gear/engines/", bta_dir + "Community Content/heatsink/"]

gyro_dir_list = [bta_dir + "Community Content/upgrade/", bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/gyro/", bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/gyro/",
    bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/internals/", bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/internals/", bta_dir + "BT Advanced Quad Mechs/upgrade/"]

jumpjet_dir_list = [bta_dir + "Community Content/jumpjet/", bta_dir + "BT Advanced Gear/MechengineerGear/data/vanilla/jumpjets/", bta_dir + "BT Advanced Gear/MechengineerGear/data/JumpJets/", 
    bta_dir + "Heavy Metal Equipment Module/jumpjets/", bta_dir + "BT Advanced Mech Quirks/jumpjet/", bta_dir + "BT Advanced Unique Mechs/jumpjet/"]

callin_dir_list = [bta_dir + "Community Content/upgrade/", bta_dir + "StrategicOperations/upgrade/"]

contract_dir_list = [bta_dir + "Community Content/upgrade/", bta_dir + "StrategicOperations/contracts/"]

structure_dir_list = [bta_dir + "Community Content/upgrade/", bta_dir + "BT Advanced Gear/MechengineerGear/data/exotics/internals/", 
    bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/internals/", bta_dir + "BT Advanced Sanctuary Worlds Equipment/upgrade/", bta_dir + "BT Advanced Clan Gear/internals/"]

myomer_dir_list = [bta_dir + "BT Advanced Gear/upgrade", bta_dir + "BT Advanced Clan Gear/internals", bta_dir + "BT Advanced Sanctuary Worlds Equipment/upgrade"]

api_url = "https://www.bta3062.com/api.php"

faction_lookup = {
    "Rezak": {"logo": "AuriganRestoration_logo.png", "name": "Aurigan Coalition", "link": "Aurigan Restoration (Arano)"},
    "AuriganPirate": {"logo": "AuriganRestoration_logo.png", "name": "Aurigan Coalition", "link": "Aurigan Restoration (Arano)"},
    "Aurigan": {"logo": "AuriganRestoration_logo.png", "name": "Aurigan Restoration (Arano)", "link": "Aurigan Coalition"},
    "Calderon": {"logo": "Calderon_Protectorate_logo.png", "name": "Calderon Protectorate", "link": "Calderon Protectorate"},
    "Liao": {"logo": "Liao_logo.png", "name": "Capellan Confederation (Liao)", "link": "Capellan Confederation"},
    "Chainelane": {"logo": "Chainelane_logo.png", "name": "Chainelane Isles", "link": "Chainelane Isles"},
    "Circinus": {"logo": "Circinus_logo.png", "name": "Circinus Federation", "link": "Circinus Federation"},
    "ClanFireMandrill": {"logo": "ClanFireMandrill_logo.png", "name": "Clan Fire Mandrill", "link": "Clan Fire Mandrill"},
    "ClanGoliathScorpion": {"logo": "ClanGoliathScorpion_logo.png", "name": "Clan Goliath Scorpion", "link": "Clan Goliath Scorpion"},
    "ClanNovaCat": {"logo": "ClanNovaCat_logo.png", "name": "Clan Nova Cat", "link": "Clan Nova Cat"},
    "ClanSnowRaven": {"logo": "ClanSnowRaven_logo.png", "name": "Clan Snow Raven", "link": "Clan Snow Raven"},
    "Comstar": {"logo": "ComStar_logo.png", "name": "ComStar", "link": "ComStar"},
    "DaneSacellum": {"logo": "DaneSacellum_logo.png", "name": "Dane Sacellum", "link": "Dane Sacellum"},
    "Kurita": {"logo": "Kurita_logo.png", "name": "Draconis Combine (Kurita)", "link": "Draconis Combine"},
    "Davion": {"logo": "Davion_logo.png", "name": "Federated Suns (Davion)", "link": "Federated Suns"},
    "Marik": {"logo": "Marik_logo.png", "name": "Free Worlds League", "link": "Free Worlds League"},
    "Fronc": {"logo": "Fronc_Reaches_logo.png", "name": "Fronc Reaches", "link": "Fronc Reaches"},
    "Hanse": {"logo": "Hanse_logo.png", "name": "Hanseatic League", "link": "Hanseatic League"},
    "Illyrian": {"logo": "Illyrian_logo.png", "name": "Illyrian Palatinate", "link": "Illyrian Palatinate"},
    "JacobsonHaven": {"logo": "JacobsonHaven_logo.png", "name": "Jacobson Haven", "link": "Jacobson Haven"},
    "JarnFolk": {"logo": "JarnFolk_logo.png", "name": "JàrnFòlk", "link": "JàrnFòlk"},
    "Lothian": {"logo": "Lothian_logo.png", "name": "Lothian League", "link": "Lothian League"},
    "Steiner": {"logo": "Steiner_logo.png", "name": "Lyran Commonwealth (Steiner)", "link": "Lyran Commonwealth"},
    "Magistracy": {"logo": "MagistracyOfCanopus_logo.png", "name": "Magistracy of Canopus", "link": "Magistracy of Canopus"},
    "MallardRepublic": {"logo": "MallardRepublic_logo.png", "name": "Mallard Republic", "link": "Mallard Republic"},
    "Marian": {"logo": "Marian_logo.png", "name": "Marian Hegemony", "link": "Marian Hegemony"},
    "Delphi": {"logo": "Delphi_logo.png", "name": "New Delphi Compact", "link": "New Delphi Compact"},
    "Oberon": {"logo": "Oberon_logo.png", "name": "Oberon Confederation", "link": "Oberon Confederation"},
    "Outworld": {"logo": "Outworld_logo.png", "name": "Outworlds Alliance", "link": "Outworlds Alliance"},
    "Rasalhague": {"logo": "Rasalhague_logo.png", "name": "Free Rasalhague Republic", "link": "Free Rasalhague Republic"},
    "Rim": {"logo": "RimWorldsRepublic_logo.png", "name": "Rim Worlds Republic", "link": "Rim Worlds Republic"},
    "RimWorldsRepublic": {"logo": "RimWorldsRepublic_logo.png", "name": "Rim Worlds Republic", "link": "Rim Worlds Republic"},
    "ScorpionEmpire": {"logo": "ScorpionEmpire_logo.png", "name": "Scorpion Empire", "link": "Scorpion Empire"},
    "Ives": {"logo": "Ives_logo.png", "name": "St. Ives Compact", "link": "St. Ives Compact"},
    "Taurian": {"logo": "TaurianConcordat_logo.png", "name": "Taurian Concordat", "link": "Taurian Concordat"},
    "Cameron": {"logo": "Cameron_logo.png", "name": "Terran Hegemony (Cameron)", "link": "Terran Hegemony"},
    "Tortuga": {"logo": "Tortuga_logo.png", "name": "Tortuga Dominions", "link": "Tortuga Dominions"},
    "WordOfBlake": {"logo": "WordOfBlake_logo.png", "name": "Word of Blake", "link": "Word of Blake"}
    }
