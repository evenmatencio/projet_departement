"""
Class for strategies
"""

import os
import sys

sys.path.append(os.path.abspath("./"))
from scooter import *


# CHARGING_SLOT = 250
# "number of time steps between two potential charging slots"
# DISCHARGE_THRESHOLD = 20
# "threshold below which  we initiate a recharging tour [%]"
# PICK_UP_THERSHOLD = 30
# "threshlod below which we pick a scooter during a recharging tour [%]"
# DISCHARGED_PROPORTION = 0.2
# "proportion of the total fleet below which we initiate the recharging tour"
# CHARGING_LEVEL = 80
#
# MIN_DISTANCE = 50
#
#
# def back_in_town(fleet):
#     placed = False
#     while placed == False:
#         point = Point.from_random(MAP_SIZE, MAP_SIZE)
#         far_enough = True
#         for other_scoot in fleet:
#             if ((point - other_scoot.coord).norm2() < MIN_DISTANCE):
#                 far_enough = False
#         if far_enough:
#             return point


# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

USED_COLORS = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
BATTERY_COLORS = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=USED_COLORS, N=100)
'''Variables used to define the render of battery's level of the scooters'''


# -------------------------------------------------------------------------------------------------------------------
# CLASS DEFINITION
# -------------------------------------------------------------------------------------------------------------------

class ChargingStrategy():

    def __init__(self, time_range, nbr_scooters):
        self.time_range = time_range
        self.nbr_scooters = nbr_scooters
        self.list_of_scooter = init_new_fleet(self.nbr_scooters)
        self.time = 0
        self.init_plot()
        self.set_up = False


    def set_parameters(self, charging_slot, discharged_proportion, discharge_threshold, pick_up_threshold, charging_level):
        self.set_up = True
        # set to true once the parameters of the strategy are defined
        self.charging_slot = charging_slot
        # number of time steps between two potential charging slots
        self.discharged_proportion = discharged_proportion
        # proportion of the total fleet below which we initiate the recharging tour
        self.discharge_threshold = discharge_threshold
        # threshold below which  we recharge the considered scooter [%]
        self.pick_up_threshold = pick_up_threshold
        # threshlod below which we pick a scooter during a recharging tour [%]
        self.charging_level = charging_level
        # level under which we stop charging a scooter
        self.charging_duration = CHARGING_DURATION*self.charging_level


    def launch(self):
        assert self.set_up, "The strategy parameters are not defined !"
        # Environment evolution
        while self.time < self.time_range:
            for t in range(self.charging_slot):
                self.step()
                plt.pause(0.01)
            # Distribution of the charged scooters
            recharged_list = [i for i in range(len(self.list_of_scooter)) if
                              self.list_of_scooter[i].charging_time >= self.charging_duration]
            self.distribution(recharged_list)
            # Charging the scooters that need it
            discharged_list = [(scooter.soc < self.discharge_threshold and not scooter.moving)
                               for scooter in self.list_of_scooter]
            self.charging(discharged_list)




    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.points = []
        for scooter in self.list_of_scooter:
            self.points.append(self.ax.plot(scooter.coord.x, scooter.coord.y, marker='s', linestyle='None', color='r')[0])
        self.ax.set_xlim(-20, MAP_SIZE + 20)
        self.ax.set_ylim(-20, MAP_SIZE + 20)


    def step(self):
        self.time += 1
        for (i, scooter) in enumerate(self.list_of_scooter):
            # Updating state
            scooter.temperature_evolution()
            # if scooter.temperature > maxtemp:
            #     maxtemp = scooter.temperature
            # if scooter.temperature < mintemp:
            #     mintemp = scooter.temperature
            if scooter.charging:
                scooter.charging_time = scooter.charging_time + 1
            else:
                if scooter.moving:
                    scooter.move()
                elif (not scooter.moving) and (scooter.soc >= 0):
                    scooter.init_new_trip(self.time, 0)
                # Updating plot
                new_x = scooter.coord.x
                new_y = scooter.coord.y
                self.points[i].set_data(new_x, new_y)
                self.points[i].set_color(BATTERY_COLORS(int(scooter.soc)))
                if scooter.moving:
                    self.points[i].set_marker('o')
                else:
                    self.points[i].set_marker('s')


    def distribution(self, recharged_list):
        if len(recharged_list) > 1:
           for j in recharged_list:
                self.list_of_scooter[j].charging_time = 0
                self.list_of_scooter[j].charging = False
                init_pos = Point.from_random(MAP_SIZE, MAP_SIZE)
                self.list_of_scooter[j].coord = init_pos
                self.list_of_scooter[j].moving = False
                self.points[j].set_data(init_pos.x, init_pos.y)
                self.points[j].set_color(BATTERY_COLORS(int(self.list_of_scooter[j].soc)))
                self.points[j].set_marker('s')


    def charging(self, discharged_list):
        if sum(discharged_list) >= int(self.nbr_scooters * self.discharged_proportion):
            for (i, scooter) in enumerate(self.list_of_scooter):
                if (scooter.soc < self.pick_up_threshold) and (not scooter.moving) :
                    scooter.charging = True
                    scooter.charging_time = 0
                    points[i].set_data(-20, -20)
                    points[i].set_color("black")
                    scooter.soc = self.charging_level
