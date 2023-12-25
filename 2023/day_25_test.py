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
        self.ordered_connections = set()
        self.first_node = None
        for raw_connection in raw_connections:
            node_a, raw_ends = raw_connection.split(": ")
            if self.first_node is None:
                self.first_node = node_a
            for node_b in raw_ends.split(" "):
                self.connects[node_a].add(node_b)
                self.connects[node_b].add(node_a)
                if node_a < node_b:
                    self.ordered_connections.add((node_a, node_b))
                else:
                    self.ordered_connections.add((node_b, node_a))

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
        # if len(self.connects) == len(visited):
        #     return True
        # return False
        return len(visited)

    def remove_in_triplicate(self):
        count = 0
        total_size = len(self.connects)
        for edge_a in self.ordered_connections:
            for edge_b in self.ordered_connections:
                if edge_b < edge_a:
                    continue
                for edge_c in self.ordered_connections:
                    if edge_c < edge_b:
                        continue
                    broken_connections = {edge_a, edge_b, edge_c}
                    connected_size = self.connected_size(broken_connections)
                    if connected_size != total_size:
                        return connected_size * (total_size - connected_size)
        return count


def test_graph():
    sample = Graph(SAMPLE)
    print(len(sample.connects))
    print(len(sample.ordered_connections))
    result = sample.remove_in_triplicate()
    assert result == 54

    puzzle_graph = Graph(RAW_INPUT)
    print(len(puzzle_graph.connects))
    print(len(puzzle_graph.ordered_connections))
    # result = puzzle_graph.remove_in_triplicate()
    # print(result)


test_graph()
