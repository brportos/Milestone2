#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.ages = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.ages} days old")

    def grow(self, increment: float = 0.8) -> None:
        self.height = round(self.height + increment, 1)

    def age(self) -> None:
        self.ages += 1


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    rose = Plant("Rose", 25.0, 30)
    rose.show()

    height_init = rose.height
    for day in range(1, 8):
        print(f'=== Day {day} ===')
        rose.grow()
        rose.age()
        rose.show()
    total = round(rose.height - height_init, 1)
    print(f"Growth this week: {total}cm")
