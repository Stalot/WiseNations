from string import ascii_letters, digits
import math
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from random import random, randint
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
            "RNG": self._rng,
            "RANDBETWEEN": self._rand_between,
            "AVG": self._average
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
        return Decimal(str(random()))
    def _rand_between(self, args: list[Decimal]):
        min_value: int = int(args[0])
        max_value: int = int(args[1])
        result = randint(min_value, max_value+1)
        return result
    def _average(self, args: list[Decimal]):
        return sum(args) / len(args)
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
        try:
            return str(self.funcs[func_id](parse_args(args)))
        except KeyError:
            raise ValueError(f"{func_id}() is not a known function")
        except IndexError as ie:
            raise ValueError(f"{ie} — Failed to satisfy {func_id}()'s necessary parameters")
if __name__ == "__main__":
    fm = FuncMaster()
    result = fm.call("CEIL", "67.757")
    print(result)