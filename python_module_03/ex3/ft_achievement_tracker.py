#!/usr/bin/env python3
import random


def gen_player_achievements() -> set[str]:
    all_achievements = [
        "Crafting Genius", "Strategist", "World Savior", "Speed Runner",
        "Survivor", "Master Explorer", "Treasure Hunter",
        "Unstoppable", "First Steps", "Collector Supreme", "Untouchable",
        "Sharp Mind", "Boss Slayer", "Hidden Path Finder"
        ]
    k = random.randint(4, len(all_achievements))
    return set(random.sample(all_achievements, k))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()
    players = [
            ("Alice", alice),
            ("Bob", bob),
            ("Charlie", charlie),
            ("Dylan", dylan)
        ]
    for name, achievements in players:
        print(f"Player {name}: {achievements}")

    all_unique = alice.union(bob, charlie, dylan)
    print(f"\nAll distinct achievements: {all_unique}")

    common = alice.intersection(bob, charlie, dylan)
    print(f"\nCommon achievements: {common}")

    print()
    for name, their_set in players:
        others: set[str] = set()
        for other_name, other_set in players:
            if other_name != name:
                others = others.union(other_set)
        unique = their_set.difference(others)
        print(f"Only {name} has: {unique}")
    print()
    for name, their_set in players:
        missing = all_unique.difference(their_set)
        print(f"{name} is missing: {missing}")
