from typing import Any
from .utils import Sheet

class SheetManager:
    """
    A class designed for managing
    Sheet() objects.
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
        """
        Gets a sheet, returns the
        default value if not found.
        """
        if not isinstance(id, str):
            raise TypeError(f"{id} must be a string, not {type(id).__name__}")
        return self.sheets.get(id, default)
    def get_all_sheets(self):
        """
        Returns all sheets.
        """
        return self.sheets.items()
    def new_sheet(self,
                  id: str) -> Sheet:
        """
        Creates a new Sheet() object.
        """
        if not isinstance(id, str):
            raise TypeError(f"{id} must be a string, not {type(id).__name__}")
        self.sheets.update({id: Sheet()})
        sheet: Sheet = self.sheets[id]
        return sheet
    def del_sheet(self, id: str) -> None:
        """
        Deletes a sheet.
        """
        if not isinstance(id, str):
            raise TypeError(f"{id} must be a string, not {type(id).__name__}")
        del self.sheets[id]
    
if __name__ == "__main__":
    pass