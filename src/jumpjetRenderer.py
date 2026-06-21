import os
import sys
import json
from pprint import pp
import genUtilities
import jumpjetParser
from settings import *

template = environment.get_template("jumpjets.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_jumpjet_table(jumpjets):
    context = {
        "jumpjets": jumpjets
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Jump Jets"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_jumpjets.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as jumpjets:
                jumpjets.write(template.render(**context))

if __name__ == "__main__":
    results = jumpjetParser.process_jumpjet_files(jumpjet_dir_list)
    render_jumpjet_table(results)