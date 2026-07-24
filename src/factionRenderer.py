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
    
    return faction_lookup[faction]

if __name__ == "__main__":
    #results = factionParser.process_files("../DynamicShops/fshops", "itemCollection_")
    results = factionParser.process_files(bta_dir + "DynamicShops/fshops", "itemCollection_")
    #pp(results)
    for faction,items in results.items():
        render_factionstore(faction, items)