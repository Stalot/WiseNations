from wisenations import SheetManager
from wisenations.utils import ExprEvaluator
from wisenations.decors import perf_checker
from pprint import pprint

@perf_checker(100, True)
def main():
    data = {
        0: "0.005",
        45: "100000"
    }
    sm: SheetManager = SheetManager()
    sm.new_sheet("fullworthia_rp")
    
    string: str = """
    max_hp = {12*6}
    strengh = {[45]*[0]}
    """
    
    #sm.del_sheet("fullworthia_rp")
    my_sheet = sm["fullworthia_rp"]
    print(my_sheet)
    my_sheet.from_file("samples/sheet1.txt")
    #my_sheet.from_string(string,
    #                     data)
    #pprint(my_sheet.solve_expressions(data))
    #print(my_sheet.get_all_stats())
if __name__ == "__main__":
    main()