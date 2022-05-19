import os
import sys

import numpy as np

sys.path.append(os.path.abspath("./"))

from scooter import *
from strategy import *

# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

TIME_RANGE = 5000
"number of steps of the simulation"
SIZE_OF_FLEET = 100
"number of scooter in our simulation"



if __name__ == "__main__":

    strategy = ChargingStrategy(TIME_RANGE, SIZE_OF_FLEET, render=False)
    strategy.set_parameters(charging_slot = 250, discharged_proportion = 0.20, discharge_threshold = 20,
                                  pick_up_threshold = 30, charging_level = 80)
    strategy.launch()

    strategy.init_plot()
    strategy.points.append(strategy.ax.plot(INTEREST_POINT_2.x, INTEREST_POINT_2.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    strategy.points.append(strategy.ax.plot(INTEREST_POINT_1.x, INTEREST_POINT_1.y, marker='s', linestyle='None', markersize=10, color='b')[0])
    plt.show()

