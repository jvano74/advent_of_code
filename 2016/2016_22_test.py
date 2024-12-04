from pathlib import Path
from typing import NamedTuple
from queue import PriorityQueue
import re


class Puzzle:
    """
    --- Day 22: Grid Computing ---
    You gain access to a massive storage cluster arranged in a grid; each storage node is only connected to the four
    nodes directly adjacent to it (three if the node is on an edge, two if it's in a corner).

    You can directly access data only on node /dev/grid/node-x0-y0, but you can perform some limited actions on the
    other nodes:

    - You can get the disk usage of all nodes (via df). The result of doing this is in your puzzle input.
    - You can instruct a node to move (not copy) all of its data to an adjacent node (if the destination node
      has enough space to receive the data). The sending node is left empty after this operation.

    Nodes are named by their position: the node named node-x10-y10 is adjacent to
    nodes node-x9-y10, node-x11-y10, node-x10-y9, and node-x10-y11.

    Before you begin, you need to understand the arrangement of data on these nodes. Even though you can only move
    data between directly connected nodes, you're going to need to rearrange a lot of the data to get access to the
    data you need. Therefore, you need to work out how you might be able to shift data around.

    To do this, you'd like to count the number of viable pairs of nodes. A viable pair is any two nodes (A,B),
    regardless of whether they are directly connected, such that:

    - Node A is not empty (its Used is not zero).
    - Nodes A and B are not the same node.
    - The data on node A (its Used) would fit on node B (its Avail).

    How many viable pairs of nodes are there?

    --- Part Two ---
    Now that you have a better understanding of the grid, it's time to get to work.

    Your goal is to gain access to the data which begins in the node with y=0 and the highest x (that is, the
    node in the top-right corner).

    For example, suppose you have the following grid:

    Filesystem            Size  Used  Avail  Use%
    /dev/grid/node-x0-y0   10T    8T     2T   80%
    /dev/grid/node-x0-y1   11T    6T     5T   54%
    /dev/grid/node-x0-y2   32T   28T     4T   87%
    /dev/grid/node-x1-y0    9T    7T     2T   77%
    /dev/grid/node-x1-y1    8T    0T     8T    0%
    /dev/grid/node-x1-y2   11T    7T     4T   63%
    /dev/grid/node-x2-y0   10T    6T     4T   60%
    /dev/grid/node-x2-y1    9T    8T     1T   88%
    /dev/grid/node-x2-y2    9T    6T     3T   66%

    In this example, you have a storage grid 3 nodes wide and 3 nodes tall. The node you can access directly,
    node-x0-y0, is almost full. The node containing the data you want to access, node-x2-y0 (because it has y=0
    and the highest x value), contains 6 terabytes of data - enough to fit on your node, if only you could make
    enough space to move it there.

    Fortunately, node-x1-y1 looks like it has enough free space to enable you to move some of this data around.
    In fact, it seems like all of the nodes have enough space to hold any node's data (except node-x0-y2, which
    is much larger, very full, and not moving any time soon). So, initially, the grid's capacities and connections
    look like this:

    ( 8T/10T) --  7T/ 9T -- [ 6T/10T]
        |           |           |
      6T/11T  --  0T/ 8T --   8T/ 9T
        |           |           |
     28T/32T  --  7T/11T --   6T/ 9T

    The node you can access directly is in parentheses; the data you want starts in the node marked by square
    brackets.

    In this example, most of the nodes are interchangable: they're full enough that no other node's data would
    fit, but small enough that their data could be moved around. Let's draw these nodes as .. The exceptions are
    the empty node, which we'll draw as _, and the very large, very full node, which we'll draw as #. Let's also
    draw the goal data as G. Then, it looks like this:

    (.) .  G
     .  _  .
     #  .  .

    The goal is to move the data in the top right, G, to the node in parentheses. To do this, we can issue some
    commands to the grid and rearrange the data:

    Move data from node-y0-x1 to node-y1-x1, leaving node node-y0-x1 empty:

    (.) _  G
     .  .  .
     #  .  .

    Move the goal data from node-y0-x2 to node-y0-x1:

    (.) G  _
     .  .  .
     #  .  .

    At this point, we're quite close. However, we have no deletion command, so we have to move some more data around.
    So, next, we move the data from node-y1-x2 to node-y0-x2:

    (.) G  .
     .  .  _
     #  .  .

    Move the data from node-y1-x1 to node-y1-x2:

    (.) G  .
     .  _  .
     #  .  .

    Move the data from node-y1-x0 to node-y1-x1:

    (.) G  .
     _  .  .
     #  .  .

    Next, we can free up space on our node by moving the data from node-y0-x0 to node-y1-x0:

    (_) G  .
     .  .  .
     #  .  .

    Finally, we can access the goal data by moving the it from node-y0-x1 to node-y0-x0:

    (G) _  .
     .  .  .
     #  .  .

    So, after 7 steps, we've accessed the data we want. Unfortunately, each of these moves takes time, and we need to
    be efficient:

    What is the fewest number of steps required to move your goal data to node-x0-y0?
    """

    pass


