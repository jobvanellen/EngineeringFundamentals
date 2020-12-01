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
arraysizey = 350
arraysizex = 80

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
# need aluminium and isolation(unknown material)
# teflon and stainless steel not needed in rod scenario 
# heatloss to water (and air)
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
material_matrix[25:325, int(arraysizex/2-15):int(arraysizex/2+15)]=1

# we'll add a power source  
pnetto [25:50, 38:42]=2000000

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

# Run simulation
for t in range (0,100001):
    #if t>50001 :
        #pnetto=0*pnetto
    # force water to 20 c
    #temp_old [watery, waterx] = 0

    # this is the actual difference equation  
    temp_new=temp_old+pnetto*dt/(rho*c)+dt/(dx*dx*rho*c)*(k_left*delta_2d_left(temp_old)+k_right*delta_2d_right(temp_old)+k_up*delta_2d_up(temp_old)+k_down*delta_2d_down(temp_old))  
    
    # in principle our boundaries are floating (perfectly isolated)  
    temp_new[0:arraysizey-1,0]=temp_new[0:arraysizey-1,1]  
    temp_new[0:arraysizey-1,arraysizex-1]=temp_new[0:arraysizey-1,arraysizex-2]  
    temp_new[0,0:arraysizex-1]=temp_new[1,0:arraysizex-1]  
    temp_new[arraysizey-1,0:arraysizex-1]=temp_new[arraysizey-2,0:arraysizex-1]  
    # This boundary is kept at a constant temperature, we force it to 20c  
    temp_new[0:arraysizey-1,0]=20 
    # for this boundary we assume it radiates energy into space  
    #temp_new[0:50,arraysizex-1]=temp_new[0:50,arraysizex-1]-5.67e-8*dt*(temp_new[0:50,arraysizex-1]+273.15)**4  

    if (t%(1000)==0):  
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

# %%
