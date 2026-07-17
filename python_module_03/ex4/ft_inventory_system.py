#!/usr/bin/env python3
import sys

print("=== Inventory System Analysis ===")

inventory = {}
for arg in sys.argv[1:]:
    parts = arg.split(":")
    if len(parts) != 2:
        print(f"Error - invalid parameter {arg!r}")
        continue
    name = parts[0].strip()
    if not name.isalpha():
        print(f"invalid {arg}")
        continue
    raw_qty = parts[1]
    if name in inventory:
        print(f"Redundant item {name!r} - discarding")
        continue
    try:
        qty = int(raw_qty)
    except ValueError as e:
        print(f"Quantity error for {name!r}: {e}")
        continue
    inventory[name] = qty

print(f"Got inventory: {inventory}")
item_lst = list(inventory.keys())
print(f"Item list: {item_lst}")

total = sum(inventory.values())
count = len(inventory)
print(f"Total quantity of the {count} items: {total}")

try:
    for item in inventory.keys():
        pct = round((inventory[item] / total) * 100, 1)
        print(f"Item {item} represents {pct} %")

    if inventory:
        most = list(inventory.keys())[0]
        least = list(inventory.keys())[0]
        for item in inventory.keys():
            if inventory[item] > inventory[most]:
                most = item
            if inventory[item] < inventory[least]:
                least = item
        print(f"Item most abundant: {most} with quantity {inventory[most]}")
        print(
        f"Item least abundant: {least} with quantity {inventory[least]}"
        )
    else:
        print("No arguments provided!")
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")
except ZeroDivisionError as e:
    print(f"{e}")