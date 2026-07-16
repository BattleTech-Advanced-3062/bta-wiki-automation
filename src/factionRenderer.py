from jinja2 import Environment, FileSystemLoader
import os
import json
import requests
import factionParser
import genUtilities
from pprint import pp
from settings import *

template = environment.get_template("factionStore.tpl")
session, csrf_token = genUtilities.create_wiki_session()

def check_faction_page(session, faction):
    faction_url = faction.replace(" ", "_")
    check_resp = session.post(api_url, data={
	"action": "query",
	"format": "json",
	"prop": "revisions",
	"titles": "Faction_Stores",
	"formatversion": "2",
	"rvprop": "content",
	"rvslots": "*"
    })
    data = check_resp.json()
    data = json.dumps(data)
    return faction_url in data


def render_factionstore(faction, items):
    faction_name = faction[:-5]
    results_filename = faction_name+"_store_Table.wiki"
    faction_info=get_faction_specific_info(faction_name)
    weapons = []
    ammunitions = []
    gears = []
    mechs = []
    vehicles = []
    battlearmors = []
    contracts = []
    for item in items:
        if item.startswith("Weapon_"):
            weapons.append(item)
        elif item.startswith("Ammo_"):
            ammunitions.append(item)
        elif item.startswith(("Gear_", "emod_")) and not item.startswith("Gear_Contract_"):
            gears.append(item)
        elif item.startswith("mechdef_") and not item.startswith("mechdef_ba_"):
            mechs.append(item)
        elif item.startswith("vehicledef_"):
            vehicles.append(item)
        elif item.startswith("mechdef_ba_"):
            battlearmors.append(item)
        elif item.startswith("Gear_Contract_"):
            contracts.append(item)
    
    for index, item in enumerate(weapons):
        weapons[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(ammunitions):
        ammunitions[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(gears):
        gears[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(mechs):
        mechs[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(vehicles):
        vehicles[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(battlearmors):
        battlearmors[index] = genUtilities.get_display_name(item)
    for index, item in enumerate(contracts):
        contracts[index] = genUtilities.get_display_name(item)
    
    for index, item in enumerate(mechs):
        mechs[index] = '#'.join(item.rsplit(' ', 1)) + '|' + item
    for index, item in enumerate(vehicles):
        vehicles[index] = '#'.join(item.rsplit(' ', 1)) + '|' + item

    context = {
        "faction_info": faction_info,
        "weapons": weapons,
        "ammunitions": ammunitions,
        "gears": gears,
        "mechs": mechs,
        "vehicles": vehicles, 
        "battlearmors": battlearmors,
        "contracts": contracts,
    }

    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Template:FS" + faction_name
        print(f"posting to wiki: Faction store for {faction_name}")
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
        if not check_faction_page(session, faction_name):
            print("Faction entry not found on Factions Store page and needs to be added: ", faction_name)
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))
            print(f"... wrote {results_filename}")

def get_faction_specific_info(faction):
    # This unfortunately needs to be maintained manually
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
    return faction_lookup[faction]

if __name__ == "__main__":
    #results = factionParser.process_files("../DynamicShops/fshops", "itemCollection_")
    results = factionParser.process_files(bta_dir + "DynamicShops/fshops", "itemCollection_")
    #pp(results)
    for faction,items in results.items():
        render_factionstore(faction, items)