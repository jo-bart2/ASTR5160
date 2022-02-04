import numpy as np
import matplotlib.pyplot as plt

#JAB The magnitudes of the first quasar, at (246.933, 40.795), are:
u1 = 18.82
g1 = 18.81
r1 = 18.73
i1 = 18.82
z1 = 18.90
#JAB The magnitudes of the second quasar, at (236.562, 2.440), are:
u2 = 19.37
g2 = 19.10
r2 = 18.79
i2 = 18.73
z2 = 18.63

#JAB plot uncorrected g-r vs r-i
plt.scatter(r1-i1,g1-r1,color='green',label='(246.933, 40.795)')
plt.scatter(r2-i2,g2-r2,color='orange',label='(236.562, 2.440)')
plt.legend()
plt.xlabel('r - i (mag)')
plt.ylabel('g - r (mag)')
plt.show()
# The two quasars are not very similar in color. The differences in r-i are only ~0.02, but \
    #the g-r values are off by more than 0.2 magnitudes.
#I feel like the colors should be similar if they are both similar quasars.

#JAB correct quasar magnitudes for extinction

    

    