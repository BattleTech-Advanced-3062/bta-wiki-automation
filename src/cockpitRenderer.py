import os
import sys
import json
from pprint import pp
import genUtilities
import cockpitParser
from settings import *

template = environment.get_template("cockpits.tpl")
session, csrf_token = genUtilities.create_wiki_session()

def render_cockpit_table(cockpits):
    context = {
        "cockpits": cockpits
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Cockpits"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_cockpits.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as cockpits:
                cockpits.write(template.render(**context))

if __name__ == "__main__":
    results = cockpitParser.process_cockpit_files(cockpit_dir_list)
    render_cockpit_table(results)