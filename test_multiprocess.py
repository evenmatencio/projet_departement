import json
import numpy as np
import matplotlib.pyplot as plt


import os
import sys
sys.path.append(os.path.abspath("./"))

with open('Results/simul_output_even_23052022.json') as json_data:
    data_dict = json.load(json_data)

min_cost = 10000
min_id = -1

for result in data_dict:
    if result['param']['discharge_threshold'] == 30.0 and  result['total_cost'] < min_cost:
        min_cost = result['total_cost']
        min_id = result['id']


print(f"min id = {min_id} with min scor = {min_cost}")

X = [10, 15, 22, 26, 30]
Y = [2220, 2209.49, 2205, 2207.27, 2208.48]

plt.plot(X,Y)
plt.show()