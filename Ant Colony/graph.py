from operator import index


class Graph(object):
    def __init__(self, nodes, init_graph, oriented=False):
        self.nodes = nodes
        self.oriented = oriented
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                # ставим феромоны
                graph[node][adjacent_node] = {
                    'weight': value, 'feromones': 0.2}

                if graph[adjacent_node].get(node, False) == False and not self.oriented:
                    graph[adjacent_node][node] = {
                        'weight': value, 'feromones': 0.2}

        return graph

    def get_node_neighbours(self, node):
        connections = []

        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)

        return connections

    def get_edge_info(self, start_node, end_node):
        return self.graph[start_node][end_node]

    def print_graph(self):
        for node, edges in self.graph.items():
            for adjacent_node, value in edges.items():
                print(f'{node} -> {adjacent_node}: {value}')

    def set_edge_feromones(self, start_node, end_node, feromones):
        self.graph[start_node][end_node]['feromones'] = feromones

    def get_nodes_amount(self):
        return len(self.nodes)

    def get_edges(self):
        graph_edges = []

        for node, edges in self.graph.items():
            for adjacent_node, value in edges.items():
                edge = {'start': node, 'end': adjacent_node, 'info': value}
                # исключение двунаправленных вершин
                if edge not in graph_edges and {'start': adjacent_node, 'end': node, 'info': value} not in graph_edges:
                    graph_edges.append(edge)

        return graph_edges
