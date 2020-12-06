from collections import defaultdict

class Puzzle:
    """
    --- Day 4: Security Through Obscurity ---
    Finally, you come across an information kiosk with a list of rooms. Of course, the list is encrypted
    and full of decoy data, but the instructions to decode the list are barely hidden nearby.
    Better remove the decoy data first.

    Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash,
    a sector ID, and a checksum in square brackets.

    A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name,
    in order, with ties broken by alphabetization. For example:

    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3),
                                              and then a tie between x, y, and z, which are listed alphabetically.

    a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first
                                              five are listed alphabetically.

    not-a-real-room-404[oarel] is a real room.

    totally-real-room-200[decoy] is not.

    Of the real rooms from the list above, the sum of their sector IDs is 1514.

    What is the sum of the sector IDs of the real rooms?

    --- Part Two ---
    With all the decoy data out of the way, it's time to decrypt this list and get moving.

    The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right
    software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master
    cryptographer like yourself.

    To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's
    sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

    For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

    What is the sector ID of the room where North Pole objects are stored?
    """
    pass


with open('day_04_input.txt') as f:
    INPUTS = [line.strip() for line in f]


SAMPLES = ['aaaaa-bbb-z-y-x-123[abxyz]',
           'a-b-c-d-e-f-g-h-987[abcde]',
           'not-a-real-room-404[oarel]',
           'totally-real-room-200[decoy]']

def parse_encrypted(encrypted):
    a, b = encrypted.split('[')
    a = a.split('-')
    checksum = b[:-1]
    sector_id = int(a[-1])
    words = a[0:-1]
    letter_list = sorted(''.join(a))
    return sector_id, checksum, letter_list, words

def generate_frequency_string(letter_list):
    letter_current = letter_list[0]
    letter_count = 0
    frequency = defaultdict(str)
    for c in letter_list:
        if c == letter_current:
            letter_count += 1
        else:
            frequency[letter_count] += letter_current
            letter_current = c
            letter_count = 1
    frequency[letter_count] += letter_current
    return ''.join([s for (_, s) in sorted(frequency.items(), key=lambda x: -x[0])])


def shift_letter(c, amount):
    return chr((ord(c)-ord('a') + amount) % 26 + ord('a'))


def shift_word(word, amount):
    return ''.join([shift_letter(c, amount) for c in word])


def decode(encrypted):
    sector_id, _, _, words = parse_encrypted(encrypted)
    return ' '.join([shift_word(w, sector_id) for w in words])


def get_sector_id(encrypted: str) -> int:
    sector_id, checksum, letter_list, _ = parse_encrypted(encrypted)
    by_frequency = generate_frequency_string(letter_list)
    if checksum == by_frequency[:len(checksum)]:
        return sector_id
    return 0


def test_get_sector_id():
    assert sum([get_sector_id(w) for w in SAMPLES]) == 1514
    assert sum([get_sector_id(w) for w in INPUTS]) == 185371


def test_gecode():
    assert shift_letter('a',1) == 'b'
    assert shift_letter('z',1) == 'a'
    assert shift_letter('a',26) == 'a'
    assert shift_word('fdw',23) == 'cat'
    assert decode('qzmt-zixmtkozy-ivhz-343[asd]') == 'very encrypted name'
    for w in INPUTS:
        if decode(w) == 'northpole object storage':
            print(w)
            assert int(w.split('-')[3].split('[')[0]) == 984
