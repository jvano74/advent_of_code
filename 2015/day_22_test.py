from typing import NamedTuple


class Puzzle:
    """
    --- Day 22: Wizard Simulator 20XX ---
    Little Henry Case decides that defeating bosses with swords and stuff is boring. Now he's playing the game with a
    wizard. Of course, he gets stuck on another boss and needs your help again.

    In this version, combat still proceeds with the player and the boss taking alternating turns. The player still
    goes first. Now, however, you don't get any equipment; instead, you must choose one of your spells to cast.
    The first character at or below 0 hit points loses.

    Since you're a wizard, you don't get to wear armor, and you can't attack normally. However, since you do magic
    damage, your opponent's armor is ignored, and so the boss effectively has zero armor as well. As before, if armor
    (from a spell, in this case) would reduce damage below 1, it becomes 1 instead - that is, the boss' attacks
    always deal at least 1 damage.

    On each of your turns, you must select one of your spells to cast. If you cannot afford to cast any spell,
    you lose. Spells cost mana; you start with 500 mana, but have no maximum limit. You must have enough mana to cast
    a spell, and its cost is immediately deducted when you cast it. Your spells are Magic Missile, Drain, Shield,
    Poison, and Recharge.

    - Magic Missile costs 53 mana. It instantly does 4 damage.
    - Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    - Shield costs 113 mana. It starts an effect that lasts for 6 turns.
      While it is active, your armor is increased by 7.
    - Poison costs 173 mana. It starts an effect that lasts for 6 turns.
      At the start of each turn while it is active, it deals the boss 3 damage.
    - Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
      At the start of each turn while it is active, it gives you 101 new mana.

    Effects all work the same way. Effects apply at the start of both the player's turns and the boss' turns. Effects
    are created with a timer (the number of turns they last); at the start of each turn, after they apply any effect
    they have, their timer is decreased by one. If this decreases the timer to zero, the effect ends. You cannot cast
    a spell that would start an effect which is already active. However, effects can be started on the same turn they
    end.

    For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:

    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 13 hit points
    Player casts Poison.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 77 mana
    - Boss has 13 hit points
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 damage.

    -- Player turn --
    - Player has 2 hit points, 0 armor, 77 mana
    - Boss has 10 hit points
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 2 hit points, 0 armor, 24 mana
    - Boss has 3 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.
    Now, suppose the same initial conditions, except that the boss has 14 hit points instead:

    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 14 hit points
    Player casts Recharge.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 21 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 4.
    Boss attacks for 8 damage!

    -- Player turn --
    - Player has 2 hit points, 0 armor, 122 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 3.
    Player casts Shield, increasing armor by 7.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 110 mana
    - Boss has 14 hit points
    Shield's timer is now 5.
    Recharge provides 101 mana; its timer is now 2.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 1 hit point, 7 armor, 211 mana
    - Boss has 14 hit points
    Shield's timer is now 4.
    Recharge provides 101 mana; its timer is now 1.
    Player casts Drain, dealing 2 damage, and healing 2 hit points.

    -- Boss turn --
    - Player has 3 hit points, 7 armor, 239 mana
    - Boss has 12 hit points
    Shield's timer is now 3.
    Recharge provides 101 mana; its timer is now 0.
    Recharge wears off.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 2 hit points, 7 armor, 340 mana
    - Boss has 12 hit points
    Shield's timer is now 2.
    Player casts Poison.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 167 mana
    - Boss has 12 hit points
    Shield's timer is now 1.
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 1 hit point, 7 armor, 167 mana
    - Boss has 9 hit points
    Shield's timer is now 0.
    Shield wears off, decreasing armor by 7.
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 1 hit point, 0 armor, 114 mana
    - Boss has 2 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.

    You start with 50 hit points and 500 mana points. The boss's actual stats are in your puzzle input. What is the
    least amount of mana you can spend and still win the fight? (Do not include mana recharge effects as "spending"
    negative mana.)

    --- Part Two ---
    On the next run through the game, you increase the difficulty to hard.

    At the start of each player turn (before any other effects apply), you lose 1 hit point. If this brings you to
    or below 0 hit points, you lose.

    With the same starting stats for you and the boss, what is the least amount of mana you can spend and still
    win the fight?
    """

    pass


