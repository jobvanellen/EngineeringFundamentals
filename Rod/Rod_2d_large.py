#%%
import numpy as np  
import matplotlib.pyplot as plt  
import copy
import os
import pandas as pd
from pathlib import Path  

# functions to calculate the delta T difference between 2 points  
def delta_2d_left (matrix):  
    matrixleft=np.roll(matrix,1,1)  
    delta =(matrixleft -matrix)  
    return delta  
  
def delta_2d_right (matrix):  
    matrixright=np.roll(matrix,-1,1)  
    delta =(matrixright -matrix)  
    return delta  
  
def delta_2d_down (matrix):  
    matrixright=np.roll(matrix,-1,0)  
    delta =(matrixright -matrix)  
    return delta  
  
def delta_2d_up (matrix):  
    matrixright=np.roll(matrix,1,0)  
    delta =(matrixright -matrix)  
    return delta  
  
# functions to calculate mixed value of k  
def determine_mixed_k_left (matrix):  
    matrixleft=np.roll(matrix,1,1)  
    mixed_k =2*(matrixleft *matrix)/(matrixleft+matrix)  
    return mixed_k  
  
def determine_mixed_k_up (matrix):  
    matrixleft=np.roll(matrix,1,0)  
    mixed_k =2*(matrixleft *matrix)/(matrixleft+matrix)  
    return mixed_k  
  
def determine_mixed_k_right (matrix):  
    matrixleft=np.roll(matrix,-1,1)  
    mixed_k =2*(matrixleft *matrix)/(matrixleft+matrix)  
    return mixed_k  
  
def determine_mixed_k_down (matrix):  
    matrixleft=np.roll(matrix,-1,0)  
    mixed_k =2*(matrixleft *matrix)/(matrixleft+matrix)  
    return mixed_k  
  
# Set up variables& constants
arraysizey = 341
arraysizex = 38

bar_length = 340
bar_width = 18

# temperature matrices
temp_old =np.ones((arraysizey,arraysizex))  
temp_new =np.ones((arraysizey,arraysizex))  
temp_old=20*temp_old  

# material property matrices
material_matrix=np.ones((arraysizey,arraysizex))  
k =np.ones((arraysizey,arraysizex))  
rho =np.ones((arraysizey,arraysizex))  
c =np.ones((arraysizey,arraysizex))

# power source array
pnetto = np.zeros((arraysizey,arraysizex))  

# heat flow array, not used
qflow = np.zeros((arraysizey,arraysizex)) 

dx=0.001 # 1 mm grid, 150 points, = 0.15 m  
dt=0.001  

# defining material constants. We will use a dict for this
# rod is 34 cm long, 1,8 cm in diameter 
# need aluminium and isolation(unknown material)
# teflon and stainless steel not needed in rod scenario 
# heatloss to water (and air)
aluminium = {  
    'rho': 2700,    # density, kg/m3
    'k': 237,       # thermal conductivity, W/m*K
    'c': 897,       # heat capacity, J/K
}  
isolation={  
    'rho': 40,  
    'k': 0.021,  
    'c': 2000,  
}
  
water={  
    'rho': 1000,  
    'k': 0.6,  
    'c': 4.186,  

} 
#used 
air={
    'rho' : 1.2,
    'k' : 0,
    'c' : 0
}


# we need a link between a number and the name of the material  
material_list={  
        1:aluminium,  
        2:isolation,  
        3:water, 
        #unused
        4:air
}  

# here we define the composition of our rectangle.
material_matrix[0:arraysizey-1,0:arraysizex-1]=2 
material_matrix[0:arraysizey-1, int((arraysizex)/2-9):int((arraysizex-1)/2+9)]=1
material_matrix[arraysizey-1, 0:arraysizex-1]=3

# power source  
pnetto [0:25, int((arraysizex-1)/2-2):int((arraysizex-1)/2+2)]=4300000

# display of the material  
plt.figure(figsize = (16,4))  
im=plt.imshow(material_matrix)   
plt.colorbar(im)
plt.scatter([int(arraysizex/2-9),int(arraysizex/2-9),int(arraysizex/2-9),\
    int(arraysizex/2-6),int(arraysizex/2-3),int(arraysizex/2),int(arraysizex/2-9),\
        int(arraysizex/2-9)],[26,103,178,178,178,178,253, 327], marker='.')   
plt.show() 

# copy all the values of the chosen materials in the different matrices y,x  
for x in range (0,arraysizex):  
    for y in range (0,arraysizey):  
        k[y,x]=material_list[material_matrix[y,x]]['k']  
        rho[y,x]=material_list[material_matrix[y,x]]['rho']  
        c[y,x]=material_list[material_matrix[y,x]]['c'] 

# determine the mixed k  
k_left=determine_mixed_k_left(k)  
k_right=determine_mixed_k_right(k)  
k_up=determine_mixed_k_up(k)  
k_down=determine_mixed_k_down(k)

# this is used for the graph at the end  
steps_to_show = 540    
temp_points=np.zeros((8,steps_to_show+1))    
temp_axis =np.zeros(steps_to_show+1)    
temp_teller=0  

