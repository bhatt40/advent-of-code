from queue import Queue
import re
from math import inf
from functools import lru_cache
from collections import defaultdict


def build_graph(grid):
    graph = {}

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col not in '.#':
                graph[col] = find_adjacents(grid, (r, c))

    return graph


def get_neighbors(grid, node):
    r, c = node
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r2 = r + dr
        c2 = c + dc

        if 0 <= r2 < len(grid) and 0 <= c2 < len(grid[r2]):
            if grid[r2][c2] != '#':
                yield r2, c2


def find_adjacents(grid, start):
    visited = {start}
    adjacents = {}

    q = Queue()
    q.put((0, start))

    while not q.empty():
        dist, node = q.get()
        n_dist = dist + 1

        for neighbor in get_neighbors(grid, node):
            if neighbor in visited:
                continue

            r, c = neighbor
            value = grid[r][c]

            if re.match(r'[a-zA-Z]', value):
                adjacents[value] = min(n_dist, adjacents[value]) if value in adjacents else n_dist
                continue

            q.put((n_dist, neighbor))

        visited.add(node)

    return adjacents


@lru_cache(maxsize=None)
def next_available_keys(current_position, keys_in_hand):
    keys = []
    distances = defaultdict(lambda: inf)
    q = Queue()
    q.put((current_position, 0))

    def add_new_positions_to_queue(items):
        for new_pos, new_dist in items:
            if dist + new_dist < distances[new_pos]:
                distances[new_pos] = dist + new_dist
                q.put((new_pos, dist + new_dist))

    while not q.empty():
        pos, dist = q.get()
        if 'a' <= pos <= 'z':
            if pos not in keys_in_hand and pos != current_position:
                keys.append((pos, dist))
            else:
                add_new_positions_to_queue(graph[pos].items())
        elif 'A' <= pos <= 'Z':
            if pos.lower() not in keys_in_hand:
                continue
            else:
                add_new_positions_to_queue(graph[pos].items())
        else:
            add_new_positions_to_queue(graph[pos].items())

    return keys


@lru_cache(maxsize=None)
def minimum_steps(positions, num_to_find, keys_in_hand):
    if num_to_find == 0:
        return 0

    min_dist = inf

    for position in positions:
        next_keys = next_available_keys(position, keys_in_hand)
        for new_pos, dist in next_keys:
            new_keys_in_hand = frozenset(keys_in_hand | {new_pos})
            new_positions = positions.replace(position, new_pos)
            dist += minimum_steps(new_positions, num_to_find - 1, new_keys_in_hand)

            if dist < min_dist:
                min_dist = dist

    return min_dist


def print_grid(grid):
    for row in grid:
        print(row)
    print('\n')


with open('input.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph = build_graph(grid)
graphs = [graph]

number_of_keys = len([
    key for key in graph.keys() if 'a' <= key <= 'z'
])

# Part 1
print(minimum_steps('@', number_of_keys, frozenset()))

# Part 2
next_available_keys.cache_clear()
minimum_steps.cache_clear()

height = len(grid)
vert_center = (height - 1) // 2
width = len(grid[0])
hor_center = (width - 1) // 2
grid[vert_center - 1] = grid[vert_center - 1][:hor_center - 1] + '1#2' + grid[vert_center - 1][hor_center + 2:]
grid[vert_center] = grid[vert_center][:hor_center - 1] + '###' + grid[vert_center][hor_center + 2:]
grid[vert_center + 1] = grid[vert_center + 1][:hor_center - 1] + '3#4' + grid[vert_center + 1][hor_center + 2:]

graph = build_graph(grid)
positions = ''.join([
    str(x+1) for x in range(4)
])
print(minimum_steps(positions, number_of_keys, frozenset()))
