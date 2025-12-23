from ast import literal_eval
from pprint import pprint
from dataclasses import dataclass
from typing import Any
import re
from exceptions import InvalidExpression
from decimal import Decimal, localcontext, ROUND_HALF_UP

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
            raise InvalidExpression(f"'{expr}' is not a valid expression")
        
        # Create and return the string instance
        return super().__new__(cls, expr.strip())

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
    
    def solve_expressions(self, ns_censuses: dict[int, Any] = None, rounding = ROUND_HALF_UP):
        if not isinstance(ns_censuses, dict):
            raise TypeError(f"ns_censuses must be a dictionary, not {type(ns_censuses).__name__}")
        all_stats = self.get_all_stats()
        solved_sheet = {}
        
        def parse_brackets(expr: SafeExpression):
            pattern = r"(\[(\d+)\])"
            matches = re.findall(pattern, expr)
            new_expr = expr
            if matches:
                for m in matches:
                    brackets_pattern = m[0]
                    census_id = int(m[1])
                    
                    new_expr = new_expr.replace(brackets_pattern, str(ns_censuses[census_id]))
                return new_expr
            return expr
        def parse_existing_stats(expr: SafeExpression):
            pattern = r"[a-zA-Z]+"
            string_variables = re.findall(pattern, expr)
            if string_variables:
                non_existing = set(string_variables) - set(all_stats.keys())
                if non_existing:
                    raise ValueError(f"Couldn't parse {non_existing} in '{expr}'")
                for var in string_variables:
                    match: None | str = all_stats.get(var)
                    expr = expr.replace(var, match)
                return expr
            return expr
                
        def evaluate_expression(expr: str) -> Any:
            safe_expr = SafeExpression(expr)
            def numbers_to_decimals(x: str):
                pattern = r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
                numbers = re.findall(pattern, expr)
                new_string = x
                if numbers:
                    for n in numbers:
                        new_string = new_string.replace(n, f"Decimal('{n}')")
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
    
if __name__ == "__main__":
    pass