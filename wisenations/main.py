import re
from typing import Iterable, Any
from pprint import pprint
from .utils import SheetManager, Sheet, Parser
from dataclasses import dataclass

@dataclass
class WiseNations:
    def __init__(self) -> None:
        self._sheetManager = SheetManager()
        self._parser = Parser()
    
    def sheet_manager(self) -> SheetManager:
        return self._sheetManager
    def read_string(self, string: str) -> dict[str, str]:
        def assign(string: str):
            string = self._parser.remove_comments(string)
            string = self._parser.remove_whitespaces(string)
            variables_and_expressions = self._parser.find_variables_and_expressions(string)
            return variables_and_expressions
        assigned = assign(string)
        return assigned

if __name__ == "__main__":
    pass