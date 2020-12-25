from collections import defaultdict, deque
import math


class Puzzle:
    """
    --- Day 20: Jurassic Jigsaw ---

    The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the
    distance! Since you have some spare time, you might as well see if there was anything interesting in
    the image the Mythical Information Bureau satellite captured.

    After decoding the satellite messages, you discover that the data actually contains many small images
    created by the satellite's camera array. The camera array consists of many cameras; rather than produce
    a single square image, they produce many smaller square image tiles that need to be reassembled back
    into a single image.

    Each camera in the camera array returns a single monochrome image tile with a random unique ID number.
    The tiles (your puzzle input) arrived in a random order.

    Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped
    to a random orientation. Your first task is to reassemble the original image by orienting the tiles
    so they fit together.

    To show how the tiles should be reassembled, each tile's image data includes a border that should
    line up exactly with its adjacent tiles. All tiles have this border, and the border lines up exactly
    when the tiles are both oriented correctly. Tiles at the edge of the image also have this border,
    but the outermost edges won't line up with any other tiles.

    For example, suppose you have the following nine tiles:

    Tile 2311:
    ..##.#..#.
    ##..#.....
    #...##..#.
    ####.#...#
    ##.##.###.
    ##...#.###
    .#.#.#..##
    ..#....#..
    ###...#.#.
    ..###..###

    Tile 1951:
    #.##...##.
    #.####...#
    .....#..##
    #...######
    .##.#....#
    .###.#####
    ###.##.##.
    .###....#.
    ..#.#..#.#
    #...##.#..

    Tile 1171:
    ####...##.
    #..##.#..#
    ##.#..#.#.
    .###.####.
    ..###.####
    .##....##.
    .#...####.
    #.##.####.
    ####..#...
    .....##...

    Tile 1427:
    ###.##.#..
    .#..#.##..
    .#.##.#..#
    #.#.#.##.#
    ....#...##
    ...##..##.
    ...#.#####
    .#.####.#.
    ..#..###.#
    ..##.#..#.

    Tile 1489:
    ##.#.#....
    ..##...#..
    .##..##...
    ..#...#...
    #####...#.
    #..#.#.#.#
    ...#.#.#..
    ##.#...##.
    ..##.##.##
    ###.##.#..

    Tile 2473:
    #....####.
    #..#.##...
    #.##..#...
    ######.#.#
    .#...#.#.#
    .#########
    .###.#..#.
    ########.#
    ##...##.#.
    ..###.#.#.

    Tile 2971:
    ..#.#....#
    #...###...
    #.#.###...
    ##.##..#..
    .#####..##
    .#..####.#
    #..#.#..#.
    ..####.###
    ..#.#.###.
    ...#.#.#.#

    Tile 2729:
    ...#.#.#.#
    ####.#....
    ..#.#.....
    ....#..#.#
    .##..##.#.
    .#.####...
    ####.#.#..
    ##.####...
    ##..#.##..
    #.##...##.

    Tile 3079:
    #.#.#####.
    .#..######
    ..#.......
    ######....
    ####.#..#.
    .#...#.##.
    #.#####.##
    ..#.###...
    ..#.......
    ..#.###...

    By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent
    borders to line up:

    #...##.#.. ..###..### #.#.#####.
    ..#.#..#.# ###...#.#. .#..######
    .###....#. ..#....#.. ..#.......
    ###.##.##. .#.#.#..## ######....
    .###.##### ##...#.### ####.#..#.
    .##.#....# ##.##.###. .#...#.##.
    #...###### ####.#...# #.#####.##
    .....#..## #...##..#. ..#.###...
    #.####...# ##..#..... ..#.......
    #.##...##. ..##.#..#. ..#.###...

    #.##...##. ..##.#..#. ..#.###...
    ##..#.##.. ..#..###.# ##.##....#
    ##.####... .#.####.#. ..#.###..#
    ####.#.#.. ...#.##### ###.#..###
    .#.####... ...##..##. .######.##
    .##..##.#. ....#...## #.#.#.#...
    ....#..#.# #.#.#.##.# #.###.###.
    ..#.#..... .#.##.#..# #.###.##..
    ####.#.... .#..#.##.. .######...
    ...#.#.#.# ###.##.#.. .##...####

    ...#.#.#.# ###.##.#.. .##...####
    ..#.#.###. ..##.##.## #..#.##..#
    ..####.### ##.#...##. .#.#..#.##
    #..#.#..#. ...#.#.#.. .####.###.
    .#..####.# #..#.#.#.# ####.###..
    .#####..## #####...#. .##....##.
    ##.##..#.. ..#...#... .####...#.
    #.#.###... .##..##... .####.##.#
    #...###... ..##...#.. ...#..####
    ..#.#....# ##.#.#.... ...##.....

    For reference, the IDs of the above tiles are:

    1951    2311    3079
    2729    1427    2473
    2971    1489    1171

    To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together.
    If you do this with the assembled tiles from the example above, you get

    1951 * 3079 * 2971 * 1171 = 20899048083289.

    Assemble the tiles into an image.

    What do you get if you multiply together the IDs of the four corner tiles?

    --- Part Two ---
    Now, you're ready to check the image for sea monsters.

    The borders of each tile are not part of the actual image; start by removing them.

    In the example above, the tiles become:

    .#.#..#. ##...#.# #..#####
    ###....# .#....#. .#......
    ##.##.## #.#.#..# #####...
    ###.#### #...#.## ###.#..#
    ##.#.... #.##.### #...#.##
    ...##### ###.#... .#####.#
    ....#..# ...##..# .#.###..
    .####... #..#.... .#......

    #..#.##. .#..###. #.##....
    #.####.. #.####.# .#.###..
    ###.#.#. ..#.#### ##.#..##
    #.####.. ..##..## ######.#
    ##..##.# ...#...# .#.#.#..
    ...#..#. .#.#.##. .###.###
    .#.#.... #.##.#.. .###.##.
    ###.#... #..#.##. ######..

    .#.#.### .##.##.# ..#.##..
    .####.## #.#...## #.#..#.#
    ..#.#..# ..#.#.#. ####.###
    #..####. ..#.#.#. ###.###.
    #####..# ####...# ##....##
    #.##..#. .#...#.. ####...#
    .#.###.. ##..##.. ####.##.
    ...###.. .##...#. ..#..###

    Remove the gaps to form the actual image:

    .#.#..#.##...#.##..#####
    ###....#.#....#..#......
    ##.##.###.#.#..######...
    ###.#####...#.#####.#..#
    ##.#....#.##.####...#.##
    ...########.#....#####.#
    ....#..#...##..#.#.###..
    .####...#..#.....#......
    #..#.##..#..###.#.##....
    #.####..#.####.#.#.###..
    ###.#.#...#.######.#..##
    #.####....##..########.#
    ##..##.#...#...#.#.#.#..
    ...#..#..#.#.##..###.###
    .#.#....#.##.#...###.##.
    ###.#...#..#.##.######..
    .#.#.###.##.##.#..#.##..
    .####.###.#...###.#..#.#
    ..#.#..#..#.#.#.####.###
    #..####...#.#.#.###.###.
    #####..#####...###....##
    #.##..#..#...#..####...#
    .#.###..##..##..####.##.
    ...###...##...#...#..###

    Now, you're ready to search for sea monsters! Because your image is monochrome,
    a sea monster will look like this:

                      #
    #    ##    ##    ###
     #  #  #  #  #  #

    When looking for this pattern in the image, the spaces can be anything;
    only the # need to match. Also, you might need to rotate or flip your image
    before it's oriented correctly to find sea monsters. In the above image, after
    flipping and rotating it to the appropriate orientation, there are two sea
    monsters (marked with O):

    .####...#####..#...###..
    #####..#..#.#.####..#.#.
    .#.#...#.###...#.##.O#..
    #.O.##.OO#.#.OO.##.OOO##
    ..#O.#O#.O##O..O.#O##.##
    ...#.#..##.##...#..#..##
    #.##.#..#.#..#..##.#.#..
    .###.##.....#...###.#...
    #.####.#.#....##.#..#.#.
    ##...#..#....#..#...####
    ..#.##...###..#.#####..#
    ....#.##.#.#####....#...
    ..##.##.###.....#.##..#.
    #...#...###..####....##.
    .#.##...#.##.#.#.###...#
    #.###.#..####...##..#...
    #.###...#.##...#.##O###.
    .O##.#OO.###OO##..OOO##.
    ..O#.O..O..O.#O##O##.###
    #.#..##.########..#..##.
    #.#####..#.#...##..#....
    #....##..#.#########..##
    #...#.....#..##...###.##
    #..###....##.#...##.##.#

    Determine how rough the waters are in the sea monsters' habitat by counting the number of # that are not
    part of a sea monster. In the above example, the habitat's water roughness is 273.

    How many # are not part of a sea monster?
    """
    pass


