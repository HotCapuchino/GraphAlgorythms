import random
from image_utils import ImageTypesEnum, ImageUtilsClass
from point import Point
from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt

neighbourhood_8 = [(-1, -1), (0, -1), (1, -1), (1, 0),
                   (1, 1), (0, 1), (-1, 1), (-1, 0)]


def check_boundaries(image, point: Point):
    width = image.shape[1]
    height = image.shape[0]

    return point.x >= 0 and point.x < width and point.y >= 0 and point.y < height


def wave_algorithm(image, start_point: Point, end_point: Point):
    q = PriorityQueue()
    wavefront_label = 1

    wavefront_labeled = np.zeros_like(image)

    q.put((wavefront_label, start_point))
    wavefront_labeled[start_point.y, start_point.x] = wavefront_label
    iterations = 0

    while not q.empty():
        iterations += 1
        current_label, current_node = q.get()

        if current_label == end_point:
            break

        for coords in neighbourhood_8:
            x_offset, y_offset = coords
            x = current_node.x + x_offset
            y = current_node.y + y_offset

            neighbour = Point(x, y)

            if check_boundaries(image, neighbour):
                if wavefront_labeled[y, x] == 0 and image[y, x] == 1:
                    new_wavefront_label = current_label + 1

                    q.put((new_wavefront_label, neighbour))
                    wavefront_labeled[y, x] = new_wavefront_label

    return wavefront_labeled


def get_randomized_min_index(labels):
    min_val = min(labels)
    min_indices = []

    for i, label in enumerate(labels):
        if label == min_val:
            min_indices.append(i)

    return min_indices[random.randint(0, len(min_indices) - 1)]


def get_path(wavefront_labeled, start_point: Point, end_point: Point):
    current_label = wavefront_labeled[end_point.y, end_point.x]
    current_node = end_point

    labeled_copy = np.copy(wavefront_labeled)
    labeled_copy[end_point.y, end_point.x] = 0

    visited = [current_node]
    path = [(current_node, current_label)]

    iterations = 0
    while current_node != start_point:
        iterations += 1
        next_found = False

        next_nodes = []
        next_nodes_labels = []

        for coords in neighbourhood_8:
            x_offset, y_offset = coords
            x = current_node.x + x_offset
            y = current_node.y + y_offset

            neighbour = Point(x, y)

            if check_boundaries(wavefront_labeled, neighbour):
                if wavefront_labeled[y, x] <= current_label and wavefront_labeled[y, x] != 0 and str(neighbour) not in visited:
                    next_nodes.append(neighbour)
                    next_nodes_labels.append(wavefront_labeled[y, x])

        if len(next_nodes_labels):
            i = get_randomized_min_index(next_nodes_labels)

            if i >= 0:
                current_node = next_nodes[i]
                labeled_copy[current_node.y, current_node.x] = 0
                current_label = next_nodes_labels[i]
                next_found = True

                path.append((current_node, current_label))
                visited.append(str(current_node))

        if not next_found:
            path.pop()
            current_node, current_label = path[-1]

    path = np.array(path)[:, 0]
    return path


im_utils = ImageUtilsClass()

print('binarizing image...')
im_utils.read_img('res/map.bmp')
binarized = im_utils.binarize()
im_utils.show_image(ImageTypesEnum.Binarized)


# FIXME: внимание, хардкод!
start_point = Point(8, 85)
end_point = Point(1320, 920)

print('building wave front...')
wavefront_labeled = wave_algorithm(binarized, start_point, end_point)

plt.imshow(wavefront_labeled)
plt.show()

print('constructing shortest path...')
path = get_path(wavefront_labeled, start_point, end_point)

im_utils.draw_the_path(path)
im_utils.show_image(ImageTypesEnum.WithPath)
