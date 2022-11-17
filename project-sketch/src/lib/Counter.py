import csv


def counter(i, sorter, is_reversed=True):
    dictionary = {}

    with open('./archive/postal.csv') as file:
        csv_reader = list(csv.reader(file))[1:]
        for car in csv_reader:
            if len(car[i]) > 1:
                if car[i] in dictionary:
                    dictionary[car[i]] += 1
                else:
                    dictionary[car[i]] = 1
        print(dictionary)
        dictionary = dict(sorted(dictionary.items(), key=sorter, reverse=is_reversed))

        return dictionary
