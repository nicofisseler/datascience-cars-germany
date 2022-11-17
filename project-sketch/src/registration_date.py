from lib.Counter import counter
import matplotlib.pyplot as plt

registration_date_dict = counter(6, lambda x: x[0], reversesort=False)

values, labels = registration_date_dict.values(), registration_date_dict.keys()

figure, axis = plt.subplots()
axis.tick_params(axis='x', labelsize=5, rotation=90)
plt.plot(labels, values)
plt.show()
