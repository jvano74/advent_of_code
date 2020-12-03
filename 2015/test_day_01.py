def ans(input):
    '''
    --- Day 1: Not Quite Lisp ---
    Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

    Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

    Here's an easy puzzle to warm you up.

    Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

    An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

    The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

    For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.
    To what floor do the instructions take Santa?

    --- Part Two ---
    Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1).
    The first character in the instructions has position 1, the second character has position 2, and so on.

    For example:

    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.
    What is the position of the character that causes Santa to first enter the basement?

    '''
    floor = 0
    moves_above_ground = 0
    visited_basement = False
    for char in input:
        if char == '(':
            floor += 1
        else:
            floor -= 1
        if (floor < 0):
            visited_basement = True
        elif not(visited_basement):
            moves_above_ground += 1
    return (floor, moves_above_ground)

def test_ans():
    tests_and_results = {
        '(())': 0,
        '(((': 3,
        '(()(()(': 3,
        '))(((((': 3,
        '())': -1,
        '))(': -1,
        ')))': -3,
        ')())())': -3,
    }
    for val in tests_and_results:
        assert ans(val)[0] == tests_and_results[val]
    assert ans(')')[1] == 0
    assert ans('()())')[1] == 4

def test_sub():
    fp = open('./input_day_01.txt','r')
    if fp.mode == 'r':
        submission_input = fp.read()
    assert ans(submission_input) == (280,1796)
