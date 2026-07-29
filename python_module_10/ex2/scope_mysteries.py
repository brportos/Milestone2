from collections.abc import Callable


def mage_counter() -> Callable[[None], int]:
    count = 0
    def counter() ->int:
        nonlocal count
        count += 1
        return count
    return counter

def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    current_power = initial_power
    def accumulates_power(amount: int) -> int:
        nonlocal current_power
        current_power += amount
        return current_power
    return accumulates_power

    
def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def specified_enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return specified_enchantment

def memory_vault() -> dict[str, Callable[[str, int | None], str | None]]:
    vault = {}
    def store(key: str, value: int) -> None:
        vault[key] = value
        
    def recall(key: str) -> str:
        try:
            return vault[key]
        except KeyError:
            return "Memory not found"

    return {
        "store": store ,
        "recall": recall
        }


if __name__ == "__main__":
    print("Testing mage counter...")
    mage1 = mage_counter()
    print(f"counter_a call 1: {mage1()}")
    print(f"counter_a call 2: {mage1()}")

    mage2 = mage_counter()
    print(f"counter_b call 1: {mage2()}\n")

    print("Testing spell accumulator...")
    accumul1 = spell_accumulator(100)
    print(f"Base 100, add 20: {accumul1(20)}")
    print(f"Base 100, add 50: {accumul1(30)}")

    print("\nTesting enchantment factory...")
    ench = enchantment_factory("Flaming Sword")
    print(ench("\nFrozen Shield\n"))

    print("Testing memory vault...")
    vault = memory_vault()
    vault['store']('secret', 42)
    recall = vault['recall']('secret')
    recall1 = vault['recall']('unknown')
    print(f"Store 'secret' = {recall}")
    print(f"Recall 'unknown': {recall1}")
