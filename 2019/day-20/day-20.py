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


with open('test.txt', 'r') as f:
    grid = [
        line.split('\n')[0] for line in f.readlines()
    ]

graph = build_graph(grid, find_portals=True)
distances = find_shortest_paths(graph, 'AA')
print(sum(distances['ZZ']))
