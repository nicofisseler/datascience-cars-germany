import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
# Regression

dat = pd.DataFrame({'x1': [1, 2, 3, 4, 6, 8, 4, 6, 9, 10], 'x2': [1, 0, 2, 4, 7, 8, 9, 6, 9, 10],  'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

x = dat[['x1', 'x2']]
y = dat.y
x = sm.add_constant(x)
lr_model = sm.OLS(y,x).fit()
print(lr_model.summary())
# Plot
y_hat = lr_model.predict(x)
plt.figure()
plt.scatter(dat.x1, dat.y)
plt.scatter(dat.x2, dat.y)
plt.plot(dat.x1, y_hat, "red")
plt.show()
