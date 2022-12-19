import math
from point import Point


class Vector:
    def __init__(self, start_point: Point, end_point: Point):
        self.start = start_point
        self.end = end_point

    def get_coords(self):
        return Point(self.end.x - self.start.x, self.end.y - self.start.y)

    def get_length(self):
        coords = self.get_coords()

        return math.sqrt(coords.x ** 2 + coords.y ** 2)

    @staticmethod
    def angle_between(vector1, vector2):
        vec1_coords = vector1.get_coords()
        vec2_coords = vector2.get_coords()

        dot_product = vec1_coords.x * vec2_coords.x + vec1_coords.y * vec2_coords.y
        multiplication = vector1.get_length() * vector2.get_length()

        if multiplication == 0:
            return 0

        return round(math.acos(dot_product / round(multiplication)) * (180 / math.pi))
