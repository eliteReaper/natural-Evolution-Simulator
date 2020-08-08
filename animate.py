'''
    This Python File is for visualizing realtime data about the Units who are currently alive on the grid
    - We can watch the current population
    - We can watch the current population sense
    - We can watch the current population speed
    - We can watch the current population size
'''

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

fig, a = plt.subplots(2, 2)
# plt.subplots_adjust(hspace=1, wspace=1)
a[0][0].set_title("Speed/Sense")
a[0][1].set_title("Sense/Size")
a[1][0].set_title("Size/Speed")
a[1][1].set_title("Population")
        
# plt.style.use("seaborn-darkgrid")
pop = []
def animate(i):
    
    '''The testing.py file continously updates the data.txt file with data about the current population'''

    global pop
    x = []
    y = []
    z = []
    with open ("data.txt", "r") as rd:
        data = rd.readlines()
        for unit in data:
            sp, se, si = unit[:-1].split()
            sp = float(sp)
            se = float(se)
            si = float(si)
            x.append((int(sp*1000)/1000))
            y.append((int(se*1000)/1000))
            z.append((int(si*1000)/1000))
        pop.append(len(data))

    if len(data) > 5:
        '''Maybe a 3D Graph later down the line'''
        # ax.cla()
        # ax.set_xlabel("Sense")
        # ax.set_ylabel("Speed")
        # ax.set_zlabel("Size")
        # ax.scatter(x, y, z)

        '''Clearing the previous graph'''
        a[0][0].cla()
        a[0][1].cla()
        a[1][0].cla()
        a[1][1].cla()

        '''Updating the graphs with the current data'''

        a[0][0].set_xlabel("Speed")
        a[0][0].set_ylabel("Sense")
        a[0][0].scatter(x, y)

        a[0][1].set_xlabel("Sense")
        a[0][1].set_ylabel("Size")
        a[0][1].scatter(y, z)

        a[1][0].set_xlabel("Size")
        a[1][0].set_ylabel("Speed")
        a[1][0].scatter(z, x)

        a[1][1].set_xlabel("Time")
        a[1][1].set_ylabel("Population")
        a[1][1].plot(range(0, len(pop)), pop)

        
'''Animating at an interval of 1000ms'''
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.tight_layout()
plt.show()