# Run simulation
for t in range (0,5400001):
    #uncomment to switch off heat source after certain amount of time
    if t>3450001 :
        pnetto=0*pnetto
    

    # difference equation  
    temp_new=temp_old+pnetto*dt/(rho*c)+dt/(dx*dx*rho*c)*(k_left*delta_2d_left(temp_old)+k_right*delta_2d_right(temp_old)+k_up*delta_2d_up(temp_old)+k_down*delta_2d_down(temp_old))  
    
    # in principle our boundaries are floating (perfectly isolated)  
    temp_new[0:arraysizey-1,0]=temp_new[0:arraysizey-1,1]  
    temp_new[0:arraysizey-1,arraysizex-1]=temp_new[0:arraysizey-1,arraysizex-2]  
    temp_new[0,0:arraysizex-1]=temp_new[1,0:arraysizex-1]  
    temp_new[arraysizey-1,0:arraysizex-1]=temp_new[arraysizey-2,0:arraysizex-1]  
    # Isolation boundaries at 20 C 
    temp_new[0:arraysizey-1,0]=20
    temp_new[0:arraysizey-1, arraysizex-1]=20
    # Bottom boundary (water) at 15 C
    temp_new[arraysizey-1, 0:arraysizex-1]= 15
    # bottom of rod can't go below 20C
    if temp_new[arraysizey-2,int(arraysizex/2)] < 20:
        temp_new[arraysizey-2, int(arraysizex/2-9):int(arraysizex/2+9)]=20

    # for these boundaries we assume it radiates energy into space  
    #temp_new[0:arraysizey-2,0]=temp_new[0:arraysizey-2,0]-5.67e-8*dt*(temp_new[0:arraysizey-2,0]+273.15)**4  
    #temp_new[0:arraysizey-2,arraysizex-1]=temp_new[0:arraysizey-2,arraysizex-1]-5.67e-8*dt*(temp_new[0:arraysizey-2,arraysizex-1]+273.15)**4  
    #temp_new[0:50,arraysizex-1]=temp_new[0:50,arraysizex-1]-5.67e-8*dt*(temp_new[0:50,arraysizex-1]+273.15)**4  

    if (t%(10000)==0):
          
        # display results.   
        plt.figure(figsize = (16,4))  
        im=plt.imshow(temp_new,cmap="gist_ncar")   
        # see https://matplotlib.org/examples/color/colormaps_reference.html  
        plt.colorbar(im) 
        plt.show()  
        #plt.figure(figsize = (16,4))  
        #im2=plt.imshow(qflow,cmap="hot")   
        # see https://matplotlib.org/examples/color/colormaps_reference.html  
        #plt.colorbar(im2)  
        #plt.show()  
        print ("t=",t*dt)

        temp_points[0,temp_teller]=temp_new[26,int(arraysizex/2-9)]  
        temp_points[1,temp_teller]=temp_new[103,int(arraysizex/2-9)]  
        temp_points[2,temp_teller]=temp_new[178,int(arraysizex/2-9)]  
        temp_points[3,temp_teller]=temp_new[178,int(arraysizex/2-6)]  
        temp_points[4,temp_teller]=temp_new[178,int(arraysizex/2-3)]  
        temp_points[5,temp_teller]=temp_new[178,int(arraysizex/2)]  
        temp_points[6,temp_teller]=temp_new[253,int(arraysizex/2-9)]  
        temp_points[7,temp_teller]=temp_new[327,int(arraysizex/2-9)]  
        temp_axis[temp_teller]=t*dt    
        temp_teller=temp_teller+1            
        plt.plot(temp_axis,temp_points[0])  
        plt.plot(temp_axis,temp_points[1])  
        plt.plot(temp_axis,temp_points[2])  
        plt.plot(temp_axis,temp_points[3])  
        plt.plot(temp_axis,temp_points[4])  
        plt.plot(temp_axis,temp_points[5])  
        plt.plot(temp_axis,temp_points[6])  
        plt.plot(temp_axis,temp_points[7])  
        plt.show()
        
        #data to file
        if (t%(100000)==0) and t > 0:  
         # each x seconds (simualation time) the file is saved  
            file = open('testfile.txt','w')
            file.write('[\n')   
            for t in range (0,steps_to_show):
                if t > 0:
                    file.write(',\n')
                file.write('[')  
                file.write(str(temp_axis[t]))     
                file.write(',')  
                file.write(str(temp_points[0][t]))   
                file.write(',')  
                file.write(str(temp_points[1][t]))   
                file.write(',')  
                file.write(str(temp_points[2][t]))   
                file.write(',')  
                file.write(str(temp_points[3][t]))   
                file.write(',')  
                file.write(str(temp_points[4][t]))   
                file.write(',')  
                file.write(str(temp_points[5][t]))   
                file.write(',')  
                file.write(str(temp_points[6][t]))   
                file.write(',')  
                file.write(str(temp_points[7][t]))   
                file.write(']')  
            file.write('\n]')
            file.close()
            localdir = Path(os.getcwd())
            txt_path = localdir / 'testfile.txt'    
            df = pd.read_json(txt_path)
            excel_path = localdir / 'sim_data.xlsx'
            try:
                df.to_excel(excel_path)
            except:
                print("excel file write failed")
    
    temp_old=copy.deepcopy(temp_new)

print("Done!")
# %%


