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
time = 0

def calculate_percentages(count, agents):
    percentages = np.zeros((max_agents+1), np.uint32)
    for i in range(0,10):
        percentages[i] = float(count[i]/agents*100)
        percentages[i] = round(percentages[i], 1)
    return percentages

def plot_all_the_stuff(count, agents):
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
    percentages = np.zeros((max_agents+1), np.uint32)
    if agents > 0:
        percentages = calculate_percentages(count, agents)
    for i in range(0,10):
        plt.annotate((str(percentages[i]) + '%'), xy=(i,-.5), ha='center')
        plt.annotate((int(count[i])), xy=(i,-1),ha='center')

    plt.xlabel('Marble results')
    plt.ylabel('Falling depth')

    #save plot
    #fname = 'Marbles-%03d.png' % time
    #plt.savefig('images/'+fname)

    #show and close plot
    plt.show(block = False)
    plt.pause(.05)
    #plt.close()
    plt.clf()

def plot_agent(x,y):
    plt.scatter(x, y, c='b', marker='o')


while time < 1011:
    #print("Time: %d" % time)
    
    #FOR every marble: move 1 down (y-1), random left (x -.5) or right (x +.5)
    for i in range(1, max_agents+1):
        #only IF marble is active
        if status[i] == 1:
            lr = random.randint(0,1)
            #move down
            y_pos[i] = y_pos[i] - 1
            #move left if 0
            if lr == 0:
                x_pos[i] = x_pos[i] - .5
            #move right if 1
            if lr == 1:
                x_pos[i] = x_pos[i] + .5
            #plot new position
            plot_agent(x_pos[i], y_pos[i])
            
            #marbles at bottom (IF y==0) to be removed and counted
            if y_pos[i] == 0:
                #update column count with level 0 marbles
                column_count[int(x_pos[i])] = column_count[int(x_pos[i])] + 1
                #remove marbles at level 0
                status[i] = 0
                finished_agents = finished_agents + 1
            

    #generate new marble only first 1000 cycles
    if time < max_agents+1:
        status[time] = 1
        x_pos[time] = 4.5
        y_pos[time] = 9
        plot_agent(x_pos[time], y_pos[time])

    time = time + 1

    #plot all the stuff & save all the plots
    plot_all_the_stuff(column_count, finished_agents)
    

#print column count
for i in range(0,10):
    print('Column: ' + str(i+1) + ': ' + str(column_count[i]) + ', ' + str(column_count[i]/10) + '%')


# %%
