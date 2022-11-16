from lib.Counter import counter
import matplotlib.pyplot as plt

car_type_dict = counter(5, lambda x: x[1])

value, label = car_type_dict.values(), car_brand_dict.keys()
