from wisenations import SheetManager
from wisenations.utils import SheetSyntax, ExprEvaluator
from wisenations.decors import perf_checker
from pprint import pprint

#@perf_checker(100, True)
def main():
    sm: SheetManager = SheetManager()
    sm.new_sheet("s1")
    #my_sheet = sm.get_sheet("s1")

    ss: SheetSyntax = SheetSyntax()
    exprEval: ExprEvaluator = ExprEvaluator()

    data: [int, str] = {
        0: "0.05",
        45: "13000000"
    }

    with open("samples/sheet1.txt", "r") as f:
        samp = ss.clear_spaces(f.read())
        result = ss.sheet_to_dict(samp,
                                  data)
        exprEval.eval_functions(result)
        pprint(result)

if __name__ == "__main__":
    main()