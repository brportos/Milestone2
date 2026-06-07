from ex0.ex0 import Creature, CreatureFactory
from .capabilities import HealCapability


class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def describe(self) -> str:
        return ("Sproutling is a Grass type Creature")
    
    def attack(self) -> str:
        return ("Sproutling uses Vine Whip!")

    def heal(self) -> str:
        return ("Sproutling heals itself for a small amount")


class Bloomelle(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Bloomelle", "Grass/Fairy")

    def describe(self) -> str:
        return ("Bloomelle is a Grass/Fairy type Creature")
    
    def attack(self) -> str:
        return ("Bloomelle uses Petal Dance!")

    def heal(self) -> str:
        return ("Bloomelle heals itself and others for a large amount")


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()
