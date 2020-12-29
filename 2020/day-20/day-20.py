import re
from copy import deepcopy, copy
from queue import PriorityQueue
from math import sqrt


class Tile:
    id = None
    rows = None

    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, id):
        self.id = id
        self.rows = []

    def __copy__(self):
        c = Tile(self.id)
        c.rows = deepcopy(self.rows)
        return c

    def append_row(self, row):
        self.rows.append(row)

    def get_border(self, border):
        if border == self.TOP:
            return self.rows[0]
        if border == self.RIGHT:
            return ''.join([
                row[-1] for row in self.rows
            ])
        if border == self.BOTTOM:
            bottom = self.rows[-1]
            return bottom[len(bottom)::-1]
        if border == self.LEFT:
            left = ''.join([
                row[0] for row in self.rows
            ])
            return left[len(left)::-1]

    def get_matching_borders(self, border, other_tiles):
        matches = set()
        this_border = self.get_border(border)
        for other_tile in other_tiles:
            for other_border in [self.TOP, self.RIGHT, self.BOTTOM, self.LEFT]:
                other = other_tile.get_border(other_border)
                if this_border == other[len(other)::-1]:
                    rotations = abs(other_border - border - 2) % 4
                    matches.add((other_tile.id, rotations, False))
                if this_border == other:
                    rotations = abs(other_border - border) % 4
                    matches.add((other_tile.id, rotations, True))

        return matches

    def rotate_clockwise(self):
        self.rows = [
            ''.join(row) for row in zip(*self.rows[::-1])
        ]

    def flip(self):
        self.rows.reverse()


class Board:

    size = None
    tiles = None
    remaining_tile_dict = None
    current_tile_index = None

    def __init__(self, size, tiles, remaining_tile_dict, current_tile_index):
        self.size = size
        self.tiles = tiles
        self.current_tile_index = current_tile_index
        self.remaining_tile_dict = remaining_tile_dict

    def __copy__(self):
        c = Board(self.size, deepcopy(self.tiles), deepcopy(self.remaining_tile_dict), self.current_tile_index)
        return c

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    @property
    def priority(self):
        return len(self.remaining_tile_dict.keys())

    @property
    def is_complete(self):
        return len(self.remaining_tile_dict.keys()) == 0

    @property
    def all_remaining_tile_configurations(self):
        return set([
            (tile_id, rotations, is_flipped) for tile_id in self.remaining_tile_dict.keys() for rotations in range(4) for is_flipped in [True, False]
        ])

    def print_ids(self):
        for row in self.tiles:
            print(' '.join(str(tile.id) for tile in row))

    def get_tile(self, index):
        row = index // self.size
        col = index % self.size
        return self.tiles[row][col]

    def get_next_possible_tiles(self):
        tile_above_index = self.current_tile_index - self.size
        if tile_above_index >= 0:
            tile_above = self.get_tile(tile_above_index)
            tile_above_match_set = tile_above.get_matching_borders(tile_above.BOTTOM, self.remaining_tile_dict.values())
        else:
            tile_above_match_set = -1

        tile_left_index = self.current_tile_index - 1
        if tile_left_index >= 0 and tile_left_index % self.size != (self.size - 1):
            tile_left = self.get_tile(tile_left_index)
            tile_left_match_set = tile_left.get_matching_borders(tile_left.RIGHT, self.remaining_tile_dict.values())
        else:
            tile_left_match_set = -1

        if tile_above_match_set == -1 and tile_left_match_set == -1:
            return self.all_remaining_tile_configurations
        if tile_above_match_set == -1:
            return tile_left_match_set
        if tile_left_match_set == -1:
            return tile_above_match_set
        return tile_above_match_set & tile_left_match_set

    def flip_rotate_and_place_tile(self, tile_id, rotations, is_flipped):
        tile = self.remaining_tile_dict.pop(tile_id)
        if is_flipped:
            tile.flip()
        for _ in range(rotations):
            tile.rotate_clockwise()
        row_index = self.current_tile_index // self.size
        col_index = self.current_tile_index % self.size
        self.tiles[row_index][col_index] = tile
        self.current_tile_index += 1


def solve(tiles):
    solved_boards = []
    board_size = int(sqrt(len(tiles.keys())))

    q = PriorityQueue()
    initial_tiles = [
        [
            None for _ in range(board_size)
        ] for _ in range(board_size)
    ]
    initial_board = Board(board_size, initial_tiles, tiles, 0)
    q.put((initial_board.priority, initial_board))

    while not q.empty():
        (priority, board) = q.get()
        next_possible_tiles = board.get_next_possible_tiles()
        for tile_id, rotations, is_flipped in next_possible_tiles:
            board_copy = deepcopy(board)
            board_copy.flip_rotate_and_place_tile(tile_id, rotations, is_flipped)
            if board_copy.is_complete:
                solved_boards.append(board_copy)
            q.put((board_copy.priority, board_copy))

    return solved_boards


with open('input.txt', 'r') as f:
    lines = f.readlines()

tiles = {}
current_tile = None

for line in lines:
    if line == '\n':
        tiles.update({
            current_tile.id: current_tile
        })
        current_tile = None
        continue

    m = re.match(r'^Tile (?P<tile_id>[0-9]+):\n$', line)
    if m:
        current_tile_id = int(m.group('tile_id'))
        current_tile = Tile(current_tile_id)
        continue

    current_tile.append_row(line.split('\n')[0])

solved_boards = solve(tiles)
for board in solved_boards:
    board.print_ids()
    print('\n')


