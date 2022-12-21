# from queue import PriorityQueue
# apparently heapq is faster but not thread safe but since I'm not doing any threading
from heapq import heappush, heappop


class Puzzle:
    """
    --- Day 16: Proboscidea Volcanium ---
    The sensors have led you to the origin of the distress signal: yet another
    handheld device, just like the one the Elves gave you. However, you don't
    see any Elves around; instead, the device is surrounded by elephants! They
    must have gotten lost in these tunnels, and one of the elephants apparently
    figured out how to turn on the distress signal.

    The ground rumbles again, much stronger this time. What kind of cave is
    this, exactly? You scan the cave with your handheld device; it reports
    mostly igneous rock, some ash, pockets of pressurized gas, magma... this
    isn't just a cave, it's a volcano!

    You need to get the elephants out of here, quickly. Your device estimates
    that you have 30 minutes before the volcano erupts, so you don't have time
    to go back out the way you came in.

    You scan the cave for other options and discover a network of pipes and
    pressure-release valves. You aren't sure how such a system got into a
    volcano, but you don't have time to complain; your device produces a report
    (your puzzle input) of each valve's flow rate if it were opened (in pressure
    per minute) and the tunnels you could use to move between the valves.

    There's even a valve in the room you and the elephants are currently
    standing in labeled AA. You estimate it will take you one minute to open a
    single valve and one minute to follow any tunnel from one valve to another.
    What is the most pressure you could release?

    For example, suppose you had the following scan output:

    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
    Valve CC has flow rate=2; tunnels lead to valves DD, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve FF has flow rate=0; tunnels lead to valves EE, GG
    Valve GG has flow rate=0; tunnels lead to valves FF, HH
    Valve HH has flow rate=22; tunnel leads to valve GG
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve JJ has flow rate=21; tunnel leads to valve II

    All of the valves begin closed. You start at valve AA, but it must be
    damaged or jammed or something: its flow rate is 0, so there's no point in
    opening it. However, you could spend one minute moving to valve BB and
    another minute opening it; doing so would release pressure during the
    remaining 28 minutes at a flow rate of 13, a total eventual pressure release
    of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC
    and your fourth minute opening it, providing an additional 26 minutes of
    eventual pressure release at a flow rate of 2, or 52 total pressure released
    by valve CC.

    Making your way through the tunnels like this, you could probably open many
    or all of the valves by the time 30 minutes have elapsed. However, you need
    to release as much pressure as possible, so you'll need to be methodical.
    Instead, consider this approach:

    == Minute 1 ==
    No valves are open.
    You move to valve DD.

    == Minute 2 ==
    No valves are open.
    You open valve DD.

    == Minute 3 ==
    Valve DD is open, releasing 20 pressure.
    You move to valve CC.

    == Minute 4 ==
    Valve DD is open, releasing 20 pressure.
    You move to valve BB.

    == Minute 5 ==
    Valve DD is open, releasing 20 pressure.
    You open valve BB.

    == Minute 6 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve AA.

    == Minute 7 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve II.

    == Minute 8 ==
    Valves BB and DD are open, releasing 33 pressure.
    You move to valve JJ.

    == Minute 9 ==
    Valves BB and DD are open, releasing 33 pressure.
    You open valve JJ.

    == Minute 10 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve II.

    == Minute 11 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve AA.

    == Minute 12 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve DD.

    == Minute 13 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve EE.

    == Minute 14 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve FF.

    == Minute 15 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve GG.

    == Minute 16 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You move to valve HH.

    == Minute 17 ==
    Valves BB, DD, and JJ are open, releasing 54 pressure.
    You open valve HH.

    == Minute 18 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve GG.

    == Minute 19 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve FF.

    == Minute 20 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve EE.

    == Minute 21 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You open valve EE.

    == Minute 22 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You move to valve DD.

    == Minute 23 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You move to valve CC.

    == Minute 24 ==
    Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
    You open valve CC.

    == Minute 25 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    == Minute 26 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    == Minute 27 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    == Minute 28 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    == Minute 29 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    == Minute 30 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    This approach lets you release the most pressure possible in 30 minutes with
    this valve layout, 1651.

    Work out the steps to release the most pressure in 30 minutes. What is the
    most pressure you can release?

    --- Part Two ---
    You're worried that even with an optimal approach, the pressure released
    won't be enough. What if you got one of the elephants to help you?

    It would take you 4 minutes to teach an elephant how to open the right
    valves in the right order, leaving you with only 26 minutes to actually
    execute your plan. Would having two of you working together be better, even
    if it means having less time? (Assume that you teach the elephant before
    opening any valves yourself, giving you both the same full 26 minutes.)

    In the example above, you could teach the elephant to help you as follows:

    == Minute 1 ==
    No valves are open.
    You move to valve II.
    The elephant moves to valve DD.

    == Minute 2 ==
    No valves are open.
    You move to valve JJ.
    The elephant opens valve DD.

    == Minute 3 ==
    Valve DD is open, releasing 20 pressure.
    You open valve JJ.
    The elephant moves to valve EE.

    == Minute 4 ==
    Valves DD and JJ are open, releasing 41 pressure.
    You move to valve II.
    The elephant moves to valve FF.

    == Minute 5 ==
    Valves DD and JJ are open, releasing 41 pressure.
    You move to valve AA.
    The elephant moves to valve GG.

    == Minute 6 ==
    Valves DD and JJ are open, releasing 41 pressure.
    You move to valve BB.
    The elephant moves to valve HH.

    == Minute 7 ==
    Valves DD and JJ are open, releasing 41 pressure.
    You open valve BB.
    The elephant opens valve HH.

    == Minute 8 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You move to valve CC.
    The elephant moves to valve GG.

    == Minute 9 ==
    Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
    You open valve CC.
    The elephant moves to valve FF.

    == Minute 10 ==
    Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
    The elephant moves to valve EE.

    == Minute 11 ==
    Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
    The elephant opens valve EE.

    (At this point, all valves are open.)

    == Minute 12 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    ...

    == Minute 20 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    ...

    == Minute 26 ==
    Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

    With the elephant helping, after 26 minutes, the best you could do would
    release a total of 1707 pressure.

    With you and an elephant working together for 26 minutes, what is the most
    pressure you could release?
    """


