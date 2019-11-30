import re


class Puzzle:
    """
    --- Day 8: Matchsticks ---
    Space on the sleigh is limited this year, and so Santa will be bringing his list as a digital copy.
    He needs to know how much space it will take up when stored.

    It is common in many programming languages to provide a way to escape special characters in strings.
    For example, C, JavaScript, Perl, Python, and even PHP handle special characters in very similar ways.

    However, it is important to realize the difference between the number of characters in the code representation
    of the string literal and the number of characters in the in-memory string itself.

    For example:

    "" is 2 characters of code (the two double quotes), but the string contains zero characters.
    "abc" is 5 characters of code, but 3 characters in the string data.
    "aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single,
        escaped quote character, for a total of 7 characters in the string data.
    "\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('),
        escaped using hexadecimal notation.

    Santa's list is a file that contains many double-quoted string literals, one on each line.
    The only escape sequences used are
        \\ (which represents a single backslash),
        \" (which represents a lone double-quote character), and
        \xFF where FF are any two hexadecimal characters (which represents a single character with that ASCII code).

    Disregarding the whitespace in the file, what is the number of characters of code for string literals
    minus the number of characters in memory for the values of the strings in total for the entire file?

    For example, given the four strings above, the total number of characters of string code (2 + 5 + 10 + 6 = 23)
    minus the total number of characters in memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.
    """
    pass


def length(escaped_string):
    if escaped_string[0] != '"' or escaped_string[-1] != '"':
        raise SyntaxError(f'Invalid string {escaped_string}')
    escaped_string = escaped_string[1:-1]
    escape_mode = False
    hex_depth = 0
    total = 0
    for c in escaped_string:
        if hex_depth > 0:
            hex_depth -= 1
            continue
        if escape_mode:
            escape_mode = False
            if c == 'x':
                hex_depth = 2
                continue
            if c == '\\':
                continue
            if c == '"':
                continue
            raise SyntaxError(f'Invalid escape {c}')
        if c == '\\':
            escape_mode = True
        total += 1
    return total


def test_length():
    assert length(r'"hello"') == 5
    assert length(r'"\\g"') == 2
    assert length(r'"\\\\g"') == 3
    assert length(r'"v\xfb\"lgs\"kvjfywmut\x9cr"') == 18
    assert length(r'"porvg\x62qghorthnc\"\\"') == 17


def test_submission():
    file_total = 0
    mem_total = 0
    extra = 0
    with open('./input_day_8.txt', 'r') as fp:
        line = fp.readline().rstrip()
        while line:
            file_total += len(line)
            extra += (2 + line.count('\\') + line.count('"'))
            calc = length(line)
            mem_total += calc
            line = fp.readline().rstrip()
    assert (file_total - mem_total) == 1342
    assert extra == 2074
