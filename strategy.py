"""
Class for strategies
"""

import os
import sys
import random

sys.path.append(os.path.abspath("./"))
from Costs import *



# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

COST_COMPUTATION_STEP = 5*(3600 / TIME_STEP)
'''Number of time step separating two computations of the cost.'''

USED_COLORS = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
BATTERY_COLORS = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=USED_COLORS, N=100)
'''Variables used to define the render of battery's level of the scooters'''

MIN_DISTANCE = MAP_SIZE//10



# -------------------------------------------------------------------------------------------------------------------
# USEFUL FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------


def smart_back_in_town(fleet):
    placed = False
    while placed == False:
        point = Point.from_random(MAP_SIZE, MAP_SIZE)
        p = rd.random()
        if p < 2*SPATIAL_PONDERATION*spatial_distribution(point):
            far_enough = True
            for other_scoot in fleet:
                if ((point - other_scoot.coord).norm2() < MIN_DISTANCE):
                    far_enough = False
            if far_enough:
                return point

def smart_back_in_town1(fleet):
    placed = False
    attemps = 0
    max_attemps = 10
    best_proba = 0
    # ne pas mettre max_attempts trop grand sinon on va vraiment concentrer les trots aux zones d'affluences
    while not placed and attemps < max_attemps:
        point = Point.from_random(MAP_SIZE, MAP_SIZE)
        p = rd.random()
        proba_point = SPATIAL_PONDERATION*spatial_distribution(point)
        attemps += 1
        if p < SPATIAL_PONDERATION*spatial_distribution(point):
            far_enough = True
            for other_scoot in fleet:
                if ((point - other_scoot.coord).norm2() < MIN_DISTANCE):
                    far_enough = False
            if far_enough:
                return point


def silly_back_in_town(fleet):
    placed = False
    while placed == False:
        point = Point.from_random(MAP_SIZE, MAP_SIZE)
        far_enough = True
        for other_scoot in fleet:
            if ((point - other_scoot.coord).norm2() < 2):  #MIN_DISTANCE):
                far_enough = False
        if far_enough:
            return point



# -------------------------------------------------------------------------------------------------------------------
# CLASS DEFINITION
# -------------------------------------------------------------------------------------------------------------------

