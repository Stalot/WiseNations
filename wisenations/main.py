from typing import Any
from .utils import Sheet
from dataclasses import dataclass

@dataclass
class SheetManager:
    """
    A class designed for managing
    your Sheet() objects.
    """
    def __init__(self) -> None:
        self.sheets = {}
    def __getitem__(self, 
                    key: str) -> Sheet:
        return self.sheets[key]
    def __setitem__(self,
                    key: str) -> None:
        self.new_sheet(key)

    def get_sheet(self,
                  id: str,
                  default: Any = None) -> Sheet | Any:
        return self.sheets.get(id, default)
    def get_all_sheets(self):
        return self.sheets.items()
    def new_sheet(self,
                  id: str) -> Sheet:
        self.sheets.update({id: Sheet()})
        sheet: Sheet = self.sheets[id]
        return sheet
    def del_sheet(self, id: str) -> None:
        del self.sheets[id]
    
if __name__ == "__main__":
    pass