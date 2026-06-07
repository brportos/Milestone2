from ex0.ex0 import Creature, CreatureFactory
from ex1.ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (BattleStrategy, NormalStrategy, AggressiveStrategy, DefensiveStrategy, InvalidStrategyError)
from ex0.ex0 import FlameFactory, AquaFactory 


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    n: int = len(opponents)
    print(f"{n} opponents involved")
    creatures: list[Creature] = [factory.create_base() for factory, _ in opponents]
    strategies: list[BattleStrategy] = [strategy for _, strategy in opponents]
    for i in range(n):
        for j in range(i + 1, n):
            print("\n* Battle *")
            c1: Creature = creatures[i]
            c2: Creature = creatures[j]
            s1: BattleStrategy = strategies[i]
            s2: BattleStrategy = strategies[j]
            print(c1.describe())
            print("vs.")
            print(c2.describe())
            print("now fight!")

            try:
                for line in s1.act(c1):
                    print(line)
                for line in s2.act(c2):
                    print(line)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    normal: NormalStrategy = NormalStrategy()
    aggressive: AggressiveStrategy = AggressiveStrategy()
    defensive: DefensiveStrategy = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(FlameFactory(), normal), (HealingCreatureFactory(), defensive)])
    print("\nTournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(FlameFactory(), aggressive), (HealingCreatureFactory(), defensive)])
    print("\nTournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([(AquaFactory(), normal), (HealingCreatureFactory(), defensive), (TransformCreatureFactory(), aggressive)])
