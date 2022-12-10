import numpy as np
import re


class Lights:
    """
    --- Day 6: Probably a Fire Hazard ---
    Because your neighbors keep defeating you in the holiday house decorating
    contest year after year, you've decided to deploy one million lights in a
    1000x1000 grid.

    Furthermore, because you've been especially nice this year, Santa has mailed
    you instructions on how to display the ideal lighting configuration.

    Lights in your grid are numbered from 0 to 999 in each direction; the lights
    at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions
    include whether to turn on, turn off, or toggle various inclusive ranges
    given as coordinate pairs. Each coordinate pair represents opposite corners
    of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore
    refers to 9 lights in a 3x3 square. The lights all start turned off.

    To defeat your neighbors this year, all you have to do is set up your lights
    by doing the instructions Santa sent you in order.

    For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
        turning off the ones that were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle
    four lights.

    After following the instructions, how many lights are lit?
    """

    grid = np.zeros((1000, 1000), dtype=int)

    def f_on(self, x):
        return 1

    def f_off(self, x):
        return 0

    def f_toggle(self, x):
        return 1 - x

    def count(self):
        return sum(sum(self.grid))

    def on(self, ul, lr):
        for x in range(ul[0], lr[0] + 1):
            for y in range(ul[1], lr[1] + 1):
                self.grid[x][y] = self.f_on(self.grid[x][y])

    def off(self, ul, lr):
        for x in range(ul[0], lr[0] + 1):
            for y in range(ul[1], lr[1] + 1):
                self.grid[x][y] = self.f_off(self.grid[x][y])

    def toggle(self, ul, lr):
        for x in range(ul[0], lr[0] + 1):
            for y in range(ul[1], lr[1] + 1):
                self.grid[x][y] = self.f_toggle(self.grid[x][y])

    def execute_direction(self, direction):
        m = re.match(
            r"(?P<action>turn on|turn off|toggle) (?P<start_x>\d+),(?P<start_y>\d+) through (?P<end_x>\d+),(?P<end_y>\d+)",
            direction,
        )
        if m:
            ul = (int(m.group("start_x")), int(m.group("start_y")))
            lr = (int(m.group("end_x")), int(m.group("end_y")))
            if m.group("action") == "toggle":
                self.toggle(ul, lr)
            elif m.group("action") == "turn off":
                self.off(ul, lr)
            elif m.group("action") == "turn on":
                self.on(ul, lr)

    def execute_directions(self):
        with open("./input_day_6.txt", "r") as fp:
            line = fp.readline()
            while line:
                self.execute_direction(line)
                line = fp.readline()


def test_lights():
    lights = Lights()
    assert lights.count() == 0
    lights.on((0, 0), (3, 5))
    assert lights.count() == 24
    lights.off((1, 1), (2, 2))
    assert lights.count() == 20
    lights.toggle((0, 0), (1, 1))
    assert lights.count() == 18
    lights.off((0, 0), (999, 999))
    assert lights.count() == 0
    lights.execute_direction("turn on 0,0 through 3,5")
    assert lights.count() == 24


def test_submit():
    lights = Lights()
    lights.execute_directions()
    assert lights.count() == 543903


class NewLights(Lights):
    pass

    def f_on(self, x):
        return x + 1

    def f_off(self, x):
        return max(x - 1, 0)

    def f_toggle(self, x):
        return x + 2


def test_new_lights():
    lights = NewLights()
    lights.execute_directions()
    assert lights.count() == 14687245
