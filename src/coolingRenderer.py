import os
import sys
import json
from pprint import pp
import genUtilities
import coolingParser
from settings import *

template = environment.get_template("cooling.tpl")

session, csrf_token = genUtilities.create_wiki_session()

def render_ecooling_table(data):
    #context = {
        #"ecoolings": ecoolings
    #}
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Cooling"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**data))
    else:
        bulk_filename = "bulk_cooling.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as ecoolings:
                ecoolings.write(template.render(**data))

if __name__ == "__main__":
    #results = coolingParser.process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    result = coolingParser.process_all_cooling()
    render_ecooling_table(result)