
#%%
import numpy as np  
import random
import matplotlib.pyplot as plt  

max_x=20  
max_y=10  
max_agents=1000  
  
# 2-d matrices  
field = np.zeros((max_y,max_x), np.uint8)  
barrier = np.zeros((max_y,max_x), np.uint8)  
# administration per agent  
x_pos = np.zeros((max_agents+1), np.uint8)  
y_pos = np.zeros((max_agents+1), np.uint8)  
status = np.zeros((max_agents+1), np.uint16)    
# Status  
# 0 not yet started   
# 1 active  
# 2 finished  
  
barrier [0,5] = 1  
barrier [1,5] = 1  
barrier [2,5] = 1  
barrier [3,5] = 1  
barrier [4,5] = 1  
barrier [max_y - 4,5] = 1  
barrier [max_y - 3,5] = 1  
barrier [max_y - 2,5] = 1  
barrier [max_y - 1,5] = 1  
print("the barrier:")  
print (barrier)  
print ()  
# do you want a pause? uncomment the next line  
#dummy=input("press return in print window to continue")  
  
def position_allowed(y,x):  
    if y < 1 or x < 1:  
        return False        # Too close to the edge : rule g  
    elif y > max_y-1 or x > max_x-1:  
        return False    # Too close to the edge : rule g  
    elif barrier[y,x] > 0:        
        return False      # There is a barrier : rule f  
    elif field[y,x] > 0:      
        return False     # Position is not free : rule e  
    else:  
        return True  
  
generation_rate = 5  
# start with an empty slate  
amount_agents = 0  
time = 0  
field.fill(0)  
x_pos.fill(0)  
y_pos.fill(0)  
status.fill(0)  
while time < 1000:  
    #execute rules  
    if amount_agents > 0:  
        for i in range (1, max_agents+1):  
            if status[i] == 1:    # is the agent active?  
                dice = random.randint(0,5)  # throw a dice to determine walking distance  
                if dice == 0 :   #rule b  
                    pass  
                    #do nothing  
                if dice == 1 :   # rule c  
                    #down   
                    if position_allowed(y_pos[i]+1, x_pos[i]):  
                        field[y_pos[i], x_pos[i]] = 0          
                        y_pos[i] = y_pos[i]+1  
                        field[y_pos[i], x_pos[i]] = 1          
                if dice == 2 :   # rule c  
                    #up   
                    if position_allowed(y_pos[i]-1,x_pos[i]):  
                       field[y_pos[i],x_pos[i]]=0          
                       y_pos[i]=y_pos[i]-1  
                       field[y_pos[i],x_pos[i]]=1          
                if dice == 3: # rule d  
                    #right   
                    if position_allowed(y_pos[i],x_pos[i]+1):  
                       field[y_pos[i],x_pos[i]]=0          
                       x_pos[i] = x_pos[i]+1  
                       field[y_pos[i],x_pos[i]]=1
                    
                #diagonal movement
                #up
                if dice == 4 and position_allowed(y_pos[i]-1,x_pos[i]+1):
                        field[y_pos[i],x_pos[i]]=0
                        x_pos[i] = x_pos[i]+1          
                        y_pos[i] = y_pos[i]-1  
                        field[y_pos[i],x_pos[i]]=1

                 #down
                if dice == 5 and position_allowed(y_pos[i]+1, x_pos[i]+1):
                        field[y_pos[i], x_pos[i]] = 0          
                        x_pos[i]= x_pos[i]+1
                        y_pos[i]= y_pos[i]+1
                        field[y_pos[i], x_pos[i]] = 1

                if x_pos[i] == max_x-1:     # removing agents  
                    field[y_pos[i], x_pos[i]] = 0          
                    status[i] = 2
                
                #plot new position
                plt.scatter(x_pos[i], y_pos[i], c='r', marker='>') 
  
    # determine if new agent is generated  
    if random.randint(1, generation_rate) == 1:  
        #Check free position: 
        succeeded = False
        teller = 0
        while (not(succeeded)and teller < 10):  
            pos_x=1   
            pos_y=random.randint(2, max_y-2)  
            if field[pos_y, pos_x] == 0:  
                succeeded = True  
            teller = teller+1      
        if succeeded:  
            # generate agent  
            amount_agents = amount_agents + 1  
            x_pos[amount_agents] = pos_x  
            y_pos[amount_agents] = pos_y  
            field[y_pos[amount_agents], x_pos[amount_agents]] = 1          
            status[amount_agents] = 1

            #add new agent to plot
            plt.scatter(pos_x, pos_y, c='r', marker='>')

    time = time+1  

    #print(field)  
    #print()  
    # do you want a pause? uncomment the next line  
    # dummy=input("press return in print window for next value")

    plt.scatter([5,5,5,5,5,5,5,5,5,5], [0,1,2,3,4,6,7,8,9,10], c='b', marker='s')
    plt.title('agent visual')
    plt.xlim(0,20)
    plt.ylim(0,11)
    plt.xlabel('Distance covered')
    plt.ylabel('Starting line')
    fname = 'Agent Race-%03d.png' % time
    #plt.savefig('images/'+fname)
    plt.show(block = False)
    plt.pause(.05)
    plt.close
    plt.clf()

    
  
# data extraction      
num_finished_agents = 0  
for i in range (1,max_agents+1):  # how many agents made it till the end?  
    if status[i]==2:  
        num_finished_agents=num_finished_agents+1  
  
print ("Generation_rate: ",1/generation_rate, " Actual_througput_rate: ",num_finished_agents/time) 

# %%
