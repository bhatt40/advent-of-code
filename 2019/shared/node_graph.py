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


def add_adjacents(grid, graph, src, start, find_portals=False):
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
                if find_portals and n_dist == 1:
                    src = ''.join(sorted([src, value]))
                else:
                    if find_portals:
                        for value_neighbor in get_neighbors(grid, neighbor):
                            v_r, v_c = value_neighbor
                            value_neighbor_value = grid[v_r][v_c]
                            if re.match(r'[a-zA-Z]', value_neighbor_value):
                                value = ''.join(sorted([value, value_neighbor_value]))

                    offset = 2 if find_portals else 0
                    adjacents[value] = min(n_dist - offset, adjacents[value]) if value in adjacents else n_dist - offset
                continue

            q.put((n_dist, neighbor))

        visited.add(node)

    graph[src].update(adjacents)

    return graph


def build_graph(grid, find_portals=False):
    graph = defaultdict(dict)

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col not in '.# ':
                graph = add_adjacents(grid, graph, col, (r, c), find_portals)

    return graph
