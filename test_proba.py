import numpy as np
import math
import matplotlib.pyplot as plt

# begin_hour=0
#
#
# def give_time(t, begin_hour=0):
#     '''
#     :param t: total time elapsed since the beginning of the simulation in [s]
#     :param begin_hour: hour of the beginning of the simulation in [h]
#     :return: the current time in second during in the frame of the current day
#     '''
#     return (begin_hour*3600 + 7.2*t) % (24*3600)
#
#
# proba = 1.
#
# print(8*3600)
# print(7*3600)
#
# print(give_time(int(((7/7.2))*3600),0))
# print(give_time(int((8/7.2)*3600),0))
# # a = 7.2* 8*3600
# # print(a)
# # b=a%(24*3600)
# # print(b)
# print(give_time(int(24*3600/7.2)-1,0))
#
# print(proba)
#
# X=[]
# Y=[]
#
#
#
# sigma=3600/7.2
#
# # for t in range(int((8/7.2)*3600-sigma),int((8/7.2)*3600+sigma)):
# #     # proba+=(0.5/ (3600*math.sqrt(2 * np.pi))) * \
# #     #             (np.exp(-(give_time(t, begin_hour) - 8 * 3600) ** 2 / (2 * 3600 ** 2)) +
# #     #              np.exp(-(give_time(t, begin_hour) - 18 * 3600) ** 2 / (2 * 3600 ** 2)))
# #     proba+=(1/ (sigma*math.sqrt(2 * np.pi))) * (np.exp(-((give_time(t, begin_hour) - 8 * 3600) ** 2) / (2 * sigma ** 2)))
#
# # for t in range(int(give_time(int((8/7.2)*3600),0) - sigma), int(give_time(int((8/7.2)*3600),0) + sigma)):
# #     # proba+=(0.5/ (3600*math.sqrt(2 * np.pi))) * \
# #     #             (np.exp(-(give_time(t, begin_hour) - 8 * 3600) ** 2 / (2 * 3600 ** 2)) +
# #     #              np.exp(-(give_time(t, begin_hour) - 18 * 3600) ** 2 / (2 * 3600 ** 2)))
# #     proba += (1 / (sigma * math.sqrt(2 * np.pi))) * (
# #         np.exp(-((t - 8 * 3600) ** 2) / (2 * sigma ** 2)))
#
# for t in range(int(8*3600-7*60), int(8*3600+7*150),7):
#     proba*=(1-(60/ (2*3600*math.sqrt(2 * np.pi))) *
#                 (np.exp(-(t - 8 * 3600) ** 2 / (2 * (2*3600) ** 2)) +
#                  np.exp(-(t - 18 * 3600) ** 2 / (2 * (2*3600) ** 2))))
#     # X.append(t)
#     # Y.append(proba)
#
# # for t in range(int(give_time(0,0)), int(give_time(int((24/7.2)*3600),0))):
# #     proba = (1 / (sigma * math.sqrt(2 * np.pi))) * (
# #             np.exp(-((t - 8 * 3600) ** 2) / (2 * sigma ** 2)))
# #     X.append(t)
# #     Y.append(proba)
#
# # plt.plot(X,Y)
# # plt.show()
#
# print(proba)

