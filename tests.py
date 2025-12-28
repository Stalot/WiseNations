from wisenations import SheetManager, Interpreter
from pprint import pprint as pp
from awesomeNations import AwesomeNations as AwesomeNations

wrapper = AwesomeNations("WiseNations Test (WiseNations 0.0.1.dev0; By: Orlys")

censuses =  wrapper.Nation("fullworthia").get_shards("census", scale="all")

census_data = {}
for c in censuses["nation"]["census"]["scale"]:
    id = int(c["id"])
    score = c["score"]
    census_data.update({id: score})

inter= Interpreter()
result = inter.script_to_dict("sample.txt", census_data=census_data)
pp(result)