class Effect(NamedTuple):
    cost: int
    armor: int
    damage: int


class Spell(NamedTuple):
    cost: int
    damage: int
    heal: int
    effect_duration: int
    effect_cost: int
    effect_armor: int
    effect_damage: int


class Character:
    def __init__(self, name, hp=50, damage=0, armor=0, mana=500, mode="normal"):
        self.print_combat = False
        self.name = name
        self.initial_hp = hp
        self.initial_damage = damage
        self.initial_armor = armor
        self.initial_mana = mana
        self.mode = mode

        # - Magic Missile costs 53 mana. It instantly does 4 damage.
        #
        # - Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
        #
        # - Shield costs 113 mana. It starts an effect that lasts for 6 turns.
        #   While it is active, your armor is increased by 7.
        #
        # - Poison costs 173 mana. It starts an effect that lasts for 6 turns.
        #   At the start of each turn while it is active, it deals the boss 3 damage.
        #
        # - Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
        #   At the start of each turn while it is active, it gives you 101 new mana.
        self.known_spells = {
            "Magic Missile": Spell(
                cost=53,
                damage=4,
                heal=0,
                effect_duration=0,
                effect_cost=0,
                effect_armor=0,
                effect_damage=0,
            ),
            "Drain": Spell(
                cost=73,
                damage=2,
                heal=2,
                effect_duration=0,
                effect_cost=0,
                effect_armor=0,
                effect_damage=0,
            ),
            "Shield": Spell(
                cost=113,
                damage=0,
                heal=0,
                effect_duration=6,
                effect_cost=0,
                effect_armor=7,
                effect_damage=0,
            ),
            "Poison": Spell(
                cost=173,
                damage=0,
                heal=0,
                effect_duration=6,
                effect_cost=0,
                effect_armor=0,
                effect_damage=3,
            ),
            "Recharge": Spell(
                cost=229,
                damage=0,
                heal=0,
                effect_duration=5,
                effect_cost=101,
                effect_armor=0,
                effect_damage=0,
            ),
        }

        # All the following to be applied when resetting character
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.mana = mana
        self.mana_spent = 0
        self.active_effects = {}

    def reset(self):
        self.hp = self.initial_hp
        self.damage = self.initial_damage
        self.armor = self.initial_armor
        self.mana = self.initial_mana
        self.mana_spent = 0
        self.active_effects = {}

    def spell_options(self):
        # NEED TO FIX - doesn't factor in effect of recharge which would allow additional spells
        # options = set(s for s in self.known_spells if self.known_spells[s].cost < self.mana)
        # return options - set(self.active_effects)
        raise Exception(
            "Feature is broken, does not factor in what recharge would add to mana"
        )

    def cast(self, spell_to_cast, target=None):
        if spell_to_cast in self.active_effects:
            # raise Exception(f'{spell_to_cast} already cast/active')
            return f"{spell_to_cast} already cast/active"
        spell = self.known_spells[spell_to_cast]

        if self.mana < spell.cost:
            # raise Exception(f'Not enough mana for {spell_to_cast}')
            return f"Not enough mana for {spell_to_cast}"
        self.mana -= spell.cost
        self.mana_spent += spell.cost

        if spell.damage > 0:
            if self.print_combat:
                print(f"{self.name} attacks with {spell_to_cast} for {self.damage}")
            if target.take_damage(spell.damage) <= 0:
                return "You Win"

        if spell.heal > 0:
            self.hp += spell.heal
            if self.print_combat:
                print(
                    f"{self.name} heals {spell.heal} hp to {self.hp} from {spell_to_cast}"
                )

        if spell.effect_duration > 0:
            if self.print_combat:
                print(f"{self.name} starts {spell_to_cast} effect")
            self.add_effect(
                spell_to_cast,
                spell.effect_duration,
                Effect(spell.effect_cost, spell.effect_armor, 0),
            )
            if spell.effect_armor > 0:
                self.armor += spell.effect_armor
                if self.print_combat:
                    print(
                        f"{self.name} armor increased {spell.effect_armor} hp to {self.armor} from {spell_to_cast}"
                    )
            if spell.effect_damage > 0:
                target.add_effect(
                    spell_to_cast,
                    spell.effect_duration,
                    Effect(0, 0, spell.effect_damage),
                )
        return "Continue"

    def add_effect(self, effect_name, duration, effect):
        self.active_effects[effect_name] = (duration, effect)

    def attack(self, opponent):
        if self.print_combat:
            print(f"{self.name} attacks with {self.damage}")
        return opponent.take_damage(self.damage)

    def take_damage(self, amount):
        damage_dealt = amount - self.armor
        if amount > 0 and damage_dealt < 1:
            damage_dealt = 1
        self.hp -= damage_dealt
        if self.print_combat:
            print(f"{self.name} took {damage_dealt}; down to {self.hp} hp")
        return self.hp

    def start_of_turn(self, role):
        if role == "Attack":
            if self.print_combat:
                print()
                print(f"-- {self.name} turn --")
            if self.mode == "hard":
                self.hp -= 1
                if self.print_combat:
                    print(f"hard mode, -1 hp, now @ {self.hp}")

        if self.print_combat:
            print(
                f"- {self.name} has {self.hp} hp, {self.armor} armor, {self.mana} mana"
            )

        effect_ending = {}
        for effect_name in self.active_effects:
            turns_left, effect = self.active_effects[effect_name]
            if effect.damage > 0:
                self.hp -= effect.damage
                if self.print_combat:
                    print(f"{effect_name} causes {effect.damage} damage")
            if effect.cost > 0:
                self.mana += effect.cost
                if self.print_combat:
                    print(f"{effect_name} gives {effect.cost} mana")
            if self.print_combat:
                print(f"{effect_name} timer now {turns_left - 1}")
            if turns_left > 1:
                self.active_effects[effect_name] = (turns_left - 1, effect)
            else:
                effect_ending[effect_name] = effect
        for effect_name, effect in effect_ending.items():
            self.active_effects.pop(effect_name)
            if effect.armor > 0:
                self.armor -= effect.armor
                if self.print_combat:
                    print(f"{effect_name} ended, armor now {self.armor}")
            else:
                if self.print_combat:
                    print(f"{effect_name} ended")

        return self.hp

    def end_of_turn(self):
        return self.hp