class FirstChargingStrategy():

    def __init__(self, time_range, nbr_scooters, interest_pt, render=True, verbose=True):
        self.time_range = time_range
        self.nbr_scooters = nbr_scooters
        self.interest_pt = interest_pt
        self.list_of_scooter = init_new_fleet(self.nbr_scooters)
        self.time = 0
        self.set_up = False
        self.transporting_cost = 0.
        self.nbr_found = 0
        self.repartition_cost = 0.
        self.benefice = 0
        self.verbose = verbose
        self.render = render
        self.total_departures = 0
        if self.render :
            self.init_plot()


    def set_parameters(self, discharged_proportion, discharge_threshold, pick_up_threshold, charging_level,
                       location_nbr, scoot_max_per_loc, charging_slot=0):
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
        # charging_duration of the scooters
        self.set_redistribution_locations(location_nbr, scoot_max_per_loc)
        self.init_smart_positon()



    def set_redistribution_locations(self, location_nbr, scoot_max_per_loc):
        '''
        :param location_nbr: number of location at which the fully charged scooters are droped
        :param scoot_max_per_loc: maximum number of scooters per location
        '''
        assert location_nbr*scoot_max_per_loc > int(1.5*len(self.list_of_scooter)), "not enough available locations for redistribution"
        self.redistri_pts_loc = []
        self.loc_nbr = location_nbr

        # Choosing locations near the center points
        for p in self.interest_pt:
            self.redistri_pts_loc.append({'loc':Point(min(p.x + MAP_SIZE//20, MAP_SIZE), p.y), \
                                          'max_nbr': int(1.5*scoot_max_per_loc),'current_nbr':0})
            # self.redistri_pts_loc.append({'loc':Point(p.x,  max(p.y, MAP_SIZE - MAP_SIZE//10)), \
            #                               'max_nbr':scoot_max_per_loc, 'current_nbr': 0})
            # self.redistri_pts_loc.append({'loc':Point(max(p.x - MAP_SIZE//20, MAP_SIZE), p.y), \
            #                               'max_nbr':scoot_max_per_loc,'current_nbr':0})
            self.redistri_pts_loc.append({'loc':Point(p.x,  min(p.y + MAP_SIZE//20, MAP_SIZE)), \
                                          'max_nbr':int(1.5*scoot_max_per_loc), 'current_nbr': 0})
        self.redistri_pts_loc = self.redistri_pts_loc[:location_nbr]

        # Choosing the remaining points randomly
        for i in range(location_nbr - len(self.redistri_pts_loc)) :
            placed = False
            while not placed :
                new_p = Point.from_random(int(0.8*MAP_SIZE), int(0.8*MAP_SIZE))
                new_p.x += int(0.1*MAP_SIZE)
                new_p.y += int(0.1*MAP_SIZE)
                far_enough = True
                for loc_dict in self.redistri_pts_loc :
                    if ((new_p - loc_dict['loc']).norm2() < MIN_DISTANCE):
                        far_enough*=False
                if far_enough :
                    self.redistri_pts_loc.append({'loc': new_p, 'max_nbr': int(0.5*scoot_max_per_loc), 'current_nbr': 0})
                    placed = True


    def init_smart_positon(self):
        for i in range(len(self.list_of_scooter)):
            point = self.smart_back_in_town0(i)
            self.list_of_scooter[i].coord = point


    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.points = []
        for scooter in self.list_of_scooter:
            self.points.append(self.ax.plot(scooter.coord.x, scooter.coord.y, marker='s', linestyle='None', markersize=5, color='r')[0])
        self.ax.set_xlim(-20, MAP_SIZE + 20)
        self.ax.set_ylim(-20, MAP_SIZE + 20)


    def smart_back_in_town0(self, scooter_index):
        scooter = self.list_of_scooter[scooter_index]
        placed = False
        loc_index = random.randint(0, self.loc_nbr - 1)
        i = 0
        point = None
        while not placed and i<self.loc_nbr:
            loc_index = (loc_index+i)%(self.loc_nbr)
            location = self.redistri_pts_loc[loc_index]
            if location["current_nbr"] < location["max_nbr"]:
                scooter.redistri_loc = loc_index
                point = location["loc"]
                placed = True
                location["current_nbr"] += 1
            i+=1
        return point



    def launch(self):
        assert self.set_up, "The strategy parameters are not defined !"
        # Environment evolution
        while self.time < self.time_range:
            # first_discharged = False
            # soc_list = [scoot.soc for scoot in self.list_of_scooter]
             # Stepping the environment
            self.step()
            # if min(soc_list)<20 and not first_discharged :
            #     first_discharged =True
            #     soc_list_dis = [scoot.soc for scoot in self.list_of_scooter if scoot.soc < 20]
            #     print(f"Nombre de trot en dessous de 20 : {len(soc_list_dis)}")
            #     print(f"Premiere trot dechargee en {self.time} time-step")
            # Some outputs
            if (self.verbose and self.time % DAY_LENGTH == 0 ):
                print("\n")
                print(f"we did {self.time} time-steps")
                print("--------------------------------")
                print(f"transport_cost={self.transporting_cost}")
                print(f"repartition_cost={self.repartition_cost}")
                print(f'nbr_foud = {self.nbr_found}')
            # Charging and replacing the scooters
            if self.time % self.charging_slot == 0 :
                # Distribution of the charged scooters
                recharged_list = [i for i in range(len(self.list_of_scooter)) if
                                  self.list_of_scooter[i].charging_time >= self.charging_duration]
                self.distribution(recharged_list)
                # Charging the scooters that need it
                discharged_list = [(scooter.soc < self.discharge_threshold and not scooter.moving)
                                   for scooter in self.list_of_scooter]
                self.charging(discharged_list)
            # Computing the cost
            if self.time % COST_COMPUTATION_STEP == 0:
                repartition_cost, nbr_found = measure_distribution(self.list_of_scooter, self.time)
                self.repartition_cost += repartition_cost
                self.nbr_found += nbr_found


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
                        self.redistri_pts_loc[scooter.redistri_loc]['current_nbr'] -= 1
                        self.total_departures+=1
                        self.benefice += scooter.cost_of_trip()
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
                init_pos = silly_back_in_town(self.list_of_scooter)
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






class SecondChargingStrategy(FirstChargingStrategy):
    '''
    The difference between the first class of strategies and this one is that we check whether we have to charge the scooters
    only when self.time reaches fixed instants in the day (like 0.0PM) instead of doing it each self.charging_slot instants
    '''

    def set_parameters(self, discharged_proportion, discharge_threshold, pick_up_threshold, charging_level, charging_slot):
        super(SecondChargingStrategy, self).set_parameters(discharge_threshold, pick_up_threshold, charging_level, discharged_proportion)
        self.charging_times = {11*3600, 22*3600}


    def launch(self):
        assert self.set_up, "The strategy parameters are not defined !"
        # Environment evolution
        while self.time < self.time_range:
            # Stepping the environment
            self.step()
            # Some outputs
            if (self.verbose and self.time % 400 == 0):
                print("\n")
                print(f"we did {self.time} time-steps")
                print("--------------------------------")
                print(f"transport_cost={self.transporting_cost}")
                print(f"repartition_cost={self.repartition_cost}")
                print(f"benefice = {self.benefice}")
            # Charging and replacing the scooters
            if self.time%DAY_LENGTH in self.charging_times:
                # Distribution of the charged scooters
                recharged_list = [i for i in range(len(self.list_of_scooter)) if
                                  self.list_of_scooter[i].charging_time >= self.charging_duration]
                self.distribution(recharged_list)
                # Charging the scooters that need it
                discharged_list = [(scooter.soc < self.discharge_threshold and not scooter.moving)
                                   for scooter in self.list_of_scooter]
                self.charging(discharged_list)
                self.repartition_cost += measure_distribution(self.list_of_scooter, self.time)[0]
                self.nbr_found += measure_distribution(self.list_of_scooter, self.time)[1]
            # Computing the cost
            if self.time % COST_COMPUTATION_STEP == 0:
                self.repartition_cost += measure_distribution(self.list_of_scooter, self.time)
