import os
import sys

import six

sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np

sys.path.append(os.path.abspath("./"))
from scooter import *

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

DISTANCE_FOR_DISTRIBUTION = 5
'''the distance under which you don't have a penalty for the lack of response to the demand [space_step]'''
COST_DISTANCE_TRAVELLED = 0.0195
'''gasoline consumption per unit of distance time price of gasoline plus amortisation of the pick-up vehicle'''
MIN_BATTERY_LEVEL = 25
'''minimal required level of battery for considering that a scooter is available in a given zone'''
AVERAGE_TRIP_DURATION = 12
'''Avergar trip duration in [minutes] taken from https://www.sciencedirect.com/science/article/pii/S2214367X19303126?ref=pdf_download&fr=RR-2&rr=70dc7315287a403d'''


BEGIN_HOUR = 0
"hour of the begining of the simulation"

# -------------------------------------------------------------------------------------------------------------------
# SOME FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------

'''
WHAT COULD BE DONE FOR COMPUTING TH EOPPORTUNITY COST :

- every AVERAGE_TRIP_DURATION we compute the opportunity cost

- we use a spatial and temporal ponderation

'''


def unitary_opportunity_cost(location='Paris'):
    if location == 'Paris':
        unlock_cost = 1
        cost_per_minute = 0.15  # https://www.tunneltime.io/en/paris-france/lime
        return AVERAGE_TRIP_DURATION * cost_per_minute + unlock_cost


def space_demand(t):
    # renvoyer un coefficient lie a la demande spatiale
    return 1


def time_demand(t):
    # ici faudra ameliorer en prenant une fonction qui prends en compte la demande future
    proba = 1
    for s in range(250):
        proba *= (INTER_ARRIVAL_FACTOR / (SIGMA * math.sqrt(2 * np.pi))) * (
                    np.exp(-(give_time(t + s, BEGIN_HOUR) - 8 * 3600) ** 2 / (2 * SIGMA ** 2)) + np.exp(
            -(give_time(t + s, BEGIN_HOUR) - 18 * 3600) ** 2 / (2 * SIGMA ** 2)))
    return 1-proba


def near_enough(list_of_scooters, i, j):
    founded = False
    current_point = Point(i, j)
    index = 0
    nbr_scooter = len(list_of_scooters)
    while (not founded) and index < nbr_scooter:
        difference = list_of_scooters[index].coord - current_point
        distance = difference.norm2()
        if distance <= DISTANCE_FOR_DISTRIBUTION and list_of_scooters[index].soc > MIN_BATTERY_LEVEL:
            founded = True
        index += 1
    return founded


def measure_distribution(list_of_scooters, t):
    unitary_cost = unitary_opportunity_cost()
    time_ponderation = time_demand(t)
    space_ponderation = space_demand(t)
    cost_of_distribution = 0
    for i in range(0, MAP_SIZE, 5):
        for j in range(0, MAP_SIZE, 5):
            if not (near_enough(list_of_scooters, i, j)):
                cost_of_distribution += time_ponderation * space_ponderation * unitary_cost
    return cost_of_distribution


def transport_cost(returning_scooters):
    list_of_coords = []
    for i in range(len(returning_scooters)):
        list_of_coords.append((returning_scooters[i].coord.x, returning_scooters[i].coord.x))
    list_of_coords.append((-20, -20))
    problem_no_fit = mlrose.TSPOpt(length=len(list_of_coords), coords=list_of_coords, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, random_state=2)
    return COST_DISTANCE_TRAVELLED * best_fitness
