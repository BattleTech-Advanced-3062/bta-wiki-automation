import os
import sys
import json
from pprint import pp
import genUtilities
import actuatorParser
from settings import *

template = environment.get_template("actuators.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_actuator_table(actuators):
    context = {
        "actuators": actuators
    }
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "Actuators"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**context))
    else:
        bulk_filename = "bulk_actuators.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as actuators:
                actuators.write(template.render(**context))

if __name__ == "__main__":
    results = actuatorParser.process_actuator_files(actuator_dir_list)
    render_actuator_table(results)