SAMPLE = [
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
    "Valve HH has flow rate=22; tunnel leads to valve GG",
    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
    "Valve JJ has flow rate=21; tunnel leads to valve II",
]


with open("day_16_input.txt") as fp:
    MY_INPUT = [line.strip() for line in fp]


class PressureMaze:
    def __init__(self, layout) -> None:
        self.valve_rates = {}
        self.tunnels = {}
        for valve_info in layout:
            rate_info, tunnel_info = valve_info.split(";")
            valve_name, rate = (
                rate_info.replace("Valve ", "").replace(" has flow rate", "").split("=")
            )
            self.valve_rates[valve_name] = int(rate)
            self.tunnels[valve_name] = (
                tunnel_info.replace(" tunnels lead to ", "")
                .replace(" tunnel leads to ", "")
                .replace("valves ", "")
                .replace("valve ", "")
                .split(", ")
            )

    def a_better_time_exist(
        self, best_progress, pt, closed_valves, time_elasped, pressure
    ):
        if (time_elasped, pt, closed_valves) not in best_progress:
            best_progress[(time_elasped, pt, closed_valves)] = pressure
            return False
        if pressure < best_progress[(time_elasped, pt, closed_valves)]:
            best_progress[(time_elasped, pt, closed_valves)] = pressure
            return False
        return True

    def a_better_pair_time_exist(
        self, best_progress, pt, closed_valves, time_elasped, pressure
    ):
        found_better = True
        thing1, thing2 = pt
        if (time_elasped, (thing1, thing2), closed_valves) not in best_progress:
            best_progress[(time_elasped, (thing1, thing2), closed_valves)] = pressure
            found_better = False
        if (time_elasped, (thing2, thing1), closed_valves) not in best_progress:
            best_progress[(time_elasped, (thing2, thing1), closed_valves)] = pressure
            found_better = False
        if pressure < best_progress[(time_elasped, (thing1, thing2), closed_valves)]:
            best_progress[(time_elasped, (thing1, thing2), closed_valves)] = pressure
            found_better = False
        if pressure < best_progress[(time_elasped, (thing2, thing1), closed_valves)]:
            best_progress[(time_elasped, (thing2, thing1), closed_valves)] = pressure
            found_better = False
        return found_better

    def a_better_time_exist2(
        self, best_progress, pt, closed_valves, time_elasped, pressure
    ):
        # I was attempting to further speed things up
        # but this function seems to fail I'm not sure why
        if (pt, closed_valves) not in best_progress:
            best_progress[(pt, closed_valves)] = (time_elasped, pressure)
            return False
        prev_time, prev_pressure = best_progress[(pt, closed_valves)]
        if pressure <= prev_pressure and time_elasped <= prev_time:
            best_progress[(pt, closed_valves)] = (time_elasped, pressure)
            return False
        if pressure >= prev_pressure and time_elasped >= prev_time:
            return True
        return False

    def get_boundry(self, rate, closed_valves, current_pt):
        boundry = []
        if current_pt in closed_valves:
            # open the valve
            new_rate = rate - self.valve_rates[current_pt]
            new_closed = closed_valves - {current_pt}
            boundry.append((new_rate, new_closed, current_pt))
        for next_pt in self.tunnels[current_pt]:
            # move to other valves
            boundry.append((rate, closed_valves, next_pt))
        return boundry

    def max_release(self, total_time=30, start="AA"):
        max_release = set()
        best_progress = {}
        # exploring = PriorityQueue()
        exploring = []

        rate = 0
        pressure = 0
        time_elapsed = 0
        closed_valves = set(v for v, r in self.valve_rates.items() if r > 0)
        current_pt = start

        edge = (rate, pressure, time_elapsed, closed_valves, current_pt)
        heappush(exploring, edge)
        # exploring.put(edge)
        while exploring:
            # rate, pressure, time_elapsed, closed_valves, current_pt = exploring.get()
            rate, pressure, time_elapsed, closed_valves, current_pt = heappop(exploring)
            if self.a_better_time_exist(
                best_progress,
                current_pt,
                frozenset(closed_valves),
                time_elapsed,
                pressure,
            ):
                continue

            # out of time
            if time_elapsed == total_time:
                max_release.add(pressure)
                continue

            # nothing more to do
            if len(closed_valves) == 0:
                max_release.add(pressure + rate * (total_time - time_elapsed))
                continue

            for next_rate, next_valves, next_pt in self.get_boundry(
                rate, closed_valves, current_pt
            ):
                heappush(
                    exploring,
                    (
                        next_rate,
                        pressure + rate,
                        time_elapsed + 1,
                        next_valves,
                        next_pt,
                    ),
                )

        return -min(max_release)

    def pair_programming(self, total_time=26, start="AA", pressure_to_beat=None):
        max_release = set()

        if pressure_to_beat is not None:
            max_release.add(pressure_to_beat)

        best_progress = {}
        # exploring = PriorityQueue()
        exploring = []

        pressure = 0
        rate = 0
        time_elapsed = 0
        closed_valves = set(v for v, r in self.valve_rates.items() if r > 0)
        current_pt = (start, start)

        max_rate = sum(self.valve_rates.values())

        # exploring.put(
        heappush(
            exploring,
            (
                rate,
                pressure,
                time_elapsed,
                closed_valves,
                current_pt,
            ),
        )
        while exploring:
            # rate, pressure, time_elapsed, closed_valves, current_pt = exploring.get()
            rate, pressure, time_elapsed, closed_valves, current_pt = heappop(exploring)

            thing1, thing2 = current_pt
            frozen_valves = frozenset(closed_valves)

            # Can't beat existing times
            if max_release and min(max_release) <= pressure - max_rate * (
                total_time - time_elapsed
            ):
                continue

            # Don't think this is super efficient - pretty slow even on sample
            if self.a_better_pair_time_exist(
                best_progress,
                current_pt,
                frozen_valves,
                time_elapsed,
                pressure,
            ):
                continue

            # out of time
            if time_elapsed == total_time:
                max_release.add(pressure)
                print(
                    f"Path out of time, len={len(max_release)} min={min(max_release)}"
                )
                continue

            # nothing more to do
            if len(closed_valves) == 0:
                max_release.add(pressure + rate * (total_time - time_elapsed))
                print(f"All open, len={len(max_release)} min={min(max_release)}")
                continue

            for next_rate1, next_valves1, next_pt1 in self.get_boundry(
                rate, closed_valves, thing1
            ):
                for next_rate2, next_valves2, next_pt2 in self.get_boundry(
                    next_rate1, next_valves1, thing2
                ):
                    heappush(
                        exploring,
                        (
                            next_rate2,
                            pressure + rate,
                            time_elapsed + 1,
                            next_valves2,
                            (next_pt1, next_pt2),
                        ),
                    )

        return -min(max_release)


