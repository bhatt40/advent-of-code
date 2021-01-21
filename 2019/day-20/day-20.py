from node_graph import build_graph
from collections import defaultdict
from math import inf


def fix_graph(graph):
    graph_2 = {}
    nodes_to_ignore = set()
    for node, neighbors in graph.items():
        if node in nodes_to_ignore:
            continue
        new_neighbors = neighbors.copy()
        portal = None
        for neighbor, distance in neighbors.items():
            if distance == 1:
                # This is a portal.
                portal = neighbor
                del new_neighbors[portal]

                # Add it to nodes_to_ignore so it'll get skipped. Copy its neighbors over to this node.
                nodes_to_ignore.add(portal)
                for other_neighbor, other_distance in graph[portal].items():
                    if other_neighbor != node:
                        new_neighbors[other_neighbor] = min(
                            other_distance - 2,
                            neighbors[other_neighbor] - 2 if other_neighbor in neighbors else inf
                        )

            else:
                new_neighbors[neighbor] = distance - 2

        new_node = '{}{}'.format(node, portal) if portal else node
        graph_2[new_node] = new_neighbors

    # Replace neighbors with portals.
    graph_3 = {}
    for node, neighbors in graph_2.items():
        new_neighbors = {}
        for neighbor, distance in neighbors.items():
            for portal in graph_2.keys():
                if neighbor in portal:
                    new_neighbors[portal] = distance
        graph_3[node] = new_neighbors

    return graph_3


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
            distances[neighbor] = min(distances[neighbor], distances[current_node] + dist)

    return distances


with open('test.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph = build_graph(grid)
graph = fix_graph(graph)
distances = find_shortest_paths(graph, 'AA')
print(distances)
