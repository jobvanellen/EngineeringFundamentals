"""  
@author: Bart Bozon  
Script for 2d temperature profile, optimised for speed 
"""  
#%%  
import numpy as np  
import matplotlib.pyplot as plt  
import copy  
from pathlib import Path
import os

#need boundary condition for heat flow to water and isolation

# Set up variables& constants  
arraysizex=30
arraysizey=300  
temp_old =np.ones((arraysizey,arraysizex))  
temp_new =np.ones((arraysizey,arraysizex))  
temp_old=20*temp_old  
alpha=9.7e-5 # alpha of aLuminium  
dx=0.001 # 1 mm grid, 150 points, = 0.15 m  
dt=0.001  

# data location
localDir = Path(os.getcwd())
localpath = localDir / "results.xlsx"
  
# this function determines the delta between two shifted matrices   
def delta_2d (matrix):  
    matrixdown=np.roll(matrix,1,0)  
    matrixright=np.roll(matrix,1,1)  
    deltadown =(matrixdown -matrix)  
    deltaright =(matrixright -matrix)  
    delta=deltadown -np.roll(deltadown,-1,0)+deltaright-np.roll(deltaright,-1,1)  
    return delta  
  
# Run simulation.    
for t in range (0,1000001):  
    temp_old[0,15:16]=68  
    temp_old[299,0:30,]=20  
    temp_new=temp_old+dt/(dx*dx)*alpha*delta_2d(temp_old)  
    temp_new[0:arraysizey-1,0]=temp_new[0:arraysizey-1,1]  
    temp_new[0:arraysizey-1,arraysizex-1]=temp_new[0:arraysizey-1,arraysizex-2]  
    temp_new[0,0:arraysizex-1]=temp_new[1,0:arraysizex-1]  
    temp_new[arraysizey-1,0:arraysizex-1]=temp_new[arraysizey-2,0:arraysizex-1]  
      
    if (t%(10000)==0):  
        # display results.   
        im=plt.imshow(temp_new,cmap="gist_ncar")   
        # see https://matplotlib.org/examples/color/colormaps_reference.html  
        plt.colorbar(im)  
        plt.show()  
        print ("t=",t*dt)
        
    temp_old=copy.deepcopy(temp_new)  

 # %%