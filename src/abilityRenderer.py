import os
import sys
import json
from pprint import pp
import genUtilities
import abilityParser
from settings import *

template = environment.get_template("ability.tpl")
session, csrf_token = genUtilities.create_wiki_session()

def render_ability_entry(ability):
    ability_info = dict(ability[1])
    file_id = ability_info.get("id")
    results_filename = "Ability_" + file_id + ".wiki"

    context = ability_info
    
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Template:Ability_" + file_id
        print(f"Writing to {page_title}")
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))

if __name__ == "__main__":
    results = abilityParser.process_ability_files(ability_dir_list)
    
    #pp(results)
    for ability in results.items():
        render_ability_entry(ability)