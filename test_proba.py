import numpy as np
import math
import matplotlib.pyplot as plt

import os
import sys
import seaborn as sns
sns.set_theme()

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








