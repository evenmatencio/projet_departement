import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np
import matplotlib.pyplot as plt


list_coords = [(1, 1), (5, 4), (2, 5), (3, 8), (1, 2)]



# for i in range(len(list_coords)):
#     plt.plot(list_coords[i][0], list_coords[i][1])
# plt.show()

problem_no_fit = mlrose.TSPOpt(length=len(list_coords), coords=list_coords, maximize=False)


best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, random_state=2)

print(f"best state = {best_state}")
print(f"best fitness = {best_fitness}")