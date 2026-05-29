import os
import sys
import json
from pprint import pp
import genUtilities
import coolingParser
from settings import *

template = environment.get_template("cooling.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_ecooling_table(ecoolings):
    context = {
        "ecoolings": ecoolings
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "ecoolings"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_ecoolings.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as ecoolings:
                ecoolings.write(template.render(**context))

if __name__ == "__main__":
    results = coolingParser.process_ecooling_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    render_ecooling_table(results)