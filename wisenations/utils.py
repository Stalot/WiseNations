from typing import Any, Generator
import re
from .exceptions import InvalidExpression, NotFound, EvaluationError
from decimal import Decimal, localcontext
from .finals import DEFAULT_ROUNDING
from .parser import SyntaxParser
from graphlib import TopologicalSorter, CycleError
from .func_master import FuncMaster

# Testing Sympy implementation for 
# expression evaluation
# Do people still read comments these
# days?
# TO DO: Proper dependency 
# licencing
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
        """
        Takes a sheet, evaluates it
        and returns it's evaluated
        version.
        """
        def decimal_rounding(value) -> str:
            with localcontext() as lc:
                lc.rounding = rounding
                d = Decimal(str(value))
                d = d.quantize(Decimal("0.001"))
                return f"{d.normalize():f}"
        def solve_functions(expr: str,
                            context: dict[Symbol, str]) -> str:
            fm = FuncMaster()
            new_expr: str = expr
            funcs = re.findall(r"(([A-Z]+)\((.+)\))",
                               new_expr,
                               re.DOTALL)
            if funcs:
                for func in funcs:
                    match = re.escape(func[0])
                    name = func[1]
                    print(f"{func[2]=}")
                    args = solve_functions(func[2], context).replace(" ", "").replace(";", ",")
                    print(f"{args=}")
                    simplified = simplify(args).subs(context)
                    result = fm.call(name, simplified)
                    new_expr = re.sub(rf"{match}",
                                      result,
                                      new_expr)
            return str(new_expr)
        previous_results: dict[Symbol, Float] = {}
        final_result: dict[str, str] = {}
        
        # After dependencies are
        # resolved and the
        # evaluation order is
        # returned...
        try:
            for var in self.resolve_dependencies(sheet,
                                                 census_data):
                expr: str = sheet[var]
                expr = solve_functions(expr,
                                       previous_results)
                simplified_expr = simplify(expr)
                # Uses previous 
                # numerical results
                # for replacing 
                # context
                # and then evaluates 
                # it:
                resolved_expr = simplified_expr.subs(previous_results)
                numerical_expr: Float = resolved_expr.evalf(chop=True)
            
                previous_results[Symbol(var)] = numerical_expr
                # Formatting...
                final_expr: str = str(numerical_expr)
                # Maps the evaluated
                # expression with
                # it's
                # respective variable
                # (stat) in the sheet:
                final_result[var] = final_expr
        except CycleError as ce:
             nodes: str = " -> ".join(ce.args[1])
             raise EvaluationError(f"Redundant dependency: {nodes}")
        return final_result

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
        """
        Returns all stats in
        this sheet.
        """
        return self._stats   
    def get_stat(self,
                 id: str) -> None | str:
        """
        Gets a stat from this sheet, 
        returns None if 
        it doesn't exist.
        """           
        return self._stats.get(id)   
    def add_stats(self,
                  stats_dict: dict[str, str]) -> None:
        """
        Add stats to this sheet.
        """
        for stat, expr in stats_dict.items():
            if not isinstance(stat, str):
                raise TypeError(f"Stats must be string objects, not {type(stat).__name__}")
            if not isinstance(expr, str):
                raise TypeError(f"{stat}: expressions must be string objects, not {type(expr).__name__}")
            self._stats.update({stat: expr})     
    def del_stats(self,
                  stat_ids: list[str]) -> None:
        """
        Removes stats from this
        sheet.
        """
        for id in stat_ids:
            self._stats.pop(id)
    def from_file(self,
                  file_path: str) -> None:
        """
        Gets stats data from a file.
        """
        parsed = self._parser.parse("file",
                                    file_path)
        self.add_stats(parsed)
    def from_string(self,
                    string: str) -> None:
        """
        Gets stats data from a string.
        """
        parsed = self._parser.parse("string",
                                    string)
        self.add_stats(parsed)
    def solve_expressions(self,
                          census_data: None | dict[int, str] = None,
                          rounding: Any = DEFAULT_ROUNDING) -> dict[str, str]:
        """
        Returns an evaluated copy of
        your stats. The original data
        remains the same.
        """
        sheet_data: dict[str, str] = self._stats.copy()
        exprEval: ExprEvaluator = ExprEvaluator()
        result: dict[str, str] = exprEval.eval_functions(sheet_data,
                                                         rounding,
                                                         census_data)
        return result
    
if __name__ == "__main__":
    ...