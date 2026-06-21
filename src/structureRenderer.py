import os
import sys
import json
from pprint import pp
import genUtilities
import structureParser
from settings import *

template = environment.get_template("structures.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_structure_table(structures):
    context = {
        "structures": structures
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Structures"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_structures.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as structures:
                structures.write(template.render(**context))

if __name__ == "__main__":
    results = structureParser.process_structure_files(structure_dir_list)
    render_structure_table(results)