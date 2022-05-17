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
BEGIN_HOUR = 0
"hour of the begining of the simulation"

# <<<<<<< HEAD
# if __name__ == "__main__":
#
#     fig, ax = plt.subplots()
#     used_colors = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
#     battery_colors = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=used_colors, N=100)
#
#     list_of_scooter = init_new_fleet(SIZE_OF_FLEET)
#     points = []
#
#     for scooter in list_of_scooter:
#         points.append(ax.plot(scooter.coord.x, scooter.coord.y, marker='s', linestyle='None', color='r')[0])
#     ax.set_xlim(-20, MAP_SIZE + 20)
#     ax.set_ylim(-20, MAP_SIZE + 20)
#
#     time = 0
#     maxtemp = AMBIENT_TEMPERATURE
#     mintemp = AMBIENT_TEMPERATURE
#
#     repartition_cost = 0
#     transport_cost = 0
#
#     while time < TIME_RANGE:
#
#         if (time % 250 == 0):
#             print(f"we did {time} time-steps")
#             print(f"maxtemp={maxtemp}")
#             print(f"transport_cost={transport_cost}")
#             print(f"repartition_cost={repartition_cost}")
#             # print(f"mintemp={mintemp}")


if __name__ == "__main__":


        # # print(recharged_list)
        # list_returning_scooter = []
        # if len(recharged_list) > 1:
        #     for j in recharged_list:
        #         list_of_scooter[j].charging_time = 0
        #         list_of_scooter[j].charging = False
        #         list_of_scooter[j].soc = CHARGING_LEVEL
        #         # init_pos = Point.from_random(MAP_SIZE, MAP_SIZE)
        #         init_pos = back_in_town(list_of_scooter)
        #         list_of_scooter[j].coord = init_pos
        #         list_of_scooter[j].moving = False
        #         points[j].set_data(init_pos.x, init_pos.y)
        #         points[j].set_color(battery_colors(int(list_of_scooter[j].soc)))
        #         points[j].set_marker('s')
        #         list_returning_scooter.append(list_of_scooter[j])
        #     transport_cost += transport_cost(list_returning_scooter)
        #
        # discharged_list = [(scooter.soc < DISCHARGE_THRESHOLD and scooter.moving == False) for scooter in
        #                    list_of_scooter]
        # # print(discharged_list)
        # if sum(discharged_list) >= int(SIZE_OF_FLEET * DISCHARGED_PROPORTION):
        #     for (i, scooter) in enumerate(list_of_scooter):
        #         if scooter.soc < PICK_UP_THERSHOLD and scooter.moving == False:
        #             scooter.charging = True
        #             scooter.charging_time = 0
        #             points[i].set_data(-20, -20)
        #             points[i].set_color("black")
        #             scooter.soc = CHARGING_LEVEL
        #
        # repartition_cost += measure_distribution(list_of_scooter, t)

    first_strategy = ChargingStrategy(TIME_RANGE, SIZE_OF_FLEET)
    first_strategy.set_parameters(charging_slot = 250, discharged_proportion = 0.20, discharge_threshold = 20,
                                  pick_up_threshold = 30, charging_level = 80)
    first_strategy.launch()


