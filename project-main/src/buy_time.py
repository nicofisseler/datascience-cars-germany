import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def get_fastets_selling(category, number_of_bars, start=0):
    vehicle_type_dict = {f"{csv_reader[category][idx]}": [] for idx in range(len(csv_reader[category])) if
                         len(csv_reader[category][idx]) > 1}

    keys = [f"{csv_reader[category][idx]}" for idx, element in enumerate(csv_reader['brand']) if
            len(element) > 1 and len(csv_reader['vehicle_type'][idx]) > 1 and len(csv_reader['fuel'][idx]) > 1 and len(
                csv_reader['gearbox'][idx]) > 1]

    print(vehicle_type_dict)

    # create a list of tuples of format (csv_reader['ad_created'][i], csv_reader['last_seen'][i])
    ad_created_last_seen = list(
        zip(keys, csv_reader['ad_created'], csv_reader['last_seen']))

    print(ad_created_last_seen)

    # group the tuples by vehicle_type
    for el in ad_created_last_seen:
        vehicle_type_dict[el[0]].append(el[1:])

    # delete key from vehicle_type_dict if its length is 0
    for el in list(vehicle_type_dict.keys()):
        if len(el) == 0:
            del vehicle_type_dict[el]

    # remove all elements that has less than 10 elements
    for el in list(vehicle_type_dict.keys()):
        if el == 'lada':
            print(len(vehicle_type_dict[el]), el)
        if len(vehicle_type_dict[el]) < 200:
            del vehicle_type_dict[el]


    # calculate time difference between ad_created and last_seen
    for el in vehicle_type_dict:
        for i in range(len(vehicle_type_dict[el])):
            vehicle_type_dict[el][i] = (
                    datetime.strptime(vehicle_type_dict[el][i][1], '%Y-%m-%d') - datetime.strptime(
                vehicle_type_dict[el][i][0], '%Y-%m-%d')).days

    # sort vehicle_type_dict by average time difference
    vehicle_type_dict = sorted(vehicle_type_dict.items(), key=lambda x: sum(x[1]) / len(x[1]))

    # plot the averead time difference for each vehicle type for the first 10 vehicle types
    n = number_of_bars
    plt.bar([el[0] for el in vehicle_type_dict[:n]], [sum(el[1]) / len(el[1]) for el in vehicle_type_dict[:n]])
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    # write exact value on top of each bar
    for i, v in enumerate([sum(x[1]) / len(x[1]) for x in vehicle_type_dict[:n]]):
        plt.text(i - 0.7, v + 0.1, str(round(v, 1)), color='black')
    plt.ylim(start)
    plt.ylabel('differenz in tagen')
    plt.show()


if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))
        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]
        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        get_fastets_selling('brand', 20, 8)
