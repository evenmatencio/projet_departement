import os
import sys

import numpy as np

sys.path.append(os.path.abspath("./"))

from scooter import *
from strategy import *
import json

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

TIME_RANGE = 5*DAY_LENGTH
'''number of steps of the simulation'''
SIZE_OF_FLEET = 100
'''number of scooter in our simulation'''


# -------------------------------------------------------------------------------------------------------------------
# BODY OF THE CODE
# -------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    '''
    TOUTES LES GRANDEURS DOIVENT ETRE DONNEES EN NOMBRE DE TIME_STEP.
    '''

    '''
    REMARQUES :
    Nombre de trajet par jour dans les bons ordres de grandeur, en adéquation avec l'étude sur austin et autres.
    Expliquer comment on été calibré les couts :     strategy.set_parameters(charging_slot = DAY_LENGTH//3, discharged_proportion = 0.20, discharge_threshold = 20,
                            pick_up_threshold = 30, charging_level = 80) donne transport_cost=278.419052451516  et repartition_cost=376.8368831790888
    '''

    results_list = []
    id = 0
    for discharged_thresh in np.linspace(10, 30, 1):
        for discharged_prop in np.linspace(0.2, 0.7, 1):
            for pick_up_threhs in np.linspace(15, 25, 1):
                for charging_lev in np.linspace(75, 85, 1):
                    for charg_slot in [DAY_LENGTH//3]:#, DAY_LENGTH//2, DAY_LENGTH, 2*DAY_LENGTH]:
                        print(f"\n Simulation n°{id}")
                        # Running the simulation
                        strategy = FirstChargingStrategy(TIME_RANGE, SIZE_OF_FLEET, render=False, verbose=True)
                        strategy.set_parameters(charging_slot=charg_slot, discharged_proportion=discharged_prop,
                                                discharge_threshold=discharged_thresh,
                                                pick_up_threshold=pick_up_threhs, charging_level=charging_lev)
                        strategy.launch()
                        # Storing the data
                        param = {"charging_slot" : charg_slot, "discharged_proportion" : discharged_prop,
                                 "discharge_threshold" : discharged_thresh, "pick_up_thershold" : pick_up_threhs,
                                 "charging_level" : charging_lev}
                        cost = {"transport" : strategy.transporting_cost, "distribution" : strategy.repartition_cost}
                        simulation = {"id" : id,  "param" : param, "cost" : cost}
                        id+=1
                        results_list.append(simulation)

    print("\n ________________________________ \n")
    print(f"Nombre simul = {len(results_list)}")
    print(f"Premier simul")
    print(results_list[0])

    with open('simul1_output.json', 'w') as outfile:
        json.dump(results_list, outfile)










    # strategy.init_plot()
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_2.x, INTEREST_POINT_2.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_1.x, INTEREST_POINT_1.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # plt.show()

