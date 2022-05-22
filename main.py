import os
import sys

import numpy as np

sys.path.append(os.path.abspath("./"))

from scooter import *
from strategy import *

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

DAY_LENGHT = int(24*3600 / TIME_STEP)
'''The number of time_step in a day'''
TIME_RANGE = DAY_LENGHT
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
    Expliquer comment on été calibré les couts.
    '''

    strategy = FirstChargingStrategy(TIME_RANGE, SIZE_OF_FLEET, render=False, verbose=False)
    strategy.set_parameters(charging_slot = DAY_LENGHT//4, discharged_proportion = 0.20, discharge_threshold = 20,
                            pick_up_threshold = 30, charging_level = 80)
    strategy.launch()
    print(strategy.total_departures)

    # strategy.init_plot()
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_2.x, INTEREST_POINT_2.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # strategy.points.append(strategy.ax.plot(INTEREST_POINT_1.x, INTEREST_POINT_1.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    # plt.show()

