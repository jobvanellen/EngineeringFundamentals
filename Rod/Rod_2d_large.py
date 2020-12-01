"""  
@author: Bart Bozon  
Script for 2d temperature profile, optimised for speed 
"""    
#%%
import numpy as np  
import matplotlib.pyplot as plt  
import copy  
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
arraysizey=100  
arraysizex=200  
temp_old =np.ones((arraysizey,arraysizex))  
temp_new =np.ones((arraysizey,arraysizex))  
temp_old=20*temp_old  
material_matrix=np.ones((arraysizey,arraysizex))  
k =np.ones((arraysizey,arraysizex))  
rho =np.ones((arraysizey,arraysizex))  
c =np.ones((arraysizey,arraysizex))  
pnetto = np.zeros((arraysizey,arraysizex))  
qflow = np.zeros((arraysizey,arraysizex))  
dx=0.001 # 1 mm grid, 150 points, = 0.15 m  
dt=0.001  
  
# defining material constants. We will use a dict for this  
aluminium = {  
    'rho': 2700,  
    'k': 237,  
    'c': 897,  
}  
stainless_steel={  
    'rho': 7500,  
    'k': 14.4,  
    'c': 502,  
}  
teflon={  
    'rho': 2200,  
    'k': 0.25,  
    'c': 1000,  
}  
# we need a link between a number and the name of the material  
material_list={  
        1:aluminium,  
        2:stainless_steel,  
        3:teflon  
}  
  
# here we define the composition of our rectangle.  
material_matrix[0:arraysizey-1,0:arraysizex-1]=2   
material_matrix[10:15,10:80]=1  
material_matrix[20:25,10:80]=1  
material_matrix[30:35,10:80]=1  
material_matrix[40:45,10:80]=1  
material_matrix[50:55,10:80]=1  
material_matrix[20:35,110:180]=1  
material_matrix[40:75,30:60]=3  
material_matrix[10:25,140:150]=3  
material_matrix[30:50,140:150]=3  
material_matrix[15:20,160:arraysizex-1]=3  
material_matrix[0:20,160:165]=3  
# we'll add a power source  
pnetto [10:50,90:100]=2000000  
# display of the material  
plt.figure(figsize = (16,4))  
im=plt.imshow(material_matrix)   
plt.colorbar(im)  
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
steps_to_show = 500    
temp_points=np.zeros((11,steps_to_show+1))    
temp_axis =np.zeros(steps_to_show+1)    
temp_teller=0    
  
  
# Run simulation.    
for t in range (0,1000001):  
    if t>500001 :  
        pnetto=0*pnetto  
    # we force part of the material to 30 c  
    temp_old[80:85,170:180]=30  
    # we force part of the material to 10 c  
    temp_old[80:85,15:25]=10  
      
    # this is the actual difference equation  
    temp_new=temp_old+pnetto*dt/(rho*c)+dt/(dx*dx*rho*c)*(k_left*delta_2d_left(temp_old)+k_right*delta_2d_right(temp_old)+k_up*delta_2d_up(temp_old)+k_down*delta_2d_down(temp_old))  
    # we will calculate the q flow as well. This is only for display purposes  
    if (t%(10000)==0):  
     qflow=abs(1/(dx*dx*rho*c)*(k_left*delta_2d_left(temp_old)+k_up*delta_2d_up(temp_old)))  
    # the boundaries are incorrectly calculated (due to the matrix roll over). We force them zero  
    qflow [0:arraysizey,0]=0  
    qflow [0:arraysizey,arraysizex-1]=0  
    qflow [0,0:arraysizex]=0  
    qflow [arraysizey-1,0:arraysizex]=0  
      
    # in princple our boundaries are floating (perfectly isolated)  
    temp_new[0:arraysizey-1,0]=temp_new[0:arraysizey-1,1]  
    temp_new[0:arraysizey-1,arraysizex-1]=temp_new[0:arraysizey-1,arraysizex-2]  
    temp_new[0,0:arraysizex-1]=temp_new[1,0:arraysizex-1]  
    temp_new[arraysizey-1,0:arraysizex-1]=temp_new[arraysizey-2,0:arraysizex-1]  
    # This boundary is kept at a constant temperature, we force it to 15c  
    temp_new[0:arraysizey-1,0]=15  
    # for this boundary we assume it radiates energy into space  
    temp_new[0:50,arraysizex-1]=temp_new[0:50,arraysizex-1]-5.67e-8*dt*(temp_new[0:50,arraysizex-1]+273.15)**4  
    # the plots are shown each x seconds.  
    if (t%(10000)==0):  
        # display results.   
        plt.figure(figsize = (16,4))  
        im=plt.imshow(temp_new,cmap="gist_ncar")   
        # see https://matplotlib.org/examples/color/colormaps_reference.html  
        plt.colorbar(im)  
        plt.show()  
        plt.figure(figsize = (16,4))  
        im2=plt.imshow(qflow,cmap="hot")   
        # see https://matplotlib.org/examples/color/colormaps_reference.html  
        plt.colorbar(im2)  
        plt.show()  
        print ("t=",t*dt)  
        # these points are used to make the graph  
        temp_points[0,temp_teller]=temp_new[40,10]  
        temp_points[1,temp_teller]=temp_new[40,30]  
        temp_points[2,temp_teller]=temp_new[40,50]  
        temp_points[3,temp_teller]=temp_new[40,70]  
        temp_points[4,temp_teller]=temp_new[40,90]  
        temp_points[5,temp_teller]=temp_new[80,25]  
        temp_points[6,temp_teller]=temp_new[80,50]  
        temp_points[7,temp_teller]=temp_new[80,75]  
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
        if (t%(100000)==0):  
         # each x seconds (simualation time) the file is saved  
         file = open('testfile.txt','w')   
         for t in range (0,500):  
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
            file.write(',')  
            file.write(str(temp_points[8][t]))   
            file.write(',')  
            file.write(str(temp_points[9][t]))   
            file.write(',')  
            file.write(str(temp_points[10][t]))   
            file.write('\n')   
         file.close()   
    temp_old=copy.deepcopy(temp_new)  

# %%
