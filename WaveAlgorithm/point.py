class Point:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def __str__(self) -> str:
        return f'{self.__x}:{self.__y}'