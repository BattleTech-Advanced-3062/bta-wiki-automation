import os
import sys
import json
from pprint import pp
import genUtilities
import gearParser
from settings import *

template = environment.get_template("weapons/modal.tpl")
session, csrf_token = genUtilities.create_wiki_session()

def render_weapon_entry(weapon):

    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Weapons"
        #genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
        #if not check_pilot_page(session, callsign):
            #print("Pilot entry not found on List of Pilots page and needs to be added: ", callsign)
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))

def render_bulk_entry(categories):
    context = {
        "categories": categories
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Test Weapons Page"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        # Local file writing
        bulk_filename = "bulk_weapons.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as weapons:
                weapons.write(template.render(**context))

if __name__ == "__main__":
    results = gearParser.process_weapon_files(weapon_dir_list)
    grouped = gearParser.group_by_category(results)
    split = gearParser.split_modes(grouped)
    render_bulk_entry(split)
    #pp(split)
    #for weapon in results.items():
        #render_weapon_entry(weapon)