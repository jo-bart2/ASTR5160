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
area = ((1/data['g'])*200)**2

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(data['ra'], data['dec'], marker='o', c='forestgreen', s=area, alpha=0.6)
ax1.set_xlabel('RA (deg)'), ax1.set_ylabel('Dec (deg)')
plt.show()
