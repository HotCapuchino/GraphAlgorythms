import sys
from graph_reader import GraphReader

from graph import Graph


def dijkstra(graph, start_node):
    if not isinstance(graph, Graph):
        raise Exception('Graph param should be of type Graph!')

    visited_nodes = []
    shortest_pathes = {}
    previous_nodes = {}

    for node in graph.nodes:
        shortest_pathes[node] = sys.maxsize

    shortest_pathes[start_node] = 0

    while len(visited_nodes) != len(graph.nodes):
        current_min_node = None
        unvisited_nodes = list(filter(
            lambda node: node not in visited_nodes, graph.nodes))

        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_pathes[node] < shortest_pathes[current_min_node]:
                current_min_node = node

        neighbors = graph.get_node_neighbours(current_min_node)

        for neighbor in neighbors:
            short_path = shortest_pathes[current_min_node] + \
                graph.get_edge_weight(current_min_node, neighbor)

            if short_path < shortest_pathes[neighbor]:
                shortest_pathes[neighbor] = short_path
                previous_nodes[neighbor] = current_min_node

        visited_nodes.append(current_min_node)

    return previous_nodes, shortest_pathes


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)

    print(
        f"Min path length from node '{start_node}' to node '{target_node}' is {shortest_path[target_node]}.")
    print("Whole path is:", " -> ".join(reversed(path)))


graph = GraphReader.read_graph('./graph.csv')

previous_nodes, shortest_path = dijkstra(graph, '1')
print_result(previous_nodes, shortest_path, '1', '9')
