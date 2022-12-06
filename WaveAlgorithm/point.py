class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'{self.x}:{self.y}'

    def __eq__(self, point: object) -> bool:
        if isinstance(point, Point):
            return self.x == point.x and self.y == point.y

        if type(point) == 'str':
            return str(self) == point

        return False

    def __lt__(self, point: object) -> bool:
        if isinstance(point, Point):
            return str(self) < str(point)

        raise Exception
