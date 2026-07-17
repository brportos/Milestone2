#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        if height >= 0:
            self._height = height
        else:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            self._height = 0.0
        if age >= 0:
            self._age = age
        else:
            print(f"{self.name}:  Error, age can't be negative")
            print("Age update rejected")
            self._age = 0

    def show(self) -> None:
        print(f"{self.name}: {self._height:.1f}cm, {self._age} days old")

    def set_height(self, height: float) -> None:
        if height >= 0:
            self._height = height
            print(f"Height updated: {self._height}cm")
        else:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            return

    def set_age(self, age: int) -> None:
        if age >= 0:
            self._age = int(age)
            print(f"Age updated: {self._age} days")
        else:
            print(f"{self.name}:  Error, age can't be negative")
            print("Age update rejected")
            return

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plants = Plant("Rose", 15, 10)
    print("Plant created: ", end="")
    plants.show()
    print()
    plants.set_height(25)
    plants.set_age(30)
    print()
    plants.set_height(-5)
    plants.set_age(-10)
    print()
    print("Current state: ", end="")
    plants.show()
