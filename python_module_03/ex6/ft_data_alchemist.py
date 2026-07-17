#!/usr/bin/env python3
import random

initial = [
    'Alice', 'bob', 'Charlie', 'dylan',
    'Emma', 'Gregory', 'john', 'kevin', 'Liam'
    ]
all_capitalized = [name.capitalize() for name in initial]
already_capitalized = [name for name in initial if name[1].isupper()]
scores = {name: random.randint(53, 908) for name in all_capitalized}
average = round(sum(scores.values()) / len(scores), 2)
high_scores = {
    name: score for name, score in scores.items() if score > average
    }

if __name__ == "__main__":
    print("=== Game Data Alchemist ===\n")
    print(f"Initial list of players: {initial}")
    print(f"New list with all names capitalized: {all_capitalized}")
    print(f"New list of capitalized names only: {already_capitalized}\n")
    print(f"Score dict: {scores}")
    print(f"Score average is {average}")
    print(f"High scores: {high_scores}")
