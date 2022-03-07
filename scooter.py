"""
Class for scooters
"""

import os
import sys

sys.path.append(os.path.abspath("./"))

from points import *


class Scooter():

    def __init__(self, coord = Point(0,0), soc=100):
        """
        :param coord: initial coordinates of the scooter
        :param soc: state of charge in percentage
        """
        self._soc = soc
        self._coord = coord
        self._moving = False
        self._destination = self._coord

    @property
    def coord(self):
        return self._coord

    @property
    def soc(self):
        return self._soc

    @property
    def moving(self):
         return self._moving

    @property
    def destination(self):
        return self._destination

    @coord.setter
    def coord(self, new_coord):
        assert new_coord.x > 0 and new_coord.y > 0, "negative coordinates"
        self._coord = new_coord

    @soc.setter
    def soc(self, new_soc):
        assert new_soc >= 0. and new_soc <= 100., "not a percentage"
        self._soc = new_soc

    @moving.setter
    def moving(self, b):
        self._moving = b



    def move(self):
        assert self.moving == True, "not moving"
        if self.coord.x != self.destination.x :
            self.coord.x = (self.coord.x + (self.destination.x - self.coord.x)/abs(self.destination.x - self.coord.x))
        elif self.coord.y != self.destination.y :
            self.coord.y = (self.coord.y + (self.destination.y - self.coord.y)/abs(self.destination.y - self.coord.y))
        if self.coord == self.destination :
            self.moving = False


if __name__ == "__main__" :

    scooter = Scooter()
    scooter.moving = True
    scooter._destination = Point(10, 10)

    scooter.move()
    print(scooter.coord)



