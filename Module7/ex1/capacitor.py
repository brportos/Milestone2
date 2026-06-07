from typing import cast
from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability
from ex0.ex0 import Creature, CreatureFactory


if __name__ == "__main__":
    print("Testing Creature with healing capability")
    heal_factory: HealingCreatureFactory = HealingCreatureFactory()
    base: Creature = heal_factory.create_base()
    evolved: Creature = heal_factory.create_evolved()
    print("base:")
    print(base.describe())
    print(base.attack())
    print(cast(HealCapability, base).heal())
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(cast(HealCapability, evolved).heal())
    print("\nTesting Creature with transform capability")
    tf_factory: TransformCreatureFactory = TransformCreatureFactory()
    base_t: Creature = tf_factory.create_base()
    evolved_t: Creature = tf_factory.create_evolved()
    for creature in [base_t, evolved_t]:
        label: str = "base:" if creature is base_t else "evolved:"
        print(label)
        tc: TransformCapability = cast(TransformCapability, creature)
        print(creature.describe())
        print(creature.attack())
        print(tc.transform())
        print(creature.attack())
        print(tc.revert())