class Tile:
    """
    Format for raw is

    Tile 2311:
    ..##.#..#.
    ##..#.....
    #...##..#.
    ####.#...#
    ##.##.###.
    ##...#.###
    .#.#.#..##
    ..#....#..
    ###...#.#.
    ..###..###
    """

    def __init__(self, raw):
        lines = raw.split('\n')
        self.id = lines[0].split(' ')[1][:-1]
        self.cc_rotation = 0
        self.flipped = False
        self.sides = defaultdict(str)
        self.grid = {}
        self.x_max = 0
        self.y_max = 0
        for y in range(len(lines) - 1):
            if y == 0:
                self.sides['N'] = lines[1]
            if lines[y + 1].count('.') > 0 or lines[y + 1].count('#') > 0:
                self.y_max = y
                self.sides['S'] = lines[y + 1]
            for x in range(len(lines[y + 1])):
                self.x_max = max(x, self.x_max)
                c = lines[y + 1][x]
                if x == 0:
                    self.sides['W'] += c
                elif x == len(lines[y + 1]) - 1:
                    self.sides['E'] += c
                if c == '#':
                    self.grid[(x, y)] = 1
        # keep self.side listing clockwise
        self.sides['S'] = ''.join(s for s in reversed(self.sides['S']))
        self.sides['W'] = ''.join(s for s in reversed(self.sides['W']))

    def get_side(self, external_side):
        direction_to_position = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        external_position = direction_to_position[external_side]
        if self.flipped:
            position_to_direction = ['N', 'W', 'S', 'E']
            internal_side = position_to_direction[(external_position - self.cc_rotation) % 4]
            return ''.join(s for s in reversed(self.sides[internal_side]))
        else:
            position_to_direction = ['N', 'E', 'S', 'W']
            internal_side = position_to_direction[(external_position + self.cc_rotation) % 4]
            return self.sides[internal_side]

    def fits_on(self, my_side, match_tile):
        direction_from_other_side = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
        my_side_pixels = self.get_side(my_side)
        match_side_pixels = match_tile.get_side(direction_from_other_side[my_side])
        return my_side_pixels == ''.join(reversed(match_side_pixels))

    def get_inner_image(self, x0=0, y0=0, b=1):
        points = set()
        for x, y in self.grid:
            if b <= x <= self.x_max - b and b <= y <= self.y_max - b:
                if self.cc_rotation == 1:
                    (x, y) = (y, self.x_max - x)
                elif self.cc_rotation == 2:
                    (x, y) = (self.x_max - x, self.y_max - y)
                elif self.cc_rotation == 3:
                    (x, y) = (self.y_max - y, x)
                if self.flipped:
                    x = self.x_max - x
                points.add((x - b + x0, y - b + y0))
        return points


