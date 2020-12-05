from collections import defaultdict


class Planet:
    def __init__(self, name: str = None):
        self.parent = None
        self.name = name

    def orbit_planet(self, parent):
        self.parent = parent

    def checksum(self):
        if self.parent:
            return 1 + self.parent.checksum()
        return 0


class Galaxy(defaultdict):
    def transfer_distance(self, you: str, santa: str):
        if you == santa:
            return 0
        santas_checksum = self[santa].checksum()
        your_checksum = self[you].checksum()
        if your_checksum > santas_checksum:
            return 1 + self.transfer_distance(self[you].parent.name, santa)
        if your_checksum < santas_checksum:
            return 1 + self.transfer_distance(self[santa].parent.name, you)
        return 2 + self.transfer_distance(self[you].parent.name, self[santa].parent.name)


def parse_orbits(input: list):
    # galaxy = defaultdict(Planet)
    galaxy = Galaxy(Planet)
    for item in input:
        planet, sattelite = item.split(')')
        if galaxy[sattelite].parent:
            raise IndexError
        galaxy[sattelite].orbit_planet(galaxy[planet])
        galaxy[sattelite].name = sattelite
        galaxy[planet].name = planet
    return galaxy


def test_planet_knows_its_name():
    planet = Planet("I'm Kylan")
    planet.name == "I'm Kylan"


def test_can_create_planet_class():
    planet = Planet()
    assert planet


def test_planet_can_set_root():
    planet1 = Planet()
    planet2 = Planet()
    planet1.orbit_planet(planet2)

    assert planet2 == planet1.parent


def test_planet_with_no_orbits_can_calculate_its_checksum():
    center_planet = Planet()
    assert center_planet.checksum() == 0


def test_planet_with_1_direct_orbit_can_calculate_its_checksum():
    center_planet = Planet()
    orbiting_planet = Planet()
    orbiting_planet.orbit_planet(center_planet)

    assert orbiting_planet.checksum() == 1


def test_planet_with_1_direct_and_1_indirect_orbits_can_calculate_its_checksum():
    center_planet = Planet()
    direct_orbiting_planet = Planet()
    indirect_orbiting_planet = Planet()
    direct_orbiting_planet.orbit_planet(center_planet)
    indirect_orbiting_planet.orbit_planet(direct_orbiting_planet)
    assert indirect_orbiting_planet.checksum() == 2


def test_Galaxy_transfer_distance_from_A_to_C_returns_2():
    galaxy = parse_orbits(['A)B', 'B)C'])
    assert galaxy.transfer_distance('A', 'C') == 2


def test_Galaxy_transfer_distance_with_unequal_starting_orbits_returns_correct():
    galaxy = parse_orbits(['A)B', 'A)C', 'B)D', 'SUN)A'])
    assert galaxy.transfer_distance('C', 'D') == galaxy.transfer_distance('D', 'C') == 3


def test_Galaxy_transfer_distance_from_C_to_A_returns_2():
    galaxy = parse_orbits(['A)B', 'B)C'])
    assert galaxy.transfer_distance('C', 'A') == 2


def test_Galaxy_transfer_distance_with_nonlinear_galaxy_returns_expected_value():
    galaxy = parse_orbits(['A)B', 'A)C'])
    assert galaxy.transfer_distance('B', 'C') == galaxy.transfer_distance('C', 'B') == 2


def test_Galaxy_transfer_distance_from_A_to_A_returns_0():
    galaxy = parse_orbits(['A)B'])
    assert galaxy.transfer_distance('A', 'A') == 0

def test_Galaxy_transfer_distance_from_A_to_B_returns_1():
    galaxy = parse_orbits(['A)B'])
    assert galaxy.transfer_distance('A', 'B') == 1


def test_parse_orbits_returns_galaxy_dict():
    galaxy = parse_orbits(['A)B'])
    assert type(galaxy) == Galaxy

def test_parse_orbits_returns_correct_number_of_planets_in_galaxy():
    galaxy = parse_orbits(['A)B'])
    all_planets = True
    for planet in galaxy.values():
        if type(planet) is not Planet:
            all_planets = False
    assert len(galaxy) == 2 and all_planets

def test_parse_orbits_returns_dict_with_planet_names_for_keys():
    planet_names = ['A', 'B']
    galaxy = parse_orbits(['A)B'])
    assert set(planet_names) == set(galaxy)

def test_parse_orbits_returns_correct_name_keys_for_any_passed_names():
    planet_names = ['D', 'F']
    galaxy = parse_orbits(['D)F'])
    assert set(planet_names) == set(galaxy)

def test_galaxy_of_one_planet_orbiting_another_returns_correct_checksums():
    galaxy = parse_orbits(['A)B'])
    assert galaxy['A'].checksum() == 0
    assert galaxy['B'].checksum() == 1

def test_galaxy_of_complex_relationship_returns_correct_checksums():
    # input = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(',')
    input = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(',')
    galaxy = parse_orbits(input)

    assert galaxy['D'].checksum() == 3
    assert galaxy['L'].checksum() == 7
    assert galaxy['COM'].checksum() == 0

    assert sum([planet.checksum() for planet in galaxy.values()]) == 42


def test_submission():
    with open('day_06_input.txt', 'r') as f:
        input = [input_line.strip() for input_line in f.readlines()]
        #print(input)

    galaxy = parse_orbits(input)

    assert sum([planet.checksum() for planet in galaxy.values()]) == 142915
    assert galaxy.transfer_distance(galaxy['YOU'].parent.name, galaxy['SAN'].parent.name) == 283