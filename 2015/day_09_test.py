from typing import List, NamedTuple
from collections import deque, defaultdict
from heapq import heappush, heappop


class Puzzle:
    """
    --- Day 9: All in a Single Night ---
    Every year, Santa manages to deliver all of his presents in a single night.

    This year, however, he has some new locations to visit; his elves have provided him the distances between
    every pair of locations. He can start and end at any two (different) locations he wants, but he must visit
    each location exactly once. What is the shortest distance he can travel to achieve this?

    For example, given the following distances:

    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    The possible routes are therefore:

    Dublin -> London -> Belfast = 982
    London -> Dublin -> Belfast = 605
    London -> Belfast -> Dublin = 659
    Dublin -> Belfast -> London = 659
    Belfast -> Dublin -> London = 605
    Belfast -> London -> Dublin = 982

    The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

    What is the distance of the shortest route?
    """

class City:
    def __init__(self):
        self.neighbors = defaultdict(int)


class Map:
    def __init__(self, distances: List):
        self.cities = defaultdict(City)

        for line in distances:
            city1, _, city2, _, distance = line.split(' ')
            self.cities[city1].neighbors[city2] = int(distance)
            self.cities[city2].neighbors[city1] = int(distance)

    def shortest_distance(self) -> List:
        city_count = len(self.cities)
        frontier = []

        for cityName in self.cities:
            heappush(frontier, (0, cityName, [cityName]))

        routes = []

        while frontier:
            dist, city, path_hx = heappop(frontier)
            for nn in self.cities[city].neighbors:
                if nn not in path_hx:
                    new_dist = dist + self.cities[city].neighbors[nn]
                    new_hx = path_hx[:]
                    new_hx.append(nn)
                    if len(new_hx) == city_count:
                        heappush(routes,(new_dist, new_hx))
                    heappush(frontier, (new_dist, nn, new_hx))
        return heappop(routes)

    def longest_distance(self) -> List:
        city_count = len(self.cities)
        frontier = []

        for cityName in self.cities:
            heappush(frontier, (0, cityName, [cityName]))

        routes = []

        while frontier:
            dist, city, path_hx = heappop(frontier)
            for nn in self.cities[city].neighbors:
                if nn not in path_hx:
                    new_dist = dist - self.cities[city].neighbors[nn]
                    new_hx = path_hx[:]
                    new_hx.append(nn)
                    if len(new_hx) == city_count:
                        heappush(routes,(new_dist, new_hx))
                    heappush(frontier, (new_dist, nn, new_hx))
        return heappop(routes)


with open('input_day_09.txt') as fp:
    SUBMISSION = fp.read()


def test_map():
    map = Map(['London to Dublin = 464',
               'London to Belfast = 518',
               'Dublin to Belfast = 141'])
    assert set(map.cities.keys()) == set(['London', 'Dublin', 'Belfast'])
    assert map.shortest_distance()[0] == 605
    assert map.longest_distance()[0] == -982

def test_submission():
    my_map = Map([dist.strip() for dist in SUBMISSION.split('\n')])
    assert set(my_map.cities.keys()) == set(['AlphaCentauri', 'Arbre',
                                             'Faerun', 'Norrath',
                                             'Snowdin', 'Straylight',
                                             'Tambi', 'Tristram'])
    assert my_map.shortest_distance()[0] == 251
    assert my_map.longest_distance()[0] == -898
