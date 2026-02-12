from dataclasses import dataclass
from typing import Any, Generator
import re
from .exceptions import InvalidExpression, NotFound
from decimal import Decimal, localcontext
from .finals import DEFAULT_ROUNDING
from .parser import SyntaxParser
from graphlib import TopologicalSorter

# Testing Sympy implementation for 
# expression evaluation
# Do people still read comments these
# days?
from sympy import simplify, Symbol, Float

# TO DO: Find a new place for this
# dude
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
    A class for managing expression
    evaluation.
    """
    def __init__(self):
        pass
    
    def resolve_dependencies(self,
                             stats: dict[str, str],
                             census_data: None | dict[int, str]) -> Generator:
        """
        Resolves dependencies and
        returns a proper evaluation
        order.
        """
        def resolve_censuses(expr, 
                             census_data: None | dict[int, str]):
            """
            Searches for censuses in
            an expression, if it finds
            something, replaces them 
            with the given census
            data.
            """
            censuses = re.findall(r"(\[(\d+)\])",
                                  expr)
            new_expr = expr
            if censuses:
                for census in censuses:
                    id: int = int(census[1])
                    # Escapes ALL
                    # regex special
                    # characters. Such
                    # as: [],*,?, ...
                    # In practical
                    # terms,
                    # automatically
                    # treats them as 
                    # litteral strings.
                    match: str = re.escape(census[0])
                    new_expr = re.sub(rf"{match}",
                                      census_data[id],
                                      new_expr)
            return new_expr
 
        dependencies = {}
        for stat, expr in stats.items():
            stats.update({stat: resolve_censuses(expr, census_data)})
            # Searches for stats
            # (variables) in the an
            # expression and adds them
            # to the dependency list!
            vars = set(re.findall(r"[a-z_]+", expr))
            dependencies[stat] = vars if vars else {}
        # Ensures stats are evaluated
        # in the best logical order
        # based on their dependencies.
        # Necessary for complex
        # dependency chains.
        ts = TopologicalSorter(dependencies)
        evaluation_order: Generator = ts.static_order()
        return evaluation_order
    def eval_functions(self,
                       sheet: dict[str, str],
                       rounding: Any = DEFAULT_ROUNDING,
                       census_data: None | dict[int, str] = None) -> dict[str, str]:
        def decimal_rounding(value) -> str:
            with localcontext() as lc:
                lc.rounding = rounding
                d = Decimal(str(value))
                d = d.quantize(Decimal("0.001"))
                return f"{d.normalize():f}"
        
        previous_results: dict[Symbol, Float] = {}
        final_result: dict[str, str] = {}
        
        # After dependencies are
        # resolved and the
        # evaluation order is
        # returned...
        for var in self.resolve_dependencies(sheet,
                                             census_data):
            simplified_expr = simplify(sheet[var])
            # Uses previous 
            # numerical results
            # for replacing context
            # and then evaluates it:
            resolved_expr = simplified_expr.subs(previous_results)
            numerical_expr: Float = resolved_expr.evalf()
            
            previous_results[Symbol(var)] = numerical_expr
            # Formatting...
            final_expr: str = decimal_rounding(str(numerical_expr))
            # Maps the evaluated
            # expression with it's
            # respective variable
            # (stat) in the sheet:
            final_result[var] = final_expr
         
        return final_result

@dataclass
class Sheet:
    def __init__(self) -> None:
        self._stats: dict[str, str] = {}
        self._parser: SyntaxParser = SyntaxParser()
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
                  file_path: str) -> None:
        """
        ... WIP
        """
        #with open(file_path, "r") as f:
            #sheetSyntax: SheetSyntax = SheetSyntax()
            #file_text: str = f.read()
            #stats_dict: dict[str, str] = sheetSyntax.text_to_dict(file_text,
            #                                                      census_data)
        parsed = self._parser.parse(file_path)
        self.add_stats(parsed)
    def from_string(self,
                  string: str) -> None:
        """
        ... WIP
        """
        parsed = self._parser.parse(string)
        self.add_stats(parsed)
    def solve_expressions(self,
                          census_data: dict[int, str] = None,
                          rounding: Any = DEFAULT_ROUNDING) -> dict[str, str]:
        sheet_data: dict[str, str] = self._stats.copy()
        exprEval: ExprEvaluator = ExprEvaluator()
        result: dict[str, str] = exprEval.eval_functions(sheet_data,
                                                         rounding,
                                                         census_data)
        return result
    
if __name__ == "__main__":
    ...