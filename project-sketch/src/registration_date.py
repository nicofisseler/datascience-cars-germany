import matplotlib

from lib.Counter import counter
import matplotlib.pyplot as plt

registration_date_dict = counter(6, lambda x: x[0], is_reversed=False)

values, labels = registration_date_dict.values(), list(registration_date_dict.keys())

figure, axis = plt.subplots(figsize=(16, 8))
axis.tick_params(axis='x', labelsize=12, rotation=90)
plt.plot(labels, values)
for i, label in enumerate(axis.xaxis.get_ticklabels()):
    if i % 5 == 0 or i == len(labels) - 1:
        label.set_visible(True)
    else:
        label.set_visible(False)
plt.show()
