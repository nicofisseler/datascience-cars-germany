import csv


def counter(index, sorter, reversesort=True):
    with open('./archive/postal.csv') as file:
        dictionary = {}
        csv_reader = csv.reader(file)
        for val in list(csv_reader)[1:]:
            value = val[index]
            if len(value) > 1:
                if value in dictionary:
                    dictionary[value] += 1
                else:
                    dictionary[value] = 1
        dictionary = dict(sorted(dictionary.items(), key=sorter, reverse=reversesort))
        return dictionary

