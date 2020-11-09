import numpy as np  
import random  
import matplotlib.pyplot as plt  
  
x = np.zeros((10),np.uint8)  
y = np.zeros((10),np.uint8)  
      
for i in range (1,15):  
    for j in range (1,10):  
        x[j]=random.randint(0,10)  
        y[j]=random.randint(0,10)  
    plt.scatter(x,y,c='b')  
    plt.title('example @ Bart Bozon')  
    plt.ylim (0,10)  
    plt.xlim (0,10)  
    plt.xlabel('nice axis')  
    plt.ylabel('really nice')  
    fname = 'name-%03d.png' % i  
    plt.savefig(fname)  
    plt.show()         
