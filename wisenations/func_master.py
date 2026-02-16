from string import ascii_letters, digits
import math
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from random import random
from typing import Any, Iterable
from sympy import Tuple

class FuncMaster:
    def __init__(self):
        self.funcs = {
            "MAX": self._max,
            "MIN": self._min,
            "CEIL": self._ceil,
            "FLOOR": self._floor,
            "SQRT": self._sqrt,
            "RNG": self._rng
        }
    
    def _max(self, args: list[Decimal]):
        return max(args)
    def _min(self, args: list[Decimal]):
        return min(args)
    def _ceil(self, args: list[Decimal]):
        num: Decimal = args[0]
        return num.to_integral_exact(rounding=ROUND_CEILING)
    def _floor(self, args: list[Decimal]):
        num: Decimal = args[0]
        return num.to_integral_exact(rounding=ROUND_FLOOR)
    def _sqrt(self, args: list[Decimal]):
        num = args[0]
        return math.sqrt(num)
    def _rng(self, args: list[Decimal]):
        max_range = args[0]
        return max_range * Decimal(str(random()))
    def call(self, 
             func_id: str,
             args: str):
        def parse_args(args: Any) -> list[Decimal]:
            if isinstance(args, Tuple):
                args = [str(arg) for arg in args]
            else:
                args: list[str] = [str(args)]
            result: list[Decimal] = []
            for item in args:
                value: str = item.strip()
                try:
                    result.append(Decimal(value))
                except InvalidOperation as io:
                    raise ValueError(f"Couldn't convert {value} to a Decimal — {io}")
            return result
        return str(self.funcs[func_id](parse_args(args)))

if __name__ == "__main__":
    fm = FuncMaster()
    result = fm.call("CEIL", "67.757")
    print(result)