import numpy as np
import math
import matplotlib.pyplot as plt

import os
import sys
# import seaborn as sns
# sns.set_theme()

sys.path.append(os.path.abspath("./"))

from scooter import *

# if __name__  == "__main__":

    # spatial_dist = np.zeros((MAP_SIZE//5, MAP_SIZE//5))
    # print(spatial_dist.shape)
    # for x in range(0, MAP_SIZE, 5):
    #     for y in range(5, MAP_SIZE + 5, 5):
    #         point = Point(x, y)
    #         spatial_dist[x//5, 40 - y//5] = spatial_distribution(point)
    #
    #
    # ax = sns.heatmap(spatial_dist)
    # plt.title("Spatial distribution of the demand")
    # #plt.tick_params(left=False, bottom=False)
    # plt.xticks(ticks= [0, 10, 20, 30, 40], labels=[0, 50, 100, 150, 200])
    # plt.yticks(ticks= [0, 10, 20, 30, 40], labels=[0, 50, 100, 150, 200])
    # plt.show()



#
#
# list_prob = []
#
# for i in range(100):
#     point = Point.from_random(MAP_SIZE,MAP_SIZE)
#     list_prob.append(SPATIAL_PONDERATION*spatial_distribution(point))
#
# print(max(list_prob))
#

proba = 1
K = 120





def time_distribution2(t, begin_hour=0):
    '''WARNING : t must be a number of time steps'''
    return (1 / (2*math.sqrt(2 * np.pi)*TIME_SIGMA) ) * \
            (np.exp(-(give_time(t, begin_hour) - 8 * 3600) ** 2 / (2 * TIME_SIGMA** 2)) +
             np.exp(-(give_time(t, begin_hour) - 13 * 3600) ** 2 / (2 * (5*TIME_SIGMA) ** 2)) +
            np.exp(-(give_time(t, begin_hour) - 18 * 3600) ** 2 / (2 * TIME_SIGMA** 2)))
    # (2 * math.sqrt(2 * np.pi)*TIME_SIGMA**2)  *

for t in range(int((8*3600/9)),int((8*3600/9)+144)):
    proba*=(1-K*time_distribution2(t))
print(proba)


X=[]
Y=[]

for t in range(int((0*3600/9)),int((24*3600/9))):
    X.append(t*9/3600)
    Y.append(K*time_distribution2(t))

plt.plot(X,Y)
plt.show()