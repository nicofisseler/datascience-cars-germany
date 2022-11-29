import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))

        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]

        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        # create a dict with the same keys as csv_reader and an empty array as value
        vehicle_type_dict = {x: [] for x in csv_reader['vehicle_type']}

        # create a list of tuples of format (csv_reader['ad_created'][i], csv_reader['last_seen'][i])
        ad_created_last_seen = list(
            zip(csv_reader['vehicle_type'], csv_reader['ad_created'], csv_reader['last_seen']))

        # group the tuples by vehicle_type
        for el in ad_created_last_seen:
            vehicle_type_dict[el[0]].append(el[1:])

        # delete key from vehicle_type_dict if its length is 0
        for el in list(vehicle_type_dict.keys()):
            if len(el) == 0:
                del vehicle_type_dict[el]

        # calculate time difference between ad_created and last_seen
        for el in vehicle_type_dict:
            for i in range(len(vehicle_type_dict[el])):
                vehicle_type_dict[el][i] = (
                        datetime.strptime(vehicle_type_dict[el][i][1], '%Y-%m-%d') - datetime.strptime(
                    vehicle_type_dict[el][i][0], '%Y-%m-%d')).days

        # sort vehicle_type_dict by average time difference
        vehicle_type_dict = sorted(vehicle_type_dict.items(), key=lambda x: sum(x[1]) / len(x[1]))

        plt.bar(np.arange(len(vehicle_type_dict)), [sum(x[1]) / len(x[1]) for x in vehicle_type_dict])
        plt.xticks(np.arange(len(vehicle_type_dict)), [x[0] for x in vehicle_type_dict], rotation=90)
        plt.subplots_adjust(bottom=0.2)
        # write exact value on top of each bar
        for i, v in enumerate([sum(x[1]) / len(x[1]) for x in vehicle_type_dict]):
            plt.text(i - 0.25, v + 0.1, str(round(v, 2)), color='black')
        plt.ylim(8)
        plt.ylabel('differenz in tagen')
        plt.show()
