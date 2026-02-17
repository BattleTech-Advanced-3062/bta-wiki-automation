import os
import sys
import json
from pprint import pp
import genUtilities
import armorParser
from settings import *

template = environment.get_template("armor.tpl")
#session, csrf_token = genUtilities.create_wiki_session()

def render_armor_table(armors):

if __name__ == "__main__":
    results = armorParser.process_armor_files(armor_dir_list)
    render_armor_table(results)