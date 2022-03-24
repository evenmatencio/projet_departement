
import os
import sys

sys.path.append(os.path.abspath("./"))

from scooter import *


# -------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------------------------------------------------------------------------

TIME_RANGE = 500
"number of steps of the simulation"
SIZE_OF_FLEET = 10
"number of scooter in our simulation"
BEGIN_HOUR = 12
"hour of the begining of the simulation"



def init_x_coordinates_list(list_of_scooter):
    x=[]
    for i in range(SIZE_OF_FLEET):
        x.append([list_of_scooter[i].coord.x])
    return x


def init_y_coordinates_list(list_of_scooter):
    y=[]
    for i in range(SIZE_OF_FLEET):
        y.append([list_of_scooter[i].coord.y])
    return y


def init_soc_list(list_of_scooter):
    soc=[]
    for i in range(SIZE_OF_FLEET):
        soc.append([list_of_scooter[i].soc])
    return soc

def init_mooving_list(list_of_scooter):
    moving=[]
    for i in range(SIZE_OF_FLEET):
        moving.append([list_of_scooter[i].moving])
    return moving


if __name__ == "__main__":

    list_of_scooter = init_new_fleet(SIZE_OF_FLEET)
    x = init_x_coordinates_list(list_of_scooter)
    y = init_y_coordinates_list(list_of_scooter)
    soc = init_soc_list(list_of_scooter)
    moving = init_mooving_list(list_of_scooter)

    for t in range(TIME_RANGE):

        for i in range(SIZE_OF_FLEET):
            list_of_scooter[i].init_new_trip(t, BEGIN_HOUR)
        for i in range(SIZE_OF_FLEET):
            if(list_of_scooter[i].moving == True):
                list_of_scooter[i].move()
            x[i].append(list_of_scooter[i].coord.x)
            y[i].append(list_of_scooter[i].coord.y)
            soc[i].append(list_of_scooter[i].soc)
            moving[i].append(list_of_scooter[i].moving)

    fig, ax = plt.subplots()
    used_colors = ["r", "orangered", "tab:orange", "orange", "gold", "yellow"]
    battery_colors = plt_colors.LinearSegmentedColormap.from_list("battery_colors", colors=used_colors, N=100)
    points = []
    for i in range(SIZE_OF_FLEET):
        points.append(i)

    for t in range(TIME_RANGE):
        if t == 0:
            for i in range(SIZE_OF_FLEET):
                points[i], = ax.plot(x[0], y[0], marker='s', linestyle='None', color='green')
                ax.set_xlim(-1, MAP_SIZE+1)
                ax.set_ylim(-1, MAP_SIZE+1)
        else:
            for i in range(SIZE_OF_FLEET):
                if(moving[i][t]==True):
                    points[i].set_marker('o')
                else:
                    points[i].set_marker('s')

                points[i].set_color(battery_colors(int(soc[i][t])))
                # if (soc[i][t] <= 50):
                #     points[i].set_color('r')
                new_x = x[i][t]
                new_y = y[i][t]
                points[i].set_data(new_x, new_y)
        plt.pause(0.1)
        if(t%100==0):
            print(f"{t} time steps from beginning")