from node_graph import build_graph
from collections import defaultdict
from math import inf


def find_shortest_paths(graph, src):
    distances = defaultdict(lambda: (inf, 0))
    distances[src] = (0, -1)
    complete_set = set()
    incomplete_set = set(graph.keys())

    while len(incomplete_set) > 0:
        current_node = min(incomplete_set, key=lambda x: distances[x][0])
        portals_passed_to_current_node = distances[current_node][1]
        complete_set.add(current_node)
        incomplete_set.remove(current_node)

        neighbors = graph[current_node]
        for neighbor, dist in neighbors.items():
            new_dist = distances[current_node][0] + dist[0]
            if new_dist < distances[neighbor][0]:
                distances[neighbor] = (new_dist, portals_passed_to_current_node + 1)

    return distances


# def find_shortest_paths_with_levels(graph, src, dest):
#     distances = defaultdict(lambda: (inf, 0, 0))
#     distances[src] = (0, -1, 0)  # (distance, number of portals passed, level)
#     # distances = defaultdict(lambda: (inf, 0))
#     # distances[src] = (0, -1)
#     complete_set = set()
#     # incomplete_set = set([
#     #     (k, l) for k in graph.keys() for l in range(max_levels)
#     # ])
#     incomplete_set = set(graph.keys())
#
#     while len(incomplete_set) > 0:
#         current_node = min(incomplete_set, key=lambda x: distances[x][0])
#         portals_passed_to_current_node = distances[current_node][1]
#         current_level = distances[current_node][2]
#
#         complete_set.add(current_node)
#         incomplete_set.remove(current_node)
#
#         neighbors = graph[current_node]
#         for neighbor, (dist, portal_type) in neighbors.items():
#             new_dist = distances[current_node][0] + dist
#             if new_dist < distances[neighbor][0]:
#                 new_level = current_level + 1 if portal_type == 'i' else current_level - 1
#                 # if neighbor == dest and current_level != 0:
#                 if neighbor == dest:
#                     continue
#                 distances[neighbor] = (new_dist, portals_passed_to_current_node + 1, new_level)
#
#     return distances

def distance_to_destination(graph, current, dest_node, visited, previous_neighbors, max_level, stored_distances):
    print(visited)
    current_node, current_portal_type, current_level, current_dist = current
    new_visited = visited.copy()
    new_visited.append((current_node, current_level))

    neighbors = graph[current_node]
    distances = set()
    new_previous_neighbors = set([
        (k, t) for k, (d, t) in neighbors.items()
    ]) | {(current_node, current_portal_type)}

    for neighbor, (dist, portal_type) in neighbors.items():
        # If a neighbor was in the previous set of neighbors, then it was on the other side of the portal that we
        # just crossed, so it should be ignored.
        if (neighbor, portal_type) in previous_neighbors:
            continue

        next_level = (current_level + 1) if portal_type == 'i' else (current_level - 1)
        if (neighbor, next_level) in new_visited:
            continue

        if neighbor == 'AA':
            continue

        if neighbor == 'ZZ':
            if current_level == 0:
                distances.add(current_dist + dist)
            continue

        if next_level > max_level or next_level < 0:
            continue

        if (neighbor, next_level) in stored_distances:
            distance = stored_distances[(neighbor, next_level)]
        else:
            distance = distance_to_destination(graph, (neighbor, portal_type, next_level, dist), dest_node,
                                           new_visited, new_previous_neighbors, max_level, stored_distances)
            stored_distances[(neighbor, next_level)] = distance

        distances.add(distance + current_dist)

    if len(distances) == 0:
        return inf

    return min(distances)


with open('test.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph = build_graph(grid, find_portals=True)

# Part 1
# distance = find_shortest_paths(graph, 'AA')
# print(distance)

# Part 2
distance = distance_to_destination(graph, ('AA', 'o', 0, 0), 'ZZ', [], set(), 30, {})
print(distance)