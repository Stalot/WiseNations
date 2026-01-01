from pprint import pprint
from dataclasses import dataclass
from typing import Any
import re
from .exceptions import InvalidExpression, NotFound
from decimal import Decimal, localcontext
from .finals import DEFAULT_ROUNDING

class SafeExpression(str):
    """
    A string subclass that validates it contains only safe mathematical characters.
    """
    
    VALID_CHARS = set("0123456789.+-*/%() ")
    
    def __new__(cls, expr: str):
        # Validate before creating the instance
        if not isinstance(expr, str):
            raise InvalidExpression("Expression must be a string")
        
        invalid_chars = set(expr) - cls.VALID_CHARS
        if invalid_chars:
            chars = list(invalid_chars)[:3]
            examples = ', '.join([f"'{c}'" for c in chars])
            label = str(expr[:64]+" [...]").strip() if len(expr) > 64 else expr
            raise InvalidExpression(f"'{label}' is not a valid expression. Characters such as {examples} are not allowed.")
        
        # Create and return the string instance
        return super().__new__(cls, expr.strip())

class InnerFunctions:
    def __init__(self):
        pass
    def call(self, identifier: str, **kwargs):
        def bigger(values: list):
            return max(x)
        match identifier:
            case "BIGGER":
                arg = kwargs["values"]
                return bigger(arg)

class Parser:
    def __init__(self):
        #self.assigned_variables_pattern = re.compile(r"([a-zA-Z_]+):\s*?")
        self.censuses_pattern = re.compile(r"\[(\d+)\]")
#self.expressions_pattern = re.compile(r"\{([\s\S]*?)\}")
        self.variable_expression_assignment = re.compile(r"([a-zA-Z_]+):\s*?\{([\s\S]*?)\}\s*?")
        self.comments_pattern = re.compile(r"(\/\/\s*[\s\S]*?\s*\/\/)")
        self.functions_pattern = re.compile(r"([A-Z]+)\(([\s\S]*?)\)")

    def find_variables_and_expressions(self, string: str):
        matches = self.variable_expression_assignment.findall(string)
        return {var: expr for var, expr in matches}
    def parse_censuses(self, string: str, data: dict):
        """
        Detects all censuses from the given expression and returns a list with their respective ids
        """
        all_censuses = self.censuses_pattern.findall(string)
        ids = [int(match) for match in all_censuses]
        parsed_string = string
        for id in ids:
            try:
                parsed_string = self.censuses_pattern.sub(str(data[id]), string)
            except KeyError:
                raise NotFound(f"Unable to parse census of id '{id}', it's data wasn't provided")
        return parsed_string
    #def parse_assigned_variables(self, string: str):
        return self.assigned_variables_pattern.findall(string)
    def find_functions(self, string: str):
        matches = self.functions_pattern.findall(string)
        funcs = {id: expr for id, expr in matches}
        return funcs
    #def parse_expressions(self, string: str):
        expressions = self.expressions_pattern.findall(string)
        return expressions
    def remove_comments(self, string: str):
        """
        Removes comments, such as // this one! //
        """
        return self.comments_pattern.sub("", string)
    def remove_whitespaces(self, string: str):
        """
        Removes whitespaces from a string
        """
        return re.sub(r"\s", "", string)
    def turn_safe(self, expr: str):
        """
        Turns a normal string expression into a SafeExpression object
        """
        return SafeExpression(expr)
    #def to_dict(self, variables, expressions):
        output = {}
        for var, expr in zip(variables, expressions):
            output.update({var: expr})
        return output

    #def open_file(self, path: str) -> dict[str, str]:
        """
        Parses a file with the WiseNations syntax
        """
        with open(path, "r") as f:
            data: str = f.read()
            data = self.remove_comments(data)
            data = self.remove_whitespaces(data)
            return data

class Interpreter:
    def __init__(self):
        pass
    
    def evaluate_expression():
        ...

@dataclass
class Sheet:
    def __init__(self) -> None:
        self.stats = {}

    def get_all_stats(self):
        return self.stats
        
    def get_stat(self, id: str):
        return self.stats.get(id)
        
    def add_stats(self, stats_dict: dict[str, str]):
        for id, expr in stats_dict.items():
            self.stats.update({id: expr})
            
    def del_stats(self, ids: list[str]):
        for id in ids:
            self.stats.pop(id)
    
    def solve_expressions(self, ns_censuses: dict[int, Any] = None, rounding = DEFAULT_ROUNDING):
        if ns_censuses and not isinstance(ns_censuses, dict):
            raise TypeError(f"ns_censuses must be a dictionary, not {type(ns_censuses).__name__}")
        all_stats = self.get_all_stats()
        solved_sheet = {}
        
        def parse_brackets(expr: str):
            def parse_match(match: str):
                replacement = ns_censuses[int(match.group(1))]
                return replacement
            pattern = r"(\[(\d+)\])"
            new_expr = re.sub(pattern, parse_match, expr)
            return new_expr
        def parse_existing_stats(expr: str):
            def parse_match(match: str):
                stat_name = match.group(0)
                replacement = all_stats.get(stat_name)
                if replacement == None:
                    raise NotFound(f"Couldn't parse '{expr}', '{stat_name}' not found")
                return parse_existing_stats(replacement)
            pattern = r"[a-z_A-Z]+"
            new_expr = re.sub(pattern, parse_match, expr)
            return new_expr
                
        def evaluate_expression(expr: str) -> Any:
            safe_expr = SafeExpression(expr)
            def numbers_to_decimals(x: str):
                def parse_match(match: str):
                    return f"Decimal('{match.group(0)}')"
                pattern = r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
                new_string = re.sub(pattern, parse_match, x)
                return new_string
            with localcontext() as local_context:
                safe_globals = {"__builtins__": {}}
                safe_locals = {"Decimal": Decimal}
                local_context.prec = 28
                local_context.rounding = rounding
                parsed_numbers = numbers_to_decimals(safe_expr)
                return eval(parsed_numbers, safe_globals, safe_locals)
        def parse_expr(expr: str):
            if not isinstance(expr, str):
                raise TypeError(f"expressions must be strings, but '{expr}' is {type(expr).__name__}")
            parsed_existing_stats = parse_existing_stats(expr)
            parsed_brackets = parse_brackets(parsed_existing_stats)
            expr_result = evaluate_expression(parsed_brackets)
            return expr_result
        
        for id, expr in all_stats.items():
            parsed = parse_expr(expr)
            solved_sheet.update({id: str(parsed)})
        return solved_sheet

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

if __name__ == "__main__":
    pass