def test_tile():
    sample_tile = Tile('Tile 2311:\n' +
                       '#...\n' +
                       '##.#\n')
    assert sample_tile.id == '2311'
    assert sample_tile.grid == {(0, 0): 1, (0, 1): 1, (1, 1): 1, (3, 1): 1}


def test_tile_get_side_with_cc_rotation_and_flipped():
    sample_tile = Tile('Tile 2311:\n' +
                       '#...\n' +
                       '##.#\n')
    assert sample_tile.get_side('N') == '#...'
    assert sample_tile.get_side('E') == '.#'
    assert sample_tile.get_side('S') == '#.##'
    assert sample_tile.get_side('W') == '##'
    sample_tile.flipped = True
    assert sample_tile.get_side('N') == '...#'
    assert sample_tile.get_side('E') == '##'
    assert sample_tile.get_side('S') == '##.#'
    assert sample_tile.get_side('W') == '#.'
    sample_tile.cc_rotation = 1
    sample_tile.flipped = False
    assert sample_tile.get_side('N') == '.#'
    assert sample_tile.get_side('E') == '#.##'
    assert sample_tile.get_side('S') == '##'
    assert sample_tile.get_side('W') == '#...'
    sample_tile.flipped = True
    assert sample_tile.get_side('N') == '#.'
    assert sample_tile.get_side('E') == '...#'
    assert sample_tile.get_side('S') == '##'
    assert sample_tile.get_side('W') == '##.#'


