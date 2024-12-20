from pathlib import Path
from collections import defaultdict
import re


class Puzzle:
    """
    --- Day 4: Repose Record ---
    You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab.
    You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab,
    so this is as close as you can safely get.

    As you search the closet for anything that might help, you discover that you're not the first person to
    want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few
    months secretly observing this guard post! They've been writing down the ID of the one guard on duty that
    night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as
    when they fall asleep or wake up while at their post (your puzzle input).

    For example, consider the following records, which have already been organized into chronological order:

    [1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up

    Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is
    always the one whose shift most recently started. Because all asleep/awake times are during the midnight
    hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

    Visually, these records show that the guards are asleep at these times:

    Date   ID   Minute
                000000000011111111112222222222333333333344444444445555555555
                012345678901234567890123456789012345678901234567890123456789
    11-01  #10  .....####################.....#########################.....
    11-02  #99  ........................................##########..........
    11-03  #10  ........................#####...............................
    11-04  #99  ....................................##########..............
    11-05  #99  .............................................##########.....

    The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on
    duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour.
    (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second
    row.) Awake is shown as ., and asleep is shown as #.

    Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they
    wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

    If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that
    guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing
    the best guard/minute combination.

    Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

    In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99
    only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas
    any other minute the guard was asleep was only seen on one day).

    While this example listed the entries in chronological order, your entries are in the order you found them.
    You'll need to organize them before they can be analyzed.

    What is the ID of the guard you chose multiplied by the minute you chose? (In the above example,
    the answer would be 10 * 24 = 240.)

    --- Part Two ---
    Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

    In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total.
    (In all other cases, any guard spent any minute asleep at most twice.)

    What is the ID of the guard you chose multiplied by the minute you chose? (In the above example,
    the answer would be 99 * 45 = 4455.)
    """

    pass


SAMPLE = [
    "[1518-11-01 00:00] Guard #10 begins shift",
    "[1518-11-01 00:05] falls asleep",
    "[1518-11-01 00:25] wakes up",
    "[1518-11-01 00:30] falls asleep",
    "[1518-11-01 00:55] wakes up",
    "[1518-11-01 23:58] Guard #99 begins shift",
    "[1518-11-02 00:40] falls asleep",
    "[1518-11-02 00:50] wakes up",
    "[1518-11-03 00:05] Guard #10 begins shift",
    "[1518-11-03 00:24] falls asleep",
    "[1518-11-03 00:29] wakes up",
    "[1518-11-04 00:02] Guard #99 begins shift",
    "[1518-11-04 00:36] falls asleep",
    "[1518-11-04 00:46] wakes up",
    "[1518-11-05 00:03] Guard #99 begins shift",
    "[1518-11-05 00:45] falls asleep",
    "[1518-11-05 00:55] wakes up",
]

with open(Path(__file__).parent / "2018_04_input.txt") as f:
    INPUTS = [line.strip() for line in f]


class Guard:
    """
    Sleepy guard
    """

    def __init__(self):
        self.sleep = [0 for _ in range(60)]

    def update_schedule(self, list_of_sleep_ranges):
        for sleep_range in list_of_sleep_ranges:
            for h in sleep_range:
                self.sleep[h] += 1

    def total_sleep(self):
        return sum(self.sleep)

    def most_sleepy(self, count=False):
        most_slept_min = 0
        most_slept_freq = 0
        for hr, times in enumerate(self.sleep):
            if times >= most_slept_freq:
                most_slept_freq = times
                most_slept_min = hr
        if count:
            return most_slept_freq
        return most_slept_min


def parse_to_day_format(schedule):
    list_of_days = []
    guard = ""
    for entry in schedule:
        min = int(entry[15:17])
        pattern_found = re.search("Guard #([0-9]*) begins shift$", entry)
        if pattern_found:
            if guard != "":
                list_of_days.append({guard: list_of_ranges})
            list_of_ranges = []
            fell_asleep = ""
            guard = int(pattern_found.group(1))
            # print(f'New day with guard {guard}')
        elif entry[19:31] == "falls asleep":
            fell_asleep = min
        elif entry[19:27] == "wakes up":
            if guard != "":
                list_of_ranges.append(range(fell_asleep, min))
            # print(f'Guard {guard} range({fell_asleep},{min}) ')
    if guard != "":
        list_of_days.append({guard: list_of_ranges})
    return list_of_days


def review_guards(day_format_schedule):
    guard_roster = defaultdict(Guard)
    for day in day_format_schedule:
        for guard in day:
            guard_roster[guard].update_schedule(day[guard])
    return guard_roster


def test_parse_to_day_format():
    assert parse_to_day_format(SAMPLE[:5]) == [{10: [range(5, 25), range(30, 55)]}]
    assert parse_to_day_format(SAMPLE) == [
        {10: [range(5, 25), range(30, 55)]},
        {99: [range(40, 50)]},
        {10: [range(24, 29)]},
        {99: [range(36, 46)]},
        {99: [range(45, 55)]},
    ], "{0} != stuff".format(parse_to_day_format(SAMPLE))


def stragety_1(raw_schedule):
    data = review_guards(parse_to_day_format(sorted(raw_schedule)))
    total_sleep = {g: data[g].total_sleep() for g in data}
    sleepiest_guard, max_sleep = max(total_sleep.items(), key=lambda x: x[1])
    return sleepiest_guard * data[sleepiest_guard].most_sleepy()


def stragety_2(raw_schedule):
    data = review_guards(parse_to_day_format(sorted(raw_schedule)))
    max_sleep = {g: data[g].most_sleepy(True) for g in data}
    sleepiest_guard, _ = max(max_sleep.items(), key=lambda x: x[1])
    print(max_sleep)
    print(
        sleepiest_guard,
        data[sleepiest_guard].most_sleepy(),
        data[sleepiest_guard].sleep,
    )
    return sleepiest_guard * data[sleepiest_guard].most_sleepy()


def test_review_guards():
    assert stragety_1(SAMPLE) == 240
    assert stragety_1(INPUTS) == 73646

    assert stragety_2(SAMPLE) == 4455
    assert stragety_2(INPUTS) == 4727
