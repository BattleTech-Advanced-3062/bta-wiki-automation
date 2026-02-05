import os
import sys
import json
from pprint import pp
import genUtilities
import pilotParser
from settings import *

template = environment.get_template("pilot.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def check_pilot_page(session, callsign):
    check_resp = session.post(api_url, data={
	"action": "query",
	"format": "json",
	"prop": "revisions",
	"titles": "Pilots",
	"formatversion": "2",
	"rvprop": "content",
	"rvslots": "*"
    })
    data = check_resp.json()
    data = json.dumps(data)
    return callsign in data

#busted, fix later
def render_pilot_entry(pilot):
    pilot_info = dict(pilot[1])
    callsign = pilot_info.get("callsign")
    results_filename = "Pilot_" + callsign + ".wiki"

    # updated with trick from gearRenderer to work with StrictUndefined
    context = pilot_info
    
    if "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
        # Wiki page writing
        page_title = "Template:Pilot_" + callsign
        genUtilities.post_to_wiki(session, csrf_token, page_title, template.render(context))
        if not check_pilot_page(session, callsign):
            print("Pilot entry not found on List of Pilots page and needs to be added: ", callsign)
    else:
        # Local file writing
        with open(results_filename, mode="w", encoding="utf-8") as results:
            results.write(template.render(context))
    

if __name__ == "__main__":
    results = pilotParser.process_pilot_files(pilot_dir_list)
    
    #pp(results)
    for pilot in results.items():
        render_pilot_entry(pilot)