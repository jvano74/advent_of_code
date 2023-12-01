from typing import List, NamedTuple
from collections import deque, defaultdict
from heapq import heappush, heappop


class Solution:
    """
    --- Day 15: Science for Hungry People ---
    Today, you set out on the task of perfecting your milk-dunking cookie recipe.
    All you have to do is find the right balance of ingredients.

    Your recipe leaves room for exactly 100 teaspoons of ingredients.
    You make a list of the remaining ingredients you could use to finish the recipe
    (your puzzle input) and their properties per teaspoon:

    capacity (how well it helps the cookie absorb milk)
    durability (how well it keeps the cookie intact when full of milk)
    flavor (how tasty it makes the cookie)
    texture (how it improves the feel of the cookie)
    calories (how many calories it adds to the cookie)

    You can only measure ingredients in whole-teaspoon amounts accurately,
    and you have to be accurate so you can reproduce your results in the future.
    The total score of a cookie can be found by adding up each of the properties
    (negative totals become 0) and then multiplying together everything except calories.

    For instance, suppose you have these two ingredients:

    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

    Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon
    (because the amounts of each ingredient must add up to 100) would result in a
    cookie with the following properties:

    A capacity of 44*-1 + 56*2 = 68
    A durability of 44*-2 + 56*3 = 80
    A flavor of 44*6 + 56*-2 = 152
    A texture of 44*3 + 56*-1 = 76

    Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in
    a total score of 62842880, which happens to be the best score possible given these ingredients.
    If any properties had produced a negative total, it would have instead become zero, causing the
    whole score to multiply to zero.

    Given the ingredients in your kitchen and their properties, what is the total score of the
    highest-scoring cookie you can make?

    My input:
    Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
    Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
    Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
    Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8

    """


class Ingredient(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


class Cookie:
    def __init__(self, options: dict, receipt: dict):
        self.options = options
        self.receipt = receipt
        self.high_score = 0
        self.high_score_receipt = {}

    def score(self):
        capacity, durability, flavor, texture, calories = 0, 0, 0, 0, 0
        for item in self.receipt:
            capacity += self.receipt[item] * self.options[item].capacity
            durability += self.receipt[item] * self.options[item].durability
            flavor += self.receipt[item] * self.options[item].flavor
            texture += self.receipt[item] * self.options[item].texture
            calories += self.receipt[item] * self.options[item].calories

        total = 1
        total *= capacity if capacity > 0 else 0
        total *= durability if durability > 0 else 0
        total *= flavor if flavor > 0 else 0
        total *= texture if texture > 0 else 0

        return total

    def new_receipt(self, receipt):
        self.receipt = receipt
        new_score = self.score()
        if new_score > self.high_score:
            self.high_score = new_score
            self.high_score_receipt = dict(self.receipt)

    def find_max(self):
        pass


def test_sample():
    sample_cookie = Cookie(
        {
            "butterscotch": Ingredient(-1, -2, 6, 3, 8),
            "cinnamon": Ingredient(2, 3, -2, -1, 3),
        },
        {"butterscotch": 44, "cinnamon": 56},
    )
    assert sample_cookie.score() == 62842880
    for a in range(101):
        sample_cookie.new_receipt({"butterscotch": a, "cinnamon": 100 - a})
    assert sample_cookie.high_score == 62842880


def test_submission():
    my_ingredients = {
        "sugar": Ingredient(3, 0, 0, -3, 2),
        "sprinkles": Ingredient(-3, 3, 0, 0, 9),
        "candy": Ingredient(-1, 0, 4, 0, 1),
        "chocolate": Ingredient(0, 0, -2, 2, 8),
    }
    my_cookie = Cookie(my_ingredients, {})
    for a in range(101):
        for b in range(101):
            for c in range(101):
                my_receipt = {
                    "sugar": a,
                    "sprinkles": b,
                    "candy": c,
                    "chocolate": 100 - (a + b + c),
                }
                my_cookie.new_receipt(my_receipt)
    assert my_cookie.high_score == 222870
    # reset high score
    my_cookie.high_score = 0
    for a in range(101):
        for b in range(101):
            for c in range(101):
                d = 100 - (a + b + c)
                if 2 * a + 9 * b + c + 8 * d == 500:
                    my_receipt = {
                        "sugar": a,
                        "sprinkles": b,
                        "candy": c,
                        "chocolate": d,
                    }
                    my_cookie.new_receipt(my_receipt)
    assert my_cookie.high_score == 222870
