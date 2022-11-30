import csv
import statsmodels.api as sm

from matplotlib import pyplot as plt


def plot_regression(x, y, car_data, make, vehicle_type, index, param, x_label):

    constant_x = sm.add_constant(x)
    lr_model = sm.OLS(y, constant_x).fit()
    b, m = lr_model.params
    price = round(m * param + b, 2)
    # Plot
    y_hat = lr_model.predict(constant_x)
    plt.figure()
    plt.scatter([float(x[index]) for x in car_data[f"{make} {vehicle_type}"]],
                [float(x[5]) for x in car_data[f"{make} {vehicle_type}"]])
    plt.plot(x, y_hat, "red")
    plt.scatter(param, m * param + b, color="red")
    # start y at 0
    plt.ylim(bottom=0)
    # add labels to x and y
    plt.xlabel(x_label)
    plt.ylabel("Preis in €")
    plt.show()
    return price


def calculate_price(make, vehicle_type, year, km, fuel, gearbox, ps):
    try:
        car_data = {f"{csv_reader['brand'][i]} {csv_reader['vehicle_type'][i]}": [] for i in
                    range(len(csv_reader['brand']))}
        for i in range(len(csv_reader['brand'])):
            car_data[f"{csv_reader['brand'][i]} {csv_reader['vehicle_type'][i]}"].append(
                (csv_reader['registration_year'][i],
                 csv_reader['odometer'][i],
                 csv_reader['fuel'][i],
                 csv_reader['gearbox'][i],
                 csv_reader['power'][i],
                 csv_reader['price'][i]))
        # remove all elements that has less than 10 elements
        car_data = {x: car_data[x] for x in car_data if len(car_data[x]) >= 10}

        # remove all elements that don't have match fuel and gearbox
        for el in list(car_data.keys()):
            car_data[el] = [x for x in car_data[el] if x[2] == fuel and x[3] == gearbox]

        # convert all values to int
        for el in list(car_data.keys()):
            car_data[el] = [(int(x[0]), int(float(x[1])), x[2], x[3], int(float(x[4])), x[5]) for x in car_data[el]]
            # remove element if key is empty
            if len(car_data[el]) == 0:
                del car_data[el]

        year_price = [(int(x[0]), float(x[5])) for x in car_data[f"{make} {vehicle_type}"]]
        # group x by year
        year_price = {x[0]: [] for x in year_price}
        for el in year_price:
            for idx, y in enumerate(car_data[f"{make} {vehicle_type}"]):
                if int(y[0]) == el:
                    year_price[el].append(float(y[5]))

        year_price = sorted(year_price.items(), key=lambda x: x[0])
        # get the average of every element in x
        year_price = [(x[0], round(sum(x[1]) / len(x[1]), 1)) for x in year_price]
        # split year_price into two lists
        x, y = zip(*year_price)
        price1 = plot_regression(x, y, car_data, make, vehicle_type, 0, year, 'Jahr')

        km_price = [(int(x[1]), float(x[5])) for x in car_data[f"{make} {vehicle_type}"]]

        km_price = {x[0]: [] for x in km_price}
        for el in km_price:
            for idx, y in enumerate(car_data[f"{make} {vehicle_type}"]):
                if int(y[1]) == el:
                    km_price[el].append(float(y[5]))
        # calculate the average of every element in km_price
        km_price = {x: round(sum(km_price[x]) / len(km_price[x]), 1) for x in km_price}
        # convert dict into tuples
        km_price = [(x, km_price[x]) for x in km_price]
        x, y = zip(*km_price)
        price2 = plot_regression(x, y, car_data, make, vehicle_type, 1, km, 'Kilometerstand')

        ps_price = [(int(x[4]), float(x[5])) for x in car_data[f"{make} {vehicle_type}"]]

        # group x by ps
        ps_price = {x[0]: [] for x in ps_price}
        for el in ps_price:
            for idx, y in enumerate(car_data[f"{make} {vehicle_type}"]):
                if int(y[4]) == el:
                    ps_price[el].append(float(y[5]))
        # calculate the average of every element in km_price
        ps_price = {x: round(sum(ps_price[x]) / len(ps_price[x]), 1) for x in ps_price}
        # convert dict into tuples
        ps_price = [(x, ps_price[x]) for x in ps_price]
        x, y = zip(*ps_price)
        price3 = plot_regression(x, y, car_data, make, vehicle_type, 4, ps, 'PS')

        # calculate the average of the three prices
        price = round((price1 + price2 + price3) / 3, 2)
        return price
    except KeyError:
        return 'Insufficient data to calculate price!'


if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))

        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]

        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        print(calculate_price('audi', 'kombi', 2008, 100000, 'benzin', 'manuell', 200))
