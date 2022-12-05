class Graph:
    def __init__(self, nodes, init_graph, oriented=False):
        self.nodes = nodes
        self.oriented = oriented
        self.graph = self.__construct_graph(nodes, init_graph)
        self.node_labels = self.__init_node_labels()

    def __construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False and not self.oriented:
                    graph[adjacent_node][node] = value

        return graph

    def __init_node_labels(self):
        node_labels = {}

        for node, edges in self.graph.items():
            for adjacent_node in edges.keys():
                node_labels.update({adjacent_node: -1})
            node_labels.update({node: -1})

        return node_labels

    def set_node_wave_label(self, node, value):
        self.node_labels[node] = value

    def get_node_wave_label(self, node):
        return self.node_labels[node]

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

    def debug_print_wave_labels(self):
        print(self.node_labels) 
