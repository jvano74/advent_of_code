from pathlib import Path
from typing import NamedTuple
from collections import defaultdict
import re


class Puzzle:
    """
    --- Day 24: Immune System Simulator 20XX ---
    After a weird buzzing noise, you appear back at the man's cottage. He seems relieved to see his friend, but quickly
    notices that the little reindeer caught some kind of cold while out exploring.

    The portly man explains that this reindeer's immune system isn't similar to regular reindeer immune systems:

    The immune system and the infection each have an army made up of several groups; each group consists of one or more
    identical units. The armies repeatedly fight until only one army has units remaining.

    Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack
    damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first
    and win ties), and sometimes weaknesses or immunities. Here is an example group:

    18 units each with 729 hit points (weak to fire; immune to cold, slashing)
     with an attack that does 8 radiation damage at initiative 10

    Each group also has an effective power: the number of units in that group multiplied by their attack damage. The
    above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group
    is removed from combat.

    Each fight consists of two phases: target selection and attacking.

    During the target selection phase, each group attempts to choose one target. In decreasing order of effective
    power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking
    group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for
    weaknesses and immunities, but not accounting for whether the defending group has enough units to actually
    receive all of that damage).

    If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to
    target the defending group with the largest effective power; if there is still a tie, it chooses the defending
    group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target.
    Defending groups can only be chosen as a target by one attacking group.

    At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is
    being attacked by zero or one groups.

    During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing
    order of initiative, regardless of whether they are part of the infection or the immune system.
    (If a group contains no units, it cannot attack.)

    The damage an attacking group deals to a defending group depends on the attacking group's attack type and the
    defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its
    effective power to the defending group. However, if the defending group is immune to the attacking group's
    attack type, the defending group instead takes no damage; if the defending group is weak to the attacking
    group's attack type, the defending group instead takes double damage.

    The defending group only loses whole units from damage; damage is always dealt in such a way that it kills
    the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored.
    For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it
    loses exactly 7 units and is left with 3 units at full health.

    After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army
    has lost all of its units.

    For example, consider the following armies:

    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with
     an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
     slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack
     that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire,
     cold) with an attack that does 12 slashing damage at initiative 4

    If these armies were to enter combat, the following fights, including details during the target selection and
    attacking phases, would take place:

    Immune System:
    Group 1 contains 17 units
    Group 2 contains 989 units
    Infection:
    Group 1 contains 801 units
    Group 2 contains 4485 units

    Infection group 1 would deal defending group 1 185832 damage
    Infection group 1 would deal defending group 2 185832 damage
    Infection group 2 would deal defending group 2 107640 damage
    Immune System group 1 would deal defending group 1 76619 damage
    Immune System group 1 would deal defending group 2 153238 damage
    Immune System group 2 would deal defending group 1 24725 damage

    Infection group 2 attacks defending group 2, killing 84 units
    Immune System group 2 attacks defending group 1, killing 4 units
    Immune System group 1 attacks defending group 2, killing 51 units
    Infection group 1 attacks defending group 1, killing 17 units
    Immune System:
    Group 2 contains 905 units
    Infection:
    Group 1 contains 797 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 184904 damage
    Immune System group 2 would deal defending group 1 22625 damage
    Immune System group 2 would deal defending group 2 22625 damage

    Immune System group 2 attacks defending group 1, killing 4 units
    Infection group 1 attacks defending group 2, killing 144 units
    Immune System:
    Group 2 contains 761 units
    Infection:
    Group 1 contains 793 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 183976 damage
    Immune System group 2 would deal defending group 1 19025 damage
    Immune System group 2 would deal defending group 2 19025 damage

    Immune System group 2 attacks defending group 1, killing 4 units
    Infection group 1 attacks defending group 2, killing 143 units
    Immune System:
    Group 2 contains 618 units
    Infection:
    Group 1 contains 789 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 183048 damage
    Immune System group 2 would deal defending group 1 15450 damage
    Immune System group 2 would deal defending group 2 15450 damage

    Immune System group 2 attacks defending group 1, killing 3 units
    Infection group 1 attacks defending group 2, killing 143 units
    Immune System:
    Group 2 contains 475 units
    Infection:
    Group 1 contains 786 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 182352 damage
    Immune System group 2 would deal defending group 1 11875 damage
    Immune System group 2 would deal defending group 2 11875 damage

    Immune System group 2 attacks defending group 1, killing 2 units
    Infection group 1 attacks defending group 2, killing 142 units
    Immune System:
    Group 2 contains 333 units
    Infection:
    Group 1 contains 784 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 181888 damage
    Immune System group 2 would deal defending group 1 8325 damage
    Immune System group 2 would deal defending group 2 8325 damage

    Immune System group 2 attacks defending group 1, killing 1 unit
    Infection group 1 attacks defending group 2, killing 142 units
    Immune System:
    Group 2 contains 191 units
    Infection:
    Group 1 contains 783 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 181656 damage
    Immune System group 2 would deal defending group 1 4775 damage
    Immune System group 2 would deal defending group 2 4775 damage

    Immune System group 2 attacks defending group 1, killing 1 unit
    Infection group 1 attacks defending group 2, killing 142 units
    Immune System:
    Group 2 contains 49 units
    Infection:
    Group 1 contains 782 units
    Group 2 contains 4434 units

    Infection group 1 would deal defending group 2 181424 damage
    Immune System group 2 would deal defending group 1 1225 damage
    Immune System group 2 would deal defending group 2 1225 damage

    Immune System group 2 attacks defending group 1, killing 0 units
    Infection group 1 attacks defending group 2, killing 49 units
    Immune System:
    No groups remain.
    Infection:
    Group 1 contains 782 units
    Group 2 contains 4434 units
    In the example above, the winning army ends up with 782 + 4434 = 5216 units.

    You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now,
    how many units would the winning army have?

    --- Part Two ---
    Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

    If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

    A boost is an integer increase in immune system units' attack damage. For example, if you were to boost the above
    example's immune system's units by 1570, the armies would instead look like this:

    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with
     an attack that does 6077 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
     slashing) with an attack that does 1595 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack
     that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire,
     cold) with an attack that does 12 slashing damage at initiative 4
    With this boost, the combat proceeds differently:

    Immune System:
    Group 2 contains 989 units
    Group 1 contains 17 units
    Infection:
    Group 1 contains 801 units
    Group 2 contains 4485 units

    Infection group 1 would deal defending group 2 185832 damage
    Infection group 1 would deal defending group 1 185832 damage
    Infection group 2 would deal defending group 1 53820 damage
    Immune System group 2 would deal defending group 1 1577455 damage
    Immune System group 2 would deal defending group 2 1577455 damage
    Immune System group 1 would deal defending group 2 206618 damage

    Infection group 2 attacks defending group 1, killing 9 units
    Immune System group 2 attacks defending group 1, killing 335 units
    Immune System group 1 attacks defending group 2, killing 32 units
    Infection group 1 attacks defending group 2, killing 84 units
    Immune System:
    Group 2 contains 905 units
    Group 1 contains 8 units
    Infection:
    Group 1 contains 466 units
    Group 2 contains 4453 units

    Infection group 1 would deal defending group 2 108112 damage
    Infection group 1 would deal defending group 1 108112 damage
    Infection group 2 would deal defending group 1 53436 damage
    Immune System group 2 would deal defending group 1 1443475 damage
    Immune System group 2 would deal defending group 2 1443475 damage
    Immune System group 1 would deal defending group 2 97232 damage

    Infection group 2 attacks defending group 1, killing 8 units
    Immune System group 2 attacks defending group 1, killing 306 units
    Infection group 1 attacks defending group 2, killing 29 units
    Immune System:
    Group 2 contains 876 units
    Infection:
    Group 2 contains 4453 units
    Group 1 contains 160 units

    Infection group 2 would deal defending group 2 106872 damage
    Immune System group 2 would deal defending group 2 1397220 damage
    Immune System group 2 would deal defending group 1 1397220 damage

    Infection group 2 attacks defending group 2, killing 83 units
    Immune System group 2 attacks defending group 2, killing 427 units
    After a few fights...

    Immune System:
    Group 2 contains 64 units
    Infection:
    Group 2 contains 214 units
    Group 1 contains 19 units

    Infection group 2 would deal defending group 2 5136 damage
    Immune System group 2 would deal defending group 2 102080 damage
    Immune System group 2 would deal defending group 1 102080 damage

    Infection group 2 attacks defending group 2, killing 4 units
    Immune System group 2 attacks defending group 2, killing 32 units
    Immune System:
    Group 2 contains 60 units
    Infection:
    Group 1 contains 19 units
    Group 2 contains 182 units

    Infection group 1 would deal defending group 2 4408 damage
    Immune System group 2 would deal defending group 1 95700 damage
    Immune System group 2 would deal defending group 2 95700 damage

    Immune System group 2 attacks defending group 1, killing 19 units
    Immune System:
    Group 2 contains 60 units
    Infection:
    Group 2 contains 182 units

    Infection group 2 would deal defending group 2 4368 damage
    Immune System group 2 would deal defending group 2 95700 damage

    Infection group 2 attacks defending group 2, killing 3 units
    Immune System group 2 attacks defending group 2, killing 30 units
    After a few more fights...

    Immune System:
    Group 2 contains 51 units
    Infection:
    Group 2 contains 40 units

    Infection group 2 would deal defending group 2 960 damage
    Immune System group 2 would deal defending group 2 81345 damage

    Infection group 2 attacks defending group 2, killing 0 units
    Immune System group 2 attacks defending group 2, killing 27 units
    Immune System:
    Group 2 contains 51 units
    Infection:
    Group 2 contains 13 units

    Infection group 2 would deal defending group 2 312 damage
    Immune System group 2 would deal defending group 2 81345 damage

    Infection group 2 attacks defending group 2, killing 0 units
    Immune System group 2 attacks defending group 2, killing 13 units
    Immune System:
    Group 2 contains 51 units
    Infection:
    No groups remain.

    This boost would allow the immune system's armies to win! It would be left with 51 units.

    You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need
    to be cautious and find the smallest boost that would allow the immune system to win.

    How many units does the immune system have left after getting the smallest boost it needs to win?
    """

    pass