def test_tile_fits_on():
    sample_tile = Tile('Tile 1:\n' +
                       '#...\n' +
                       '##.#\n')
    sample_tile2 = Tile('Tile 2:\n' +
                        '##.#\n' +
                        '#...\n')
    assert sample_tile.fits_on('N', sample_tile2)
    sample_tile.cc_rotation = 1
    sample_tile2.cc_rotation = 3
    assert sample_tile.fits_on('N', sample_tile2)
    assert sample_tile.fits_on('S', sample_tile2)
    assert not sample_tile.fits_on('E', sample_tile2)


class Board:
    def __init__(self, raw, width=0, height=0):
        raw_tiles = raw.split('\n\n')
        self.tiles = {}
        self.solutions = []
        for raw_tile in raw_tiles:
            new_tile = Tile(raw_tile)
            self.tiles[new_tile.id] = new_tile
        if height == 0 and width == 0:
            height = int(math.sqrt(len(self.tiles)))
            width = height
        self.width = width
        self.height = height
        self.orientations = set((r, False if t == 0 else True) for r in range(4) for t in range(2))
        self.positions = [(i, j) for i in range(height) for j in range(width)]

    def find_next_location(self, working_board):
        remaining_pos = [p for p in self.positions if p not in working_board]
        return remaining_pos[0]

    def new_piece_fits(self, working_board, location, tile_id, cc_rotation, flipped):
        tile = self.tiles[tile_id]
        tile.cc_rotation = cc_rotation
        tile.flipped = flipped
        if location[0] > 0:
            left_tile_id, rot, flip = working_board[(location[0] - 1, location[1])]
            left_tile = self.tiles[left_tile_id]
            left_tile.cc_rotation = rot
            left_tile.flipped = flip
            if not tile.fits_on('W', left_tile):
                return False
        if location[1] > 0:
            above_tile_id, rot, flip = working_board[(location[0], location[1] - 1)]
            above_tile = self.tiles[above_tile_id]
            above_tile.cc_rotation = rot
            above_tile.flipped = flip
            if not tile.fits_on('N', above_tile):
                return False
        return True

    def solve(self, starting_board=None):
        frontier = deque()

        if starting_board is None:
            for tile_id in self.tiles.keys():
                free_tiles = set(t_id for t_id in self.tiles.keys() if t_id != tile_id)
                for cc_rotation, flipped in self.orientations:
                    frontier.append(({(0, 0): (tile_id, cc_rotation, flipped)}, free_tiles.copy()))
        else:
            used_tiles = set(t_id for t_id, _, _ in starting_board.values())
            free_tiles = set(t_id for t_id in self.tiles.keys() if t_id not in used_tiles)
            frontier.append((starting_board, free_tiles))

        while len(frontier) > 0:
            # print(f'{len(frontier)} yet to explore')
            working_board, free_tiles = frontier.pop()
            if len(working_board) + len(free_tiles) != len(self.tiles):
                raise Exception('Something is wrong with tile counts.')
            if len(working_board) == len(self.tiles):
                self.solutions.append(working_board)
                # print(f'SOLUTION {working_board}')
                return working_board
            else:
                next_location = self.find_next_location(working_board)
                for tile_id in free_tiles:
                    tile_id_fit = 0
                    for cc_rotation, flipped in self.orientations:
                        if self.new_piece_fits(working_board, next_location, tile_id, cc_rotation, flipped):
                            tile_id_fit += 1
                            new_board = working_board.copy()
                            next_free_tiles = set(t_id for t_id in free_tiles if t_id != tile_id)
                            new_board[next_location] = (tile_id, cc_rotation, flipped)
                            if len(new_board) == len(self.tiles):
                                self.solutions.append(new_board)
                                # print(f'SOLUTION {new_board}')
                                return new_board
                            else:
                                frontier.append((new_board, next_free_tiles))
                                # print(f'{tile_id} fit {next_location} on board {working_board}')
                    # print(f'{tile_id} fit {tile_id_fit} in {next_location} on board {working_board}')
        return dict()

    def build_image(self, solved_board):
        image = {}
        for loc in solved_board:
            x, y = loc
            tile_id, cc_rot, flipped = solved_board[loc]
            tile = self.tiles[tile_id]
            tile.cc_rotation = cc_rot
            tile.flipped = flipped
            x0 = x * (tile.x_max - 1)
            y0 = y * (tile.y_max - 1)
            bits_to_add = tile.get_inner_image(x0, y0)
            for bit in bits_to_add:
                image[bit] = 1
        return image


