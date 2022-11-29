import csv
import folium
import pgeocode
import matplotlib.pyplot as plt

from folium.plugins import HeatMap

# load data from ./archive/postal.csv
with open('./archive/postal.csv') as csv_handler:
    csv_reader = list(csv.reader(csv_handler))[1:]

    nomi = pgeocode.Nominatim('de')

    # get postal codes and make sure they are 5 characters long
    postal_codes = [str(x[16]).zfill(5) for x in csv_reader]
    # group postal codes by district
    postal_codes_by_district = {}
    for postal_code in postal_codes:
        district = str(nomi.query_postal_code(postal_code).community_name)
        if district not in postal_codes_by_district:
            postal_codes_by_district[district] = []
        postal_codes_by_district[district].append(postal_code)

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
    plt.show()
