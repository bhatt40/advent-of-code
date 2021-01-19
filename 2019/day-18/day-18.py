from queue import Queue
import re

def build_graph(grid):
    graph = {}
    start_position = None

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col not in '.#':
                graph[col] = find_adjacents(grid, (r, c))

            if col == '@':
                start_position = (r, c)

    return graph, start_position


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


def next_available_moves(graph, current_position, keys_in_hand):
    moves = {}
    q = Queue()
    q.put((current_position, 0, set()))

    def add_new_positions_to_queue(items, prev):
        for new_pos, new_dist in items:
            if new_pos not in prev:
                new_prev = prev | {pos}
                q.put((new_pos, dist + new_dist, new_prev))

    while not q.empty():
        pos, dist, prev = q.get()
        if 'a' <= pos <= 'z':
            if pos not in keys_in_hand and pos != current_position:
                moves[pos] = dist
            else:
                add_new_positions_to_queue(graph[pos].items(), prev)
        elif 'A' <= pos <= 'Z':
            if pos.lower() not in keys_in_hand:
                continue
            else:
                add_new_positions_to_queue(graph[pos].items(), prev)
        else:
            add_new_positions_to_queue(graph[pos].items(), prev)

    return moves


def get_shortest_distance(graph, current_position, number_of_keys):
    shortest_dist = None
    q = Queue()
    q.put((current_position, 0, set()))

    while not q.empty():
        pos, dist_traveled, keys_in_hand = q.get()

        new_keys_in_hand = keys_in_hand.copy()
        if pos != '@':
            new_keys_in_hand.add(pos)

        if len(new_keys_in_hand) == number_of_keys:
            if not shortest_dist or dist_traveled < shortest_dist:
                shortest_dist = dist_traveled
        else:
            next_moves = next_available_moves(graph, pos, new_keys_in_hand)
            for new_pos, new_dist in next_moves.items():
                q.put((new_pos, dist_traveled + new_dist, new_keys_in_hand))

    return shortest_dist


with open('test.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph, starting_position = build_graph(grid)

number_of_keys = len([
    key for key in graph.keys() if 'a' <= key <= 'z'
])

# print(next_available_moves(graph, 'b', {'g', 'd', 'a', 'i', 'f', 'e', 'c'}))
print(get_shortest_distance(graph, '@', number_of_keys))
