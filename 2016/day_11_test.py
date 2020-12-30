from queue import PriorityQueue


class Puzzle:
    """
    --- Day 11: Radioisotope Thermoelectric Generators ---

    You come upon a column of four floors that have been entirely sealed off from the rest of the building
    except for a small dedicated lobby. There are some radiation warnings and a big sign which reads
    "Radioisotope Testing Facility".

    According to the project status board, this facility is currently being used to experiment with
    Radioisotope Thermoelectric Generators (RTGs, or simply "generators") that are designed to be paired
    with specially-constructed microchips. Basically, an RTG is a highly radioactive rock that generates
    electricity through heat.

    The experimental RTGs have poor radiation containment, so they're dangerously radioactive. The chips
    are prototypes and don't have normal radiation shielding, but they do have the ability to generate
    an electromagnetic radiation shield when powered. Unfortunately, they can only be powered by their
    corresponding RTG. An RTG powering a microchip is still dangerous to other microchips.

    In other words, if a chip is ever left in the same area as another RTG, and it's not connected to its own RTG,
    the chip will be fried. Therefore, it is assumed that you will follow procedure and keep chips connected to
    their corresponding RTG when they're in the same room, and away from other RTGs otherwise.

    These microchips sound very interesting and useful to your current activities, and you'd like to try to retrieve
    them. The fourth floor of the facility has an assembling machine which can make a self-contained, shielded
    computer for you to take with you - that is, if you can bring it all of the RTGs and microchips.

    Within the radiation-shielded part of the facility (in which it's safe to have these pre-assembly RTGs), there
    is an elevator that can move between the four floors. Its capacity rating means it can carry at most yourself and
    two RTGs or microchips in any combination. (They're rigged to some heavy diagnostic equipment - the assembling
    machine will detach it for you.) As a security measure, the elevator will only function if it contains at least
    one RTG or microchip. The elevator always stops on each floor to recharge, and this takes long enough that the
    items within it and the items on that floor can irradiate each other. (You can prevent this if a Microchip and
    its Generator end up on the same floor in this way, as they can be connected while the elevator is recharging.)

    You make some notes of the locations of each component of interest (your puzzle input). Before you don a hazmat
    suit and start moving things around, you'd like to have an idea of what you need to do.

    When you enter the containment area, you and the elevator will start on the first floor.

    For example, suppose the isolated area has the following arrangement:

    The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    The second floor contains a hydrogen generator.
    The third floor contains a lithium generator.
    The fourth floor contains nothing relevant.

    As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for Lithium, M for Microchip,
    and G for Generator), the initial state looks like this:

    F4 .  .  .  .  .
    F3 .  .  .  LG .
    F2 .  HG .  .  .
    F1 E  .  HM .  LM

    Then, to get everything up to the assembling machine on the fourth floor, the following steps could be taken:

    Bring the Hydrogen-compatible Microchip to the second floor, which is safe because it can get power from
    the Hydrogen Generator:

    F4 .  .  .  .  .
    F3 .  .  .  LG .
    F2 E  HG HM .  .
    F1 .  .  .  .  LM

    Bring both Hydrogen-related items to the third floor, which is safe because the Hydrogen-compatible
    microchip is getting power from its generator:

    F4 .  .  .  .  .
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  LM

    Leave the Hydrogen Generator on floor three, but bring the Hydrogen-compatible Microchip back down with
    you so you can still use the elevator:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  .
    F1 .  .  .  .  LM

    At the first floor, grab the Lithium-compatible Microchip, which is safe because Microchips
    don't affect each other:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 E  .  HM .  LM

    Bring both Microchips up one floor, where there is nothing to fry them:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  LM
    F1 .  .  .  .  .

    Bring both Microchips up again to floor three, where they can be temporarily connected to their
    corresponding generators while the elevator recharges, preventing either of them from being fried:

    F4 .  .  .  .  .
    F3 E  HG HM LG LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  .  HM .  LM
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Leave the Lithium-compatible microchip on the fourth floor, but bring the Hydrogen-compatible one
    so you can still use the elevator; this is safe because although the Lithium Generator is on the
    destination floor, you can connect Hydrogen-compatible microchip to the Hydrogen Generator there:

    F4 .  .  .  .  LM
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Generators up to the fourth floor, which is safe because you can connect the
    Lithium-compatible Microchip to the Lithium Generator upon arrival:

    F4 E  HG .  LG LM
    F3 .  .  HM .  .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring the Lithium Microchip with you to the third floor so you can use the elevator:

    F4 .  HG .  LG .
    F3 E  .  HM .  LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  HG HM LG LM
    F3 .  .  .  .  .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly.
    (Each elevator stop counts as one step, even if nothing is added to or removed from it.)

    In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?

    --- Part Two ---
    You step into the cleanroom separating the lobby from the isolated area and put on the hazmat suit.

    Upon entering the isolated containment area, however, you notice some extra parts on the first floor that
    weren't listed on the record outside:

    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.

    These work just like the other generators and microchips. You'll have to get them up to assembly as well.

    What is the minimum number of steps required to bring all of the objects, including these four new ones,
    to the fourth floor?
    """
    pass


