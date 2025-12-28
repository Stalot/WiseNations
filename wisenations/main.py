import re
from typing import Iterable, Any
from pprint import pprint
from .utils import Sheet
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
    
    def script_to_dict(self, file_path: str):
        variables_pattern = re.compile(r"([a-zA-Z_]+):\s*?")
        expressions_pattern = re.compile(r"\{([\s\S]*?)\}")
        comments_pattern = re.compile(r"(\/\/\s*[\s\S]*?\s*\/\/)")
        def remove_comments(string: str):
            return comments_pattern.sub("", string)
        def get_variables(string: str):
            vars = variables_pattern.findall(string)
            return vars
        def get_expressions(string: str):
            expressions = expressions_pattern.findall(string)
            return [expr.strip() for expr in expressions]
        def assign(all_variables, all_expressions):
            global_variables = {}
            def assign_variables(variables: list, expressions: list[str]):
                for var, expr in zip(variables, expressions):
                    global_variables.update({var: expr })
            assign_variables(all_variables, all_expressions)
            return global_variables
            
        with open(file_path, "r") as f:
            file_content = f.read()
            file_content = remove_comments(file_content)
            detected_variables = get_variables(file_content)
            detected_expressions = get_expressions(file_content)
            assigned_values = assign(detected_variables, detected_expressions)
            return assigned_values

if __name__ == "__main__":
    pass