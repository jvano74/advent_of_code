from collections import defaultdict


class Puzzle:
    """
    --- Day 25: Snowverload ---
    Still somehow without snow, you go to the last place you haven't checked:
    the center of Snow Island, directly below the waterfall.

    Here, someone has clearly been trying to fix the problem. Scattered
    everywhere are hundreds of weather machines, almanacs, communication
    modules, hoof prints, machine parts, mirrors, lenses, and so on.

    Somehow, everything has been wired together into a massive snow-producing
    apparatus, but nothing seems to be running. You check a tiny screen on one
    of the communication modules: Error 2023. It doesn't say what Error 2023
    means, but it does have the phone number for a support line printed on it.

    "Hi, you've reached Weather Machines And So On, Inc. How can I help you?"
    You explain the situation.

    "Error 2023, you say? Why, that's a power overload error, of course! It
    means you have too many components plugged in. Try unplugging some
    components and--" You explain that there are hundreds of components here and
    you're in a bit of a hurry.

    "Well, let's see how bad it is; do you see a big red reset button somewhere?
    It should be on its own module. If you push it, it probably won't fix
    anything, but it'll report how overloaded things are." After a minute or
    two, you find the reset button; it's so big that it takes two hands just to
    get enough leverage to push it. Its screen then displays:

    SYSTEM OVERLOAD!

    Connected components would require
    power equal to at least 100 stars!

    "Wait, how many components did you say are plugged in? With that much
    equipment, you could produce snow for an entire--" You disconnect the call.

    You have nowhere near that many stars - you need to find a way to disconnect
    at least half of the equipment here, but it's already Christmas! You only
    have time to disconnect three wires.

    Fortunately, someone left a wiring diagram (your puzzle input) that shows
    how the components are connected. For example:

    jqt: rhn xhk nvd
    rsh: frs pzl lsr
    xhk: hfx
    cmg: qnr nvd lhk bvb
    rhn: xhk bvb hfx
    bvb: xhk hfx
    pzl: lsr hfx nvd
    qnr: nvd
    ntq: jqt hfx bvb xhk
    nvd: lhk
    lsr: lhk
    rzs: qnr cmg lsr rsh
    frs: qnr lhk lsr

    Each line shows the name of a component, a colon, and then a list of other
    components to which that component is connected. Connections aren't
    directional; abc: xyz and xyz: abc both represent the same configuration.
    Each connection between two components is represented only once, so some
    components might only ever appear on the left or right side of a colon.

    In this example, if you disconnect the wire between hfx/pzl, the wire
    between bvb/cmg, and the wire between nvd/jqt, you will divide the
    components into two separate, disconnected groups:

    9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
    6 components: bvb, hfx, jqt, ntq, rhn, and xhk.

    Multiplying the sizes of these groups together produces 54.

    Find the three wires you need to disconnect in order to divide the
    components into two separate groups. What do you get if you multiply the
    sizes of these two groups together?

    Your puzzle answer was 554064.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    You climb over weather machines, under giant springs, and narrowly avoid a
    pile of pipes as you find and disconnect the three wires.

    A moment after you disconnect the last wire, the big red reset button module
    makes a small ding noise:

    System overload resolved!
    Power required is now 50 stars.

    Out of the corner of your eye, you notice goggles and a loose-fitting hard
    hat peeking at you from behind an ultra crucible. You think you see a faint
    glow, but before you can investigate, you hear another small ding:

    Power required is now 49 stars.

    Please supply the necessary stars and
    push the button to restart the system.
    """


SAMPLE = [
    "jqt: rhn xhk nvd",
    "rsh: frs pzl lsr",
    "xhk: hfx",
    "cmg: qnr nvd lhk bvb",
    "rhn: xhk bvb hfx",
    "bvb: xhk hfx",
    "pzl: lsr hfx nvd",
    "qnr: nvd",
    "ntq: jqt hfx bvb xhk",
    "nvd: lhk",
    "lsr: lhk",
    "rzs: qnr cmg lsr rsh",
    "frs: qnr lhk lsr",
]

with open("day_25_input.txt") as fp:
    RAW_INPUT = fp.read().split("\n")


