import os
import sys
import json
from pprint import pp
import genUtilities
import armorParser
from settings import *

template = environment.get_template("armor.tpl")
session, csrf_token = genUtilities.create_wiki_session()

def render_armor_table(armors):
    context = {
        "armors": armors
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Armor"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_armors.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as armors:
                armors.write(template.render(**context))

if __name__ == "__main__":
    results = armorParser.process_armor_files(armor_dir_list)
    render_armor_table(results)