SAMPLE = [
    'The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.',
    'The second floor contains a hydrogen generator.',
    'The third floor contains a lithium generator.',
    'The fourth floor contains nothing relevant.'
]

SAMPLE_FAC = {
    'e': 1,
    'hy_c': 1,
    'li_c': 1,
    'hy_g': 2,
    'li_g': 3}

INPUT = [
    'The first floor contains a promethium generator and a promethium-compatible microchip.',
    'The second floor contains a cobalt generator, a curium generator, a ruthenium generator, '
    + 'and a plutonium generator.',
    'The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, '
    + 'a ruthenium-compatible microchip, and a plutonium-compatible microchip.',
    'The fourth floor contains nothing relevant.']

INPUT_FAC = {
    'e': 1,
    'pr_c': 1,
    'pr_g': 1,
    'co_c': 3,
    'co_g': 2,
    'cu_c': 3,
    'cu_g': 2,
    'ru_c': 3,
    'ru_g': 2,
    'pl_c': 3,
    'pl_g': 2}


def fac_is_safe(fac_map):
    """
    Chips not connected to gen can't be next to other gen
    """
    for component, floor in fac_map.items():
        if component != 'e':
            c_name, c_type = component.split('_')
            if c_type == 'c' and fac_map[c_name + '_g'] != floor:
                c_on_floor = set(c for c, f in fac_map.items() if f == floor and c != 'e')
                for c in c_on_floor:
                    if c.split('_')[1] == 'g':
                        return False
    return True


def test_fac_is_safe():
    mod_fac = SAMPLE_FAC.copy()
    assert fac_is_safe(mod_fac)
    mod_fac['li_c'] = 4
    assert fac_is_safe(mod_fac)
    mod_fac['li_c'] = 2
    assert not fac_is_safe(mod_fac)


def fac_is_complete(fac_map):
    return all(v == 4 for v in fac_map.values())


def test_fac_is_complete():
    fac_map = SAMPLE_FAC.copy()
    assert not fac_is_complete(fac_map)
    fac_map['hy_c'] = 4
    fac_map['li_c'] = 4
    fac_map['hy_g'] = 4
    fac_map['li_g'] = 4
    fac_map['e'] = 4
    assert fac_is_complete(fac_map)


def fac_make_move(orig_fac_map, components_to_floor):
    fac_map = orig_fac_map.copy()
    new_floor, component_list = components_to_floor
    orig_floor = fac_map['e']
    fac_map['e'] = new_floor
    for c in component_list:
        if fac_map[c] != orig_floor:
            raise Exception(f'Unable to move {components_to_floor} from {orig_fac_map}')
        fac_map[c] = new_floor
    return fac_map


def test_fac_make_moves():
    fac_map = SAMPLE_FAC.copy()
    assert fac_make_move(fac_map, (2, ['hy_c'])) == {
        'e': 2,
        'hy_c': 2,
        'hy_g': 2,
        'li_c': 1,
        'li_g': 3}
    assert fac_make_move(fac_map, (2, ['hy_c', 'li_c'])) == {
        'e': 2,
        'hy_c': 2,
        'hy_g': 2,
        'li_c': 2,
        'li_g': 3}


