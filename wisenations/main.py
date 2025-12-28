import re
from typing import Iterable, Any
from pprint import pprint
from .utils import Sheet, Parser
from dataclasses import dataclass

@dataclass
class SheetManager:
    def __init__(self) -> None:
        self.sheets = {}

    def get_sheet(self, id: str) -> Sheet:
        return self.sheets.get(id)
    
    def get_all_sheets(self):
        return self.sheets.items()
   
    def new_sheet(self, id: str) -> None:
        self.sheets.update({id: Sheet()})
    
    def del_sheet(self, id: str) -> None:
        self.sheets.pop(id)

class Interpreter:
    def __init__(self):
        self.custom_operators = {}
        self.parser = Parser()
    
    def script_to_dict(self, file_path: str, **kwargs):
        parsed_file: str = self.parser.open_file(file_path)
        census_data = kwargs.get("census_data")
        if census_data:
            parsed_file = self.parser.parse_censuses(parsed_file, census_data)
        return parsed_file

if __name__ == "__main__":
    pass