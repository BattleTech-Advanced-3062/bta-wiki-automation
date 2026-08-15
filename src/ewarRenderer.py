import os
import sys
import json
from pprint import pp
import genUtilities
import ewarParser
from settings import *

template = environment.get_template("ewar.tpl")

#session, csrf_token = genUtilities.create_wiki_session()

def render_ewar_table(data):
    #context = {
        #"ewars": ewars
    #}
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Test E-War"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**data))
    else:
        bulk_filename = "ewar.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as ewars:
                ewars.write(template.render(**data))

if __name__ == "__main__":
    #results = ewarParser.process_ewar_files(bta_dir + "BT Advanced Gear/MechengineerGear/data/basic/engine_parts/")
    result = ewarParser.process_all_ewar()
    render_ewar_table(result)