import os
import sys
import json
from pprint import pp
import genUtilities
import thermalParser
from settings import *

template = environment.get_template("thermalgear.tpl")

session, csrf_token = genUtilities.create_wiki_session()

def render_thermalgear_table(data):
    context = {
        "thermalgear": data
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Thermal Gear"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_thermalgear.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as thermalgears:
                thermalgears.write(template.render(**context))

if __name__ == "__main__":
    #results = thermalgearParser.process_thermalgear_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    result = thermalParser.process_thermalgear_files(thermal_dir_list)
    render_thermalgear_table(result)