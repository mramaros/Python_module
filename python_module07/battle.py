from ex0 import AquaFactory, FlameFactory, CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(base.attack())


def battle(creature1: CreatureFactory, creature2: CreatureFactory) -> None:
    print("Testing battle")
    base1 = creature1.create_base()
    base2 = creature2.create_base()
    print(base1.describe())
    print("VS.")
    print(base2.describe())
    print("fight!")
    print(base1.attack())
    print(base2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_Factory = AquaFactory()
    test_factory(flame_factory)
    print("")
    test_factory(aqua_Factory)
    print("")
    battle(flame_factory, aqua_Factory)