def test_maze():
    sample = PressureMaze(SAMPLE)
    assert sample.valve_rates == {
        "AA": 0,
        "BB": 13,
        "CC": 2,
        "DD": 20,
        "EE": 3,
        "FF": 0,
        "GG": 0,
        "HH": 22,
        "II": 0,
        "JJ": 21,
    }
    assert sample.tunnels == {
        "AA": ["DD", "II", "BB"],
        "BB": ["CC", "AA"],
        "CC": ["DD", "BB"],
        "DD": ["CC", "AA", "EE"],
        "EE": ["FF", "DD"],
        "FF": ["EE", "GG"],
        "GG": ["FF", "HH"],
        "HH": ["GG"],
        "II": ["AA", "JJ"],
        "JJ": ["II"],
    }
    assert sample.max_release() == 1651
    assert sample.pair_programming() == 1707


def test_my_input():
    my_input = PressureMaze(MY_INPUT)
    assert my_input.max_release() == 2330
    # assert my_input.pair_programming() == 2675
    pass


if __name__ == "__main__":
    my_input = PressureMaze(MY_INPUT)
    # minimum values from previous work:
    # 1559 too low
    # 2531 too low
    # 2549
    # 2651
    # 2665
    # finally got answer 2675
    print(f"answer = {my_input.pair_programming(pressure_to_beat=-2330)}")  
