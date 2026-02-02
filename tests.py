from wisenations import SheetManager
from wisenations.utils import SheetSyntax, ExprEvaluator
from pprint import pprint
from pathlib import Path
import re

sm = SheetManager()
sm.new_sheet("s1")
my_sheet = sm.get_sheet("s1")

ss = SheetSyntax()
exprEval = ExprEvaluator()

with open("sample.txt", "r") as f:
    samp = ss.clear_spaces(f.read())
    result = ss.sheet_to_dict(samp)
    exprEval.eval_functions(result)
    pprint(result)