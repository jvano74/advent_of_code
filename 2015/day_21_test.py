from typing import NamedTuple


class Puzzle:
    """
    --- Day 21: RPG Simulator 20XX ---
    Little Henry Case got a new video game for Christmas. It's an RPG, and he's stuck on a boss. He needs to know what
    equipment to buy at the shop. He hands you the controller.

    In this game, the player (you) and the enemy (the boss) take turns attacking. The player always goes first. Each
    attack reduces the opponent's hit points by at least 1. The first character at or below 0 hit points loses.

    Damage dealt by an attacker each turn is equal to the attacker's damage score minus the defender's armor score. An
    attacker always does at least 1 damage. So, if the attacker has a damage score of 8, and the defender has an armor
    score of 3, the defender loses 5 hit points. If the defender had an armor score of 300, the defender would still
    lose 1 hit point.

    Your damage score and armor score both start at zero. They can be increased by buying items in exchange for gold.
    You start with no items and have as much gold as you need. Your total damage or armor is equal to the sum of those
    stats from all of your items. You have 100 hit points.

    Here is what the item shop is selling:

    Weapons:    Cost  Damage  Armor
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0

    Armor:      Cost  Damage  Armor
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5

    Rings:      Cost  Damage  Armor
    Damage +1    25     1       0
    Damage +2    50     2       0
    Damage +3   100     3       0
    Defense +1   20     0       1
    Defense +2   40     0       2
    Defense +3   80     0       3

    You must buy exactly one weapon; no dual-wielding. Armor is optional, but you can't use more than one. You can buy
    0-2 rings (at most one for each hand). You must use any items you buy. The shop only has one of each item, so you
    can't buy, for example, two rings of Damage +3.

    For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage,
    and 2 armor:

    The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.
    In this scenario, the player wins! (Barely.)

    You have 100 hit points. The boss's actual stats are in your puzzle input.

    What is the least amount of gold you can spend and still win the fight?

    --- Part Two ---
    Turns out the shopkeeper is working with the boss, and can persuade you to buy whatever items he wants. The other
    rules still apply, and he still only has one of each item.

    What is the most amount of gold you can spend and still lose the fight?
    """
    pass


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int

    def __lt__(self, other):
        return self.cost < other.cost

    def __add__(self, other):
        return Item(f'{self.name}, {other.name}',
                    self.cost + other.cost,
                    self.damage + other.damage,
                    self.armor + other.armor)


def test_items():
    assert Weapons[0] + Weapons[1] == Item('Dagger, Shortsword', 18, 9, 0)


class Stats(NamedTuple):
    name: str
    hp: int
    damage: int
    armor: int

    def attacks(self, other, print_combat=False):
        """
        Damage dealt by an attacker each turn is equal to the attacker's damage score minus the defender's armor score.
        An attacker always does at least 1 damage.

        So, if the attacker has a damage score of 8, and the defender has an armor score of 3,
        the defender loses 5 hit points.

        If the defender had an armor score of 300, the defender would still lose 1 hit point.
        """
        damage_delt = self.damage - other.armor
        if damage_delt < 1:
            damage_delt = 1
        if print_combat:
            print(f'{self.name} deals {damage_delt}; {other.name} down to {other.hp - damage_delt} hp')
        return Stats(other.name, other.hp - damage_delt, other.damage, other.armor)


class Player:
    def __init__(self, enemy, items, hp=100):
        self.items = items
        self.enemy = enemy
        self.stats = Stats('Player', hp, items.damage, items.armor)

    def run_combat(self, print_combat=False):
        while True:
            self.enemy = self.stats.attacks(self.enemy, print_combat)
            if self.enemy.hp <= 0:
                if print_combat:
                    print('You won')
                return 'You won'
            self.stats = self.enemy.attacks(self.stats, print_combat)
            if self.stats.hp <= 0:
                if print_combat:
                    print('You lost')
                return 'You lost'


def test_player():
    print()
    player1 = Player(Stats('Sample Boss', 12, 7, 2), Item('Total Items', 0, 5, 5), 8)
    assert player1.run_combat(print_combat=True) == 'You won'


# Real game values
INPUT_BOSS = Stats('Boss', 104, 8, 1)

Weapons = [Item('Dagger', 8, 4, 0),
           Item('Shortsword', 10, 5, 0),
           Item('Warhammer', 25, 6, 0),
           Item('Longsword', 40, 7, 0),
           Item('Greataxe', 74, 8, 0)]

Armor = [Item('Leather', 13, 0, 1),
         Item('Chainmail', 31, 0, 2),
         Item('Splintmail', 53, 0, 3),
         Item('Bandedmail', 75, 0, 4),
         Item('Platemail', 102, 0, 5)]

Rings = [Item('Damage +1', 25, 1, 0),
         Item('Damage +2', 50, 2, 0),
         Item('Damage +3', 100, 3, 0),
         Item('Defense +1', 20, 0, 1),
         Item('Defense +2', 40, 0, 2),
         Item('Defense +3', 80, 0, 3)]


def generate_player_items(weapons, armor, rings):
    weapon_only = set(weapons)
    weapon_and_armor = set()
    for w in weapon_only:
        for a in armor:
            weapon_and_armor.add(w + a)
    ring_options = set()
    for i in range(0, len(rings)):
        ring_options.add(rings[i])
        for j in range(i+1, len(rings)):
            ring_options.add(rings[i] + rings[j])
    non_ring_options = weapon_only.union(weapon_and_armor)
    total_options = set(non_ring_options)
    for option in non_ring_options:
        for rings in ring_options:
            total_options.add(option + rings)
    return sorted(list(total_options))


def find_solution(win=True):
    possible_gear = generate_player_items(Weapons, Armor, Rings)
    if not win:
        possible_gear = reversed(possible_gear)
    for gear in possible_gear:
        player1 = Player(INPUT_BOSS, gear)
        if win and player1.run_combat() == 'You won':
            return player1.items
        elif not win and player1.run_combat() != 'You won':
            return player1.items


def test_find_solution():
    assert find_solution() == Item(name='Longsword, Leather, Damage +1', cost=78, damage=8, armor=1)


def test_find_solution2():
    assert find_solution(win=False) == Item(name='Dagger, Damage +3, Defense +2', cost=148, damage=7, armor=2)
