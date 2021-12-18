from typing import NamedTuple


class Puzzle:
    """
--- Day 18: Snailfish ---

You descend into the ocean trench and encounter some snailfish. They say they saw the sleigh keys! They'll
even tell you which direction the keys went if you help one of the smaller snailfish with his math homework.

Snailfish numbers aren't like regular numbers. Instead, every snailfish number is a pair - an ordered list
of two elements. Each element of the pair can be either a regular number or another pair.

Pairs are written as [x,y], where x and y are the elements within the pair. Here are some example snailfish
numbers, one snailfish number per line:

[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]

This snailfish homework is about addition. To add two snailfish numbers, form a pair from the left and
right parameters of the addition operator. For example, [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].

There's only one problem: snailfish numbers must always be reduced, and the process of adding two
snailfish numbers can result in snailfish numbers that need to be reduced.

To reduce a snailfish number, you must repeatedly do the first action in this list that applies to
the snailfish number:

- If any pair is nested inside four pairs, the leftmost such pair explodes.
- If any regular number is 10 or greater, the leftmost such regular number splits.

Once no action in the above list applies, the snailfish number is reduced.

During reduction, at most one action applies, after which the process returns to the top of the
list of actions. For example, if split produces a pair that meets the explode criteria, that pair
explodes before other splits occur.

To explode a pair, the pair's left value is added to the first regular number to the left of the
exploding pair (if any), and the pair's right value is added to the first regular number to the
right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers.
Then, the entire exploding pair is replaced with the regular number 0.

Here are some examples of a single explode action:

[[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]
(the 9 has no regular number to its left, so it is not added to any regular number).

[7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]
(the 2 has no regular number to its right, and so it is not added to any regular number).

[[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].

[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
(the pair [3,2] is unaffected because the pair [7,3] is further to the left;
 [3,2] would explode on the next action).

[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].

To split a regular number, replace it with a pair; the left element of the pair should be the
regular number divided by two and rounded down, while the right element of the pair should be the
regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6],
12 becomes [6,6], and so on.

Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

Once no reduce actions apply, the snailfish number that remains is the actual result of
the addition operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]].

The homework assignment involves adding up a list of snailfish numbers (your puzzle input).
The snailfish numbers are each listed on a separate line. Add the first snailfish number and
the second, then add that result and the third, then add that result and the fourth, and so
on until all numbers in the list have been used once.

For example, the final sum of this list is [[[[1,1],[2,2]],[3,3]],[4,4]]:

[1,1]
[2,2]
[3,3]
[4,4]

The final sum of this list is [[[[3,0],[5,3]],[4,4]],[5,5]]:

[1,1]
[2,2]
[3,3]
[4,4]
[5,5]

The final sum of this list is [[[[5,0],[7,4]],[5,5]],[6,6]]:

[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]

Here's a slightly larger example:

[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]

The final sum [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] is found after
adding up the above snailfish numbers:

  [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
+ [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
= [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

  [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
+ [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
= [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

  [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
+ [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
= [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

  [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
+ [7,[5,[[3,8],[1,4]]]]
= [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

  [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
+ [[2,[2,2]],[8,[8,1]]]
= [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

  [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
+ [2,9]
= [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

  [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
+ [1,[[[9,3],9],[[9,0],[0,7]]]]
= [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

  [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
+ [[[5,[7,4]],7],1]
= [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

  [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
+ [[[[4,2],2],6],[8,7]]
= [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

To check whether it's the right answer, the snailfish teacher only checks the magnitude of
the final sum. The magnitude of a pair is 3 times the magnitude of its left element plus 2
times the magnitude of its right element. The magnitude of a regular number is just that number.

For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9] is 3*1 + 2*9 = 21.
Magnitude calculations are recursive: the magnitude of [[9,1],[1,9]] is 3*29 + 2*21 = 129.

Here are a few more magnitude examples:

[[1,2],[[3,4],5]] becomes 143.
[[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
[[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
[[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
[[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.

So, given this example homework assignment:

[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]

The final sum is:

[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
The magnitude of this final sum is 4140.

Add up all of the snailfish numbers from the homework assignment in the order they appear.
What is the magnitude of the final sum?

To begin, get your puzzle input.

--- Part Two ---
You notice a second question on the back of the homework assignment:

What is the largest magnitude you can get from adding only two of the snailfish numbers?

Note that snailfish addition is not commutative - that is, x + y and y + x can produce different results.

Again considering the last example homework assignment above:

[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]

The largest magnitude of the sum of any two snailfish numbers in this list is 3993.

This is the magnitude of [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]] + [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
which reduces to [[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]].

What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?

    """


