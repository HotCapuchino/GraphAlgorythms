import cv2
from skimage.measure import label, regionprops
from matplotlib import pyplot as plt
import numpy as np
from enum import Enum

from point import Point


class ImageTypesEnum(Enum):
    Default = 1,
    Binarized = 2,
    WithPath = 3


class ImageUtilsClass:
    def __init__(self) -> None:
        self.__image = None
        self.__binarized_image = None
        self.__with_path = None

    def __rough_binarization(self, image):
        r_m, b_m, g_m = image[:, :, 0], image[:, :, 1], image[:, :, 2]

        black = 0
        white = 255

        r_m = np.where(r_m > black, white, black)
        b_m = np.where(b_m > black, white, black)
        g_m = np.where(g_m > black, white, black)

        blacked = np.int64(
            np.all(np.dstack(tup=(r_m, b_m, g_m))[:, :, :-1] == 0, axis=2))

        return blacked

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
        elif im_type == ImageTypesEnum.WithPath:
            if self.__with_path is None:
                print('Path has not been painted yet!')
            else:
                plt.imshow(self.__with_path)
                plt.show()
            return

        print('Provide ImageTypesEnum value as func param!')

    def draw_the_path(self, path):
        if self.__image is None:
            print('Image has not been loaded yet!')
            return

        red = [170, 20, 90]
        image_copied = np.copy(self.__image)

        for point in path:
            if isinstance(point, Point):
                x, y = point.x, point.y
            else:
                x, y = str(point).split(":")[0], str(point).split(":")[1]

            image_copied[y, x] = red

        self.__with_path = image_copied
