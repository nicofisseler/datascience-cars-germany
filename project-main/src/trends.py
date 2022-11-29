import csv

if __name__ == '__main__':
    # load data from ./archive/postal.csv
    with open('./archive/postal.csv') as csv_handler:
        csv_reader = list(csv.reader(csv_handler))

        # rotate csv_reader clockwise
        csv_reader = list(zip(*csv_reader))[1:]

        # create dict from list with first element as key and the rest as value
        csv_reader = {x[0]: x[1:] for x in csv_reader}

        for el in csv_reader:
            print(el, len(csv_reader[el]))


