import csv
import folium
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

        # get a tuple of latitude and longitude for every postal code and the price

        # group postal codes by first two characters
        postal_codes = {x[:2]: [] for x in postal_codes}
        for el in postal_codes:
            for idx, y in enumerate(csv_reader['postal_code']):
                if str(y).zfill(5)[:2] == el:
                    postal_codes[el].append(str(y).zfill(5))
        # sort postal codes
        postal_codes = sorted(postal_codes.items(), key=lambda x: x[0])
        # sort values of postal codes
        postal_codes = [(x[0], sorted(x[1])) for x in postal_codes]

        print(postal_codes)

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
