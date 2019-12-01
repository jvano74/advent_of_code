import re


def new_password(pwd):
    """
    --- Day 11: Corporate Policy ---
    Santa's previous password expired, and he needs help choosing a new one.

    To help him remember his new password after the old one expires, Santa has devised a method of coming up with
    a password based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase
    letters (for security reasons), so he finds his new password by incrementing his old password string repeatedly
    until it is valid.

    Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter
    one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't
    wrap around.

    Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password
    requirements:

    Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on,
    up to xyz. They cannot skip letters; abd doesn't count.

    Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters
    and are therefore confusing.

    Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

    For example:

    hijklmmn meets the first requirement (because it contains the straight hij) but fails the second
        requirement requirement (because it contains i and l).
    abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
    abbcegjk fails the third requirement, because it only has one double letter (bb).

    The next password after abcdefgh is abcdffaa.
    The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start
        with ghi..., since i is not allowed.

    Given Santa's current password (your puzzle input), what should his next password be?

    Your puzzle input is vzbxkghb.
    """
    new_pwd = incrament(pwd)
    while not is_pwd_valid(new_pwd):
        new_pwd = incrament(new_pwd)
    return new_pwd


def incrament(pwd):
    tail = 1
    while pwd[-tail] == 'z':
        tail += 1
        if tail == 1 + len(pwd):
            return 'a' * len(pwd)
    return pwd[:-tail] + chr(ord(pwd[-tail]) + 1) + ('a' * (tail-1))


def has_straight(pwd):
    run = 1
    next = chr(ord(pwd[0]) + 1)
    for c in pwd[1:]:
        if c == next:
            run += 1
            if run == 3:
                return True
        else:
            run = 1
        next = chr(ord(c) + 1)
    return False


def is_pwd_valid(pwd):
    if re.match(r'.*[iol]', pwd):
        return False
    doubles = re.findall(r'(.)\1', pwd)
    if doubles:
        if len(set(doubles)) < 2:
            return False
        if has_straight(pwd):
            return True
    return False


def test_new_password():
    assert incrament('aaa') == 'aab'
    assert incrament('abb') == 'abc'
    assert incrament('abz') == 'aca'
    assert incrament('czz') == 'daa'
    assert incrament('zzzz') == 'aaaa'
    assert has_straight('abceef') == True
    assert has_straight('abbcdd') == True
    assert has_straight('abbccdd') == False
    assert is_pwd_valid('aia') == False
    assert is_pwd_valid('hijklmmn') == False
    assert is_pwd_valid('abbceffg') == False
    assert is_pwd_valid('abbcegjk') == False
    assert new_password('abcdefgh') == 'abcdffaa'
    assert new_password('ghijklmn') == 'ghjaabcc'

def test_submission():
    assert new_password('vzbxkghb') == 'vzbxxyzz'
    assert new_password('vzbxxyzz') == 'vzcaabcc'

