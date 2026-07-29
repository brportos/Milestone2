from collections.abc import Callable


def spell_combiner(spell1: Callable[[str, int], str], spell2: Callable[[str, int], str]) -> Callable[[str, int], str]:
    def  combined_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))

    return  combined_spell

def power_amplifier(base_spell: Callable[[str, int], str], multiplier: int) -> Callable[[str, int], str]:
    def amplifier_spell(target: str , power: int) -> str:
        new_power = power * multiplier
        return base_spell(target, new_power)

    return amplifier_spell

def conditional_caster(condition: Callable[[str, int], str], spell: Callable[[str, int], str]) -> Callable[[str, int], str]:
    def condition_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)

        return "Spell fizzled"
    return combined_spell

def spell_sequence(spells: list[Callable[[str, int], str]]) -> Callable[[str, int], list[str]]:
    def spell_sequence(target: str, power: int) -> list[str]:
        return [spell[target, power] for spell in spells]

    return spell_sequence


if __name__ == "__main__":
    def fireball(target: str, power: int) -> str:
        return f" Fireball hits {target}"

    def heal(target: str, power: int) -> str:
        return f"Heal {target}"

    print("Testing spell combiner...")
    combiner = spell_combiner(fireball, heal)
    result1, result2 = combiner("Dragon", "Dragon")
    print(f"Combined spell result: {result1}, { result2}")
