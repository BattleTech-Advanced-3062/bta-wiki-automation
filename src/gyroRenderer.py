import os
import sys
import json
from pprint import pp
import genUtilities
import gyroParser
from settings import *

template = environment.get_template("gyros.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_gyro_table(gyros):
    context = {
        "gyros": gyros
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Gyros"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_gyros.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as gyros:
                gyros.write(template.render(**context))

if __name__ == "__main__":
    results = gyroParser.process_gyro_files(gyro_dir_list)
    render_gyro_table(results)