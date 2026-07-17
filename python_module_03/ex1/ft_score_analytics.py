#!/usr/bin/env python3
import sys

print("=== Player Score Analytics ===")
script = sys.argv[0].removeprefix("./")
if len(sys.argv) <= 1:
    print(
        f"No scores provided. Usage: "
        f"python3 {script} <score1> <score2> ..."
        )
else:
    scores = []
    for arg in sys.argv[1:]:
        try:
            scores += [int(arg)]
        except ValueError:
            print(f"Invalid parameter: {arg!r}")
    if len(scores) == 0:
        print(f"No scores provided. Usage: "
              f"python3 {script} <score1> <score2> ...")
    else:
        total_score = sum(scores)
        count = len(scores)
        average_score = total_score / count
        highest_score = max(scores)
        lowest_score = min(scores)
        Score_range = highest_score - lowest_score
        print(f"Scores processed: {scores}")
        print(f"Total players: {count}")
        print(f"Total score: {total_score}")
        print(f"Average score: {average_score}")
        print(f"High score: {highest_score}")
        print(f"Low score: {lowest_score}")
        print(f"Score range: {Score_range}")