with open(Path(__file__).parent / "2018_24_input.txt") as fp:
    RAW_IMMUNE_SYSTEM, RAW_INFECTION = fp.read().split("\n\n")
    IMMUNE_SYSTEM_INPUT = RAW_IMMUNE_SYSTEM.split("\n")[1:]
    INFECTION_INPUT = RAW_INFECTION.split("\n")[1:]


def test_input():
    assert len(IMMUNE_SYSTEM_INPUT) == 10
    assert IMMUNE_SYSTEM_INPUT[0].count("8808 units") == 1
    assert IMMUNE_SYSTEM_INPUT[-1].count("1284 units") == 1
    assert len(INFECTION_INPUT) == 10
    assert INFECTION_INPUT[0].count("23427 hit points") == 1
    assert INFECTION_INPUT[-1].count("30 fire damage") == 1


class Group(NamedTuple):
    type: str
    units: int
    unit_hp: int
    immunity: set
    weakness: set
    attack_damage: int
    attack_type: str
    initiative: int

    def effective_power(self):
        return self.units * self.attack_damage

    def damage_multiplier(self, other):
        if other.attack_type in self.immunity:
            return 0
        if other.attack_type in self.weakness:
            return 2
        return 1

    def attacked_by(self, attacker):
        """
        The damage an attacking group deals to a defending group depends on the attacking group's attack type and the
        defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its
        effective power to the defending group. However, if the defending group is immune to the attacking group's
        attack type, the defending group instead takes no damage; if the defending group is weak to the attacking
        group's attack type, the defending group instead takes double damage.

        The defending group only loses whole units from damage; damage is always dealt in such a way that it kills
        the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored.
        For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it
        loses exactly 7 units and is left with 3 units at full health.
        """
        damage = self.damage_multiplier(attacker) * attacker.effective_power()
        damaged_units = damage // self.unit_hp
        new_units = self.units - damaged_units
        return Group(
            type=self.type,
            units=new_units if new_units > 0 else 0,
            unit_hp=self.unit_hp,
            immunity=self.immunity,
            weakness=self.weakness,
            attack_damage=self.attack_damage,
            attack_type=self.attack_type,
            initiative=self.initiative,
        )

    @staticmethod
    def from_raw(line, group_type, boost=0):
        units = int(re.findall(r"^(\d+) units", line)[0])
        unit_hp = int(re.findall(r"each with (\d+) hit points", line)[0])
        immunity = set()
        weakness = set()
        specials = re.findall(r"\((.*)\)", line)
        if len(specials) > 0:
            for s in specials[0].split(";"):
                if s.count("weak to") > 0:
                    for e in s.split("weak to ")[1].split(", "):
                        weakness.add(e)
                if s.count("immune to") > 0:
                    for e in s.split("immune to ")[1].split(", "):
                        immunity.add(e)
        attack_damage = (
            int(re.findall(r"with an attack that does (\d+)", line)[0]) + boost
        )
        attack_type = re.findall(r"(\w+) damage", line)[0]
        initiative = int(re.findall(r"at initiative (\d+)$", line)[0])
        return Group(
            type=group_type,
            units=units,
            unit_hp=unit_hp,
            immunity=immunity,
            weakness=weakness,
            attack_damage=attack_damage,
            attack_type=attack_type,
            initiative=initiative,
        )


