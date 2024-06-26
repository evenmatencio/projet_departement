import os
import sys
import time

import numpy as np

sys.path.append(os.path.abspath("./"))

from scooter import *
from strategy import *
import json

from multiprocessing import Pool

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

TIME_RANGE =  2*DAY_LENGTH  #5*DAY_LENGTH
'''number of steps of the simulation'''
SIZE_OF_FLEET = 100
'''number of scooter in our simulation'''


def exec_simul(input):
    strategy = FirstChargingStrategy(TIME_RANGE, SIZE_OF_FLEET, interest_pt= [INTEREST_POINT_2, INTEREST_POINT_1], render=False, verbose=False)
    strategy.set_parameters(charging_slot=input[0], discharged_proportion=input[1],
                            discharge_threshold=input[2], pick_up_threshold=input[3], charging_level=input[4],
                            location_nbr=100, scoot_max_per_loc=100)
    strategy.launch()
    # Storing the data
    param = {"charging_slot": input[0], "discharged_proportion": input[1],
             "discharge_threshold": input[2], "pick_up_threshold": input[3],
             "charging_level": input[4]}
    cost = {"transport": strategy.transporting_cost, "distribution": strategy.repartition_cost}
    total_cost = strategy.transporting_cost + strategy.repartition_cost
    benef = strategy.benefice
    simulation = {"id": input[5], "param": param, "cost": cost, "total_cost": total_cost, "benefice": benef}
    return simulation


# -------------------------------------------------------------------------------------------------------------------
# BODY OF THE CODE
# -------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    '''
    TOUTES LES GRANDEURS DOIVENT ETRE DONNEES EN NOMBRE DE TIME_STEP.
    
    La variable inputs_list est une liste contenant des jeux de parameres sur lesquels doivent etre lancees les simulations.
    '''


    results_list = []
    id = 0
    charging_lev = 80
    inputs_list = []
    for discharged_thresh in np.linspace(10, 30, 6):  # 30 6
        for discharged_prop in np.linspace(0.2, 0.8, 4):  # 0.8 4
            for pick_up_threhs in np.linspace(15, 24, 4):  #15 24 4
                for charg_slot in [2*3600/TIME_STEP, 3*3600/TIME_STEP, 4*3600/TIME_STEP, 6*3600/TIME_STEP, 12*3600/TIME_STEP, 24*3600/TIME_STEP]: #, DAY_LENGTH // 2, DAY_LENGTH]:
                    # print(f"\n Simulation n°{id}")
                    inputs_list.append([charg_slot, discharged_prop, discharged_thresh, pick_up_threhs, charging_lev, id])
                    id+=1

                    # # Running the simulation
                    # strategy = FirstChargingStrategy(TIME_RANGE, SIZE_OF_FLEET, render=False, verbose=False)
                    # strategy.set_parameters(charging_slot=charg_slot, discharged_proportion=discharged_prop,
                    #                         discharge_threshold=discharged_thresh,
                    #                         pick_up_threshold=pick_up_threhs, charging_level=charging_lev)
                    # strategy.launch()
                    # # Storing the data
                    # param = {"charging_slot" : charg_slot, "discharged_proportion" : discharged_prop,
                    #          "discharge_threshold" : discharged_thresh, "pick_up_threshold" : pick_up_threhs,
                    #          "charging_level" : charging_lev}
                    # cost = {"transport" : strategy.transporting_cost, "distribution" : strategy.repartition_cost}
                    # total_cost = strategy.transporting_cost + strategy.repartition_cost
                    # simulation = {"id" : id,  "param" : param, "cost" : cost, "total_cost" : total_cost}
                    # id+=1
                    # results_list.append(simulation)
    with Pool(60) as p:
        results_list = p.map(exec_simul, inputs_list)


    # print("\n ________________________________ \n")
    # print(f"Nombre simul = {len(results_list)}")
    # print(f"Premier simul")
    # print(results_list[0])

    #
    # with open('loop_ChrgSlt_new_bit.json', 'w') as outfile:


    with open('simul_smart_back1_output.json', 'w') as outfile:
        json.dump(results_list, outfile)

    # strategy.init_plot()
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_2.x, INTEREST_POINT_2.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_1.x, INTEREST_POINT_1.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # plt.show()


    '''
    REMARQUES :
    Nombre de trajet par jour dans les bons ordres de grandeur, en adéquation avec l'étude sur austin et autres.
    Expliquer comment on été calibré les couts :     strategy.set_parameters(charging_slot = DAY_LENGTH//3, discharged_proportion = 0.20, discharge_threshold = 20,
                            pick_up_threshold = 30, charging_level = 80) donne transport_cost=278.419052451516  et repartition_cost=376.8368831790888
    '''