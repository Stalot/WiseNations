import re
from typing import Iterable, Any
from pprint import pprint
from awesomeNations import AwesomeNations as awn
from utils import Sheet
from dataclasses import dataclass

@dataclass
class SheetManager:
    def __init__(self) -> None:
        self.sheets = {}

    def get_sheet(self, id: str):
        return self.sheets.get(id)
    
    def get_all_sheets(self):
        return self.sheets.items()
   
    def new_sheet(self, id: str):
        self.sheets.update({id: Sheet()})
    
    def del_sheet(self, id: str) -> None:
        self.sheets.pop(id)
    
if __name__ == "__main__":
    # ————————————
    # Getting data using a extern wrapper 
    # (in this case, AwesomeNations)
    wrapper = awn("WiseNations test (by: Orlys)")
    
    censuses = wrapper.Nation("novaros").get_shards("census", scale="all")["nation"]["census"]["scale"]
    
    data = {c["id"]: c["score"] for c in censuses}
    # ————————————
    
    pprint(data)
    
    sheetManager = SheetManager()
    sheetManager.new_sheet("s1")
    
    stats = {
        "attack_speed": "20 + ([2]*0.5)",
        "force": "[48]/10",
        "AGI": "32",
        "DEFENSE": '[48]',
        "speed": "AGI * [12] - DEFENSE"
    }
    
    sheet = sheetManager.get_sheet("s1")
    sheet.add_stats(stats)
    pprint(sheet.get_all_stats())
    result = sheet.solve_expressions(data)
    pprint(result)