"""
Class for strategies
"""

import os
import sys

sys.path.append(os.path.abspath("./"))
from scooter import *

CHARGING_SLOT = 250
"number of time steps between two potential charging slots"
DISCHARGE_THRESHOLD = 20
"threshold below which  we initiate a recharging tour [%]"
PICK_UP_THERSHOLD = 30
"threshlod below which we pick a scooter during a recharging tour [%]"
DISCHARGED_PROPORTION = 0.2
"proportion of the total fleet below which we initiate the recharging tour"
CHARGING_LEVEL = 80