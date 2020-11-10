#%%
import numpy as np  
import random
import matplotlib.pyplot as plt  

height = 10
width = 10.0
max_agents = 1000
finished_agents = 0

# administration per agent  
x_pos = np.zeros((max_agents+1), np.float32)  
y_pos = np.zeros((max_agents+1), np.uint8)  
status = np.zeros((max_agents+1), np.uint16)

#column administration
column_count = np.zeros((11), np.float32)

x_pos.fill(0)  
y_pos.fill(0)  
status.fill(0)
column_count.fill(0)

def calculate_precentages(count, agents):
    ret = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for i in range(0,10):
        ret[i] = float(count[i]/agents*100)
        ret[i] = round(ret[i], 1)
    return ret

time = 0
while time < 1011:
    
    #all marbles move 1 down (y-1), random left (x -.5) or right (x +.5)
    for i in range(1, max_agents+1):
        if status[i] == 1:

            lr = random.randint(0,1)
            #move left
            if lr == 1:
                x_pos[i] = x_pos[i] - .5
                y_pos[i] = y_pos[i] - 1
            #move right
            if lr == 0:
                x_pos[i] = x_pos[i] + .5
                y_pos[i] = y_pos[i] - 1

            #plot new position
            plt.scatter(x_pos[i], y_pos[i], c='b', marker='o')

            if y_pos[i] == 0:
                #update column count with level 0 marbles
                column_count[int(x_pos[i])] = column_count[int(x_pos[i])] + 1
                #remove marbles at level 0
                status[i] = 0
                finished_agents = finished_agents + 1
            

    #generate new marble first 1000 cycles
    if time < 1000:
        status[time] = 1
        x_pos[time] = 4.5
        y_pos[time] = 9
        plt.scatter(x_pos[time], y_pos[time], c='b', marker='o')

    time = time + 1

    #plot all the stuff & save all the plots

    #plot dividers
    plt.scatter([4.5],[8.5], c='r', marker='^')
    plt.scatter([4,5],[7.5,7.5], c='r', marker='^')
    plt.scatter([3.5, 4.5, 5.5],[6.5,6.5,6.5], c='r', marker='^')
    plt.scatter([3,4,5,6],[5.5,5.5,5.5,5.5], c='r', marker='^')
    plt.scatter([2.5, 3.5, 4.5, 5.5, 6.5],[4.5,4.5,4.5,4.5,4.5], c='r', marker='^')
    plt.scatter([2,3,4,5,6,7],[3.5,3.5,3.5,3.5,3.5,3.5], c='r', marker='^')
    plt.scatter([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5],[2.5,2.5,2.5,2.5,2.5,2.5,2.5], c='r', marker='^')
    plt.scatter([1,2,3,4,5,6,7,8],[1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5], c='r', marker='^')
    plt.scatter([.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5],[.5,.5,.5,.5,.5,.5,.5,.5,.5], c='r', marker='^')

    #plot axes
    plt.title('Pascal\'s Marbles')
    plt.xlim(-.5,9.5)
    plt.ylim(-1.5,9.5)
    plt.xticks(np.arange(0, 10, 1.0))
    plt.yticks(np.arange(0, 10, 1.0))

    #keep track of percentages
    percentages = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    if finished_agents > 0:
        percentages = calculate_precentages(column_count, finished_agents)
    for i in range(0,10):
        plt.annotate((str(percentages[i]) + '%'), xy=(i,-.5), ha='center')
        plt.annotate((int(column_count[i])), xy=(i,-1),ha='center')

    plt.xlabel('Marble results')
    plt.ylabel('Falling depth')

    fname = 'Marbles-%03d.png' % time
    plt.savefig('images/'+fname)
    #plt.show(block = False)
    #plt.pause(.05)
    #plt.close
    plt.clf()

#print column count
for i in range(0,10):
    print('Column: ' + str(i+1) + ': ' + str(column_count[i]) + ', ' + str(column_count[i]/10) + '%')


# %%
