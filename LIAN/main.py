from image_utils import ImageTypesEnum, ImageUtilsClass
from point import Point
from lian import LIAN


im_utils = ImageUtilsClass()

print('binarizing image...')
im_utils.read_img('res/map.bmp')
binarized = im_utils.binarize()
im_utils.show_image(ImageTypesEnum.Binarized)

# FIXME: внимание, хардкод!
start_point = Point(8, 85)
end_point = Point(1320, 920)
max_angle = 50
delta = 30

print('searching for an optimal path...')
lian = LIAN(binarized, start_point, end_point, max_angle,  delta)
path = lian.execute()

if path:
    for point in path:
        im_utils.draw_the_path(path)

    im_utils.show_image(ImageTypesEnum.WithPath)
else:
    print('path wasn\'t found!')
