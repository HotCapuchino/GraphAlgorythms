import cv2
from skimage.measure import label, regionprops
from matplotlib import pyplot as plt
import numpy as np
from enum import Enum
import math
from graph import Graph
from point import Point


class ImageTypesEnum(Enum):
    Default = 1,
    Binarized = 2,


class ImageUtilsClass:
    def __init__(self) -> None:
        self.__image = None
        self.__binarized_image = None

    def __rough_binarization(self, image):
        r_m, b_m, g_m = image[:, :, 0], image[:, :, 1], image[:, :, 2]

        black = 0
        white = 255

        r_m = np.where(r_m > black, black, white)
        b_m = np.where(b_m > black, black, white)
        g_m = np.where(g_m > black, black, white)

        return np.dstack(tup=(r_m, b_m, g_m))

    def __clean_image(self, thresholded):
        labeled = label(thresholded, 255, connectivity=2)

        regions = regionprops(labeled)

        region_amount = 0
        average_region_area = 0
        acc = 0

        for region in regions:
            region_amount += 1
            acc += region.area

        average_region_area = acc/region_amount

        for region in regions:
            bbox = region.bbox

            if region.area < average_region_area * 0.08:
                labeled[bbox[0]:bbox[3], bbox[1]:bbox[4]] = [0, 0, 0]

        return labeled

    def binarize(self):
        image = cv2.medianBlur(self.__image, 5)

        _, thresholded = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY)
        labeled = self.__clean_image(thresholded)

        self.__binarized_image = self.__rough_binarization(labeled)
        return self.__binarized_image

    def read_img(self, filename):
        self.__image = cv2.cvtColor(cv2.imread(
            filename, cv2.IMREAD_GRAYSCALE), cv2.COLOR_BGR2RGB)

        return self.__image

    def show_image(self, im_type):
        if im_type == ImageTypesEnum.Default:
            if self.__image is None:
                print('Image has not been loaded yet!')
            else:
                plt.imshow(self.__image)
                plt.show()
            return
        elif im_type == ImageTypesEnum.Binarized:
            if self.__binarized_image is None:
                print('Image has not been binarized yet!')
            else:
                plt.imshow(self.__binarized_image)
                plt.show()
            return

        print('Provide ImageTypesEnum value as func param!')

    # TODO: нарисовать путь 
    def draw_the_way(self, way):
        pass

    def get_graph(self, image=None) -> Graph:
        target_image = image if image else self.__image

        if target_image is None:
            print('You have not provided image or image has not been loadaed yet!')
            return

        target_image = np.array(target_image)

        nodes = []
        init_graph = {}

        x_vector = [-1, 0, 1, 1, 1, 0, -1, -1]
        y_vector = [-1, -1, -1, 0, 1, 1, 1, 0]

        for y in range(target_image.shape[0]):
            for x in range(target_image.shape[1]):
                node = Point(x, y)
                node_string = str(node)

                nodes.append(node_string)
                init_graph[node_string] = {}

                for i in range(len(x_vector)):
                    target_x = x + x_vector[i]
                    target_y = y + y_vector[i]

                    if target_x < 0 or target_y < 0 or target_x >= target_image.shape[1] or target_y >= target_image.shape[0]:
                        continue

                    adjacent_node = Point(target_x, target_y)

                    distance = math.sqrt(
                        2) if target_x + target_y == 0 else 1

                    init_graph[node_string][str(adjacent_node)] = distance

        graph = Graph(nodes, init_graph, False)
        return graph
