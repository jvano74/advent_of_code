from collections import defaultdict


class Puzzle:
    """
    --- Day 6: Universal Orbit Map ---
    You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves
    transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example,
    you and Santa. You download a map of the local orbits (your puzzle input).

    Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object.
    An orbit looks roughly like this:

                      \
                       \
                        |
                        |
    AAA--> o            o <--BBB
                        |
                        |
                       /
                      /

    In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is
    only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit
    around AAA".

    Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download.
    To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits
    (like the one shown above) and indirect orbits.

    Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long:
    if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

    For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L

    Visually, the above map of orbits looks like this:

            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I

    In this visual representation, when two objects are connected by a line, the one on the right directly orbits
    the one on the left.

    Here, we can count the total number of orbits as follows:

    D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
    L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
    COM orbits nothing.
    The total number of direct and indirect orbits in this example is 42.

    What is the total number of direct and indirect orbits in your map data?

    Your puzzle answer was 142915.

    --- Part Two ---
    Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

    You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets
    you move from any object to an object orbiting or orbited by that object.

    For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN
    Visually, the above map of orbits looks like this:

                              YOU
                             /
            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN

    In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4
    orbital transfers are required:

    K to J
    J to E
    E to D
    D to I
    Afterward, the map of orbits looks like this:

            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN
                     \
                      YOU
    What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object
    SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

    Your puzzle answer was 283.
    """
    pass


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


def parse_orbits(orbit_input: list):
    galaxy = Galaxy(Planet)
    for item in orbit_input:
        planet, satellite = item.split(')')
        if galaxy[satellite].parent:
            raise IndexError
        galaxy[satellite].orbit_planet(galaxy[planet])
        galaxy[satellite].name = satellite
        galaxy[planet].name = planet
    return galaxy


def test_planet_knows_its_name():
    planet = Planet("I'm Kylan")
    assert planet.name == "I'm Kylan"


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


def test_galaxy_transfer_distance_from_a_to_c_returns_2():
    galaxy = parse_orbits(['A)B', 'B)C'])
    assert galaxy.transfer_distance('A', 'C') == 2


def test_galaxy_transfer_distance_with_unequal_starting_orbits_returns_correct():
    galaxy = parse_orbits(['A)B', 'A)C', 'B)D', 'SUN)A'])
    assert galaxy.transfer_distance('C', 'D') == galaxy.transfer_distance('D', 'C') == 3


def test_galaxy_transfer_distance_from_c_to_a_returns_2():
    galaxy = parse_orbits(['A)B', 'B)C'])
    assert galaxy.transfer_distance('C', 'A') == 2


def test_galaxy_transfer_distance_with_nonlinear_galaxy_returns_expected_value():
    galaxy = parse_orbits(['A)B', 'A)C'])
    assert galaxy.transfer_distance('B', 'C') == galaxy.transfer_distance('C', 'B') == 2


def test_galaxy_transfer_distance_from_a_to_a_returns_0():
    galaxy = parse_orbits(['A)B'])
    assert galaxy.transfer_distance('A', 'A') == 0


def test_galaxy_transfer_distance_from_a_to_b_returns_1():
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
    # sample_input = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(',')
    sample_input = 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(',')
    galaxy = parse_orbits(sample_input)
    assert galaxy['D'].checksum() == 3
    assert galaxy['L'].checksum() == 7
    assert galaxy['COM'].checksum() == 0
    assert sum([planet.checksum() for planet in galaxy.values()]) == 42


def test_submission():
    with open('day_06_input.txt', 'r') as f:
        puzzle_input = [input_line.strip() for input_line in f.readlines()]
        # print(puzzle_input)

    galaxy = parse_orbits(puzzle_input)

    assert sum([planet.checksum() for planet in galaxy.values()]) == 142915
    assert galaxy.transfer_distance(galaxy['YOU'].parent.name, galaxy['SAN'].parent.name) == 283
