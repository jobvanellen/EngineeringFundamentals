#%%
""" 
@author: Hildo Bijl 
Fall simulation with friction 
"""  
import numpy as np  
import matplotlib.pyplot as plt  
  
# Define settings.  
endTime = 60 # The time (seconds) that we simulate.  
dt = 0.1 # The time step (seconds) that we use in the discretization.  
v0 = 0 # The initial velocity [m/s].  
s0 = 0 # The initial position [m].  
g = 9.81 # The gravitational acceleration [m/s^2].  
b = 0.02 # The friction coefficient [N/(m/s)^2].  
m = 80 # The mass of the skydiver [kg].  
  
# Set up variables.  
time = np.arange(0, endTime + dt, dt) # A list with all times we want to plot at.  
v = np.zeros(len(time)) # A list for the velocity.  
s = np.zeros(len(time)) # A list for the distance.  
v[0] = v0
s[0] = s0
  
# Run simulation.  
for i in range(1, len(time)):  
    v[i] = v[i-1] + (b/m*v[i-1]**2 - g)*dt  
    s[i] = s[i-1] + v[i-1]*dt  
  
# Display results.  
plt.plot(time, s, marker=".")  
plt.xlabel('Time [s]')  
plt.ylabel('Distance [m]')  
plt.show()  
print("Distance traveled after", endTime, "seconds:", round(s[-1],3), "meters")  
print("Final velocity:", round(v[-1],3), "m/s") 

# %%