class Fight:
    def __init__(self, player, boss, print_combat=False):
        self.player = player
        self.boss = boss
        self.print_combat = print_combat

        self.player.print_combat = print_combat
        self.boss.print_combat = print_combat
        if print_combat:
            print()

    def reset(self):
        self.player.reset()
        self.boss.reset()

    def combat_round(self, spell_to_cast):
        if self.print_combat:
            print()
        # Player goes first
        if self.player.start_of_turn("Attack") <= 0:
            return "You Lose"
        if self.boss.start_of_turn("Defend") <= 0:
            return "You Win"

        cast_result = self.player.cast(spell_to_cast, self.boss)
        if cast_result == "You Win":
            return "You Win"
        elif cast_result != "Continue":
            return "You Lose"

        if self.boss.end_of_turn() <= 0:
            return "You Win"
        if self.player.end_of_turn() <= 0:
            return "You Lose"

        # Next boss takes turn
        if self.boss.start_of_turn("Attack") <= 0:
            return "You Win"
        if self.player.start_of_turn("Defend") <= 0:
            return "You Lose"
        if self.boss.attack(self.player) <= 0:
            return "You Lose"
        if self.player.end_of_turn() <= 0:
            return "You Lose"
        if self.boss.end_of_turn() <= 0:
            return "You Win"
        return f"player at {self.player.hp}, boss at {self.boss.hp}"

    def multiple_rounds(self, list_of_spells):
        status = f"player at {self.player.hp}, boss at {self.boss.hp}"
        for spell in list_of_spells:
            status = self.combat_round(spell)
            if status in {"You Lose", "You Win"}:
                return status, self.player.mana_spent
        return status, self.player.mana_spent


