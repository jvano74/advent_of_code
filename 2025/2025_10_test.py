import sympy as sp
import numpy as np

from sympy.core.numbers import int_valued
from scipy.optimize import milp, LinearConstraint

from pathlib import Path
from typing import List
from itertools import combinations


class Puzzle:
    """
    --- Day 10: Factory ---
    Just across the hall, you find a large factory. Fortunately, the Elves here
    have plenty of time to decorate. Unfortunately, it's because the factory
    machines are all offline, and none of the Elves can figure out the
    initialization procedure.

    The Elves do have the manual for the machines, but the section detailing the
    initialization procedure was eaten by a Shiba Inu. All that remains of the
    manual are some indicator light diagrams, button wiring schematics, and
    joltage requirements for each machine.

    For example:

    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

    The manual describes one machine per line. Each line contains a single
    indicator light diagram in [square brackets], one or more button wiring
    schematics in (parentheses), and joltage requirements in {curly braces}.

    To start a machine, its indicator lights must match those shown in the
    diagram, where . means off and # means on. The machine has the number of
    indicator lights shown, but its indicator lights are all initially off.

    So, an indicator light diagram like [.##.] means that the machine has four
    indicator lights which are initially off and that the goal is to
    simultaneously configure the first light to be off, the second light to be
    on, the third to be on, and the fourth to be off.

    You can toggle the state of indicator lights by pushing any of the listed
    buttons. Each button lists which indicator lights it toggles, where 0 means
    the first light, 1 means the second light, and so on. When you push a
    button, each listed indicator light either turns on (if it was off) or turns
    off (if it was on). You have to push each button an integer number of times;
    there's no such thing as "0.5 presses" (nor can you push a button a negative
    number of times).

    So, a button wiring schematic like (0,3,4) means that each time you push
    that button, the first, fourth, and fifth indicator lights would all toggle
    between on and off. If the indicator lights were [#.....], pushing the
    button would change them to be [...##.] instead.

    Because none of the machines are running, the joltage requirements are
    irrelevant and can be safely ignored.

    You can push each button as many times as you like. However, to save on
    time, you will need to determine the fewest total presses required to
    correctly configure all indicator lights for all machines in your list.

    There are a few ways to correctly configure the first machine:

    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    You could press the first three buttons once each, a total of 3 button
    presses.

    You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button
    presses.

    You could press all of the buttons except (1,3) once each, a total of 5
    button presses.

    However, the fewest button presses required is 2. One way to do this is by
    pressing the last two buttons ((0,2) and (0,1)) once each.

    The second machine can be configured with as few as 3 button presses:

    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}

    One way to achieve this is by pressing the last three buttons ((0,4),
    (0,1,2), and (1,2,3,4)) once each.

    The third machine has a total of six indicator lights that need to be
    configured correctly:

    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

    The fewest presses required to correctly configure it is 2; one way to do
    this is by pressing buttons (0,3,4) and (0,1,2,4,5) once each.

    So, the fewest button presses required to correctly configure the indicator
    lights on all of the machines is 2 + 3 + 2 = 7.

    Analyze each machine's indicator light diagram and button wiring schematics.
    What is the fewest button presses required to correctly configure the
    indicator lights on all of the machines?

    Your puzzle answer was 396.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    All of the machines are starting to come online! Now, it's time to worry
    about the joltage requirements.

    Each machine needs to be configured to exactly the specified joltage levels
    to function properly. Below the buttons on each machine is a big lever that
    you can use to switch the buttons from configuring the indicator lights to
    increasing the joltage levels. (Ignore the indicator light diagrams.)

    The machines each have a set of numeric counters tracking its joltage
    levels, one counter per joltage requirement. The counters are all initially
    set to zero.

    So, joltage requirements like {3,5,4,7} mean that the machine has four
    counters which are initially 0 and that the goal is to simultaneously
    configure the first counter to be 3, the second counter to be 5, the third
    to be 4, and the fourth to be 7.

    The button wiring schematics are still relevant: in this new joltage
    configuration mode, each button now indicates which counters it affects,
    where 0 means the first counter, 1 means the second counter, and so on. When
    you push a button, each listed counter is increased by 1.

    So, a button wiring schematic like (1,3) means that each time you push that
    button, the second and fourth counters would each increase by 1. If the
    current joltage levels were {0,1,2,3}, pushing the button would change them
    to be {0,2,2,4}.

    You can push each button as many times as you like. However, your finger is
    getting sore from all the button pushing, and so you will need to determine
    the fewest total presses required to correctly configure each machine's
    joltage level counters to match the specified joltage requirements.

    Consider again the example from before:

    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

    Configuring the first machine's counters requires a minimum of 10 button
    presses. One way to do this is by pressing (3) once, (1,3) three times,
    (2,3) three times, (0,2) once, and (0,1) twice.

    Configuring the second machine's counters requires a minimum of 12 button
    presses. One way to do this is by pressing (0,2,3,4) twice, (2,3) five
    times, and (0,1,2) five times.

    Configuring the third machine's counters requires a minimum of 11 button
    presses. One way to do this is by pressing (0,1,2,3,4) five times,
    (0,1,2,4,5) five times, and (1,2) once.

    So, the fewest button presses required to correctly configure the joltage
    level counters on all of the machines is 10 + 12 + 11 = 33.

    Analyze each machine's joltage requirements and button wiring schematics.
    What is the fewest button presses required to correctly configure the
    joltage level counters on all of the machines?

    Your puzzle answer was 15688.

    Both parts of this puzzle are complete! They provide two gold stars: **
    """


