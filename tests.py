from wisenations import SheetManager, Interpreter
from pprint import pprint as pp

inter= Interpreter()
result = inter.script_to_dict("sample.txt")
pp(result)