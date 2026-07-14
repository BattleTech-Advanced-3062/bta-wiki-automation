import os
from pprint import pp
import genUtilities
import myomerParser
from settings import *

template = environment.get_template("gofast.tpl")

#session, csrf_token = genUtilities.create_wiki_session()

def render_myomer_table(data):
    #context = {
        #"myomers": myomers
    #}
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        print("Posting to the wiki")
        page_title = "GoFasts"
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(**data))
    else:
        bulk_filename = "bulk_myomers.wiki"
        #pp(context)
        print("Writing locally")
        with open(bulk_filename, mode="w", encoding="utf-8") as myomers:
                myomers.write(template.render(**data))

if __name__ == "__main__":
    result = myomerParser.process_all_speed()
    render_myomer_table(result)