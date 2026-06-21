import os
import sys
import json
from pprint import pp
import genUtilities
import airdropParser
from settings import *

template = environment.get_template("airdrops.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_airdrop_table(airdrops):
    context = {
        "airdrops": airdrops
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Air Drops"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_airdrops.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as airdrops:
                airdrops.write(template.render(**context))

if __name__ == "__main__":
    results = airdropParser.process_airdrop_files(airdrop_dir_list)
    render_airdrop_table(results)