def test_group():
    sample = (
        "8808 units each with 5616 hit points (immune to cold; weak to radiation) "
        + "with an attack that does 5 bludgeoning damage at initiative 10"
    )
    group = Group.from_raw(sample, "foo")
    assert group.type == "foo"
    assert group.units == 8808
    assert group.unit_hp == 5616
    assert group.immunity == {"cold"}
    assert group.weakness == {"radiation"}
    assert group.attack_damage == 5
    assert group.attack_type == "bludgeoning"
    assert group.initiative == 10

    sample2 = (
        "3098 units each with 19840 hit points (weak to bludgeoning, cold) "
        + "with an attack that does 12 radiation damage at initiative 3"
    )
    group2 = Group.from_raw(sample2, "bar")
    assert group2.type == "bar"
    assert group2.units == 3098
    assert group2.unit_hp == 19840
    assert group2.immunity == set()
    assert group2.weakness == {"bludgeoning", "cold"}
    assert group2.attack_damage == 12
    assert group2.attack_type == "radiation"
    assert group2.initiative == 3


class ImmuneSystem:
    def __init__(self, immune_system, infection, immune_boost=0):
        self.groups = []

        for raw_group in immune_system:
            self.groups.append(Group.from_raw(raw_group, "immune", immune_boost))

        for raw_group in infection:
            self.groups.append(Group.from_raw(raw_group, "infection"))

    def count(self):
        return sum(g.units for g in self.groups if g.type == "immune"), sum(
            g.units for g in self.groups if g.type != "immune"
        )

    def target_selection_order(self):
        """
        In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher
        initiative chooses first.
        """
        order = [
            (g.effective_power(), g.initiative, i)
            for i, g in enumerate(self.groups)
            if g.units > 0
        ]
        sorted_order = sorted(order, reverse=True)
        return [i for _, _, i in sorted_order]

    def select_target(self):
        """
        During the target selection phase, each group attempts to choose one target.

        The attacking group chooses to target the group in the enemy army to which it would deal the most damage
        (after accounting for weaknesses and immunities, but not accounting for whether the defending group has
        enough units to actually receive all of that damage).

        If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to
        target the defending group with the largest effective power; if there is still a tie, it chooses the defending
        group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target.
        Defending groups can only be chosen as a target by one attacking group.

        At the end of the target selection phase, each group has selected zero or one groups to attack, and each
        group is being attacked by zero or one groups.
        """
        targets = []
        already_picked = set()
        for attacker_position in self.target_selection_order():
            attacker = self.groups[attacker_position]
            possible_targets = {
                (g.damage_multiplier(attacker), g.effective_power(), g.initiative, i)
                for i, g in enumerate(self.groups)
                if i not in already_picked
                and g.type != attacker.type
                and g.units > 0
                and g.damage_multiplier(attacker) > 0
            }
            if len(possible_targets) > 0:
                _, _, _, target_position = max(possible_targets)
                targets.append((attacker_position, target_position))
                already_picked.add(target_position)
        return targets

    def attack_order(self):
        """
        Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or
        the immune system. (If a group contains no units, it cannot attack.)
        """
        order = [
            (self.groups[ag].initiative, ag, tg) for ag, tg in self.select_target()
        ]
        sorted_order = sorted(order, reverse=True)
        return [(ag, tg) for _, ag, tg in sorted_order]

    def attack(self):
        """
        During the attacking phase, each group deals damage to the target it selected, if any.

        After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army
        has lost all of its units.
        """

        for attacker_position, target_position in self.attack_order():
            attacker = self.groups[attacker_position]
            target = self.groups[target_position]
            new_target = target.attacked_by(attacker)
            self.groups[target_position] = new_target

        return self.count()

    def fight(self):
        """
        Each fight consists of two phases: target selection and attacking.
        """
        stale_mate_check = defaultdict(int)
        remaining_immune, remaining_infection = self.count()
        while remaining_immune > 0 and remaining_infection > 0:
            remaining_immune, remaining_infection = self.attack()
            stale_mate_check[(remaining_immune, remaining_infection)] += 1
            if stale_mate_check[(remaining_immune, remaining_infection)] > 1_000:
                break
        return remaining_immune, remaining_infection


