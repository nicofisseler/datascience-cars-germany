from lib.Counter import counter
import matplotlib.pyplot as plt

car_brand_dict = counter(13, lambda x: x[1])
car_brand_dict['andere'] = 0
too_small_keys = []

for key in car_brand_dict:
    if car_brand_dict[key] <= 50:
        too_small_keys.append(key)

for key in too_small_keys:
    car_brand_dict['andere'] = car_brand_dict[key]
    del car_brand_dict[key]

value, label = car_brand_dict.values(), [x.capitalize() for x in list(car_brand_dict.keys())]

figure, axis = plt.subplots(figsize=(16, 8))
axis.tick_params(rotation=-90, labelsize=12)
axis.bar(label, value)
plt.subplots_adjust(bottom=0.2)
plt.show()
