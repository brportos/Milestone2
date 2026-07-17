#!/usr/bin/env python3
import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        coords = []
        try:
            for i in parts:
                coords.append(float(i))
            return tuple(coords)
        except ValueError as e:
            print(f"Error on parameter {i!r}: {e}")


if __name__ == "__main__":
    try:
        print("=== Game Coordinate System ===\n")
        print("Get a first set of coordinates")
        pos1 = get_player_pos()
        print(f"Got a first tuple: {pos1}")
        x1, y1, z1 = pos1
        print(f"It includes: X={x1} Y={y1} Z={z1}")
        dist_center = math.sqrt(x1**2 + y1**2 + z1**2)
        print(f"Distance to center: {round(dist_center, 4)}")
        print("\nGet a second set of coordinates")
        x2, y2, z2 = get_player_pos()
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        print(f"Distance between the 2 sets of coordinates: {round(dist, 4)}")
    except KeyboardInterrupt as e:
        print(f"{e}")

