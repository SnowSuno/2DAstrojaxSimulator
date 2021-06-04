import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation




fig, ax = plt.subplots()

ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))

points, = ax.plot([], [], 'ro')

def init():
    points.set_data([], [])
    return points,

def animate(i):
    x = [np.sin(0.01*i), -np.sin(0.01*i)]
    y = [np.cos(0.01*i), 0]
    points.set_data(x, y)
    return points,


ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=1000, interval=1, blit=True)

plt.show()

