"""
Class for integer points
"""

import random as rd

class Point():

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, nx):
        self._x = int(nx)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, ny):
        self._y = int(ny)

    @staticmethod
    def from_random(x_max, y_max):
        """
        :param x_max:
        :param y_max:
        :return: an integer point randomly created, with coordinate x in [0, x_max] and y in [0, y_max]
        """
        assert x_max >0 and y_max>0,  "negative entries"
        return Point(rd.randint(0, x_max-1), rd.randint(0, y_max-1))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, point2):
        return self.x == point2.x and self.y == point2.y


if __name__ == "__main__":

    p = Point.from_random(189, 8)
    print(p)





