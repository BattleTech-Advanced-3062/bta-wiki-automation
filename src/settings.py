import os
from jinja2 import Environment, FileSystemLoader

if not "GITHUB_ACTIONS" in os.environ or "LOCAL_OVERRIDE" in os.environ:
    bta_dir = "../../BattleTech-Advanced/"
    jinja_dir = "../templates/"
elif "GITHUB_ACTIONS" in os.environ:
    bta_dir = "/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/bta/"
    jinja_dir = "/home/runner/work/BattleTech-Advanced/BattleTech-Advanced/wiki-gen/templates/"

environment = Environment(loader=FileSystemLoader(jinja_dir))

csv_dir_list = [bta_dir + "DynamicShops/", bta_dir + "Community Content/", bta_dir + "Flashpoint Unit Module/",
    bta_dir + "Heavy Metal Unit Module/", bta_dir + "Urban Warfare Unit Module/"]

pilot_dir_list = [bta_dir + "BT Advanced Core/StreamingAssets/data/pilot/", bta_dir + "BT Advanced Pilots/pilot/",
                  bta_dir + "Community Content/pilot/", bta_dir + "BT Advanced Events/pilot/"]

api_url = "https://www.bta3062.com/api.php"