with open(Path(__file__).parent / "2025_10_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")
    RAW_INPUT.pop()

SAMPLE = [
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
]


class Machine:
    def __init__(self, raw_machine: str):
        self.raw_machine = raw_machine
        raw_machine = raw_machine.split(" ")

        joltage = raw_machine.pop()
        self.joltage = [int(d) for d in joltage[1:-1].split(",")]

        state = raw_machine.pop(0)
        self.target = sum(2**p if d == "#" else 0 for p, d in enumerate(state[1:-1]))

        self.buttons = []
        rows = []

        while raw_machine:
            element = raw_machine.pop(0)
            if element[0] != "(":
                raise Exception("something went wrong with input data")
            element = [int(d) for d in element[1:-1].split(",")]
            self.buttons.append(sum(2**d for d in element))
            row = [1 if d in element else 0 for d, _ in enumerate(self.joltage)]
            rows.append(row)

        self.matrix = sp.Matrix(rows).T
        # self.np_matrix = np.array(rows, dtype=float).T
        self.np_matrix = np.array(rows, dtype=int).T

    def min_on(self):
        for n in range(1, len(self.buttons) + 1):
            for pushed in combinations(self.buttons, n):
                state = 0
                for push in pushed:
                    state ^= push
                if state == self.target:
                    return n
        raise Exception("could not turn on")

    def np_find_joltage(self):
        A = self.np_matrix
        b = np.array(self.joltage, dtype=int).flatten()
        integrality = np.ones(A.shape[1])
        constraints = LinearConstraint(A, b, b)
        c = np.ones(A.shape[1])
        res = milp(c=c, constraints=constraints, integrality=integrality)
        return res.fun

    def find_joltage(self):
        M = self.matrix
        b = sp.Matrix(self.joltage)
        vars = sp.symbols(f"x0:{M.cols}")
        solutions = sp.linsolve((M, b), vars)
        solution = list(solutions)[0]
        # ----------------
        # SAMPLE[0]
        # (-x3 + x5 + 2, 5 - x5, -x3 + x5 + 1, x3, 3 - x5, x5)
        # -x3 + x5 + 2 -> 1
        #     - x5 + 5 -> 2
        # -x3 + x5 + 1 -> 0
        #  x3          -> 4
        #     - x5 + 3 -> 0
        #       x5     -> 3
        # ----------------
        #  x5 = 0, 1, 2, 3
        #  x3 = 1, 2, 3, 4
        # ----------------
        # SAMPLE[1]
        # (2 - x2, x2 + 5, x2, 5, 0)
        # -x2 + 2 -> 2
        #  x2 + 5 -> 5
        #  x2     -> 0
        #       5 -> 5
        #       0 -> 0
        # ----------------
        # SAMPLE[2]
        # (6 - x3, x3 - 1, 5, x3)
        # -x3 + 6 -> 5
        #  x3 - 1 -> 0
        #       5 -> 5
        #  x3     -> 1
        # ----------------
        # Non integer example
        # -x11/3 + 7*x12/3 + x7 - 634/3
        # 4*x11/3 - 10*x12/3 - x7 + 670/3
        # -x11 + x12 + 8
        # -2*x11/3 - x12/3 - x7 + 634/3
        # x11/3 - x12/3 + 37/3
        # x12 - 12
        # -2*x11/3 - 4*x12/3 + 112/3, x7
        # x11/3 - 4*x12/3 + 91/3
        # x11/3 + 2*x12/3 - 5/3
        # 2
        # x11
        # x12

        val_to_minimize = sum(solution)
        constraints = [eq >= 0 for eq in solution]

        ans = sp.solvers.simplex.lpmin(val_to_minimize, constraints)
        if int_valued(ans[0]) and all(int_valued(val) for val in ans[1].values()):
            return ans

        # try again with scipy solver
        all_symbols = set().union(*(eq.free_symbols for eq in solution))
        vars_list = sorted(list(all_symbols), key=lambda s: s.name)
        integrality = np.ones(len(vars_list))

        A_sym, b_sym = sp.linear_eq_to_matrix(solution, vars_list)
        A = np.array(A_sym.tolist(), dtype=float)
        b_l = np.array(b_sym.tolist(), dtype=float).flatten()
        b_u = np.full_like(b_l, np.inf)
        constraints = LinearConstraint(A, b_l, b_u)

        c_sym, c_sym_ofset = sp.linear_eq_to_matrix(val_to_minimize, vars_list)
        c = np.array(c_sym.tolist(), dtype=float).flatten()
        c_ofset = c_sym_ofset[0, 0]
        res = milp(c=c, constraints=constraints, integrality=integrality)
        if not int_valued(c_ofset):
            return -1, c_ofset
        c_int = np.round(res.fun).astype(int) + c_ofset
        return c_int, "via_milp"


