from heapq import heappush, heappop
from typing import NamedTuple

# from tqdm import tqdm


class Puzzle:
    """
    --- Day 19: Not Enough Minerals ---

    Your scans show that the lava did indeed form obsidian!

    The wind has changed direction enough to stop sending lava droplets toward
    you, so you and the elephants exit the cave. As you do, you notice a
    collection of geodes around the pond. Perhaps you could use the obsidian to
    create some geode-cracking robots and break them open?

    To collect the obsidian from the bottom of the pond, you'll need waterproof
    obsidian-collecting robots. Fortunately, there is an abundant amount of clay
    nearby that you can use to make them waterproof.

    In order to harvest the clay, you'll need special-purpose clay-collecting
    robots. To make any type of robot, you'll need ore, which is also plentiful
    but in the opposite direction from the clay.

    Collecting ore requires ore-collecting robots with big drills. Fortunately,
    you have exactly one ore-collecting robot in your pack that you can use to
    kickstart the whole operation.

    Each robot can collect 1 of its resource type per minute. It also takes one
    minute for the robot factory (also conveniently from your pack) to construct
    any type of robot, although it consumes the necessary resources available
    when construction begins.

    The robot factory has many blueprints (your puzzle input) you can choose
    from, but once you've configured it with a blueprint, you can't change it.
    You'll need to work out which blueprint is best.

    For example:

    Blueprint 1:
    Each ore robot costs 4 ore.
    Each clay robot costs 2 ore.
    Each obsidian robot costs 3 ore and 14 clay.
    Each geode robot costs 2 ore and 7 obsidian.

    Blueprint 2:
    Each ore robot costs 2 ore.
    Each clay robot costs 3 ore.
    Each obsidian robot costs 3 ore and 8 clay.
    Each geode robot costs 3 ore and 12 obsidian.

    (Blueprints have been line-wrapped here for legibility. The robot factory's
    actual assortment of blueprints are provided one blueprint per line.)

    The elephants are starting to look hungry, so you shouldn't take too long;
    you need to figure out which blueprint would maximize the number of opened
    geodes after 24 minutes by figuring out which robots to build and when to
    build them.

    Using blueprint 1 in the example above, the largest number of geodes you
    could open in 24 minutes is 9. One way to achieve that is:

    == Minute 1 ==
    1 ore-collecting robot collects 1 ore; you now have 1 ore.

    == Minute 2 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.

    == Minute 3 ==
    Spend 2 ore to start building a clay-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    The new clay-collecting robot is ready; you now have 1 of them.

    == Minute 4 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    1 clay-collecting robot collects 1 clay; you now have 1 clay.

    == Minute 5 ==
    Spend 2 ore to start building a clay-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    1 clay-collecting robot collects 1 clay; you now have 2 clay.
    The new clay-collecting robot is ready; you now have 2 of them.

    == Minute 6 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    2 clay-collecting robots collect 2 clay; you now have 4 clay.

    == Minute 7 ==
    Spend 2 ore to start building a clay-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    2 clay-collecting robots collect 2 clay; you now have 6 clay.
    The new clay-collecting robot is ready; you now have 3 of them.

    == Minute 8 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    3 clay-collecting robots collect 3 clay; you now have 9 clay.

    == Minute 9 ==
    1 ore-collecting robot collects 1 ore; you now have 3 ore.
    3 clay-collecting robots collect 3 clay; you now have 12 clay.

    == Minute 10 ==
    1 ore-collecting robot collects 1 ore; you now have 4 ore.
    3 clay-collecting robots collect 3 clay; you now have 15 clay.

    == Minute 11 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    3 clay-collecting robots collect 3 clay; you now have 4 clay.
    The new obsidian-collecting robot is ready; you now have 1 of them.

    == Minute 12 ==
    Spend 2 ore to start building a clay-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    3 clay-collecting robots collect 3 clay; you now have 7 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.
    The new clay-collecting robot is ready; you now have 4 of them.

    == Minute 13 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    4 clay-collecting robots collect 4 clay; you now have 11 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.

    == Minute 14 ==
    1 ore-collecting robot collects 1 ore; you now have 3 ore.
    4 clay-collecting robots collect 4 clay; you now have 15 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 3 obsidian.

    == Minute 15 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    4 clay-collecting robots collect 4 clay; you now have 5 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 4 obsidian.
    The new obsidian-collecting robot is ready; you now have 2 of them.

    == Minute 16 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    4 clay-collecting robots collect 4 clay; you now have 9 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.

    == Minute 17 ==
    1 ore-collecting robot collects 1 ore; you now have 3 ore.
    4 clay-collecting robots collect 4 clay; you now have 13 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.

    == Minute 18 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    1 ore-collecting robot collects 1 ore; you now have 2 ore.
    4 clay-collecting robots collect 4 clay; you now have 17 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 3 obsidian.
    The new geode-cracking robot is ready; you now have 1 of them.

    == Minute 19 ==
    1 ore-collecting robot collects 1 ore; you now have 3 ore.
    4 clay-collecting robots collect 4 clay; you now have 21 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 5 obsidian.
    1 geode-cracking robot cracks 1 geode; you now have 1 open geode.

    == Minute 20 ==
    1 ore-collecting robot collects 1 ore; you now have 4 ore.
    4 clay-collecting robots collect 4 clay; you now have 25 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 7 obsidian.
    1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.

    == Minute 21 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    1 ore-collecting robot collects 1 ore; you now have 3 ore.
    4 clay-collecting robots collect 4 clay; you now have 29 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 2 obsidian.
    1 geode-cracking robot cracks 1 geode; you now have 3 open geodes.
    The new geode-cracking robot is ready; you now have 2 of them.

    == Minute 22 ==
    1 ore-collecting robot collects 1 ore; you now have 4 ore.
    4 clay-collecting robots collect 4 clay; you now have 33 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.
    2 geode-cracking robots crack 2 geodes; you now have 5 open geodes.

    == Minute 23 ==
    1 ore-collecting robot collects 1 ore; you now have 5 ore.
    4 clay-collecting robots collect 4 clay; you now have 37 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.
    2 geode-cracking robots crack 2 geodes; you now have 7 open geodes.

    == Minute 24 ==
    1 ore-collecting robot collects 1 ore; you now have 6 ore.
    4 clay-collecting robots collect 4 clay; you now have 41 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.
    2 geode-cracking robots crack 2 geodes; you now have 9 open geodes.

    However, by using blueprint 2 in the example above, you could do even
    better: the largest number of geodes you could open in 24 minutes is 12.

    Determine the quality level of each blueprint by multiplying that
    blueprint's ID number with the largest number of geodes that can be opened
    in 24 minutes using that blueprint. In this example, the first blueprint has
    ID 1 and can open 9 geodes, so its quality level is 9. The second blueprint
    has ID 2 and can open 12 geodes, so its quality level is 24. Finally, if you
    add up the quality levels of all of the blueprints in the list, you get 33.

    Determine the quality level of each blueprint using the largest number of
    geodes it could produce in 24 minutes. What do you get if you add up the
    quality level of all of the blueprints in your list?

    Your puzzle answer was 1389.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    While you were choosing the best blueprint, the elephants found some food on
    their own, so you're not in as much of a hurry; you figure you probably have
    32 minutes before the wind changes direction again and you'll need to get
    out of range of the erupting volcano.

    Unfortunately, one of the elephants ate most of your blueprint list! Now,
    only the first three blueprints in your list are intact.

    In 32 minutes, the largest number of geodes blueprint 1 (from the example
    above) can open is 56. One way to achieve that is:

    == Minute 1 ==
    1 ore-collecting robot collects 1 ore; you now have 1 ore.

    == Minute 2 ==
    1 ore-collecting robot collects 1 ore; you now have 2 ore.

    == Minute 3 ==
    1 ore-collecting robot collects 1 ore; you now have 3 ore.

    == Minute 4 ==
    1 ore-collecting robot collects 1 ore; you now have 4 ore.

    == Minute 5 ==
    Spend 4 ore to start building an ore-collecting robot.
    1 ore-collecting robot collects 1 ore; you now have 1 ore.
    The new ore-collecting robot is ready; you now have 2 of them.

    == Minute 6 ==
    2 ore-collecting robots collect 2 ore; you now have 3 ore.

    == Minute 7 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    The new clay-collecting robot is ready; you now have 1 of them.

    == Minute 8 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    1 clay-collecting robot collects 1 clay; you now have 1 clay.
    The new clay-collecting robot is ready; you now have 2 of them.

    == Minute 9 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    2 clay-collecting robots collect 2 clay; you now have 3 clay.
    The new clay-collecting robot is ready; you now have 3 of them.

    == Minute 10 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    3 clay-collecting robots collect 3 clay; you now have 6 clay.
    The new clay-collecting robot is ready; you now have 4 of them.

    == Minute 11 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    4 clay-collecting robots collect 4 clay; you now have 10 clay.
    The new clay-collecting robot is ready; you now have 5 of them.

    == Minute 12 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    5 clay-collecting robots collect 5 clay; you now have 15 clay.
    The new clay-collecting robot is ready; you now have 6 of them.

    == Minute 13 ==
    Spend 2 ore to start building a clay-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    6 clay-collecting robots collect 6 clay; you now have 21 clay.
    The new clay-collecting robot is ready; you now have 7 of them.

    == Minute 14 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 14 clay.
    The new obsidian-collecting robot is ready; you now have 1 of them.

    == Minute 15 ==
    2 ore-collecting robots collect 2 ore; you now have 4 ore.
    7 clay-collecting robots collect 7 clay; you now have 21 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.

    == Minute 16 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    7 clay-collecting robots collect 7 clay; you now have 14 clay.
    1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.
    The new obsidian-collecting robot is ready; you now have 2 of them.

    == Minute 17 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 7 clay.
    2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.
    The new obsidian-collecting robot is ready; you now have 3 of them.

    == Minute 18 ==
    2 ore-collecting robots collect 2 ore; you now have 4 ore.
    7 clay-collecting robots collect 7 clay; you now have 14 clay.
    3 obsidian-collecting robots collect 3 obsidian; you now have 7 obsidian.

    == Minute 19 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    7 clay-collecting robots collect 7 clay; you now have 7 clay.
    3 obsidian-collecting robots collect 3 obsidian; you now have 10 obsidian.
    The new obsidian-collecting robot is ready; you now have 4 of them.

    == Minute 20 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 3 ore.
    7 clay-collecting robots collect 7 clay; you now have 14 clay.
    4 obsidian-collecting robots collect 4 obsidian; you now have 7 obsidian.
    The new geode-cracking robot is ready; you now have 1 of them.

    == Minute 21 ==
    Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 7 clay.
    4 obsidian-collecting robots collect 4 obsidian; you now have 11 obsidian.
    1 geode-cracking robot cracks 1 geode; you now have 1 open geode.
    The new obsidian-collecting robot is ready; you now have 5 of them.

    == Minute 22 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 14 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 9 obsidian.
    1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.
    The new geode-cracking robot is ready; you now have 2 of them.

    == Minute 23 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 21 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 7 obsidian.
    2 geode-cracking robots crack 2 geodes; you now have 4 open geodes.
    The new geode-cracking robot is ready; you now have 3 of them.

    == Minute 24 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 2 ore.
    7 clay-collecting robots collect 7 clay; you now have 28 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 5 obsidian.
    3 geode-cracking robots crack 3 geodes; you now have 7 open geodes.
    The new geode-cracking robot is ready; you now have 4 of them.

    == Minute 25 ==
    2 ore-collecting robots collect 2 ore; you now have 4 ore.
    7 clay-collecting robots collect 7 clay; you now have 35 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 10 obsidian.
    4 geode-cracking robots crack 4 geodes; you now have 11 open geodes.

    == Minute 26 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 4 ore.
    7 clay-collecting robots collect 7 clay; you now have 42 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 8 obsidian.
    4 geode-cracking robots crack 4 geodes; you now have 15 open geodes.
    The new geode-cracking robot is ready; you now have 5 of them.

    == Minute 27 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 4 ore.
    7 clay-collecting robots collect 7 clay; you now have 49 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 6 obsidian.
    5 geode-cracking robots crack 5 geodes; you now have 20 open geodes.
    The new geode-cracking robot is ready; you now have 6 of them.

    == Minute 28 ==
    2 ore-collecting robots collect 2 ore; you now have 6 ore.
    7 clay-collecting robots collect 7 clay; you now have 56 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 11 obsidian.
    6 geode-cracking robots crack 6 geodes; you now have 26 open geodes.

    == Minute 29 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 6 ore.
    7 clay-collecting robots collect 7 clay; you now have 63 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 9 obsidian.
    6 geode-cracking robots crack 6 geodes; you now have 32 open geodes.
    The new geode-cracking robot is ready; you now have 7 of them.

    == Minute 30 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 6 ore.
    7 clay-collecting robots collect 7 clay; you now have 70 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 7 obsidian.
    7 geode-cracking robots crack 7 geodes; you now have 39 open geodes.
    The new geode-cracking robot is ready; you now have 8 of them.

    == Minute 31 ==
    Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
    2 ore-collecting robots collect 2 ore; you now have 6 ore.
    7 clay-collecting robots collect 7 clay; you now have 77 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 5 obsidian.
    8 geode-cracking robots crack 8 geodes; you now have 47 open geodes.
    The new geode-cracking robot is ready; you now have 9 of them.

    == Minute 32 ==
    2 ore-collecting robots collect 2 ore; you now have 8 ore.
    7 clay-collecting robots collect 7 clay; you now have 84 clay.
    5 obsidian-collecting robots collect 5 obsidian; you now have 10 obsidian.
    9 geode-cracking robots crack 9 geodes; you now have 56 open geodes.

    However, blueprint 2 from the example above is still better; using it, the
    largest number of geodes you could open in 32 minutes is 62.

    You no longer have enough blueprints to worry about quality levels. Instead,
    for each of the first three blueprints, determine the largest number of
    geodes you could open; then, multiply these three values together.

    Don't worry about quality levels; instead, just determine the largest number
    of geodes you could open using each of the first three blueprints. What do
    you get if you multiply these numbers together?
    """


