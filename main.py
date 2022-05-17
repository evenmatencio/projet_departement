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
SIZE_OF_FLEET = 10
"number of scooter in our simulation"
BEGIN_HOUR = 0
"hour of the begining of the simulation"


if __name__ == "__main__":

    first_strategy = ChargingStrategy(TIME_RANGE, SIZE_OF_FLEET)
    first_strategy.set_parameters(charging_slot = 200, discharged_proportion = 80, discharge_threshold = 20,
                                  pick_up_threshold = 20, charging_level = 80)
    first_strategy.launch()

