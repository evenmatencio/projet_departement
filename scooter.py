"""
Class for scooters
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import numpy as np
import random as rd
import math

sys.path.append(os.path.abspath("./"))
from points import *

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------


SPACE_STEP = 50
'''The distance separating two points of the map such that norm2(point1-point2) = 1 [meter]'''
MAP_SIZE = 200
'''The size of the map on which the scooters move [SPACE_STEP]'''

CHARGING_DURATION = 1500
'''Average duration of the charging of a scooter'''
AMBIENT_TEMPERATURE = 293
'''Temperature in Celsius'''
EXCHANGE_SURFACE = 1 #0.05 on prends 1 en considérant que le R=0.75 prends deja en compte la surface
'''Surface of exchange with ambient air'''
BATTERY_MASS = 4
'''Mass in kilograms'''
BATTERY_THERMAL_CAPACITY = 1054
'''mass thermal capacity'''
STEEL_CONDUCTIVITY = 50
'''Thermic conductivity'''
BATTERY_EXTERIOR_WIDTH = 0.01



class Scooter():
    # -------------------------------------------------------------------------------------------------------------------
    # CLASS VARIABLES AND INITIALIZER
    # -------------------------------------------------------------------------------------------------------------------

    AVERAGE_TOTAL_DISTANCE = 20000
    "Average distance ran by a fully charged scooter [meter]"
    AVERAGE_MASS = 70
    "Averge mass of the scooters'users [kilogram]"

    def __init__(self, coord=Point(0, 0), soc=100):
        """
        :param coord: initial coordinates of the scooter
        :param soc: state of charge in percentage
        """
        self._soc = soc
        self._coord = coord
        self._moving = False
        self._destination = self._coord
        self._charging = False
        self._charging_time = 0
        self._mass_user = rd.randint(self.AVERAGE_MASS - 20, self.AVERAGE_MASS + 50)
        self._temperature = AMBIENT_TEMPERATURE

    # -------------------------------------------------------------------------------------------------------------------
    # READERS AND WRITERS
    # -------------------------------------------------------------------------------------------------------------------

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

    @property
    def charging(self):
        return self._charging

    @property
    def charging_time(self):
        return self._charging_time

    @property
    def temperature(self):
        return self._temperature

    @coord.setter
    def coord(self, new_coord):
        assert new_coord.x >= 0 and new_coord.y >= 0, "negative coordinates"
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

    @mass_user.setter
    def mass_user(self, new_mass):
        self._mass_user = new_mass

    @charging.setter
    def charging(self, in_charge):
        self._charging = in_charge

    @charging_time.setter
    def charging_time(self, time):
        self._charging_time = time

    @temperature.setter
    def temperature(self, temp):
        assert temp >= 0, "temperature not negative"
        self._temperature = temp

    # -------------------------------------------------------------------------------------------------------------------
    # OTHER METHODS
    # -------------------------------------------------------------------------------------------------------------------

    def estim_consumption(self, new_destination):
        consumption = abs(self.coord.x - new_destination.x) * 100 * (SPACE_STEP / self.AVERAGE_TOTAL_DISTANCE) * (
                1 + ((self.mass_user - self.AVERAGE_MASS) / self.AVERAGE_MASS))
        consumption += abs(self.coord.y - new_destination.y) * 100 * (SPACE_STEP / self.AVERAGE_TOTAL_DISTANCE) * (
                1 + ((self.mass_user - self.AVERAGE_MASS) / self.AVERAGE_MASS))
        return consumption

    def move(self):
        """
        This method performs one step of simulation.
        A scooter first moves on x_axis and after on y_axis.
        """
        assert self.moving, "not moving"
        if (self.soc - 100 * (SPACE_STEP / self.AVERAGE_TOTAL_DISTANCE) * (
                1 + ((self.mass_user - self.AVERAGE_MASS) / self.AVERAGE_MASS)) >= 0):
            if self.coord.x != self.destination.x:
                self.coord.x = \
                    (self.coord.x + (self.destination.x - self.coord.x) / abs(self.destination.x - self.coord.x))
                self.soc = self.soc - 100 * (SPACE_STEP / self.AVERAGE_TOTAL_DISTANCE) * \
                           (1 + ((self.mass_user - self.AVERAGE_MASS) / self.AVERAGE_MASS))
            elif self.coord.y != self.destination.y:
                self.coord.y = (
                        self.coord.y + (self.destination.y - self.coord.y) / abs(self.destination.y - self.coord.y))
                self.soc = self.soc - 100 * (SPACE_STEP / self.AVERAGE_TOTAL_DISTANCE) * \
                        (1 + ((self.mass_user - self.AVERAGE_MASS) / self.AVERAGE_MASS))
            if self.coord == self.destination:
                self.moving = False
        else:
            self.moving = False

    def temperature_evolution(self):
        if not self.moving:
            for i in range(7):
                self.temperature = self.temperature + (1 / (BATTERY_MASS * BATTERY_THERMAL_CAPACITY)) * (
                        (AMBIENT_TEMPERATURE - self.temperature) * (
                            1/0.75) * EXCHANGE_SURFACE) + int(self.moving)*0.016
            self.temperature = self.temperature + (0.2 / (BATTERY_MASS * BATTERY_THERMAL_CAPACITY)) * (
                    (AMBIENT_TEMPERATURE - self.temperature) * (
                        1/0.75) * EXCHANGE_SURFACE) + 0.2*int(self.moving)*0.016
        if self.moving:
            for i in range(7):
                self.temperature = self.temperature + (1 / (BATTERY_MASS * BATTERY_THERMAL_CAPACITY)) * (
                        (AMBIENT_TEMPERATURE - self.temperature) * (
                            1/0.375) * EXCHANGE_SURFACE) + int(self.moving)*0.016
                self.temperature = self.temperature + 0.016
            self.temperature = self.temperature + (0.2 / (BATTERY_MASS * BATTERY_THERMAL_CAPACITY)) * (
                    (AMBIENT_TEMPERATURE - self.temperature) * (
                        1/0.375) * EXCHANGE_SURFACE) + 0.2*int(self.moving)*0.016
            self.temperature = self.temperature + 0.016 * 0.2

    def init_new_trip(self, t, begin_hour):
        p = rd.random()
        proba = (0.25 / math.sqrt(2 * np.pi)) * (np.exp(-(give_time(t, begin_hour) - 8 * 3600) ** 2 / (2 * 3600 ** 2)) +np.exp(-(give_time(t, begin_hour) - 18 * 3600) ** 2 / (2 * 3600 ** 2)))
        if p < proba:
            print(f"p={p}, proba={proba}")
            self.mass_user = rd.randint(self.AVERAGE_MASS - 20, self.AVERAGE_MASS + 50)
            new_destin = Point.from_random(MAP_SIZE, MAP_SIZE)
            while (self.coord - new_destin).norm2() < 4 :
                new_destin = Point.from_random(MAP_SIZE, MAP_SIZE)
            if (self.estim_consumption(new_destin) <= self.soc):
                self.destination = new_destin
                self.moving = True


def init_new_fleet(nbr_scooter):
    list_of_scooter = []
    for i in range(nbr_scooter):
        list_of_scooter.append(Scooter(Point.from_random(MAP_SIZE, MAP_SIZE)))
    return list_of_scooter


def give_time(t, begin_hour=0):
    '''
    :param t: total time elapsed since the beginning of the simulation in [s]
    :param begin_hour: hour of the beginning of the simulation in [h]
    :return: the current time in second during in the frame of the current day
    '''
    return (begin_hour*3600 + 7.2*t) % 24*3600


def simulation():
    scooter = Scooter()
    scooter.moving = True
    scooter._destination = Point(10, 10)
    x = [scooter.coord.x]
    y = [scooter.coord.y]
    soc = [scooter.soc]
    while (scooter.coord != scooter.destination):
        scooter.move()
        x.append(scooter.coord.x)
        y.append(scooter.coord.y)
        soc.append(scooter.soc)
    return x, y, soc


if __name__ == "__main__":

    x, y, soc = simulation()
    fig, ax = plt.subplots()

    for t in range(50):
        if t == 0:
            points, = ax.plot(x[0], y[0], marker='s', linestyle='None', color='g')
            ax.set_xlim(-1, 11)
            ax.set_ylim(-1, 11)
        else:
            if (soc[t] <= 98):
                points.set_color('r')
                points.set_marker('o')
            print(soc[t])
            new_x = x[t]
            new_y = y[t]
            points.set_data(new_x, new_y)

        plt.pause(0.5)

    plt.show()
