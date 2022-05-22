"""
Class for strategies
"""

import os
import sys

sys.path.append(os.path.abspath("./"))
from scooter import *
from Costs import *


MIN_DISTANCE = 2



def back_in_town(fleet):
    placed = False
    while placed == False:
        point = Point.from_random(MAP_SIZE, MAP_SIZE)
        far_enough = True
        for other_scoot in fleet:
            if ((point - other_scoot.coord).norm2() < MIN_DISTANCE):
                far_enough = False
        if far_enough:
            return point


# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

COST_COMPUTATION_STEP = 4*(3600 / TIME_STEP)
'''Number of time step separating two computations of the cost.'''

USED_COLORS = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
BATTERY_COLORS = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=USED_COLORS, N=100)
'''Variables used to define the render of battery's level of the scooters'''


# -------------------------------------------------------------------------------------------------------------------
# CLASS DEFINITION
# -------------------------------------------------------------------------------------------------------------------

class ChargingStrategy():

    def __init__(self, time_range, nbr_scooters, render=True, verbose=True):
        self.time_range = time_range
        self.nbr_scooters = nbr_scooters
        self.list_of_scooter = init_new_fleet(self.nbr_scooters)
        self.time = 0
        self.set_up = False
        self.transporting_cost = 0
        self.repartition_cost = 0
        self.verbose = verbose
        self.render = render
        self.total_departures = 0
        if self.render :
            self.init_plot()


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
        self.charging_duration = CHARGING_DURATION


    def launch(self):
        assert self.set_up, "The strategy parameters are not defined !"
        # Environment evolution
        while self.time < self.time_range:
            # Stepping the environment
            self.step()
            # Some outputs
            if (self.verbose and self.time % 400 == 0 ):
                print("\n")
                print(f"we did {self.time} time-steps")
                print("--------------------------------")
                print(f"transport_cost={self.transporting_cost}")
                print(f"repartition_cost={self.repartition_cost}")
            # Charging and replacing the scooters
            if self.time % self.charging_slot == 0 :
                # Distribution of the charged scooters
                recharged_list = [i for i in range(len(self.list_of_scooter)) if
                                  self.list_of_scooter[i].charging_time >= self.charging_duration]
                print(f"recharged list len = {len(recharged_list)}")
                print(f"time charging for scoot 0 = {self.list_of_scooter[0].charging_time}")
                self.distribution(recharged_list)
                # Charging the scooters that need it
                discharged_list = [(scooter.soc < self.discharge_threshold and not scooter.moving)
                                   for scooter in self.list_of_scooter]
                self.charging(discharged_list)
                self.repartition_cost += measure_distribution(self.list_of_scooter, self.time)
            # Computing the cost
            if self.time % COST_COMPUTATION_STEP == 0:
               self.repartition_cost += measure_distribution(self.list_of_scooter, self.time)



    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.points = []
        for scooter in self.list_of_scooter:
            self.points.append(self.ax.plot(scooter.coord.x, scooter.coord.y, marker='s', linestyle='None', markersize=5, color='r')[0])
        self.ax.set_xlim(-20, MAP_SIZE + 20)
        self.ax.set_ylim(-20, MAP_SIZE + 20)


    def step(self):
        self.time += 1
        for (i, scooter) in enumerate(self.list_of_scooter):
            # Updating state
            scooter.temperature_evolution()
            if scooter.charging:
                scooter.charging_time = scooter.charging_time + 1
            else:
                if scooter.moving:
                    scooter.move()
                elif (not scooter.moving) and (scooter.soc >= 0):
                    if scooter.init_new_trip(self.time, BEGIN_HOUR):
                        self.total_departures+=1
                # Updating plot
                if self.render :
                    new_x = scooter.coord.x
                    new_y = scooter.coord.y
                    self.points[i].set_data(new_x, new_y)
                    self.points[i].set_color(BATTERY_COLORS(int(scooter.soc)))
                    if scooter.moving:
                        self.points[i].set_marker('o')
                    else:
                        self.points[i].set_marker('s')
                    plt.pause(0.001)


    def distribution(self, recharged_list):
        list_returning_scooter=[]
        if len(recharged_list) > 1:
            for j in recharged_list:
                self.list_of_scooter[j].charging_time = 0
                self.list_of_scooter[j].charging = False
                init_pos = back_in_town(self.list_of_scooter)
                self.list_of_scooter[j].coord = init_pos
                self.list_of_scooter[j].moving = False
                list_returning_scooter.append(self.list_of_scooter[j])
                if self.render:
                    self.points[j].set_data(init_pos.x, init_pos.y)
                    self.points[j].set_color(BATTERY_COLORS(int(self.list_of_scooter[j].soc)))
                    self.points[j].set_marker('s')
            self.transporting_cost += transport_cost(list_returning_scooter)


    def charging(self, discharged_list):
        if sum(discharged_list) >= int(self.nbr_scooters * self.discharged_proportion):
            transported_scooters = []
            for (i, scooter) in enumerate(self.list_of_scooter):
                if (scooter.soc < self.pick_up_threshold) and (not scooter.moving) :
                    scooter.charging = True
                    scooter.charging_time = 0
                    scooter.soc = self.charging_level
                    transported_scooters.append(scooter)
                    if self.render :
                        self.points[i].set_data(-20, -20)
                        self.points[i].set_color("black")
            self.transporting_cost += transport_cost(transported_scooters)