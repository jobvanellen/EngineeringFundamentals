#%%
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

#Define settings
dt = 0.1 # time step
endTime = 130 #s, simulated duraiton
g = 9.81 #m/s^2 gravitational constant
A1 = .049 #m^2, cross-sectional area at surface
A2 = 6.36*(10**(-5)) #m^2, cross-sectional area of the hole
Cd = 0.8 #discharge coefficient (0.6<Cd<1.0)
z0 = .09 #m, initial height

# Set up variables
time = np.arange(0, endTime + dt, dt) # times to plot  
z = np.zeros(len(time)) # list for height
zSim = np.zeros(len(time)) # list for height at simulation
zSim[0] = z0 # first simulated value is z0

for i in range (0, len(time)):
    t = time[i]
    z[i] = ((-((sqrt(g)*Cd*A2)/(sqrt(2)*A1))*t) + sqrt(z0))**2
    z[i] = z[i]*100

for i in range (1, len(time)):
    zSim[i] = zSim[i-1] - Cd*(A2/A1)*sqrt(2*g*zSim[i-1])*dt

for i in range (0, len(time)):
    zSim[i] = zSim[i]*100

plt.plot(time, z, marker=".")
plt.plot(time, zSim, marker=".")
plt.xlabel('Time [s]')  
plt.ylabel('Height [cm]')
plt.show()
# %%
