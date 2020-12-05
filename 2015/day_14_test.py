import re


class Reindeer:
    """
    --- Day 14: Reindeer Olympics ---
    This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover
    their energy. Santa would like to know which of his reindeer is fastest, and so he has them race.

    Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend
    whole seconds in either state.

    For example, suppose you have the following Reindeer:

    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

    After one second, Comet has gone 14 km, while Dancer has gone 16 km.
    After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km.
    On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on
    for a total distance of 176 km.
    On the 12th second, both reindeer are resting.
    They continue to rest until the 138th second, when Comet flies for another ten seconds.
    On the 174th second, Dancer flies for another 11 seconds.

    In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead
    at 1120 km (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win
    (if the race ended at 1000 seconds).

    Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds,
    what distance has the winning reindeer traveled?
    """

    def __init__(self, rate, run, rest):
        self.rate = int(rate)
        self.run = int(run)
        self.rest = int(rest)

    def clock(self):
        _distance = 0
        _run = self.run
        _rest = 0
        while True:
            if _rest > 0:
                _rest -= 1
                if _rest == 0:
                    _run = self.run
            elif _run > 0:
                _distance += self.rate
                _run -= 1
                if _run == 0:
                    _rest = self.rest
            yield _distance


def test_stuff():
    comet = Reindeer(14, 10, 127)
    dancer = Reindeer(16, 11, 162)
    racers = [comet.clock(), dancer.clock()]
    race = [next(zip(*racers)) for _ in range(1000)]
    assert race[0] == (14, 16)
    assert race[9] == (140, 160)
    assert race[10] == (140, 176)
    assert race[11] == race[10]
    assert race[11] == race[136]
    assert race[999] == (1120, 1056)


def test_submission():
    max_time = 2503
    reindeer = {re.split(' ', ln)[0]: Reindeer(*re.findall(r'\d+', ln)) for ln in open('day_14_input.txt', 'r')}
    assert len(reindeer) == 9
    race = {}
    final_distances = []
    for name in reindeer:
        name_clock = reindeer[name].clock()
        name_race = [next(name_clock) for _ in range(max_time)]
        race[name] = name_race
        final_distances.append(name_race[-1])
    assert max(final_distances) == 2696

class Race:
    """
    --- Part Two ---
    Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

    Instead, at the end of each second, he awards one point to the reindeer currently in the lead.
    (If there are multiple reindeer tied for the lead, they each get one point.) He keeps the traditional
    2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

    Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point.
    He stays in the lead until several seconds into Comet's second burst: after the 140th second, Comet pulls
    into the lead and gets his first point. Of course, since Dancer had been in the lead for the 139 seconds
    before that, he has accumulated 139 points by the 140th second.

    After the 1000th second, Dancer has accumulated 689 points, while poor Comet, our old champion, only has 312.
    So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

    Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, how many
    points does the winning reindeer have?
    """

    def __init__(self):
        self.max_time = 2503
        self.reindeer = {re.split(' ', ln)[0]: Reindeer(*re.findall(r'\d+', ln)) for ln in open('day_14_input.txt', 'r')}

    def runners_take_your_marks(self):
        self.score = {name: 0 for name in self.reindeer}
        self.track = {name: self.reindeer[name].clock() for name in self.reindeer}

    def go(self):
        for time in range(self.max_time):
            snapshot = { name: next(self.track[name]) for name in self.track}
            front = max(snapshot.values())
            for name in snapshot:
                if snapshot[name] == front:
                    self.score[name] += 1
        return max(self.score.values())


def test_new_race():
    race = Race()
    race.runners_take_your_marks()
    assert race.go() == 1084
