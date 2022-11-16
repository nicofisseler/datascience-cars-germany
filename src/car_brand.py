from lib.Counter import counter
import matplotlib.pyplot as plt

car_brand_dict = counter(13, lambda x: x[1])

value, label = car_brand_dict.values(), car_brand_dict.keys()


