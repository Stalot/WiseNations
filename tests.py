from wisenations import WiseNations
from pprint import pprint as pp
from awesomeNations import AwesomeNations as AwesomeNations

wrapper = AwesomeNations("WiseNations Test (WiseNations 0.0.1.dev0; By: Orlys")

censuses =  wrapper.Nation("fullworthia").get_shards("census", scale="all")

census_data = {}
for c in censuses["nation"]["census"]["scale"]:
    id = int(c["id"])
    score = c["score"]
    census_data.update({id: score})

wn = WiseNations()
sheet_manager = wn.sheet_manager()
sheet_manager.new_sheet("s1")

with open("sample.txt", "r") as f:
    result = wn.read_string(f.read())
    print(result)