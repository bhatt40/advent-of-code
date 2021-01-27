from node_graph import build_graph
from collections import defaultdict
from math import inf


def find_shortest_paths(graph, src):
    distances = defaultdict(lambda: inf)
    distances[src] = 0
    complete_set = set()
    incomplete_set = set(graph.keys())

    while len(incomplete_set) > 0:
        current_node = min(incomplete_set, key=lambda x: distances[x])
        complete_set.add(current_node)
        incomplete_set.remove(current_node)

        neighbors = graph[current_node]
        for neighbor, dist in neighbors.items():
            new_dist = distances[current_node] + dist
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist

    return distances


def distance_to_destination(graph, current, dest_node, visited, max_level):
    current_node, current_portal_type, current_level, current_dist = current

    if current_node == 'ZZ':
        if current_level == 0:
            return current_dist
        else:
            return inf

    new_visited = visited.copy()
    new_visited.append(((current_node, current_portal_type), current_level))

    neighbors = graph[(current_node, current_portal_type)]
    opposite_node = (current_node, 'i' if current_portal_type == 'o' else 'o')

    # If portal hasn't been crossed, next move is to cross portal. Otherwise, cycle through all neighbors.
    next_nodes = neighbors
    if len(visited):
        last_visited_node = visited[-1][0]
        if opposite_node != last_visited_node and current_node not in ['AA', 'ZZ']:
            next_nodes = {
                n: v for n, v in neighbors.items() if n == opposite_node
            }

    distances = set()
    for (neighbor, portal_type), dist in next_nodes.items():
        next_level = current_level
        if neighbor == current_node:
            next_level += 1 if portal_type == 'o' else -1

        if ((neighbor, portal_type), next_level) in new_visited:
            continue

        if neighbor == 'AA':
            continue

        if next_level > max_level or next_level < 0:
            continue

        else:
            distance = distance_to_destination(graph, (neighbor, portal_type, next_level, dist), dest_node,
                                           new_visited, max_level)

        distances.add(distance + current_dist)

    smallest_distance = inf if len(distances) == 0 else min(distances)

    return smallest_distance


with open('input.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph = build_graph(grid, find_portals=True)

# Part 1
distances = find_shortest_paths(graph, ('AA', 'o'))
print(distances[('ZZ', 'o')])

# Part 2
distance = distance_to_destination(graph, ('AA', 'o', 0, 0), 'ZZ', [], 25)
print(distance)
