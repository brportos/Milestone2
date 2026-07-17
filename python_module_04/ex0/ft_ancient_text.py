#!/usr/bin/env python3
import sys


def display_usage() -> None:
    if sys.argv[0]:
          print(f"Usage: {sys.argv[0]} <file>\n")


def recover_ancient_text(filename: str) -> None:
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file {filename!r}")

    try:
        file = open(filename, "r")
    except Exception as e:
        print(f"Error opening file {filename!r}: {e}")
        return
    try:
        content: str = file.read()
        print(f"---\n\n{content}\n---")
    except Exception as e:
        print(e)
    file.close()
    print(f"File {filename!r} closed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        display_usage()
        sys.exit(1)
    filename: str = sys.argv[1]
    recover_ancient_text(filename)
