#%%
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#Define settings
dt = 0.001 # time step
endTime = 11 #s, simulated duraiton
g = 9.81 #m/s^2 gravitational constant
A1 = .23 #m^2, cross-sectional area at surface
A2 = .011 #m^2, cross-sectional area at surface and hole
Cd = .6 #discharge coefficient (0.6<Cd<1.0)
z0 = .4 #m, initial height


# Set up variables
time = np.arange(0, endTime + dt, dt) # A list with all times we want to plot at.  
z = np.zeros(len(time)) # list for height

for i in range (0, len(time)):
    t = time[i]
    z[i] = ((-(sqrt(g)*Cd*A2)/(sqrt(2)*A1)*t) + sqrt(z0))**2
    z[i] = z[i]*100

plt.plot(time, z, marker=".")
plt.xlabel('Time [s]')  
plt.ylabel('Height [cm]')
plt.show()
# %%
