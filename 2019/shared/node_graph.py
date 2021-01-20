from queue import Queue
import re
from collections import defaultdict


def get_neighbors(grid, node):
    r, c = node
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r2 = r + dr
        c2 = c + dc

        if 0 <= r2 < len(grid) and 0 <= c2 < len(grid[r2]):
            if grid[r2][c2] not in '# ':
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


def build_graph(grid):
    graph = defaultdict(dict)

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col not in '.# ':
                graph[col].update(find_adjacents(grid, (r, c)))

    return graph
