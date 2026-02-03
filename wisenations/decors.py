from functools import wraps
from typing import Callable
import time
import gc
from random import random

def perf_checker(iters: int = 1,
                 verbose: bool = False,
                 break_in_exception: bool = True) -> Callable:
    if not isinstance(iters, int):
        raise TypeError(f"iters must be a positive integer above 0, not {type(iters).__name__}")
    if iters <= 0:
        raise ValueError(f"iters must be a positive integer above 0, not {iters}")
    if not isinstance(verbose, bool):
        raise TypeError(f"verbose must be a boolean, not {type(verbose).__name__}")
    if not isinstance(break_in_exception, bool):
        raise TypeError(f"break_in_exception must be a boolean, not {type(break_in_exception).__name__}")
    def decorator(func) -> Callable:
        func_name: str = func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            iterations: list[float] = []
            exceptions: list[int] = []
            print(f"> {func_name}():")
            gc_was_enabled: bool = gc.isenabled()
            gc.collect()
            gc.disable()
            for _ in range(iters):
                try:
                    now: float = time.perf_counter()
                    func(*args, **kwargs)
                    then: float = time.perf_counter()
                    duration: float = then - now
                    iterations.append(duration)
                    #exceptions.update({_: False})
                    if verbose:
                        print(f"    > {_+1}°: {duration:.6f}")
                except Exception as e:
                    exceptions.append(_)
                    if verbose:
                        print(f"    > {_+1}°: Exception raised – '{e}'")
                    if break_in_exception:
                        break
                finally:
                    if gc_was_enabled:
                        gc.enable()
            if not iterations:
                print("> No sucessfull iterations to be analyzed")
                print("> perf_checker finished")
                return 0
            iters_num: int = len(iterations)
            exceptions_num: int = len(exceptions) if exceptions else 0
            total_time: float = sum(iterations)
            average: float = total_time / iters_num
            print(f"> {iters_num}/{iters} sucessfull iterations of {func_name}() took {total_time:.6f} seconds to run:")
            print(f"    > Biggest exec time: {max(iterations):.6f}")
            print(f"    > Fastest exec time: {min(iterations):.6f}")
            print(f"    > Average: {average:.6f}")
            print(f"    > Exceptions raised: {exceptions_num}")
            print("> perf_checker finished")
        return wrapper
    return decorator

if __name__ == "__main__":
    @perf_checker(1_000_000, True, False)
    def main():
        if random() > 0.9:
            raise ValueError("Lucky")
        return 0
    main()