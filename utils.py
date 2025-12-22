from ast import literal_eval
from pprint import pprint
from dataclasses import dataclass
from typing import Any
import re

@dataclass
class NsCensus:
    def __init__(self, id: int) -> None:
        self.id = id
        self.true_value = None
    
    def __str__(self):
        return f"{type(self).__name__}[{self.id}]"

@dataclass
class Sheet:
    def __init__(self) -> None:
        self.stats = {}

    def get_all_stats(self):
        return self.stats
        
    def get_stat(self, id: str):
        return self.stats.get(id)
        
    def add_stats(self, stats_dict: dict[str, str]):
        for id, expression in stats_dict.items():
            self.stats.update({id: expression})
            
    def del_stats(self, ids: list[str]):
        for id in ids:
            self.stats.pop(id)
    
    def solve_expressions(self, ns_censuses: dict[int, Any] = None):
        all_stats = self.get_all_stats()
        solved_sheet = {}
        
        def parse_brackets(expr: str):
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
        def parse_existing_stats(expr: str):
            chunks = expr.split(" ")
            for chunk in chunks:
                if all_stats.get(chunk):
                    return expr.replace(chunk, all_stats.get(chunk))
            return expr
                
        def evaluate_expression(expr: str) -> Any:
            result = eval(expr)
            return result
        def parse_expr(expr):
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