#!/usr/bin/env python3

class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, {self._age_calls} age,"
                  f" {self._show_calls} show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = str(name)
        self.height = float(height)
        self.ages = int(age)
        self.stats = Plant.Stats()

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.ages} days old")
        self.stats._show_calls += 1

    def grow(self, increment: float = 8.0) -> None:
        self.height = round(self.height + increment, 1)
        self.stats._grow_calls += 1

    def age(self, increment: int = 20) -> None:
        self.ages += increment
        self.stats._age_calls += 1

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls(name="Unknown plant", height=0.0, age=0)


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
    class Stats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self.shade_calls = 0

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, {self._age_calls} age,"
                  f" {self._show_calls} show {self.shade_calls} shade")

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float):
        super().__init__(name, height, age)
        self.trunk_diameter = float(trunk_diameter)
        self.stats: Tree.Stats = Tree.Stats()

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self.trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        print(
            f"Tree {self.name} now produces a shade "
            f"of {self.height:.1f}cm long and "
            f"{self.trunk_diameter:.1f}cm wide."
            )
        self.stats.shade_calls += 1


class Seed(Flower):
    def __init__(self, name: str, height: float,
                 age: int, color: str, seeds: int) -> None:
        super().__init__(name, height, age, color)
        self.seeds = int(seeds)

    def grow(self, increment: float = 30.0) -> None:
        self.height = round(self.height + increment, 1)
        self.stats._grow_calls += 1

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seeds}")


def display_stats(plant: "Plant") -> None:
    plant.stats.display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("\n=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    rose = Flower("Rose", 15, 10, "red")
    print("\n=== Flower")
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)

    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)

    oak = Tree("Oak", 200.0, 365, 5.0)
    print("\n=== Tree")
    oak.show()
    print("[statistics for Oak]")
    display_stats(oak)

    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 0)
    sunflower.show()

    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.seeds = 42
    sunflower.show()
    print("[statistics for Sunflower]")
    display_stats(sunflower)

    print("\n=== Anonymous")
    unknown = Plant.create_anonymous()
    unknown.show()
    print("[statistics for Unknown plant]")
    display_stats(unknown)
