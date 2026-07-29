from collections.abc import Callable
from typing import Any
from operator import add, mul


from functools import reduce
def spell_reducer(spells: list[int], operation: str) -> int:
    OPERATIONS = {
        "add": add,
        "multiply": mul,
        "max": max,
        "min": min
    }
    if not spells:
        return 0
    if operation not in OPERATIONS:
        print("Operation is unknown")
    return reduce(OPERATIONS[operation], spells)

from functools import partial

def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    version1 = partial(base_enchantment, 50, element, target)
    version2 = partial(base_enchantment, 50, element, target)
    version3 = partial(base_enchantment, 50, element, target)
    return {
        "version1": version1,
        "version2": version2,
        "version3": version3
    }


def memoized_fibonacci(n: int) -> int:
    ...
def spell_dispatcher() -> Callable[[Any], str]:
    ...


if __name__ == "__main__":
    def base_enchantment(power, element, target):
        return f"{power} {element} for {target}"
par = partial_enchanter(base_enchantment)
print(par['version1'](50, "fir"))