def rotate_and_flip(points, x_max, y_max, cc_rotation, flipped):
    result = {}
    for x, y in points:
        val = points[(x, y)]
        if cc_rotation == 1:
            (x, y) = (y, x_max - x)
        elif cc_rotation == 2:
            (x, y) = (x_max - x, y_max - y)
        elif cc_rotation == 3:
            (x, y) = (y_max - y, x)
        if flipped:
            x = x_max - x
        result[(x, y)] = val
    return result


def update_sea_monsters(image_as_dict, to_screen=False):
    """
    Sea monster is the following 15 points
      01234567890123456789
    0:                  #
    1:#    ##    ##    ###
    2: #  #  #  #  #  #
    """
    orientations = set((r, False if t == 0 else True) for r in range(4) for t in range(2))

    base_monster = {(1, 0), (2, 1), (2, 4), (1, 5), (1, 6), (2, 7),
                    (2, 10), (1, 11), (1, 12), (2, 13),
                    (2, 16), (1, 17), (1, 18), (0, 18), (1, 19)}

    # Well - reading more closely we rotate and flip image not the sea monsters
    # monster_orientations = [rotate_and_flip(base_monster, 19, 2, rot, flip) for rot, flip in orientations]

    image_x_max = 0
    image_y_max = 0
    for x, y in image_as_dict:
        image_x_max = max(x, image_x_max)
        image_y_max = max(y, image_y_max)

    for rot, flip in orientations:
        new_image_dict = rotate_and_flip(image_as_dict, image_x_max, image_y_max, rot, flip)
        found_monsters = False
        for y in range(image_y_max):
            for x in range(image_x_max):
                # for monster in monster_orientations:
                no_monster_here = False
                for mx, my in base_monster:
                    if (x + mx, y + my) not in new_image_dict:
                        no_monster_here = True
                if not no_monster_here:
                    found_monsters = True
                    for mx, my in base_monster:
                        new_image_dict[(x + mx, y + my)] = 0
        if found_monsters:
            if to_screen:
                print_image(new_image_dict, True)
            return sum(new_image_dict.values()), new_image_dict


with open('day_20_sample.txt') as fp:
    SAMPLE = fp.read()

SAMPLE_IMAGE = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".split('\n')


