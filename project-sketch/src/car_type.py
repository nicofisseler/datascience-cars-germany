from lib.Counter import counter
import matplotlib.pyplot as plt

car_type_dict = counter(5, lambda x: x[1])

values, label = list(car_type_dict.values()), list(car_type_dict.keys())

overall = sum(values)

relative_values = [x/overall for x in values]

label = [f'{label[i].capitalize()} - {round(relative_values[i]*100)}%' for i in range(len(label))]


plt.figure(figsize=(8,8))
plt.pie(relative_values, labels=label)
plt.show()
