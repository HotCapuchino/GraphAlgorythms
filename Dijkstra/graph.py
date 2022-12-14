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
                if graph[adjacent_node].get(node, False) == False and not self.oriented:
                    graph[adjacent_node][node] = value

        return graph

    def get_node_neighbours(self, node):
        connections = []

        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def get_edge_weight(self, start_node, end_node):
        return self.graph[start_node][end_node]

    def print_graph(self):
        for node, edges in self.graph.items():
            for adjacent_node, value in edges.items():
                print(f'{node} -> {adjacent_node}: {value}')
