from queue import PriorityQueue
from point import Point
from vector import Vector


class LIAN:
    def __init__(self, image, start_point: Point, end_point: Point, max_angle, delta):
        self.image = image
        self.start_point = start_point
        self.end_point = end_point

        # максимальный угол не может быть отрицательным и больше 2pi
        if max_angle <= 0 or max_angle >= 360:
            raise Exception('Max angle should be in range (0; 360) degrees!')

        self.max_angle = max_angle
        self.delta = delta
        self.__closed = []
        pass

    # построение прямой при помощи алгоритма Брезенхема
    def __get_bresenham_line(self, start_point: Point, end_point: Point):
        line_points = []

        dx = end_point.x - start_point.x
        dy = end_point.y - start_point.y

        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if dx < 0:
            dx = -dx
        if dy < 0:
            dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = start_point.x, start_point.y
        line_points.append(start_point)

        error, t = el / 2, 0

        while t < el:
            error -= es

            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1

            line_points.append(Point(x, y))

        return line_points

    def __check_point_existance(self, point: Point):
        limit_x, limit_y = self.image.shape[1], self.image.shape[0]

        if 0 <= point.x < limit_x and 0 <= point.y < limit_y:
            return True
        return False

    # получение окружности при помощи Midpoint algorithm
    def __get_midpoint_circle(self, center: Point):
        circle_points = []

        x_centre = center.x
        y_centre = center.y

        x = self.delta
        y = 0

        if self.__check_point_existance(Point(x + x_centre, y + y_centre)):
            circle_points.append(Point(x + x_centre, y + y_centre))

        if (self.delta > 0):
            if self.__check_point_existance(Point(x + x_centre, -y + y_centre)):
                circle_points.append(
                    Point(x + x_centre, -y + y_centre))  # right
            if self.__check_point_existance(Point(y + x_centre, x + y_centre)):
                circle_points.append(
                    Point(y + x_centre, x + y_centre))  # bottom
            if self.__check_point_existance(Point(-x + x_centre, -y + y_centre)):
                circle_points.append(
                    Point(-x + x_centre, -y + y_centre))  # left
            if self.__check_point_existance(Point(y + x_centre, -x + y_centre)):
                circle_points.append(Point(y + x_centre, -x + y_centre))  # top

        P = 1 - self.delta

        while x > y:

            y += 1

            if P <= 0:
                P = P + 2 * y + 1
            else:
                x -= 1
                P = P + 2 * y - 2 * x + 1

            if (x < y):
                break

            if self.__check_point_existance(Point(x + x_centre, y + y_centre)):
                circle_points.append(Point(x + x_centre, y + y_centre))
            if self.__check_point_existance(Point(-x + x_centre, y + y_centre)):
                circle_points.append(Point(-x + x_centre, y + y_centre))
            if self.__check_point_existance(Point(x + x_centre, -y + y_centre)):
                circle_points.append(Point(x + x_centre, -y + y_centre))
            if self.__check_point_existance(Point(-x + x_centre, -y + y_centre)):
                circle_points.append(Point(-x + x_centre, -y + y_centre))

            if x != y:
                if self.__check_point_existance(Point(y + x_centre, x + y_centre)):
                    circle_points.append(Point(y + x_centre, x + y_centre))
                if self.__check_point_existance(Point(-y + x_centre, x + y_centre)):
                    circle_points.append(Point(-y + x_centre, x + y_centre))
                if self.__check_point_existance(Point(y + x_centre, -x + y_centre)):
                    circle_points.append(Point(y + x_centre, -x + y_centre))
                if self.__check_point_existance(Point(-y + x_centre, -x + y_centre)):
                    circle_points.append(Point(-y + x_centre, -x + y_centre))

        return circle_points

    # проверка пути на наличие препятствий
    def __check_path_available(self, line):
        for point in line:
            if self.image[point.y, point.x] == 0:
                return False

        return True

    # получение итогового пути
    def __get_path(self):
        path = []
        current_point = self.end_point.previous_point

        while current_point != self.start_point:
            bresenham_line = self.__get_bresenham_line(
                current_point.previous_point, current_point)

            path.extend(bresenham_line)
            current_point = current_point.previous_point

        path.append(self.start_point)
        return list(reversed(path))

    # генерация точек для дальнейшего перехода
    def __generate_successors(self, circle_center: Point):
        successors = []
        vec1 = Vector(circle_center.previous_point, circle_center)

        # строим окружность, выбираем из нее только конкрентый кусок, соответствующий углу + незанятые точки
        circle_points = self.__get_midpoint_circle(circle_center)
        for point in circle_points:
            vec2 = Vector(circle_center, point)

            if point in self.__closed or \
                self.image[point.y, point.x] == 0 or \
                ((circle_center != self.start_point) and (Vector.angle_between(vec1, vec2) > self.max_angle)) or \
                    not self.__check_point_existance(point):
                continue

            successors.append(point)

        vec2 = Vector(circle_center, self.end_point)

        if Vector(circle_center, self.end_point).get_length() < self.delta and Vector.angle_between(vec1, vec2) < self.max_angle:
            successors.append(self.end_point)

        return successors

    def execute(self):
        open = PriorityQueue()
        self.start_point.previous_point = self.start_point
        open.put((0, self.start_point))

        while not open.empty():
            _, point = open.get()

            bresenham_line = self.__get_bresenham_line(
                point.previous_point, point)

            self.__closed.append(point)

            # проверка проходимости тропы
            if self.__check_path_available(bresenham_line):
                # проверка достижения конечной точки
                if point == self.end_point:
                    self.end_point.previous_point = point.previous_point
                    return self.__get_path()

                successors = self.__generate_successors(point)

                for point_to_go in successors:
                    weight = Vector(point_to_go, self.end_point).get_length()
                    point_to_go.previous_point = point

                    open.put((weight, point_to_go))

        return False
