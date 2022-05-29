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

SPATIAL_COST_PONDERATION = 2*math.sqrt(SPATIAL_SIGMA)
TEMPORAL_COST_PONDERATION = 4*2*143*4/(3*5)
#Diviser par 5 pour compenser le fait qu'on calcule les couts 5 fois plus dans la journee
#On multiplie par 4 pour compenser les descentes successives du cout de distribution : s'adapter en permanence

BEGIN_HOUR = 0
"hour of the begining of the simulation"

# -------------------------------------------------------------------------------------------------------------------
# SOME FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------

'''
WHAT COULD BE DONE FOR COMPUTING THE OPPORTUNITY COST :

- every AVERAGE_TRIP_DURATION we compute the opportunity cost

- we use a spatial and temporal ponderation

'''


def unitary_opportunity_cost(location='Paris'):
    if location == 'Paris':
        unlock_cost = 1
        cost_per_minute = 0.15  # https://www.tunneltime.io/en/paris-france/lime
        return AVERAGE_TRIP_DURATION * cost_per_minute + unlock_cost


def time_demand(t):
    proba = 1
    for s in range(250):
        proba *= 1 - time_distribution(s + t)
    return proba


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
    time_ponderation = TEMPORAL_COST_PONDERATION*time_distribution(t)
    cost_of_distribution = 0
    nbr_found = 0
    for i in range(0, MAP_SIZE, 5):
        for j in range(0, MAP_SIZE, 5):
            space_ponderation = SPATIAL_COST_PONDERATION * spatial_distribution(Point(i, j))
            if not (near_enough(list_of_scooters, i, j)):
                cost_of_distribution += time_ponderation * space_ponderation * unitary_cost
                #print(f"(i, j) = ({i}, {j})")
                #print(f"unitar c_f_d : {time_ponderation * space_ponderation * unitary_cost}")
            else :
                nbr_found+=1
                # cost_of_distribution -= time_ponderation * space_ponderation * unitary_cost
    return cost_of_distribution, nbr_found


def transport_cost(transported_scooters):
    list_of_coords = []
    for i in range(len(transported_scooters)):
        list_of_coords.append((transported_scooters[i].coord.x, transported_scooters[i].coord.x))
    list_of_coords.append((-20, -20))
    problem_no_fit = mlrose.TSPOpt(length=len(list_of_coords), coords=list_of_coords, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, random_state=2)
    return COST_DISTANCE_TRAVELLED * best_fitness


if __name__ == "__main__":

    temps = range(0, int(24*3600 / TIME_STEP))
    temp_distri_function = [time_distribution(t) for t in temps]
    plt.plot([TIME_STEP*t/3600 for t in temps], temp_distri_function)
    plt.title("Temporal distribution of the demand (not normalized)")
    plt.xlabel("Time [in h]")
    plt.show()




    # reference_proba = 1
    # time_for_20_min = int(20*60 / TIME_STEP)
    # init_time = (8*3600 - 600) / TIME_STEP
    # for t in range(time_for_20_min):
    #     reference_proba *= pow(time_distribution(init_time + t), 1/time_for_20_min)
    #
    # coef = 0.9 / reference_proba
    # print(coef)

    # print((3600 / TIME_STEP))