class Graph:
    def __init__(self, raw_connections) -> None:
        self.connects = defaultdict(set)
        self.ordered_connections = dict()
        self.first_node = None
        for raw_connection in raw_connections:
            node_a, raw_ends = raw_connection.split(": ")
            if self.first_node is None:
                self.first_node = node_a
            for node_b in raw_ends.split(" "):
                self.connects[node_a].add(node_b)
                self.connects[node_b].add(node_a)
                if node_a < node_b:
                    self.ordered_connections[(node_a, node_b)] = 0
                else:
                    self.ordered_connections[(node_b, node_a)] = 0

    def connected_size(self, broken_connections, start_node=None):
        if start_node is None:
            start_node = self.first_node
        boundary = [start_node]
        visited = {
            start_node,
        }
        while boundary:
            test_node = boundary.pop(0)
            for next_node in self.connects[test_node]:
                if next_node not in visited:
                    if test_node < next_node:
                        node_a = test_node
                        node_b = next_node
                    else:
                        node_b = test_node
                        node_a = next_node
                    if (node_a, node_b) not in broken_connections:
                        visited.add(next_node)
                        boundary.append(next_node)
        return len(visited)

    def order_connections(self):
        total = len(self.connects.keys())
        values = sum(self.ordered_connections.values())
        if values == 0:
            print(f"Calculating edge weights for {total} edges.")
            for n, start_node in enumerate(self.connects.keys()):
                boundary = [start_node]
                visited = {
                    start_node,
                }
                while boundary:
                    test_node = boundary.pop(0)
                    for next_node in self.connects[test_node]:
                        if next_node not in visited:
                            if test_node < next_node:
                                node_a = test_node
                                node_b = next_node
                            else:
                                node_b = test_node
                                node_a = next_node
                            visited.add(next_node)
                            boundary.append(next_node)
                            self.ordered_connections[(node_a, node_b)] += 1
                if n % 1000 == 0:
                    print(f"{n}/{total}")
            print(f"{n}/{total} --- all edge weights calculated")
        return [
            k for _, k in sorted((-v, k) for k, v in self.ordered_connections.items())
        ]

    def remove_in_triplicate(self):
        total_size = len(self.connects)
        ordered_connections = self.order_connections()
        for edge_a in ordered_connections:
            for edge_b in ordered_connections:
                if edge_b < edge_a:
                    continue
                for edge_c in ordered_connections:
                    if edge_c < edge_b:
                        continue
                    broken_connections = {edge_a, edge_b, edge_c}
                    connected_size = self.connected_size(broken_connections)
                    if connected_size != total_size:
                        print(f"{broken_connections=}")
                        return connected_size, (total_size - connected_size)
        return total_size, 0


def test_graph():
    sample = Graph(SAMPLE)
    # print(len(sample.connects))
    # print(len(sample.ordered_connections))
    result = sample.remove_in_triplicate()
    assert result[0] * result[1] == 54

    # print("Starting full puzzle input.")
    puzzle_graph = Graph(RAW_INPUT)
    # Calculating edge weights for 1490 edges.
    # 1489/1490 --- all edge weights calculated
    # ('kzx', 'qmr')=1488
    # ('jff', 'zns')=1486
    # ('fts', 'nvb')=1477
    # ('lzg', 'qfh')=1150
    # ('rxc', 'tzd')=1147
    # ('rxc', 'vmb')=1146
    # ('fhv', 'qzr')=1136
    # ('pgr', 'xxs')=1134
    # ('jff', 'vht')=1130
    # ('fvm', 'hbx')=1129
    # for i, k in enumerate(puzzle_graph.order_connections()):
    #    if i < 10:
    #        print(f"{k}={puzzle_graph.ordered_connections[k]}")
    # print(len(puzzle_graph.connects))
    # print(len(puzzle_graph.ordered_connections))
    result = puzzle_graph.remove_in_triplicate()
    # broken_connections={('kzx', 'qmr'), ('jff', 'zns'), ('fts', 'nvb')}
    # print(result)
    # (776, 714)
    assert result[0] * result[1] == 554064


test_graph()