SAMPLE_IMMUNE = [
    "17 units each with 5390 hit points (weak to radiation, bludgeoning) "
    + "with an attack that does 4507 fire damage at initiative 2",
    "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) "
    + "with an attack that does 25 slashing damage at initiative 3",
]

SAMPLE_INFECTION = [
    "801 units each with 4706 hit points (weak to radiation) "
    + "with an attack that does 116 bludgeoning damage at initiative 1",
    "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) "
    + "with an attack that does 12 slashing damage at initiative 4",
]


def test_immune_system():
    immune_system = ImmuneSystem(SAMPLE_IMMUNE, SAMPLE_INFECTION)
    assert immune_system.count() == (17 + 989, 801 + 4485)
    assert immune_system.attack() == (905, 797 + 4434)
    assert immune_system.attack() == (761, 793 + 4434)
    assert immune_system.fight() == (0, 5216)


def test_puzzle_immune_system():
    immune_system = ImmuneSystem(IMMUNE_SYSTEM_INPUT, INFECTION_INPUT)
    assert immune_system.count() == (27227, 24392)
    assert immune_system.fight() == (0, 21127)


def test_puzzle_part2_immune_system():
    boost = 32
    while True:
        boost += 1
        immune_system = ImmuneSystem(IMMUNE_SYSTEM_INPUT, INFECTION_INPUT, boost)
        result = immune_system.fight()
        if result[0] > 0 and result[1] == 0:
            break
    assert boost == 34
    assert result == (2456, 0)
