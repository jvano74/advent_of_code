import re

def nice(word):
    """
    --- Day 5: Doesn't He Have Intern-Elves For This? ---
    Santa needs help figuring out which strings in his text file are naughty or nice.

    A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

    For example:

    ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...),
        a double letter (...dd...), and none of the disallowed substrings.
    aaa is nice because it has at least three vowels and a double letter,
        even though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

    How many strings are nice?
    """
    if re.match('.*(ab|cd|pq|xy)', word):
        return False
    if len(re.findall('(a|e|i|o|u)', word)) > 2:
        if re.match(r'.*(.){1}\1', word):
            return True
    return False

def test_nice():
    assert re.match(r'.*(.){1}\1', 'abb')
    assert nice('ugknbfddgicrmopn')
    assert nice('aaa')
    assert not(nice('jchzalrnumimnmhp'))
    assert not(nice('haegwjzuvuyypxyu'))
    assert not(nice('dvszwmarrgswjxmb'))

def test_wrapping_paper_sub():
    with open('./input_day_5.txt','r') as fp:
        total = 0
        line = fp.readline()
        while line:
            if nice(line):
                total += 1
            line = fp.readline()
    assert total == 238

def nice2(word):
    """
    --- Part Two ---
    Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice.
    None of the old rules apply, as they are all clearly ridiculous.

    Now, a nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy)
        or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe),
        or even aaa.

    For example:

    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly
        one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though
        the letters used by each rule overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

    How many strings are nice under these new rules?
    """
    if re.match(r'.*(..){1}.*\1', word):
        if re.match(r'.*(.){1}(.){1}\1', word):
            return True
    return False


def test_nice():
    assert re.match(r'.*(..){1}.*\1','xyxy')
    assert re.match(r'.*(..){1}.*\1','aabcdefgaa')
    assert not(re.match(r'.*(..){1}(.*)\1','aaa'))
    assert nice2('qjhvhtzxzqqjkmpb')
    assert nice2('xxyxx')
    assert not (nice2('uurcxstgmygtbstg'))
    assert not (nice2('ieodomkazucvgmuy'))


def test_wrapping_paper_sub():
    with open('./input_day_5.txt', 'r') as fp:
        total = 0
        line = fp.readline()
        while line:
            if nice2(line):
                total += 1
            line = fp.readline()
    assert total == 69

