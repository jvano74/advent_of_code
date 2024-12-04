class Puzzle:
    """
    --- Day 14: Chocolate Charts ---
    You finally have a chance to look at all of the produce moving around. Chocolate, cinnamon, mint, chili peppers,
    nutmeg, vanilla... the Elves must be growing these plants to make hot chocolate! As you realize this, you hear a
    conversation in the distance. When you go to investigate, you discover two Elves in what appears to be a
    makeshift underground kitchen/laboratory.

    The Elves are trying to come up with the ultimate hot chocolate recipe; they're even maintaining a scoreboard
    which tracks the quality score (0-9) of each recipe.

    Only two recipes are on the board: the first recipe got a score of 3, the second, 7. Each of the two Elves has
    a current recipe: the first Elf starts with the first recipe, and the second Elf starts with the second recipe.

    To create new recipes, the two Elves combine their current recipes. This creates new recipes from the digits
    of the sum of the current recipes' scores. With the current recipes' scores of 3 and 7, their sum is 10, and
    so two new recipes would be created: the first with score 1 and the second with score 0. If the current
    recipes' scores were 2 and 3, the sum, 5, would only create one recipe (with a score of 5) with its single digit.

    The new recipes are added to the end of the scoreboard in the order they are created. So, after the first
    round, the scoreboard is 3, 7, 1, 0.

    After all new recipes are added to the scoreboard, each Elf picks a new current recipe. To do this,
    the Elf steps forward through the scoreboard a number of recipes equal to 1 plus the score of their current
    recipe. So, after the first round, the first Elf moves forward 1 + 3 = 4 times, while the second Elf moves
    forward 1 + 7 = 8 times. If they run out of recipes, they loop back around to the beginning. After the first
    round, both Elves happen to loop around until they land on the same recipe that they had in the beginning;
    in general, they will move to different recipes.

    Drawing the first Elf as parentheses and the second Elf as square brackets, they continue this process:

    (3)[7]
    (3)[7] 1  0
     3  7  1 [0](1) 0
     3  7  1  0 [1] 0 (1)
    (3) 7  1  0  1  0 [1] 2
     3  7  1  0 (1) 0  1  2 [4]
     3  7  1 [0] 1  0 (1) 2  4  5
     3  7  1  0 [1] 0  1  2 (4) 5  1
     3 (7) 1  0  1  0 [1] 2  4  5  1  5
     3  7  1  0  1  0  1  2 [4](5) 1  5  8
     3 (7) 1  0  1  0  1  2  4  5  1  5  8 [9]
     3  7  1  0  1  0  1 [2] 4 (5) 1  5  8  9  1  6
     3  7  1  0  1  0  1  2  4  5 [1] 5  8  9  1 (6) 7
     3  7  1  0 (1) 0  1  2  4  5  1  5 [8] 9  1  6  7  7
     3  7 [1] 0  1  0 (1) 2  4  5  1  5  8  9  1  6  7  7  9
     3  7  1  0 [1] 0  1  2 (4) 5  1  5  8  9  1  6  7  7  9  2

    The Elves think their skill will improve after making a few recipes (your puzzle input). However, that could take
    ages; you can speed this up considerably by identifying the scores of the ten recipes after that. For example:

    If the Elves think their skill will improve after making 9 recipes, the scores of the ten recipes after the first
    nine on the scoreboard would be 5158916779 (highlighted in the last line of the diagram).
    After 5 recipes, the scores of the next ten would be 0124515891.
    After 18 recipes, the scores of the next ten would be 9251071085.
    After 2018 recipes, the scores of the next ten would be 5941429882.

    What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?

    Your puzzle input is 793061.

    --- Part Two ---
    As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the
    scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

    51589 first appears after 9 recipes.
    01245 first appears after 5 recipes.
    92510 first appears after 18 recipes.
    59414 first appears after 2018 recipes.

    How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
    """
    pass


def coco_score(elf_1_repipe, elf_2_repipe):
    recipe_book = [elf_1_repipe, elf_2_repipe]
    elf_1 = 0
    elf_2 = 1
    loc = 0
    while True:
        recipe_book_len = len(recipe_book)
        if loc < recipe_book_len:
            yield recipe_book[loc]
            loc += 1
        elf_1 = elf_1 % recipe_book_len
        elf_2 = elf_2 % recipe_book_len
        total = recipe_book[elf_1] + recipe_book[elf_2]
        if total >= 10:
            recipe_book.append(1)
            total = total % 10
        recipe_book.append(total)
        elf_1 += 1 + recipe_book[elf_1]
        elf_2 += 1 + recipe_book[elf_2]


def extract_range(generator, start, length):
    result = []
    for _ in range(start):
        next(generator)
    for _ in range(length):
        result.append(f'{next(generator)}')
    return ''.join(result)


def match_sequence(generator, sequence):
    count = 0
    test = ''
    slen = len(sequence)
    while len(test) < slen:
        test = f'{test}{next(generator)}'
        count += 1
    while test != sequence:
        test = f'{test[1:]}{next(generator)}'
        count += 1
    return count - slen


def test_coco_score():
    cook_off = coco_score(3, 7)
    expected = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]
    assert all(v == next(cook_off) for v in expected)
    assert extract_range(coco_score(3, 7), 9, 10) == '5158916779'
    assert match_sequence(coco_score(3, 7), '51589') == 9
    assert match_sequence(coco_score(3, 7), '01245') == 5
    assert match_sequence(coco_score(3, 7), '92510') == 18
    assert match_sequence(coco_score(3, 7), '59414') == 2018
    # puzzle
    assert extract_range(coco_score(3, 7), 793061, 10) == '4138145721'
    assert match_sequence(coco_score(3, 7), '793061') == 20276284
