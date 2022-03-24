
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
BEGIN_HOUR = 12
"hour of the begining of the simulation"
CHARGING_DURATION = 1500
"average duration of the charging of a scooter"



if __name__ == "__main__":

    fig, ax = plt.subplots()
    used_colors = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
    battery_colors = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=used_colors, N=100)

    list_of_scooter = init_new_fleet(SIZE_OF_FLEET)
    points = []

    for scooter in list_of_scooter:
        points.append(ax.plot(scooter.coord.x, scooter.coord.y, marker='s', linestyle='None', color='r')[0])
        ax.set_xlim(-20, MAP_SIZE + 20)
        ax.set_ylim(-20, MAP_SIZE + 20)

    time = 0
    while time < TIME_RANGE :

        for t in range(CHARGING_SLOT):
            time+=1
            for (i,scooter) in enumerate(list_of_scooter):

                if not scooter.charging :
                    scooter.init_new_trip(time, BEGIN_HOUR)

                    if scooter.moving :
                        scooter.move()

                    new_x = scooter.coord.x
                    new_y = scooter.coord.y
                    points[i].set_data(new_x, new_y)
                    points[i].set_color(battery_colors(int(scooter.soc)))

                    if scooter.moving:
                        points[i].set_marker('o')
                    else:
                        points[i].set_marker('s')

            plt.pause(0.1)

                # else :
                #     scooter.charging_time+=1
                #     if scooter.charging_time >= CHARGING


        discharged_list = [scooter.soc > DISCHARGE_THRESHOLD for scooter in list_of_scooter]
        if sum(discharged_list) > int(SIZE_OF_FLEET*DISCHARGED_PROPORTION) :
            for (i,scooter)in enumerate (list_of_scooter):
                if  scooter.soc < PICK_UP_THERSHOLD:
                    scooter.charging = True
                    scooter.charging_time = 0
                    points[i].set_data(-20, -20)
                    points[i].set_color("black")


        recharged_list = [i for i in range(len(list_of_scooter)) if list_of_scooter[i].charging_time > CHARGING_DURATION ]
        if len(recharged_list) > 1:
            for j in recharged_list :
                list_of_scooter[j].charging_time = 0
                list_of_scooter[j].charging = False
                list_of_scooter[j].soc = CHARGING_LEVEL
                init_pos = Point.from_random(MAP_SIZE, MAP_SIZE)
                list_of_scooter[j].coord = init_pos


            
        
        






