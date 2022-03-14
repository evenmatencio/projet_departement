"""
Class for scooters
"""

import os
import sys

sys.path.append(os.path.abspath("./"))

from points import *

import matplotlib.pyplot as plt


class Scooter():

    def __init__(self, coord=Point(0, 0), soc=100):
        """
        :param coord: initial coordinates of the scooter
        :param soc: state of charge in percentage
        """
        self._soc = soc
        self._coord = coord
        self._moving = False
        self._destination = self._coord
        self._mass_user = rd.randint(50,120)

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

    @property
    def mass_user(self):
        return self._mass_user

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

    @destination.setter
    def destination(self, destin):
        self._destination = destin

    def move(self):
        assert self.moving == True, "not moving"
        if self.coord.x != self.destination.x:
            self.coord.x = (self.coord.x + (self.destination.x - self.coord.x) / abs(self.destination.x - self.coord.x))
            self.soc = self.soc-100*(50/20000)*(1+(self.mass_user-70)/70)
        elif self.coord.y != self.destination.y:
            self.coord.y = (self.coord.y + (self.destination.y - self.coord.y) / abs(self.destination.y - self.coord.y))
            self.soc = self.soc - 100 * (50 / 20000) * (1 + (self.mass_user - 70) / 70)
        if self.coord == self.destination:
            self.moving = False

    def init_new_trip(self,t):
        if(self.moving==False):
            



def simulation():
    scooter = Scooter()
    scooter.moving = True
    scooter._destination = Point(10, 10)
    x = [scooter.coord.x]
    y = [scooter.coord.y]
    while (scooter.coord != scooter.destination):
        scooter.move()
        x.append(scooter.coord.x)
        y.append(scooter.coord.y)
    return x, y



if __name__ == "__main__":
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='2d')

    x, y = simulation()

    # # create the first plot
    # point, = ax.plot([x[0]], [y[0]], 'o')
    # line, = ax.plot(x, y, z, label='parametric curve')
    # ax.legend()
    # ax.set_xlim([-1, 10])
    # ax.set_ylim([-1, 10])
    #
    # ani = animation.FuncAnimation(fig, update_point, 15, fargs=(x, y, point))

    fig, ax = plt.subplots()

    for t in range(50):
        if t == 0:
            points, = ax.plot(x[0], y[0], marker='s', linestyle='-', color='g')
            ax.set_xlim(-1, 11)
            ax.set_ylim(-1, 11)
        else:
            if(t==8):
                points.set_color('r')
                points.set_marker('o')
            new_x = x[t]
            new_y = y[t]
            points.set_data(new_x, new_y)

        plt.pause(0.5)

    # plt.show()
