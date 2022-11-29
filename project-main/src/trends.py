import csv
from matplotlib import pyplot as plt


def get_trend_plot(trend_name):
    year_dict = {str(x): [] for x in range(2000, 2016)}
    for idx, x in enumerate(csv_reader[trend_name]):
        if int(csv_reader['registration_year'][idx]) >= 2000:
            year_dict[csv_reader['registration_year'][idx]].append(csv_reader[trend_name][idx])
            # count occurences of each element in year_dict
    for el in year_dict:
        year_dict[el] = {x: year_dict[el].count(x) for x in year_dict[el]}
    # add sum key to every value in year_dict with the sum of all values
    for el in year_dict:
        year_dict[el]['sum'] = sum(year_dict[el].values())
    # get the 10 biggest values in year_dict
    for el in year_dict:
        year_dict[el] = sorted(year_dict[el].items(), key=lambda x: x[1], reverse=True)[:10]
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
    # plot every element in trend_dict as a curve
    for el in trend_dict:
        plt.plot(*zip(*trend_dict[el]), label=el)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.subplots_adjust(right=0.7)
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

        get_trend_plot('brand')
        get_trend_plot('gearbox')
        get_trend_plot('fuel')