def test_wizard_first_example():
    """
    For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:
    """
    example_boss = Character("Boss", hp=13, damage=8)
    example_wizard = Character("Player", hp=10, mana=250)
    example_fight = Fight(player=example_wizard, boss=example_boss, print_combat=True)
    print()

    """
    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 13 hit points
    Player casts Poison.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 77 mana
    - Boss has 13 hit points
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 damage.
    """
    print("=== First round cast Poison ===")
    result = example_fight.combat_round("Poison")
    print(result)
    assert result == "player at 2, boss at 10"

    """
    -- Player turn --
    - Player has 2 hit points, 0 armor, 77 mana
    - Boss has 10 hit points
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 2 hit points, 0 armor, 24 mana
    - Boss has 3 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.
    """
    print("=== Second round cast Magic Missile ===")
    result = example_fight.combat_round("Magic Missile")
    print(result)
    assert result == "You Win"


def test_wizard_second_example():
    """
    Now, suppose the same initial conditions, except that the boss has 14 hit points instead:
    """
    example_boss = Character("Boss", hp=14, damage=8)
    example_wizard = Character("Player", hp=10, mana=250)
    example_fight = Fight(player=example_wizard, boss=example_boss, print_combat=True)

    """
    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 14 hit points
    Player casts Recharge.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 21 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 4.
    Boss attacks for 8 damage!
    """
    print("=== First round cast Recharge ===")
    result = example_fight.combat_round("Recharge")
    print(result)
    assert result == "player at 2, boss at 14"

    """
    -- Player turn --
    - Player has 2 hit points, 0 armor, 122 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 3.
    Player casts Shield, increasing armor by 7.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 110 mana
    - Boss has 14 hit points
    Shield's timer is now 5.
    Recharge provides 101 mana; its timer is now 2.
    Boss attacks for 8 - 7 = 1 damage!
    """
    print("=== Second round cast Shield ===")
    result = example_fight.combat_round("Shield")
    print(result)
    assert result == "player at 1, boss at 14"

    """
    -- Player turn --
    - Player has 1 hit point, 7 armor, 211 mana
    - Boss has 14 hit points
    Shield's timer is now 4.
    Recharge provides 101 mana; its timer is now 1.
    Player casts Drain, dealing 2 damage, and healing 2 hit points.

    -- Boss turn --
    - Player has 3 hit points, 7 armor, 239 mana
    - Boss has 12 hit points
    Shield's timer is now 3.
    Recharge provides 101 mana; its timer is now 0.
    Recharge wears off.
    Boss attacks for 8 - 7 = 1 damage!
    """
    print("=== Third round cast Drain ===")
    result = example_fight.combat_round("Drain")
    print(result)
    assert result == "player at 2, boss at 12"

    """
    -- Player turn --
    - Player has 2 hit points, 7 armor, 340 mana
    - Boss has 12 hit points
    Shield's timer is now 2.
    Player casts Poison.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 167 mana
    - Boss has 12 hit points
    Shield's timer is now 1.
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 - 7 = 1 damage!
    """
    print("=== Fourth round cast Poison ===")
    result = example_fight.combat_round("Poison")
    print(result)
    assert result == "player at 1, boss at 9"

    """
    -- Player turn --
    - Player has 1 hit point, 7 armor, 167 mana
    - Boss has 9 hit points
    Shield's timer is now 0.
    Shield wears off, decreasing armor by 7.
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 1 hit point, 0 armor, 114 mana
    - Boss has 2 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.
    """
    print("=== Fourth round cast Magic Missile ===")
    result = example_fight.combat_round("Magic Missile")
    print(result)
    assert result == "You Win"


