import csv

from graph import Graph


class GraphReader:
    @staticmethod
    def read_graph(filename, mode='csv') -> Graph:
        file = open(filename, 'r')

        if mode == 'csv':
            csv_reader = csv.reader(file)
            next(csv_reader)

            nodes = []
            init_graph = {}
            oriented = False

            for row in csv_reader:
                node1, conn_type, node2, weight = row[0], row[1], row[2], int(
                    row[3])

                if node1 not in nodes:
                    nodes.append(node1)
                    init_graph[node1] = {}

                if node2 not in nodes:
                    nodes.append(node2)
                    init_graph[node2] = {}

                if conn_type == '->' or conn_type == '=>':
                    init_graph[node1][node2] = weight
                    oriented = True
                elif conn_type == '<-' or conn_type == '<=':
                    init_graph[node2][node1] = weight
                    oriented = True
                elif conn_type == '<->' or conn_type == '<=>':
                    init_graph[node1][node2] = weight
                    init_graph[node2][node1] = weight

            graph = Graph(nodes, init_graph, oriented)
            return graph

        file.close()
