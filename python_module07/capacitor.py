from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilitities import HealCapability, TransformCapability


def test_healing(factory: HealingCreatureFactory) -> None:
    print("Testing Creature with healing capability")
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, HealCapability):
        print(base.heal())

    print("evolved:")
    print(evolved.describe())
    print(base.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal())


def test_transform(factory: TransformCapability) -> None:
    print("Testing Creature with transform capability")
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())

    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert())


if __name__ == "__main__":
    heal_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    test_healing(heal_factory)
    print("")
    test_transform(transform_factory)
