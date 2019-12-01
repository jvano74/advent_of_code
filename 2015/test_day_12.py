import re
import json


def string_sum(string):
    """
    --- Day 12: JSAbacusFramework.io ---
    Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting
    software uses a peculiar storage format. That's where you come in.

    They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers,
    and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

    For example:

    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.
    You will not encounter any strings containing numbers.

    What is the sum of all numbers in the document?
    """
    return sum([int(d) for d in re.findall(r'-?\d+', string)])


def test_sum():
    assert string_sum('[1,2,3]') == 6
    assert string_sum('{"a":2,"b":4}') == 6
    assert string_sum('{"a":[-1,1]}') == 0
    assert string_sum('[-1,{"a":1}]') == 0
    assert string_sum('[]') == 0
    assert string_sum('{}') == 0


def test_submission():
    assert sum([string_sum(l) for l in open('input_day_12.txt', 'r')]) == 119433


def non_red_sum(string):
    """
    --- Part Two ---
    Uh oh - the Accounting-Elves have realized that they double-counted everything red.

    Ignore any object (and all of its children) which has any property with the value "red". Do this only for
    objects ({...}), not arrays ([...]).

    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.
    """
    return string_sum(remove_red(string))


def trim_right_to_bracket(string):
    cnt = 0
    pos = len(string) - 1
    string_array = list(string)
    while pos >= 0:
        if re.match(r'\d', string_array[pos]):
            string_array[pos] = '0'
        elif string_array[pos] == '{':
            cnt += 1
        elif string_array[pos] == '}':
            cnt -= 1
        if cnt == 1:
            break
        pos -= 1
    return ''.join(string_array)


def trim_left_to_bracket(string):
    cnt = 0
    pos = 0
    string_array = list(string)
    while pos < len(string_array):
        if re.match(r'\d', string_array[pos]):
            string_array[pos] = '0'
        elif string_array[pos] == '{':
            cnt += 1
        elif string_array[pos] == '}':
            cnt -= 1
        if cnt == -1:
            break
        pos += 1
    # return string[pos:]
    return ''.join(string_array)


def remove_red(string):
    pieces = re.split(r':"red"', string, maxsplit=1)
    if len(pieces) == 1:
        return pieces[0]
    non_red = ''
    while len(pieces) > 1:
        non_red += trim_right_to_bracket(pieces[0]) + ':"red"'
        pieces = re.split(r':"red"', trim_left_to_bracket(pieces[1]), maxsplit=1)
    non_red += pieces[0]
    return non_red


def test_remove_red():
    assert remove_red('[1,2,3]') == '[1,2,3]'
    assert remove_red('[1,"red",5]') == '[1,"red",5]'
    assert remove_red('[1,{"c":"red","b":2},3]') == '[1,{"c":"red","b":0},3]'
    assert remove_red('{"d":"red","e":[1,2,3,4],"f":5}') == '{"d":"red","e":[0,0,0,0],"f":0}'
    assert remove_red('[1,{"b":2,"bb":{"m":8},"c":"red",{"d":3}},3]') == '[1,{"b":0,"bb":{"m":0},"c":"red",{"d":0}},3]'
    assert remove_red('[1,{"b":2,"cc":"red","bb":{"m":8},"c":"red",{"d":3}},3]') == '[1,{"b":0,"cc":"red","bb":{' \
                                                                                    '"m":0},"c":"red",{"d":0}},3] '


def test_remove_red_submission():
    assert [remove_red(l) for l in open('input_day_12.txt', 'r')] == []


def test_submission2():
    assert sum([non_red_sum(l) for l in open('input_day_12.txt', 'r')]) == 77651


# ===== SOLUTION FROM REDDIT =====
# Still not sure where my more manual solution above is going astray...

def sum_object(obj):
    if type(obj) is int:
        return obj

    if type(obj) is list:
        return sum(map(sum_object, obj))

    if type(obj) is dict:
        vals = obj.values()

        # remove these two lines for part one
        if "red" in vals:
            return 0

        return sum(map(sum_object, vals))

    else:
        return 0


def test_from_redit():
    with open("input_day_12.txt") as f:
        obj = json.loads(f.read())
        assert sum_object(obj) == 68466
