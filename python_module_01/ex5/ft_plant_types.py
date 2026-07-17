#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = str(name)
        self.height = float(height)
        self.ages = int(age)

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.ages} days old")

    def grow(self) -> None:
        self.height = round(self.height + 2.1, 1)

    def age(self) -> None:
        self.ages += 1


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color = color
        self.blooming = False

    def show(self) -> None:
        super().show()
        print(f" Color: {self.color}")
        if self.blooming:
            print(f" {self.name} is blooming beautifully!")
        else:
            print(f" {self.name} has not bloomed yet")

    def bloom(self) -> None:
        self.blooming = True


class Tree(Plant):
    def __init__(
            self, name: str, height: float, age: int, trunk_diameter: float
            ) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter = float(trunk_diameter)

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        print(f"Tree {self.name} now produces a shade of {self.height:.1f}cm"
              f" long and {self.trunk_diameter:.1f}cm wide.")


class Vegetable(Plant):
    def __init__(self, name: str,
                 height: float, age: int, harvest_season: str,
                 nutritional_value: int
                 ) -> None:
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self.harvest_season}")
        print(f" Nutritional value: {self.nutritional_value}")

    def grow(self) -> None:
        super().grow()
        self.nutritional_value += 1

    def age(self) -> None:
        super().age()


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    rose = Flower("Rose", 15.0, 10, "red")
    print("=== Flower")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    oak = Tree("Oak", 200.0, 365, 5.0)
    print("\n=== Tree")
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    tomato = Vegetable("Tomato", 5.0, 10, "April", 0)
    print("\n=== Vegetable")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for i in range(20):
        tomato.age()
        tomato.grow()
    tomato.show()
