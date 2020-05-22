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
        # ax.cla()
        # ax.set_xlabel("Sense")
        # ax.set_ylabel("Speed")
        # ax.set_zlabel("Size")
        # ax.scatter(x, y, z)
        a[0][0].cla()
        a[0][1].cla()
        a[1][0].cla()
        a[1][1].cla()

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

        
        
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.tight_layout()
plt.show()