def print_image(image_as_dict, to_screen=False):
    max_x = 0
    max_y = 0
    result = []
    for x, y in image_as_dict:
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    for y in range(max_y+1):
        line = []
        for x in range(max_x+1):
            if (x, y) in image_as_dict and image_as_dict[(x, y)] == 1:
                line.append('#')
            elif (x, y) in image_as_dict  and image_as_dict[(x, y)] == 0:
                line.append('O')
            else:
                line.append('.')
        if to_screen:
            print(''.join(line))
        result.append(''.join(line))
    return result


def get_solution_checksum(board):
    x_max, y_max = max(board.keys())
    value = 1
    value *= int(board[(0, 0)][0])
    value *= int(board[(x_max, 0)][0])
    value *= int(board[(0, y_max)][0])
    value *= int(board[(x_max, y_max)][0])
    return value


def test_board_basics():
    sample_board = Board(SAMPLE)
    assert len(sample_board.tiles) == 9
    assert '2311' in sample_board.tiles
    assert '3079' in sample_board.tiles
    assert sample_board.height == 3
    assert sample_board.width == 3


def test_sample_board():
    sample_board = Board(SAMPLE)
    # Check sample puzzle fit (before checking solve function)
    # First row
    tile_1951 = sample_board.tiles['1951']
    tile_1951.cc_rotation = 2
    tile_1951.flipped = True
    # First tile, nothing to check

    tile_2311 = sample_board.tiles['2311']
    tile_2311.cc_rotation = 2
    tile_2311.flipped = True
    assert tile_2311.fits_on('W', tile_1951)
    assert tile_1951.fits_on('E', tile_2311)

    tile_3079 = sample_board.tiles['3079']
    tile_3079.cc_rotation = 0
    tile_3079.flipped = False
    assert tile_3079.fits_on('W', tile_2311)
    assert tile_2311.fits_on('E', tile_3079)

    # Second row
    tile_2729 = sample_board.tiles['2729']
    tile_2729.cc_rotation = 2
    tile_2729.flipped = True
    assert tile_2729.fits_on('N', tile_1951)
    assert tile_1951.fits_on('S', tile_2729)

    tile_1427 = sample_board.tiles['1427']
    tile_1427.cc_rotation = 2
    tile_1427.flipped = True
    assert tile_1427.fits_on('W', tile_2729)
    assert tile_1427.fits_on('N', tile_2311)
    assert tile_2729.fits_on('E', tile_1427)
    assert tile_2311.fits_on('S', tile_1427)

    tile_2473 = sample_board.tiles['2473']
    tile_2473.cc_rotation = 1
    tile_2473.flipped = True
    assert tile_2473.get_side('N') == '..#.###...'
    assert tile_2473.get_side('W') == '..###.#.#.'

    assert tile_2473.fits_on('W', tile_1427)
    assert tile_2473.fits_on('N', tile_3079)
    assert tile_1427.fits_on('E', tile_2473)
    assert tile_3079.fits_on('S', tile_2473)

    # Third row
    tile_2971 = sample_board.tiles['2971']
    tile_2971.cc_rotation = 2
    tile_2971.flipped = True
    assert tile_2971.get_side('N') == '...#.#.#.#'

    assert tile_2971.fits_on('N', tile_2729)
    assert tile_2729.fits_on('S', tile_2971)

    tile_1489 = sample_board.tiles['1489']
    tile_1489.cc_rotation = 2
    tile_1489.flipped = True
    assert tile_1489.get_side('N') == '###.##.#..'

    assert tile_1489.fits_on('W', tile_2971)
    assert tile_1489.fits_on('N', tile_1427)
    assert tile_2971.fits_on('E', tile_1489)
    assert tile_1427.fits_on('S', tile_1489)

    tile_1171 = sample_board.tiles['1171']
    tile_1171.cc_rotation = 0
    tile_1171.flipped = True
    assert tile_1171.get_side('N') == '.##...####'

    assert tile_1171.fits_on('W', tile_1489)
    assert tile_1171.fits_on('N', tile_2473)
    assert tile_1489.fits_on('E', tile_1171)
    assert tile_2473.fits_on('S', tile_1171)


