from collections.abc import Callable
from typing import Any
from operator import add, mul
from functools import reduce, partial, lru_cache, singledispatch


def spell_reducer(spells: list[int], operation: str) -> int:
    OPERATIONS: dict[str, Callable[[int, int], int]] = {
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


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str]
) -> dict[str, Callable[[str], str]]:
    return {
        "flaming": partial(base_enchantment, 50, "Flaming"),
        "earthen": partial(base_enchantment, 50, "Earthen"),
        "flowing": partial(base_enchantment, 50, "Flowing")
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        print("Index can not negative")
    if n in (0, 1):
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def spell(spell: Any) -> str:
        return ("Unknown spell type")

    @spell.register(int)
    def _(spell: int) -> str:
        return (f"Damage spell: {spell} damage")

    @spell.register(str)
    def _(spell: str) -> str:
        return (f"Enchantment: {spell}")

    @spell.register(list)
    def _(spell: list[Any]) -> str:
        return (f"Multi-cast: {len(spell)} spells")

    return spell


if __name__ == "__main__":
    print("\nTesting spell reducer...")
    reducer = spell_reducer([40, 30, 20, 10], "add")
    print(f"Sum: {reducer}")
    reducer = spell_reducer([40, 30, 20, 10], "multiply")
    print(f"Product: {reducer}")
    reducer = spell_reducer([40, 30, 20, 10], "max")
    print(f"Max: {reducer}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(memoized_fibonacci.cache_info())

    dispatch = spell_dispatcher()
    print("\nTesting spell dispatcher...")
    print(dispatch(42))
    print(dispatch("fireball"))
    print(dispatch(["Hello", "42", "Tana"]))
    print(dispatch({"1": 1, "2": 4}))

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{power} {element} enchantment for {target}"

    print("\nTesting partial enchancer...")
    partialer = partial_enchanter(base_enchantment)
    print(partialer['flaming']("wand"))
    print(partialer['flaming']("Sword"))
    print(partialer['flaming']("Cloak"))
