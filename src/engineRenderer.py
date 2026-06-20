import os
import sys
import json
from pprint import pp
import genUtilities
import engineParser
from settings import *

template = environment.get_template("engines.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_engine_table(engines):
    context = {
        "engines": engines
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Engines"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_engines.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as engines:
                engines.write(template.render(**context))

if __name__ == "__main__":
    results = engineParser.process_engine_files(engine_dir_list)
    render_engine_table(results)