SAMPLE = [
    "Blueprint 1: "
    + "Each ore robot costs 4 ore. "
    + "Each clay robot costs 2 ore. "
    + "Each obsidian robot costs 3 ore and 14 clay. "
    + "Each geode robot costs 2 ore and 7 obsidian.",
    "Blueprint 2: "
    + "Each ore robot costs 2 ore. "
    + "Each clay robot costs 3 ore. "
    + "Each obsidian robot costs 3 ore and 8 clay. "
    + "Each geode robot costs 3 ore and 12 obsidian.",
]


with open("day_19_input.txt") as fp:
    MY_INPUT = [line.strip() for line in fp]


class Resource(NamedTuple):
    geode: int
    obsidian: int
    clay: int
    ore: int

    def __add__(self, other):
        return Resource(
            self.geode + other.geode,
            self.obsidian + other.obsidian,
            self.clay + other.clay,
            self.ore + other.ore,
        )

    def __sub__(self, other):
        return Resource(
            self.geode - other.geode,
            self.obsidian - other.obsidian,
            self.clay - other.clay,
            self.ore - other.ore,
        )


class State(NamedTuple):
    time: int
    rate: Resource
    inventory: Resource

    def geode_max_extra(self, max_time=24):
        time = self.time
        geodes = self.inventory.geode
        robots = self.rate.geode
        while time < max_time:
            time += 1
            geodes += robots
            robots += 1
        return geodes

    def priority(self, max_time=24):
        return tuple(
            [
                -self.geode_max_extra(max_time=max_time),
                -self.rate.geode,
                -self.inventory.geode,
                -self.rate.obsidian,
                -self.inventory.obsidian,
                -self.inventory.clay,
            ]
        )


