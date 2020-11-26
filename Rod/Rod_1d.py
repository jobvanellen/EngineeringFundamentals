"""  
@author: Bart Bozon  
script to simulate a temperature profile with time axis  
"""   
#%%   
import numpy as np    
import matplotlib.pyplot as plt    
    
# Set up variables.    
arraysize=100    
temp_profile_old =np.zeros(arraysize)    
temp_profile_new =np.zeros(arraysize)    
    
# defining constants    
alfa=9.7e-5 # alfa of aLuminium    
dx=0.001 # 1 mm grid, 100 points, = 0.1 m    
dt=0.001     # 100 seconde    
simulation_time=50    
steps_to_show = 50    
temp_points=np.zeros(steps_to_show+1)    
temp_axis =np.zeros(steps_to_show+1)    
x_axis = np.arange(0.0,arraysize*dx, dx)    
temp_profile_old[arraysize-1]=0.001    
temp_teller=0    
    
# Run simulation.    
plt.plot(x_axis,temp_profile_old)    
for t in range (0,int(simulation_time/dx)+1):    
    temp_profile_old[arraysize-1]=100    
    temp_profile_old[0]=0    
    for x in range (1,arraysize-1):    
        temp_profile_new[x]=temp_profile_old[x]+dt/(dx*dx)*alfa*(-2*temp_profile_old[x]+temp_profile_old[x-1]+temp_profile_old[x+1])    
    temp_profile_new[0]=temp_profile_old[0]+dt/(dx*dx)*alfa*(-1*temp_profile_old[0]+temp_profile_old[1])    
    if (t%(int((simulation_time/dx)/steps_to_show))==0):    
       plt.plot(x_axis,temp_profile_old)    
       temp_points[temp_teller]=temp_profile_new[int(arraysize/2)]    
       temp_axis[temp_teller]=t*dt    
       temp_teller=temp_teller+1            
    temp_profile_old=temp_profile_new    
    
# Display results.    
plt.xlabel('x [m]')   
plt.ylabel('temperature [c]')    
plt.show()    
print ("elapsed time", t* dt ,"seconds")    
print ("time elapsed per line",simulation_time/steps_to_show,"seconds" )    
plt.plot(temp_axis,temp_points)    
plt.xlabel('time [s]')    
plt.ylabel('temperature [c]')    
plt.show()    

# %%
