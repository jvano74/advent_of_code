from pathlib import Path


class Puzzle:
    """
    --- Day 21: Allergen Assessment ---
    You reach the train's last stop and the closest you can get to your vacation island without getting wet.
    There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few
    days' worth of food for your journey.

    You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens
    are listed in a language you do understand. You should be able to use this information to determine which
    ingredient contains which allergen and work out which foods are safe to take with you on your trip.

    You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that
    food's ingredients list followed by some or all of the allergens the food contains.

    Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens
    aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list),
    the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list.
    However, even if an allergen isn't listed, the ingredient that contains that allergen could still be
    present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

    For example, consider the following list of foods:

    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)

    The first food in the list has four ingredients (written in a language you don't understand):
    mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens
    the food definitely contains are listed afterward: dairy and fish.

    The first step is to determine which ingredients can't possibly contain any of the allergens in
    any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh
    can contain an allergen. Counting the number of times any of these ingredients appear in any
    ingredients list produces 5: they all appear once each except sbzzf, which appears twice.

    Determine which ingredients cannot possibly contain any of the allergens in your list. How many
    times do any of those ingredients appear?

    --- Part Two ---
    Now that you've isolated the inert ingredients, you should have enough information to figure out which
    ingredient contains which allergen.

    In the above example:

    mxmxvkd contains dairy.
    sqjhc contains fish.
    fvjkl contains soy.

    Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your
    canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous
    ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.

    Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
    """

    pass


SAMPLE = [
    "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
    "trh fvjkl sbzzf mxmxvkd (contains dairy)",
    "sqjhc fvjkl (contains soy)",
    "sqjhc mxmxvkd sbzzf (contains fish)",
]


with open(Path(__file__).parent / "2020_21_input.txt") as fp:
    INPUT = [line.strip() for line in fp]


def get_allergens(foods):
    may_be_in = {}
    found_in = {}
    total_ingredients = []
    for food in foods:
        ingredients, allergens = food.split(" (contains ")
        ingredients = ingredients.split(" ")
        total_ingredients.extend(ingredients)
        allergens = allergens[:-1].split(", ")
        for allergen in allergens:
            if allergen in may_be_in:
                may_be_in[allergen] = may_be_in[allergen].intersection(ingredients)
            else:
                may_be_in[allergen] = set(ingredients)
    while len(may_be_in) > 0:
        known_ingredients = set(found_in.values())
        for allergen, possible_ingredients in may_be_in.items():
            updated_list = possible_ingredients - known_ingredients
            may_be_in[allergen] = updated_list
            if len(updated_list) == 1:
                found_in[allergen] = updated_list.pop()
        for known_allergen, known_ingredient in found_in.items():
            if known_allergen in may_be_in:
                may_be_in.pop(known_allergen)
    ok_count = sum(
        1 for ingredient in total_ingredients if ingredient not in found_in.values()
    )
    bad_list = ",".join(v for k, v in sorted(found_in.items()))
    return bad_list, ok_count


def test_get_allergens():
    assert get_allergens(SAMPLE) == ("mxmxvkd,sqjhc,fvjkl", 5)
    assert get_allergens(INPUT) == ("mxkh,gkcqxs,bvh,sp,rgc,krjn,bpbdlmg,tdbcfb", 1829)
