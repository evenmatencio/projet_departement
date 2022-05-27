import os
import sys
import json

import matplotlib.pyplot as plt

sys.path.append(os.path.abspath("./"))
from main import *

#######################################################################################################################
# PREPROCESSING
#######################################################################################################################


ARG1 = "charging_slot"
ARG2 = "discharged_proportion"
ARG3 = "discharge_threshold"
ARG4 = "pick_up_threshold"
ARG5 = "charging_level"


def extract_data(results, param, param_to_plot):
    '''
    :param results: list containing dicts that stores the results of simulation.
    :param param: a list containing pairs of ("param_name_string", param_value). Must be of lenght m-1, where m is the number
    of parameters studied for the simulation
    :param: param_to_plot
    '''
    assert len(param) == (len(results[0]["param"].keys()) - 1), "number of parameters given does not match with simulation"
    tot_cost_list = []
    transport_cost_list = []
    repartition_cost_list = []
    benefice_list = []
    param_to_plot_list= []
    for simul in results:
        match = True
        for pair in param:
            if round(simul["param"][pair[0]], 2) != pair[1] :
                match = False
                break
        if match :
            tot_cost_list.append(simul["total_cost"])
            transport_cost_list.append(simul["cost"]["transport"])
            repartition_cost_list.append(simul["cost"]["distribution"])
            benefice_list.append(simul["benefice"])
            param_to_plot_list.append(simul["param"][param_to_plot])
    return tot_cost_list, transport_cost_list, repartition_cost_list, benefice_list, param_to_plot_list



#######################################################################################################################
# PLOTS AND RENDER
#######################################################################################################################


if __name__ == "__main__" :

    with open(os.getcwd() + '/Results/loop_ChrgSlt_new_bit_maillage5.json') as json_file:
        results = json.load(json_file)

    print(results)

    param1 = [ [ARG2, 0.6], [ARG3, 22.0], [ARG4, 21.0], [ARG5, 80] ]
    param_to_plot1 = ARG1

    tot_cost, transport_cost, repartition_cost, benefice_list, arg = extract_data(results, param1, param_to_plot1)
    arg_in_hour = [i/(3600/TIME_STEP) for i in arg]

    plt.plot(arg_in_hour, tot_cost, 'r', label="Total cost" )
    plt.plot(arg_in_hour, transport_cost, 'g', label="Transport cost")
    plt.plot(arg_in_hour, repartition_cost, 'b', label="Repartition cost")
    plt.plot(arg_in_hour, benefice_list, color='orange', label="Benefice")
    plt.xticks(arg_in_hour)
    plt.ylabel("Costs in euros")
    plt.xlabel("Charging slots value [in hour]")
    plt.title("Costs evolution depending on charging_slot value")
    plt.legend()
    plt.show()