def test_wizard_second_example_automated():
    example_boss = Character("Boss", hp=14, damage=8)
    example_wizard = Character("Player", hp=10, mana=250)
    example_fight = Fight(player=example_wizard, boss=example_boss)
    results = example_fight.multiple_rounds(
        ["Recharge", "Shield", "Drain", "Poison", "Magic Missile"]
    )
    assert results == ("You Win", 641)


def search_real_game(current_min_mana_soln=0, mode="normal"):
    # after running and finding at least one solution
    # we can pass in current_min_mana_soln to reduce search space
    # e.g. know solution exists below ??? mana
    real_boss = Character("Boss", hp=71, damage=10)
    real_wizard = Character("Player", hp=50, mana=500, mode=mode)
    real_fight = Fight(player=real_wizard, boss=real_boss)
    results = []
    paths_to_explore = [(0, [])]
    while True:
        # paths_to_explore = sorted(paths_to_explore, reverse=True)
        paths_to_explore = sorted(paths_to_explore)
        spell_list = ""
        while spell_list == "" and len(paths_to_explore) > 0:
            cost, spell_list = paths_to_explore.pop()
            if cost > current_min_mana_soln > 0:
                spell_list = ""
        if spell_list == "" and len(paths_to_explore) == 0:
            break
        real_fight.reset()
        status, mana_spent = real_fight.multiple_rounds(spell_list)
        if status == "You Win":
            if current_min_mana_soln == 0:
                current_min_mana_soln = mana_spent
            current_min_mana_soln = min(current_min_mana_soln, mana_spent)
            results.append((mana_spent, spell_list))
        elif status != "You Lose":
            for next_spell in real_wizard.known_spells:
                new_path = spell_list[:]
                new_path.append(next_spell)
                new_weight = mana_spent + real_wizard.known_spells[next_spell].cost
                paths_to_explore.append((new_weight, new_path))
    return results


def play_real_game():
    real_boss = Character("Boss", hp=71, damage=10)
    real_wizard = Character("Player", hp=50, mana=500)
    real_fight = Fight(player=real_wizard, boss=real_boss, print_combat=True)
    result = ""
    while True:
        while real_boss.hp > 0 and real_wizard.hp > 0:
            print(f"Spent {real_wizard.mana_spent} remaining {real_wizard.mana}")
            next_spell = input("@! Enter Spell to cast:")
            result = real_fight.combat_round(next_spell)
            print(result)
        print("GAME OVER")
        if input("Play again") != "n":
            real_fight.reset()
        else:
            break
    return result


def test_search_real_game():
    search_result = search_real_game()
    print(search_result)
    assert min(search_result)[0] == 1824


def test_search_hard_game():
    search_result = search_real_game(mode="hard")
    print(search_result)
    assert min(search_result)[0] == 1937


def test_wizard_examples_from_search():
    real_boss = Character("Boss", hp=71, damage=10)
    real_wizard = Character("Player", hp=50, mana=500)
    real_fight = Fight(player=real_wizard, boss=real_boss, print_combat=True)
    list_of_spells = [
        "Recharge",
        "Poison",
        "Shield",
        "Recharge",
        "Poison",
        "Shield",
        "Recharge",
        "Poison",
        "Shield",
        "Magic Missile",
        "Poison",
        "Magic Missile",
    ]
    assert real_fight.multiple_rounds(list_of_spells) == ("You Win", 1824)


if __name__ == "__main__":
    play_real_game()
