from ex0.ex0 import Creature, CreatureFactory
from .capabilities import TransformCapability


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
        self.transformed: bool = False

    def describe(self) -> str:
        return (f"Shiffting is a Normal type Creature")

    def attack(self) -> str:
        if self.transformed:
            return ("Shiftling performs a boosted strike!")
        return ("Shiftling attacks normally.")

    def transform(self) -> str:
        self.transformed = True
        return ("Shiftling shifts into a sharper form!")
    
    def revert(self) -> str:
        self.transformed = False
        return("Shiftling returns to normal.")


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        super().__init__("Morphagon", "Normal/Dragon")
        self.transformed = False

    def describe(self) -> str:
        return ("Morphagon is a Normal/Dragon type Creature")

    def attack(self) -> str:
        if self.transformed:
            return ("Morphagon unleashes a devastating morph strike!")
        return ("Morphagon attacks normally.")

    def transform(self) -> str:
        self.transformed = True
        return ("Morphagon morphs into a dragonic battle form!")
    
    def revert(self) -> str:
        self.transformed = False
        return("Morphagon stabilizes its form.")


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
