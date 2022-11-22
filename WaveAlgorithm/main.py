from image_utils import ImageTypesEnum, ImageUtilsClass


def wave_algorithm():
    pass


im_utils = ImageUtilsClass()

im_utils.read_img('res/map.bmp')
binarized = im_utils.binarize()
# im_utils.show_image(ImageTypesEnum.Default)

graph = im_utils.get_graph()
graph.print_graph()


# FIXME: внимание, хардкод!
# start_x = 8
# start_y = 85

# end_x =
# end_y =
