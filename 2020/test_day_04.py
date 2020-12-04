from __future__ import annotations
from typing import NamedTuple
import re

def day04():
    """
    --- Day 4: Passport Processing ---

    You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport.
    While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore
    aren't actually valid documentation for travel in most of the world.

    It seems like you're not the only one having problems, though; a very long line has formed for the automatic
    passport scanners, and the delay could upset your travel itinerary.

    Due to some questionable network security, you realize you might be able to solve both of these problems at
    the same time.

    The automatic passport scanners are slow because they're having trouble detecting which passports have
    all required fields. The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

    Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of
    key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

    Here is an example batch file containing four passports:

    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in

    The first passport is valid - all eight fields are present. The second passport is invalid - it is
    missing hgt (the Height field).

    The third passport is interesting; the only missing field is cid, so it looks like data from North
    Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily
    ignore missing cid fields. Treat this "passport" as valid.

    The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other
    field is not, so this passport is invalid.

    According to the above rules, your improved system would report 2 valid passports.

    Count the number of valid passports - those that have all required fields. Treat cid as optional.
    In your batch file, how many passports are valid?
    """

SAMPLE = [
    'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
    'byr:1937 iyr:2017 cid:147 hgt:183cm',
    '',
    'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
    'hcl:#cfa07d byr:1929',
    '',
    'hcl:#ae17e1 iyr:2013',
    'eyr:2024',
    'ecl:brn pid:760753108 byr:1931',
    'hgt:179cm',
    '',
    'hcl:#cfa07d eyr:2025 pid:166559648',
    'iyr:2011 ecl:brn hgt:59in'
   ]

SAMPLE_AS_DICT = [
    {
        'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd', 'byr': '1937',
        'iyr': '2017', 'cid': '147', 'hgt': '183cm',
     },
    {
        'iyr': '2013', 'ecl': 'amb', 'cid':'350', 'eyr':'2023', 'pid':'028048884',
        'hcl':'#cfa07d', 'byr':'1929',
    },
    {
        'hcl': '#ae17e1', 'iyr': '2013', 'eyr':'2024', 'ecl':'brn', 'pid':'760753108',
        'byr':'1931', 'hgt':'179cm',
    },
    {
        'hcl': '#cfa07d', 'eyr': '2025', 'pid':'166559648', 'iyr':'2011', 'ecl':'brn', 'hgt':'59in',
    }
   ]

SAMPLE_INVALID_ENHANCED = [
    'eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
    '',
    'iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946'
    '',
    'hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277'
    '',
    'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007'
]

SAMPLE_VALID_ENHANCED = [
    'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f',
    '',
    'eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
    '',
    'hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022',
    '',
    'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'
    ]

with open('input_day_04.txt') as f:
    INPUTS = [line.strip() for line in f]

class EnhancedPassport(NamedTuple):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str

    def is_valid(self):
        try:
            if not (1920 <= int(self.byr) <= 2002):
                raise Exception('Invalid Birth Year')
            if not (2010 <= int(self.iyr) <= 2020):
                raise Exception('Invalid Issue Year')
            if not (2020 <= int(self.eyr) <= 2030) :
                raise Exception('Invalid Expiration Year')
            ht_units = self.hgt[-2:]
            if not (ht_units == 'cm' or ht_units == 'in'):
                raise Exception('Invalid Height Units')
            ht = int(self.hgt[:-2])
            if ht_units == 'cm' and not ( 150 <= ht <= 193):
                raise Exception('Invalid Height')
            if ht_units == 'in' and not ( 59 <= ht <= 76):
                raise Exception('Invalid Height')
            if not re.match(r'^\#[0-9a-f]{6}$',self.hcl):
                raise Exception('Invalid Hair Color')
            if not (self.ecl in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])):
                raise Exception('Invalid Eye Color')
            if not (len(self.pid) == 9 and int(self.pid) >= 0):
                raise Exception('Invalid Passport ID')
        except:
            return False
        else:
            return True

    @staticmethod
    def from_dict(basic_passport: dict) -> EnhancedPassport:
        return EnhancedPassport(
                basic_passport.get('byr',''),
                basic_passport.get('iyr',''),
                basic_passport.get('eyr',''),
                basic_passport.get('hgt',''),
                basic_passport.get('hcl',''),
                basic_passport.get('ecl',''),
                basic_passport.get('pid',''))


def parse_input(input_array):
    passports = []
    passport = {}
    for line in input_array:
        if line == '' and passport != {}:
            passports.append(passport)
            passport = {}
        else:
            for key_value in line.split():
                key, value = key_value.split(':')
                passport[key] = value
    if passport != {}:
        passports.append(passport)
    return passports


def validate_passport(passport: dict) -> bool:
    required_fields = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    ]

    for key in required_fields:
        if key not in passport:
            return False
    return True


def test_parse_input():
    resulting_sample_as_dict = parse_input(SAMPLE)
    assert resulting_sample_as_dict[0] == SAMPLE_AS_DICT[0]
    assert resulting_sample_as_dict[1] == SAMPLE_AS_DICT[1]
    assert resulting_sample_as_dict[2] == SAMPLE_AS_DICT[2]
    assert resulting_sample_as_dict[3] == SAMPLE_AS_DICT[3]


def test_validate_passport():
    assert validate_passport(SAMPLE_AS_DICT[0])
    assert not validate_passport(SAMPLE_AS_DICT[1])

def test_part_1():
    assert sum([validate_passport(passport) for passport in parse_input(INPUTS)]) == 204

def test_part_2():
    valid_as_dict = parse_input(SAMPLE_VALID_ENHANCED)
    invalid_as_dict = parse_input(SAMPLE_INVALID_ENHANCED)
    assert not EnhancedPassport.from_dict(invalid_as_dict[0]).is_valid()
    assert sum([EnhancedPassport.from_dict(passport).is_valid() for passport in invalid_as_dict]) == 0
    assert EnhancedPassport.from_dict(valid_as_dict[0]).is_valid()
    assert sum([EnhancedPassport.from_dict(passport).is_valid() for passport in valid_as_dict]) == len(valid_as_dict)
    assert sum([EnhancedPassport.from_dict(passport).is_valid() for passport in parse_input(INPUTS)]) == 1