SAMPLE = [
    "Filesystem            Size  Used  Avail  Use%",
    "/dev/grid/node-x0-y0   10T    8T     2T   80%",
    "/dev/grid/node-x0-y1   11T    6T     5T   54%",
    "/dev/grid/node-x0-y2   32T   28T     4T   87%",
    "/dev/grid/node-x1-y0    9T    7T     2T   77%",
    "/dev/grid/node-x1-y1    8T    0T     8T    0%",
    "/dev/grid/node-x1-y2   11T    7T     4T   63%",
    "/dev/grid/node-x2-y0   10T    6T     4T   60%",
    "/dev/grid/node-x2-y1    9T    8T     1T   88%",
    "/dev/grid/node-x2-y2    9T    6T     3T   66%",
]


with open(Path(__file__).parent / "2016_22_input.txt") as fp:
    INPUTS = [line.strip() for line in fp]


class Pt(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def next_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    def neighbors(self, pt_set):
        nbs = set()
        for delta in [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]:
            new_pt = self + delta
            if new_pt in pt_set:
                nbs.add(new_pt)
        return nbs


class Node(NamedTuple):
    size: int
    used: int
    label: str

    def avail(self):
        return self.size - self.used

    def move(self, new_node):
        """To call: node, new_node = node.move(new_node)"""
        if new_node.used == 0 and self.used <= new_node.size:
            return Node(self.size, 0, new_node.label), Node(
                new_node.size, self.used, self.label
            )
        else:
            raise Exception(f"Cannot move node {self} to {new_node}")


class Path(NamedTuple):
    dist: int
    state: dict

    def __lt__(self, other):
        return self.dist < other.dist


def parse_raw(lines):
    nodes = {}
    for line in lines:
        if line[0] == "/":
            result = re.findall(
                r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line
            )
            x, y, size, used, avail = result[0]
            node = Node(int(size), int(used), f"o=x{x},y{y}")
            nodes[Pt(int(x), int(y))] = node
            if int(avail) != node.avail():
                raise Exception(f"Invalid node input at {Pt(x,y)}")
    return nodes


def print_nodes(nodes, large=100):
    results = []
    max_x = max(pt.x for pt in nodes.keys() if pt.y == 0)
    max_y = max(pt.y for pt in nodes.keys() if pt.x == 0)
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            node = nodes[Pt(x, y)]
            line.append("_" if node.used == 0 else "#" if node.used > large else ".")
        results.append("".join(line))
    return results


def find_pairs(nodes, any_pairs=True, large=100):
    pairs = set()
    non_zero_pairs = set()
    non_fitting_small_pairs = set()
    non_fitting_large_pairs = set()
    node_locs = set(nodes.keys())
    for node_a in nodes:
        if nodes[node_a].used > 0:
            nearby_nodes = (
                node_locs - {node_a} if any_pairs else node_a.neighbors(node_locs)
            )
            for node_b in nearby_nodes:
                if nodes[node_a].used <= nodes[node_b].avail():
                    if any_pairs and nodes[node_b].used > 0:
                        # let's do an additional check to see if we can move any data onto a non-empty disk
                        non_zero_pairs.add((node_a, node_b))
                    else:
                        pairs.add((node_a, node_b))
                elif nodes[node_a].used > nodes[node_b].size:
                    if nodes[node_a].used <= large:
                        non_fitting_small_pairs.add((node_a, node_b))
                    else:
                        non_fitting_large_pairs.add((node_a, node_b))
    if any_pairs:
        return pairs, non_zero_pairs, non_fitting_small_pairs, non_fitting_large_pairs
    return pairs


def state_to_hx_hash(new_state, target_label):
    """
    Reviewing state of input, just like puzzle drives of more than 100T are not moving
    Otherwise treat nodes as empty (-) or move-able (.)
    """
    goal = None
    empty = set()
    mobile = set()

    for pt in new_state:
        if new_state[pt].label == target_label:
            goal = pt
        elif new_state[pt].used == 0:
            empty.add(pt)
        elif new_state[pt].used < 100:
            mobile.add(pt)
    return goal, frozenset(empty), frozenset(mobile)


def move_node_to_origin(nodes, target_label):
    boundary = PriorityQueue()
    history = set()

    boundary.put(Path(0, nodes))
    history.add(state_to_hx_hash(nodes, target_label))
    while boundary.not_empty:
        moves, test_state = boundary.get()
        if test_state[Pt(0, 0)].label == target_label:
            return moves
        for pos_a, pos_b in find_pairs(test_state, any_pairs=False):
            new_state = test_state.copy()
            node_a, node_b = test_state[pos_a], test_state[pos_b]
            node_a, node_b = node_a.move(node_b)
            new_state[pos_a], new_state[pos_b] = node_a, node_b
            hx_state = state_to_hx_hash(new_state, target_label)
            if hx_state not in history:
                boundary.put(Path(moves + 1, new_state))
                history.add(hx_state)


def test_sample_inputs():
    nodes = parse_raw(SAMPLE)
    pairs, non_zero_pairs, non_fitting_small_pairs, non_fitting_large_pairs = (
        find_pairs(nodes, large=20)
    )
    assert len(pairs) == 7
    # additional checks
    assert len(non_zero_pairs) == 0  # e.g. cannot move any full to a partially full
    assert len(non_fitting_small_pairs) == 0  # e.g. can move any full to any empty
    assert (
        len(non_fitting_large_pairs) == 8
    )  # e.g. 1 node can't move to any other 8 (e.g. 1 cannot move)
    assert len(set(a for a, b in non_fitting_large_pairs)) == 1  # 1 large nodes
    assert find_pairs(nodes, any_pairs=False) == {
        (Pt(x=0, y=1), Pt(x=1, y=1)),
        (Pt(x=1, y=0), Pt(x=1, y=1)),
        (Pt(x=1, y=2), Pt(x=1, y=1)),
        (Pt(x=2, y=1), Pt(x=1, y=1)),
    }
    assert move_node_to_origin(nodes, "o=x2,y0") == 7


def test_puzzle_grid_test():
    nodes = parse_raw(INPUTS)
    assert max(pt.x for pt in nodes.keys() if pt.y == 0) == 37
    assert max(pt.y for pt in nodes.keys() if pt.x == 0) == 25
    assert all(Pt(x, y) in nodes for x in range(38) for y in range(26))
    assert nodes[Pt(37, 25)].used == 66  # lets see if size on target node is unique
    assert (
        sum(1 for v in nodes.values() if v.used == 66) == 100
    )  # nope, looks like multiple


def test_puzzle_inputs():
    nodes = parse_raw(INPUTS)
    pairs, non_zero_pairs, non_fitting_small_pairs, non_fitting_large_pairs = (
        find_pairs(nodes, large=100)
    )
    assert len(pairs) == 950
    # additional checks
    assert len(non_zero_pairs) == 0  # e.g. cannot move any full to a partially full
    assert len(non_fitting_small_pairs) == 0  # e.g. can move any full to any empty
    assert len(non_fitting_large_pairs) == 35187  # I think there are 37 large nodes?
    assert (
        len(set(a for a, b in non_fitting_large_pairs)) == 37
    )  # There are 37 large nodes?
    assert find_pairs(nodes, any_pairs=False) == {
        (Pt(x=16, y=22), Pt(x=17, y=22)),
        (Pt(x=17, y=21), Pt(x=17, y=22)),
        (Pt(x=17, y=23), Pt(x=17, y=22)),
        (Pt(x=18, y=22), Pt(x=17, y=22)),
    }
    print()
    print("\n".join(print_nodes(nodes)))
    # looking at the output of this we can determine solution by hand
    # ...................................... <= 75 to get left of goal
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # .##################################### <- 26 to get space to here
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ................._....................
    # ......................................
    # ......................................
    # ......................................
    # assert move_node_to_origin(nodes, 'o=x37,y0') == 7
    #
    # O..................................._G <= 75 to get left of goal
    # ......................................
    # O...................................G_ <= 76
    # ......................................
    # O..................................G_+ <= 76 + 5
    # ......................................
    # G-.................................... <= 76 + 180 = 256
    # ......................................
    by_hand_answer = 256
    assert by_hand_answer == 256
