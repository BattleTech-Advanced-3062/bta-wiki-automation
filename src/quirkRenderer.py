import os
import sys
import json
from pprint import pp
import genUtilities
import quirkParser
from settings import *

template = environment.get_template("quirk.tpl")
session, csrf_token = genUtilities.create_wiki_session()


def render_quirk_entry(quirk):
    quirk_info = dict(quirk[1])
    quirk_title = quirk_info.get("title")
    results_filename = "Quirk" + quirk_title + ".wiki"

    context = quirk_info
    
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Template:Quirk" + quirk_title
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))

if __name__ == "__main__":
    results = quirkParser.process_quirk_files(quirk_dir_list)
    
    #pp(results)
    for quirk in results.items():
        render_quirk_entry(quirk)