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


def identify_portal(grid, src, value):
    r, c = src
    portal_value, portal_type = None, None
    for index, neighbor in enumerate(get_neighbors(grid, src)):
        n_r, n_c = neighbor
        neighbor_value = grid[n_r][n_c]
        if re.match(r'[a-zA-Z]', neighbor_value):
            portal_value = ''.join(sorted([value, neighbor_value]))
            # Determine if inner or outer portal by moving one more in same direction and one or
            # more in opposite direction. If it's an outer portal, one of these will be outside
            # of the grid.
            next_r = (2 * (n_r - r)) + r
            next_c = (2 * (n_c - c)) + c
            opp_r = (-1 * (n_r - r)) + r
            opp_c = (-1 * (n_c - c)) + c
            try:
                if all([
                    0 <= next_r < len(grid),
                    0 <= next_c < len(grid[next_r]),
                    0 <= opp_r < len(grid),
                    0 <= opp_c < len(grid[opp_r])
                ]):
                    portal_type = 'i'
                else:
                    portal_type = 'o'
            except IndexError:
                portal_type = 'o'

    return portal_value, portal_type


def add_adjacents(grid, graph, src, start, find_portals=False):
    visited = {start}
    adjacents = {}

    q = Queue()

    if find_portals:
        src_portal_value, src_portal_type = identify_portal(grid, start, src)

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
                    continue
                else:
                    if find_portals:
                        portal_value, portal_type = identify_portal(grid, neighbor, value)
                        key = (portal_value, portal_type)
                        adjacents[key] = min(n_dist - 2, adjacents[key]) if key in adjacents else n_dist - 2

                    else:
                        adjacents[value] = min(n_dist, adjacents[value]) if value in adjacents else n_dist

                continue

            q.put((n_dist, neighbor))

        visited.add(node)

    key = (src_portal_value, src_portal_type) if find_portals else src
    graph[key].update(adjacents)

    return graph


def build_graph(grid, find_portals=False):
    graph = defaultdict(dict)

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col not in '.# ':
                graph = add_adjacents(grid, graph, col, (r, c), find_portals)

    if find_portals:
        for (node, portal_type), neighbors in graph.items():
            if node not in ['AA', 'ZZ']:
                opposite_portal_type = 'i' if portal_type == 'o' else 'o'
                neighbors[(node, opposite_portal_type)] = 1

    return graph
