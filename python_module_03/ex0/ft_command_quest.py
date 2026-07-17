#!/usr/bin/env python3
import sys

print("=== Command Quest ===")
if sys.argv[0][:2] == "./":
    print("Program name:", sys.argv[0][2:])
else:
    print("Program name:", sys.argv[0])
if len(sys.argv) <= 1:
    print("No arguments provided!")
else:
    print("Arguments received:", len(sys.argv) - 1)
    i = 1
    while i < len(sys.argv):
        print(f"Argument {i}: {sys.argv[i]}")
        i += 1
print("Total arguments:", len(sys.argv))