class Factory:

    def __init__(self, raw_machines: List[str]):
        self.machines = [Machine(raw_machine) for raw_machine in raw_machines]

    def total_min(self):
        return sum(machine.min_on() for machine in self.machines)

    def np_total_joltage(self):
        return sum(machine.np_find_joltage() for machine in self.machines)

    def total_joltage(self):
        total = 0
        non_int_machines = []
        for machine in self.machines:
            ans = machine.find_joltage()
            if ans[0] == -1:
                non_int_machines.append((machine, ans))
            else:
                total += ans[0]
        return total


def test_machine():
    sample_machine = Machine(SAMPLE[0])
    assert sample_machine.min_on() == 2
    assert sample_machine.find_joltage()[0] == 10
    sample_machine = Machine(SAMPLE[1])
    assert sample_machine.min_on() == 3
    assert sample_machine.find_joltage()[0] == 12
    sample_machine = Machine(SAMPLE[2])
    assert sample_machine.min_on() == 2
    assert sample_machine.find_joltage()[0] == 11


def test_factory():
    sample_factory = Factory(SAMPLE)
    assert sample_factory.total_min() == 7
    assert sample_factory.total_joltage() == 33
    assert sample_factory.np_total_joltage() == 33

    my_factory = Factory(RAW_INPUT)
    assert my_factory.total_min() == 396
    assert my_factory.np_total_joltage() == 15688.0
