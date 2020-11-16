#%%
""" 
@author: Hildo Bijl 
Fall simulation without friction 
"""  
import numpy as np  
import matplotlib.pyplot as plt  
  
# Define settings.  
endTime = 10 # The time (seconds) that we simulate.  
dt = 0.0001 # The time step (seconds) that we use in the first discretization.  
v0 = 0 # The initial velocity [m/s].  
s0 = 0 # The initial position [m].  
g = 9.81 # The gravitational acceleration [m/s^2].  

 
# Set up variables.  
time = np.arange(0, endTime + dt, dt) # A list with all times we want to plot at.  
vAnalytical = np.zeros(len(time)) # A list for the velocity (analytical).  
sAnalytical = np.zeros(len(time)) # A list for the distance (analytical).  
vSimulated = np.zeros(len(time)) # A list for the velocity (simulated).  
sSimulated = np.zeros(len(time)) # A list for the distance (simulated).  
vSimulated[0] = v0
sSimulated[0] = s0

# Run analytical solution.  
for i in range(0, len(time)):  
    t = time[i]  
    vAnalytical[i] = -g*t + v0  
    sAnalytical[i] = -0.5*g*t**2 + v0*t + s0  

# Run simulation.  
for i in range(1, len(time)):  
    vSimulated[i] = vSimulated[i-1] - g*dt  
    sSimulated[i] = sSimulated[i-1] + vSimulated[i-1]*dt  

# Display results.  
plt.plot(time, sAnalytical, marker=".")  
plt.plot(time, sSimulated, marker=".")  
plt.xlabel('Time [s]')  
plt.ylabel('Distance [m]')  
plt.show()  

# Analyze outcome.  
print("Distance traveled after", endTime, "seconds")  
print("Analytical:", sAnalytical[-1])  
print("Simulated (dt= %.1f):" % dt, sSimulated[-1])
print("Difference: ", abs(sAnalytical[-1]-sSimulated[-1]), 'metres.')



# %%
