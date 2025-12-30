import os
import sys
import json
from pprint import pp
import genUtilities
import gearParser
from settings import *

template = environment.get_template("weapons/default.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_weapon_entry(weapon):

    weapon_info = dict(weapon[1])
    weapon_name = weapon_info.get("name")
    fixed_weapon_name = weapon_name.replace("/", "_")
    results_filename = "weapon_" + fixed_weapon_name + ".wiki"
    context = {
        "name": weapon_info.get("name"),
        "ammo": weapon_info.get("ammo"),
        "hardpoint": weapon_info.get("hardpoint"),
        "tonnage": weapon_info.get("tonnage"),
        "slots": weapon_info.get("slots"),
        "damage": weapon_info.get("damage"),
        "heatdamage": weapon_info.get("heatdamage"),
        "instability": weapon_info.get("instability"),
        "shots": weapon_info.get("shots"),
        "projectiles": weapon_info.get("projectiles"),
        "heat": weapon_info.get("heat"),
        "recoil": weapon_info.get("recoil"),
        "accuracy": weapon_info.get("accuracy"),
        "evasionignored": weapon_info.get("evasionignored"),
        "bonuscritchance": weapon_info.get("bonuscritchance"),
        "rangemin": weapon_info.get("rangemin"),
        "rangeshort": weapon_info.get("rangeshort"),
        "rangemedium": weapon_info.get("rangemedium"),
        "rangelong": weapon_info.get("rangelong"),
        "rangemax": weapon_info.get("rangemax"),
        "firesinmelee": weapon_info.get("firesinmelee"),
        "additionalinfo": weapon_info.get("additionalinfo"), 
    }

    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Template:Pilot_" + weapon_name
        #genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
        #if not check_pilot_page(session, callsign):
            #print("Pilot entry not found on List of Pilots page and needs to be added: ", callsign)
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))

if __name__ == "__main__":
    results = gearParser.process_weapon_files(bta_dir + "BT Advanced Gear")
    
    #pp(results)
    for weapon in results.items():
        render_weapon_entry(weapon)