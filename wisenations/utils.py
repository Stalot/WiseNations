from pprint import pprint
from dataclasses import dataclass
from typing import Any
import re
from .exceptions import InvalidExpression, NotFound
from decimal import Decimal, localcontext, ROUND_HALF_UP
from .finals import DEFAULT_ROUNDING

# Testing Sympy implementation for expression evaluation
# Wait, are you really reading this?
from sympy import simplify

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

class ExprEvaluator:
    """
    A class for managing expression evaluation.
    """
    def __init__(self):
        pass
    
    def eval_functions(self,
                       sheet: dict[str, str],
                       rounding: Any = DEFAULT_ROUNDING):
        def decimal_rounding(value):
            with localcontext() as lc:
                lc.rounding = rounding
                d = Decimal(str(value))
                d = d.quantize(Decimal("0.001"))
                return f"{d.normalize():f}"
 
        for var, expr in sheet.items():
            new_expr = simplify(expr,
                                rational=True).n()
            new_expr = decimal_rounding(new_expr)
            sheet.update({var: new_expr})
    

class SheetSyntax:
    def __init__(self):
        pass
    
    def clear_spaces(self, text: str) -> str:
        return re.sub(r"\s",
                      "",
                      text)
    def clear_comments(self, text: str) -> str:
        patt = r"\s*#.*"
        comments_found = re.findall(patt,
                                    text,
                                    re.MULTILINE)
        new_text: str = text
        for comment in comments_found:
            new_text = re.sub(rf"{comment}",
                              "",
                              new_text,
                              re.IGNORECASE)
        return new_text
    def text_to_dict(self,
                      text: str,
                      census_data: None | dict[int: str] = None):
        def replace_censuses(expression: str,
                             census_data: None | dict [int, str]) -> str:
            new_expr = expression
            censuses_found = re.findall(r"(\[(\d+)\])",
                                        new_expr)
            for census in censuses_found:
                id: int = int(census[1]) # 13, 88, 2, ...
                instance: str = str(census[0]) # [13], [88], [2], ...
                if instance and not census_data or not id in census_data:   
                    raise ValueError(f"{new_expr} -> '{instance}', census {id} not found in the given data!")
                repl: None | str = census_data.get(id) if census_data else None
                if repl:
                    new_expr = new_expr.replace(instance, repl)
            return new_expr
        def replace_vars(dictionary: dict[str, str]) -> dict[str, str]:
            for k, v in dictionary.items():
                new_value = v
                new_value = replace_censuses(v, census_data)
                vars_found = re.findall(r"[a-z_]+", v)
                for var in vars_found:
                    repl: None | str = dictionary.get(var)
                    if repl:
                        pattern = rf"\b{var}\b"
                        new_value = re.sub(pattern, repl, new_value)
                dictionary[k] = new_value
            return dictionary
        text = self.clear_comments(text)
        text = self.clear_spaces(text)
        data = re.findall(r"([a-z_]+?)\s*=\s*\{(.+?)\}",
                          text,
                          re.MULTILINE)
        new_dict: dict[str, str] = {}
        for key, value in data:
            new_dict.update({key: value})
        replace_vars(new_dict)
        return new_dict

@dataclass
class Sheet:
    def __init__(self) -> None:
        self._stats: dict[str, str] = {}
    def __getitem__(self, key: str):
        return self._stats[key]
    def __setitem__(self,
                    key: str,
                    value: str):
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError(f"key and value must be of type string, but got {type(key).__name__}: {type(value).__name__}")
        self._stats[key] = value
    def __len__(self):
        return len(self._stats.keys())
    def __str__(self):
        return f"Sheet({len(self)} stats)"
        
    def get_all_stats(self) -> dict[str, str]:
        return self._stats   
    def get_stat(self,
                 id: str) -> str:
        return self._stats.get(id)   
    def add_stats(self,
                  stats_dict: dict[str, str]) -> None:
        for id, expr in stats_dict.items():
            self._stats.update({id: expr})     
    def del_stats(self,
                  stats_ids: list[str]) -> None:
        for id in stats_ids:
            self._stats.pop(id)
    def from_file(self,
                  file_path: str,
                  census_data: None | dict[int, str] = None) -> None:
        """
        ... WIP
        """
        with open(file_path, "r") as f:
            sheetSyntax: SheetSyntax = SheetSyntax()
            file_text: str = f.read()
            stats_dict: dict[str, str] = sheetSyntax.text_to_dict(file_text,
                                                                  census_data)
            self.add_stats(stats_dict)
    def from_string(self,
                  string: str,
                  census_data: None | dict[int, str] = None) -> None:
        """
        ... WIP
        """
        sheetSyntax: SheetSyntax = SheetSyntax()
        stats_dict: dict[str, str] = sheetSyntax.text_to_dict(string,
                                                              census_data)
        self.add_stats(stats_dict)
    def solve_expressions(self,
                          census_data: dict[int, str] = None,
                          rounding: Any = DEFAULT_ROUNDING) -> dict[str, str]:
        sheet_data: dict[str, str] = self._stats
        exprEval: ExprEvaluator = ExprEvaluator()
        result: dict[str, str] = exprEval.eval_functions(sheet_data,
                                                         rounding)
        return result
    
if __name__ == "__main__":
    ...