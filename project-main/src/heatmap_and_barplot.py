import csv
import json
import re

import folium
import pandas as pd
import pgeocode
import matplotlib.pyplot as plt

from folium.plugins import HeatMap

if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))

        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]

        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        nomi = pgeocode.Nominatim('de')

        # get a tuple with postal code and price
        postal_code_price = [(str(csv_reader['postal_code'][idx]).zfill(5), csv_reader['price'][idx]) for idx in range(len(csv_reader['postal_code']))]

        # sort by postal code
        postal_code_price.sort(key=lambda x: x[0])

        # group all postal codes in a dict
        postal_code_price = {x[0]: [] for x in postal_code_price}
        for idx in range(len(csv_reader['postal_code'])):
            postal_code_price[str(csv_reader['postal_code'][idx]).zfill(5)].append((csv_reader['postal_code'][idx], csv_reader['price'][idx]))

        # replace every value with a tuple containing the number of elements and the average price
        for el in postal_code_price:
            postal_code_price[el] = (len(postal_code_price[el]), sum([float(x[1]) for x in postal_code_price[el]]) / len(postal_code_price[el]))

        # convert every key to a tuple containing the latitude and longitude
        # postal_code_price = {str(nomi.query_postal_code(el).latitude) + ',' + str(nomi.query_postal_code(el).longitude): list(postal_code_price[el]) for el in postal_code_price}

        # dump data to a json file in ./assets
        """with open('./assets/postal_code_price.json', 'w') as json_handler:
            json.dump(postal_code_price, json_handler, indent=2)"""

        # load data from ./assets/postal_code_price.json
        with open('./assets/postal_code_price.json') as json_handler:
            postal_code_price = json.load(json_handler)

        postal_code_price = {tuple(map(float, x.split(','))): tuple(postal_code_price[x]) for x in postal_code_price}

        # create a list of tuples containing the latitude, longitude, number of elements
        # and the average price
        postal_code_value_by_number_of_elements = [(x[0], x[1], postal_code_price[x][0]) for x in postal_code_price]
        postal_code_value_by_average_price = [(x[0], x[1], postal_code_price[x][1]) for x in postal_code_price]

        # sort postal_code_price by 3rd element
        postal_code_value_by_number_of_elements.sort(key=lambda x: x[2])

        # convert postal_code_value_by_number_of_elements to three panda dataframes
        postal_code_value_by_number_of_elements = pd.DataFrame(postal_code_value_by_number_of_elements, columns=['latitude', 'longitude', 'number_of_elements'])
        postal_code_value_by_average_price = pd.DataFrame(postal_code_value_by_average_price, columns=['latitude', 'longitude', 'average_price'])

        # remove all null values from postal_code_value_by_number_of_elements
        postal_code_value_by_number_of_elements = postal_code_value_by_number_of_elements.dropna()
        postal_code_value_by_average_price = postal_code_value_by_average_price.dropna()

        print(postal_code_value_by_number_of_elements)

        # create a heatmap using foilum with the keys as coordinates and the first element as indicator
        m1 = folium.Map(location=[52.520008, 13.404954], zoom_start=10)
        HeatMap(postal_code_value_by_number_of_elements, radius=15).add_to(m1)
        m1.save('./assets/heatmap_noe.html')

        m2 = folium.Map(location=[52.520008, 13.404954], zoom_start=10)
        HeatMap(postal_code_value_by_average_price, radius=15).add_to(m2)
        m1.save('./assets/heatmap_ap.html')


        print(postal_code_price)

        """
        # group postal codes by district
        

        # convert postal codes to coordinates using pgeocode
        postal_codes_coordinates = nomi.query_postal_code(postal_codes)

        # remove elements with missing coordinates
        postal_codes_coordinates = postal_codes_coordinates[postal_codes_coordinates.latitude.notna()]

        # create map
        data_map = folium.Map(location=[52.520008, 13.404954], zoom_start=6)
        # create heatmap
        HeatMap(data=postal_codes_coordinates[['latitude', 'longitude']].values.tolist(), radius=12).add_to(data_map)
        # save map
        data_map.save('./out/map.html')

        # sort districts by number of postal codes
        postal_codes_by_district = {k: v for k, v in
                                    sorted(postal_codes_by_district.items(), key=lambda item: len(item[1]), reverse=True)}

        # set figure size to 24 x 16
        plt.figure(figsize=(24, 16))
        # plot bar chart with the first 10 elements
        plt.barh(list(postal_codes_by_district.keys())[:10][::-1], [len(x) for x in list(postal_codes_by_district.values())[:10]][::-1])
        # increase label size
        plt.tick_params(labelsize=28)
        # increase left space
        plt.subplots_adjust(left=0.3)
        # set title
        plt.title("10 Bundesländer in denen am meisten Autos verkauft wurden", fontsize=40, fontweight="bold")
        plt.show()"""
