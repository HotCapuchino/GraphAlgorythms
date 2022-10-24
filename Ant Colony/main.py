import operator
from functools import reduce
import random
from comb_utils import CombUtils

from opts import AntColonyAlgParams
from graph import Graph
from graph_reader import GraphReader


def get_proximity_const(weights):
    numerator = reduce(operator.mul, weights, 1)

    k = len(weights) - 1
    if k == 0:
        k = 1
    combs = CombUtils.getCombs(weights, k)

    muls = []

    for comb in combs:
        muls.append(reduce(operator.mul, comb, 1))

    denominator = sum(muls)

    return float(numerator) / denominator


def ant_colony(graph, start_node, end_node, alg_params):
    if not isinstance(graph, Graph):
        raise Exception('Graph param should be of type Graph!')

    if not isinstance(alg_params, AntColonyAlgParams):
        raise Exception('Alg params should be of type AntColonyAlgParams!')

    ant_pathes = []

    for i in range(alg_params.ant_amount):
        ant_pathes.append({'path': [], 'weight': 0})

    result = None

    while True:
        for i in range(alg_params.ant_amount):
            current_node = start_node
            visited_nodes = []
            # инициализация пути
            ant_pathes[i]['path'].append(current_node)

            while current_node != end_node:
                neighbours = graph.get_node_neighbours(current_node)

                ant_desires = []
                proximity_const = get_proximity_const(list(map(
                    lambda neighbour: graph.get_edge_info(current_node, neighbour)['weight'], neighbours)))

                # подсчет индивидуальных желаний
                for neighbour in neighbours:

                    # учет уже посещенных узлов для исключения цикличности
                    if not neighbour in visited_nodes:
                        edge_info = graph.get_edge_info(
                            current_node, neighbour)
                        feromone_amount = edge_info['feromones']
                        weight = edge_info['weight']

                        # желание муравья пойти в конкретную вершину
                        ant_desire = feromone_amount ** alg_params.alfa * \
                            (proximity_const / weight) ** alg_params.beta
                        ant_desires.append(
                            {'node': neighbour, 'desire': ant_desire})

                # сценарий, когда муравей попал в цикл
                if len(ant_desires) == 0:
                    break

                denominator = sum(
                    list(map(lambda val: val['desire'], ant_desires)))

                # числовая прямая вероятностей
                probabilities = []
                # для разложения на числовой прямой
                start = 0.0
                for ant_desire in ant_desires:
                    probability = ant_desire['desire'] / float(denominator)
                    end = start + probability

                    probabilities.append(
                        {'node': ant_desire['node'], 'start': start, 'end': end})
                    start = end

                random_probability = random.random()
                next_node = None

                # определение, в какую вершину пойдет муравей
                for prob in probabilities:
                    if prob['start'] <= random_probability and prob['end'] > random_probability:
                        next_node = prob['node']
                        break

                edge_weight = graph.get_edge_info(
                    current_node, next_node)['weight']

                ant_pathes[i]['path'].append(next_node)
                ant_pathes[i]['weight'] += edge_weight

                visited_nodes.append(current_node)
                current_node = next_node

        consistency_arr = len(ant_pathes) * [0.0]
        path_index = -1

        # проверка, какое кол-во муравьев прошли одним и тем же маршрутом
        for i in range(len(ant_pathes)):
            for j in range(len(ant_pathes)):
                if ant_pathes[i] == ant_pathes[j] and i != j:
                    consistency_arr[i] += 1

            # расчет согласованности
            if consistency_arr[i] / len(consistency_arr) >= alg_params.consistency_percentage:
                path_index = i
                break

        if path_index >= 0:
            result = ant_pathes[i]
            break
        else:
            # TODO: (выбрать делитель - 10 или 100?)
            q_coeff = max(
                list(map(lambda path: path['weight'], ant_pathes))) / 10

            feromone_coeffs = list(
                map(lambda path: q_coeff / path['weight'], ant_pathes))

            # испарение феромонов на гранях
            edges = graph.get_edges()
            for edge in edges:
                current_feromones = edge['info']['feromones'] * \
                    alg_params.after_evaporation
                graph.set_edge_feromones(
                    edge['start'], edge['end'], current_feromones)

            # расчет и добавление феромонов на грани графа
            for path_index, ant_path in enumerate(ant_pathes):
                actual_path = ant_path['path']

                for i in range(1, len(actual_path), 1):
                    current_feromones = graph.get_edge_info(
                        actual_path[i - 1], actual_path[i])['feromones']
                    current_feromones += feromone_coeffs[path_index]

                    graph.set_edge_feromones(
                        actual_path[i - 1], actual_path[i], current_feromones)

            ant_pathes = []

            for i in range(alg_params.ant_amount):
                ant_pathes.append({'path': [], 'weight': 0})

    return result


graph = GraphReader.read_graph('graph.csv')

alg_params = AntColonyAlgParams(0.5, 0.5, graph.get_nodes_amount(), 0.75, 0.33)
result = ant_colony(graph, '1', '9', alg_params)

print('Ants found the shortest way!')
path = ' -> '.join(result['path'])
print(path, 'with length of', result['weight'])
