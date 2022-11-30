import csv

import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm


def get_trend_plot(trend_name, number_of_lines):
    upper_bound, lower_bound = 2015, 2000
    year_dict = {str(x): [] for x in range(lower_bound, upper_bound + 1)}
    for idx, x in enumerate(csv_reader[trend_name]):
        if upper_bound >= int(csv_reader['registration_year'][idx]) >= lower_bound:
            year_dict[csv_reader['registration_year'][idx]].append(csv_reader[trend_name][idx])
            # count occurences of each element in year_dict
    for el in year_dict:
        year_dict[el] = {x: year_dict[el].count(x) for x in year_dict[el]}
    # add sum key to every value in year_dict with the sum of all values
    for el in year_dict:
        year_dict[el]['sum'] = sum(year_dict[el].values())
    # get the 10 biggest values in year_dict
    for el in year_dict:
        year_dict[el] = sorted(year_dict[el].items(), key=lambda x: x[1], reverse=True)[:number_of_lines + 1]
    # get the percentage of each value in year_dict
    for el in year_dict:
        for idx, x in enumerate(year_dict[el][1:]):
            year_dict[el][idx + 1] = (x[0], round(x[1] / year_dict[el][0][1] * 100, 2))
    # add key to the first element of every tuple in year_dict
    for el in year_dict:
        for idx, x in enumerate(year_dict[el]):
            year_dict[el][idx] = (el, x[0], x[1])
    # get every tuple of year_dict in a list and remove the sum key
    year_dict = [x for el in year_dict for x in year_dict[el] if x[1] != 'sum']
    # group elements by trend_name
    trend_dict = {x[1]: [] for x in year_dict}
    for el in year_dict:
        trend_dict[el[1]].append(el)

    # remove the second element of every tuple in trend_dict
    for el in trend_dict:
        for idx, x in enumerate(trend_dict[el]):
            trend_dict[el][idx] = (x[0], x[2])
    # set figure size to 8 x 5
    plt.figure(figsize=(8, 5))
    # plot every element in trend_dict as a curve
    for idx, el in enumerate(trend_dict):
        if len(el) > 0:
            plt.plot(*zip(*trend_dict[el]), label=el.capitalize())
            # set line opacity to 50%
            plt.gca().lines[-1].set_alpha(0.5)
            x, y = zip(*trend_dict[el])
            # convert x and y to lists
            df = pd.DataFrame({'x': [float(x) for x in x], 'y': list(y)})
            constant_x = sm.add_constant(df['x'])
            lr_model = sm.OLS(df['y'], constant_x).fit()
            b, m = lr_model.params
            # Plot
            y_hat = lr_model.predict(constant_x)
            # label every line with element name
            plt.plot(x, y_hat, lw=2, color='C' + str(list(trend_dict.keys()).index(el)), label=el.capitalize(), linestyle='--')
            # print element name over line
            print(type(x[-1]), y[-1], y_hat.iloc[-1])
            plt.text('2016', y_hat.iloc[-1], el, color='C' + str(list(trend_dict.keys()).index(el)), fontweight='bold', fontsize=10)
        # remove the top and left line from the plot
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.subplots_adjust(right=0.85)
    plt.xticks(rotation=90)
    plt.show()


if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))

        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]

        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        get_trend_plot('brand', 5)
        get_trend_plot('gearbox', 3)
        get_trend_plot('fuel', 2)
        get_trend_plot('vehicle_type', 10)