class RobotFactory:
    def __init__(self, blueprints) -> None:
        self.blueprints = {}
        for blueprint in blueprints:
            blueprint_name, blueprint_data = blueprint.split(": ")
            blueprint_id = int(blueprint_name.replace("Blueprint ", ""))
            self.blueprints[blueprint_id] = {
                "geode": None,
                "obsidian": None,
                "clay": None,
                "ore": None,
            }
            blueprint_data = blueprint_data[:-1]
            for robot_cost in blueprint_data.split(". "):
                robot_type, raw_costs = robot_cost.replace("Each ", "").split(
                    " robot costs "
                )
                blueprint_robot_type = {
                    "geode": 0,
                    "obsidian": 0,
                    "clay": 0,
                    "ore": 0,
                }
                for cost in raw_costs.split(" and "):
                    amount, material_type = cost.split(" ")
                    blueprint_robot_type[material_type] = int(amount)
                self.blueprints[blueprint_id][robot_type] = Resource(
                    **blueprint_robot_type
                )

    def max_geodes(self, blueprint_id, max_time=24):
        add_robot = {
            "geode": Resource(geode=1, obsidian=0, clay=0, ore=0),
            "obsidian": Resource(geode=0, obsidian=1, clay=0, ore=0),
            "clay": Resource(geode=0, obsidian=0, clay=1, ore=0),
            "ore": Resource(geode=0, obsidian=0, clay=0, ore=1),
        }

        blueprint = self.blueprints[blueprint_id]
        max_geode_count = 0
        history = set()
        starting_state = State(
            time=0,
            rate=Resource(geode=0, obsidian=0, clay=0, ore=1),
            inventory=Resource(geode=0, obsidian=0, clay=0, ore=0),
        )

        exploring = []
        heappush(
            exploring, (starting_state.priority(max_time=max_time), starting_state)
        )
        while exploring:
            priority, state = heappop(exploring)

            if state in history:
                continue
            history.add(state)

            if state.inventory.geode > max_geode_count:
                print(f"new max {max_geode_count}>{state.inventory.geode} from {state}")
                max_geode_count = state.inventory.geode
            if state.time == max_time:
                continue

            if -priority[0] <= max_geode_count:
                continue

            # no factory use
            grown_inventory = state.inventory + state.rate
            next_state = State(
                time=state.time + 1, inventory=grown_inventory, rate=state.rate
            )
            heappush(exploring, (next_state.priority(max_time=max_time), next_state))

            # use factory
            for next_robot, costs in blueprint.items():
                if min(state.inventory - costs) >= 0:
                    next_inventory = grown_inventory - costs
                    next_rate = state.rate + add_robot[next_robot]
                    next_state = State(
                        time=state.time + 1, inventory=next_inventory, rate=next_rate
                    )
                    heappush(
                        exploring, (next_state.priority(max_time=max_time), next_state)
                    )
        return max_geode_count

    def find_quality_level(self):
        max_geodes = {}
        # for id in tqdm(self.blueprints):
        for id in self.blueprints:
            max_geodes[id] = self.max_geodes(id)
        return sum(k * v for k, v in max_geodes.items())

    def find_first_three_product(self):
        answer = 1
        for id in range(1, 4):
            answer *= self.max_geodes(id, max_time=32)
        return answer


def test_sample_factory():
    sample = RobotFactory(SAMPLE)
    assert sample.blueprints[1] == {
        "geode": Resource(geode=0, obsidian=7, clay=0, ore=2),
        "obsidian": Resource(geode=0, obsidian=0, clay=14, ore=3),
        "clay": Resource(geode=0, obsidian=0, clay=0, ore=2),
        "ore": Resource(geode=0, obsidian=0, clay=0, ore=4),
    }
    assert sample.max_geodes(1) == 9  # not 37
    assert sample.find_quality_level() == 33


def test_my_factory():
    my_factory = RobotFactory(MY_INPUT)
    assert my_factory.find_quality_level() == 1389
    assert my_factory.find_first_three_product() == 3003
