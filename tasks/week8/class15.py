import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# JAB Problem 2
# JAB Read in csv file
data = pd.read_csv('data.csv', delimiter=',')

# JAB Plot ra vs dec
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(data['ra'], data['dec'], marker='o', c='forestgreen')
ax.set_xlabel('RA (deg)'), ax.set_ylabel('Dec (deg)')
plt.show()

# JAB Replot with different sized points