def test_board_new_piece_fits():
    sample_board = Board(SAMPLE)
    working_board = {(0, 1): ('2729', 2, True), (1, 0): ('2311', 2, True)}
    location = (1, 1)
    tile_id = '1427'
    cc_rotation = 2
    flipped = True
    assert sample_board.new_piece_fits(working_board, location, tile_id, cc_rotation, flipped)
    working_board = {(0, 0): ('1951', 2, True), (1, 0): ('2311', 2, True), (2, 0): ('3079', 0, False),
                     (0, 1): ('2729', 2, True), (1, 1): ('1427', 2, True), (2, 1): ('2473', 1, True),
                     (0, 2): ('2971', 2, True), (1, 2): ('1489', 2, True)}
    location = (2, 2)
    tile_id = '1171'
    cc_rotation = 0
    flipped = True
    assert sample_board.new_piece_fits(working_board, location, tile_id, cc_rotation, flipped)


def test_board_solve():
    sample_board = Board(SAMPLE)
    solution_board = {(0, 0): ('1951', 2, True), (1, 0): ('2311', 2, True), (2, 0): ('3079', 0, False),
                      (0, 1): ('2729', 2, True), (1, 1): ('1427', 2, True), (2, 1): ('2473', 1, True),
                      (0, 2): ('2971', 2, True), (1, 2): ('1489', 2, True), (2, 2): ('1171', 0, True)}
    assert sample_board.solve(solution_board) == solution_board
    starting_board = solution_board.copy()
    starting_board.pop((1, 1))
    starting_board.pop((2, 1))
    starting_board.pop((0, 2))
    starting_board.pop((1, 2))
    starting_board.pop((2, 2))
    assert len(starting_board) == 4
    assert sample_board.solve(starting_board) == solution_board

    # now only place first piece
    assert sample_board.solve({(0, 0): ('1951', 2, True)}) == solution_board

    # finally test full solution - might not be same orientation though...
    my_soln = sample_board.solve()
    assert get_solution_checksum(my_soln) == 20899048083289


def test_sample_images():
    sample_board = Board(SAMPLE)
    solution_board = {(0, 0): ('1951', 2, True), (1, 0): ('2311', 2, True), (2, 0): ('3079', 0, False),
                      (0, 1): ('2729', 2, True), (1, 1): ('1427', 2, True), (2, 1): ('2473', 1, True),
                      (0, 2): ('2971', 2, True), (1, 2): ('1489', 2, True), (2, 2): ('1171', 0, True)}

    show_test = False
    if show_test:
        test_tile = sample_board.tiles['1951']
        test_tile.cc_rotation = 2
        test_tile.flipped = True
        test_bits = test_tile.get_inner_image()
        print('Full un-rotated tile')
        printed_image_full = print_image(test_tile.grid)
        print('Rotated Inner')
        printed_image = print_image(test_bits)

    show_test = False
    if show_test:
        test_tile2 = sample_board.tiles['2473']
        test_tile2.cc_rotation = 1
        test_tile2.flipped = True
        test_bits = test_tile2.get_inner_image(16, 8)
        print('Full un-rotated tile')
        printed_image_full = print_image(test_tile2.grid)
        print('Rotated Inner')
        printed_image = print_image(test_bits)

    solution_image = sample_board.build_image(solution_board)
    printed_image = print_image(solution_image)
    assert printed_image == SAMPLE_IMAGE
    print()
    sea_count, new_image = update_sea_monsters(solution_image, True)
    assert sea_count == 273


with open('day_20_input.txt') as fp:
    INPUT = fp.read()


def test_solution():
    game_board = Board(INPUT)
    assert len(game_board.tiles) == 144
    my_soln = game_board.solve()
    assert get_solution_checksum(my_soln) == 29584525501199
    solution_image = game_board.build_image(my_soln)
    print()
    assert update_sea_monsters(solution_image)[0] == 1665  # 1740 is too nigh
    printed_image = print_image(solution_image, True)