def fac_open_moves(fac_map):
    elevator_floor = fac_map['e']
    c_on_elevator_floor = list(c for c, f in fac_map.items() if f == elevator_floor and c != 'e')
    floors = []
    if elevator_floor == 1:
        floors = [2]
    elif elevator_floor == 2:
        floors = [1, 3]
    elif elevator_floor == 3:
        floors = [2, 4]
    elif elevator_floor == 4:
        floors = [3]
    options = []
    for f in floors:
        for i in range(0, len(c_on_elevator_floor)):
            options.append((f, [c_on_elevator_floor[i]]))
            for j in range(i + 1, len(c_on_elevator_floor)):
                options.append((f, [c_on_elevator_floor[i], c_on_elevator_floor[j]]))
    return options


def test_fac_open_moves():
    fac_map = SAMPLE_FAC.copy()
    assert fac_open_moves(fac_map) == [(2, ['hy_c']),
                                       (2, ['hy_c', 'li_c']),
                                       (2, ['li_c'])]
    fac_map['e'] = 2
    assert fac_open_moves(fac_map) == [(1, ['hy_g']), (3, ['hy_g'])]


def find_solution_non_sorted(fac_map):
    history = {}
    current_min = 0
    fac_map_hash = ''.join(sorted(f'{i}:{f}' for i, f in fac_map.items()))
    history[fac_map_hash] = 0
    exploring = [(0, fac_map.copy())]
    while len(exploring) > 0:
        move_count, fac_to_test = exploring.pop()
        if fac_is_complete(fac_to_test):
            if current_min > 0:
                current_min = min(move_count, current_min)
            else:
                current_min = move_count
        elif move_count >= current_min > 0:
            pass
        else:
            moves = fac_open_moves(fac_to_test)
            for mv in moves:
                possible_fac = fac_make_move(fac_to_test, mv)
                possible_fac_hash = ''.join(sorted(f'{i}:{f}' for i, f in possible_fac.items()))
                if fac_is_safe(possible_fac):
                    if possible_fac_hash in history and history[possible_fac_hash] <= (move_count + 1):
                        pass
                    else:
                        history[possible_fac_hash] = move_count + 1
                        exploring.append((move_count + 1, possible_fac.copy()))
    return current_min


def find_solution(fac_map):
    hold = {}
    exploring = PriorityQueue()
    history = set()
    fac_map_hash = ','.join(sorted(f'{i}:{f}' for i, f in fac_map.items()))
    hold[fac_map_hash] = fac_map
    exploring.put((0, fac_map_hash))
    history.add(fac_map_hash)
    while not exploring.empty():
        move_count, fac_to_test_hash = exploring.get()
        fac_to_test = hold.pop(fac_to_test_hash)
        if fac_is_complete(fac_to_test):
            return move_count
        else:
            moves = fac_open_moves(fac_to_test)
            for mv in moves:
                possible_fac = fac_make_move(fac_to_test, mv)
                possible_fac_hash = ','.join(sorted(f'{i}:{f}' for i, f in possible_fac.items()))
                if fac_is_safe(possible_fac) and possible_fac_hash not in history:
                    hold[possible_fac_hash] = possible_fac
                    exploring.put((move_count + 1, possible_fac_hash))
                    history.add(possible_fac_hash)
    raise Exception('Could not find solution')


def test_example_find_solution():
    assert find_solution(SAMPLE_FAC) == 11
    assert find_solution_non_sorted(SAMPLE_FAC) == 11


def test_find_solution():
    assert find_solution(INPUT_FAC) == 33
    # assert find_solution_non_sorted(INPUT_FAC) == 33


def xtest_find_solution_part2():
    # disabling as it took quite a while for search to run
    # curious if there is a better/faster way to search?
    fac_part_2 = INPUT_FAC.copy()
    fac_part_2['el_c'] = 1
    fac_part_2['el_g'] = 1
    fac_part_2['di_c'] = 1
    fac_part_2['di_g'] = 1
    assert find_solution(fac_part_2) == 57