SAMPLE = []

with open('day_18_input.txt') as fp:
    INPUTS = [line.strip() for line in fp]


def add_ss(v, snail_seg, reverse=False):
    answer = snail_seg[::-1] if reverse else snail_seg
    for i, c in enumerate(answer):
        if c.isdigit():
            if reverse:
                digits = min(f'{answer[i:]},'.find(','), f'{answer[i:]}['.find('['))
                mirror_n = answer[i:i+digits]
                real_sum = str(v + int(mirror_n[::-1]))
                reversed_answer = f'{answer[:i]}{real_sum[::-1]}{answer[i+digits:]}'
                return reversed_answer[::-1]
            digits = min(f'{answer[i:]},'.find(','), f'{answer[i:]}]'.find(']'))
            return f'{answer[:i]}{v + int(answer[i:i+digits])}{answer[i+digits:]}'
    return snail_seg


def explode(snail):
    depth = 0
    for p in range(len(snail)):
        if snail[p] == ']':
            depth -= 1
        elif snail[p] == '[':
            depth += 1
            if depth > 4:
                l_str = snail[:p]
                regular_close = snail[p+1:].find(']')
                pair = snail[p+1:p+1+regular_close]
                r_str = snail[p+2+regular_close:]
                a, b = pair.split(',')
                if a.isdigit() and b.isdigit():
                    new_l_str = add_ss(int(a), l_str, True)
                    new_r_str = add_ss(int(b), r_str, False)
                    return True, f'{new_l_str}0{new_r_str}'
    return False, snail


def test_explode():
    assert explode('[[[[[9,8],1],2],3],4]') == (True, '[[[[0,9],2],3],4]')
    assert explode('[[[[[15,18],1],2],3],4]') == (True, '[[[[0,19],2],3],4]')
    assert explode('[7,[6,[5,[4,[3,2]]]]]') == (True, '[7,[6,[5,[7,0]]]]')
    assert explode('[[6,[5,[4,[3,2]]]],1]') == (True, '[[6,[5,[7,0]]],3]')
    assert explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]') \
           == (True, '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    assert explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]') \
           == (True, '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')


def split(snail):
    for i, c in enumerate(snail):
        if c.isdigit():
            digits = min(f'{snail[i:]},'.find(','), f'{snail[i:]}]'.find(']'))
            n = int(snail[i:i+digits])
            if n > 9:
                return True, f'{snail[:i]}[{n // 2},{(n + 1) // 2}]{snail[i+digits:]}'
    return False, snail


def test_split():
    assert split('[[[[0,7],4],[15,[0,13]]],[1,1]]') == (True, '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')


def reduce_snail(snail):
    next_snail = snail
    check_exploded = True
    while check_exploded:
        while check_exploded:
            check_exploded, next_snail = explode(next_snail)
        check_exploded, next_snail = split(next_snail)
    return next_snail


def test_reduce_snail():
    assert reduce_snail('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'


def add_snail(left, right):
    return reduce_snail(f'[{left},{right}]')


def test_add_snail():
    assert add_snail('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
    assert add_snail('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]', '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]') \
           == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'


def add_snail_list(snail_list):
    snail_sum = snail_list[0]
    for next_snail in snail_list[1:]:
        new_sum = add_snail(snail_sum, next_snail)
        snail_sum = new_sum
    return snail_sum


def test_add_snail_list():
    assert add_snail_list(['[1,1]', '[2,2]', '[3,3]', '[4,4]']) == '[[[[1,1],[2,2]],[3,3]],[4,4]]'
    assert add_snail_list(['[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                           '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                           '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                           '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                           '[7,[5,[[3,8],[1,4]]]]',
                           '[[2,[2,2]],[8,[8,1]]]',
                           '[2,9]',
                           '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                           '[[[5,[7,4]],7],1]',
                           '[[[[4,2],2],6],[8,7]]']) \
           == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'


def find_magnitude(snail):
    if snail.isdigit():
        return int(snail)
    depth = 0
    snail = snail[1:-1]
    for i, c in enumerate(snail):
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif c == ',' and depth == 0:
            left, right = snail[:i], snail[i+1:]
            return 3 * find_magnitude(left) + 2 * find_magnitude(right)


def test_find_magnitude():
    assert find_magnitude('[[1,2],[[3,4],5]]') == 143
    assert find_magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384
    assert find_magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445
    assert find_magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791
    assert find_magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137
    assert find_magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488


def test_submission():
    assert find_magnitude(add_snail_list(INPUTS)) == 4132
    assert max(find_magnitude(add_snail(a, b)) for a in INPUTS for b in INPUTS if a != b) == 4685
