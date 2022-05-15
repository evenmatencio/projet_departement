import os
import sys


import six
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np

sys.path.append(os.path.abspath("./"))
from scooter import *

DISTANCE_FOR_DISTRIBUTION = 5
"the distance under which you don't have a penalty for the lack of response to the demand"
COST_DISTANCE_TRAVELLED =  0.0195
"gasoline consumption per unit of idtance time price of gasoline plus amortisation of the pick-up vehicle"

def ponderation_demand(t):
    #ici faudra ameliorer en prenant une fonction qui prends en compte la demande future
    return 1

def near_enough(list_of_scooters,i,j):
    founded = False
    current_point = Point(i,j)
    index = 0
    nbr_scooter = len(list_of_scooters)
    while founded==False and index<nbr_scooter:
        difference = list_of_scooters[i].coord - current_point
        distance = difference.norm2
        if distance<=DISTANCE_FOR_DISTRIBUTION:
            founded = True
        i+=1
    return founded

def measure_distribution(list_of_scooters,t):
    cost_of_distribution = 0
    time_ponderation = ponderation_demand(t)
    for i in range(0,MAP_SIZE,5):
        for j in range(0,MAP_SIZE,5):
            if near_enough(list_of_scooters,i,j) == False:
                cost_of_distribution += time_ponderation*1
    return cost_of_distribution


def transport_cost(returning_scooters):
    list_of_coords=[]
    for i in range(len(returning_scooters)):
        list_of_coords.append((returning_scooters[i].coord.x,returning_scooters[i].coord.x))
    list_of_coords.apend((-20,-20))
    problem_no_fit = mlrose.TSPOpt(length=len(list_of_coords), coords=list_of_coords, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, random_state=2)
    return COST_DISTANCE_TRAVELLED*best_fitness