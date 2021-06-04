from numpy import pi, sin, cos
import matplotlib.pyplot as plt
from tqdm import trange

from matplotlib import animation
# simulation setting
dt = 10**-4
speed = 4000


# constants/parameters
g = 9.81

m1 = 17.5*10**-3
m2 = 17.5*10**-3


# kinetics
initial = [0.5359995637977941, 2.790011502298171, 9.818272698011025, 0.0028165473659351077, 0.6084960000022929]
'''
    [0.702105624776348,     # r
           0.756737508197128,     # w1
           10.5124506461295,      # w2
           -0.00358421714606101,  # rD
           0.5906400000021759]    # T
'''

theta = 0
phi = pi
L = 0.8
r = initial[0]


w1 = initial[1]
w2 = initial[2]
rD = initial[3]

w = 2*pi/0.45647
A = 0.00
t = 0



# period check
n = 1  # number of rotations
tprev = 0
m = 1

T_tot = 0
w1t_tot = 0
w2t_tot = 0
rDt_tot = 0
rt_tot = 0


T = 0
w1t = 0
w2t = 0
rDt = 0
rt = 0

steps = 100000
skip = 20
data = [{}] * (steps//skip)

print('Calculating...')
for i in trange(steps):
    numer = -(cos(phi-theta) - 1)*(r*w1**2 + g*cos(theta)) + (L-r)*w2**2 + \
        g*cos(phi) + r*w1**2*cos(phi-theta) + \
        g*sin(theta)*sin(phi-theta)
    denom = (1/m1)*(cos(phi-theta)-1)**2 + (1/m2) + (1/m1)*sin(phi-theta)**2
    T = numer / denom

    rDD = r*w1**2 + g*cos(theta) + (T/m1)*(cos(phi-theta) - 1)
    thetaDD = (1/r)*(-2*rD*w1 - g*sin(theta) + (T/m1)*sin(phi-theta))
    phiDD = (1/(L-r))*(2*rD*w2 - g*sin(phi) + (rDD - r*w1**2)
                       * sin(phi-theta) - (r*thetaDD + 2*rD*w1)*cos(phi-theta))

    w1 += thetaDD*dt
    w2 += phiDD*dt
    rD += rDD*dt

    theta += w1*dt
    phi += w2*dt
    r += rD*dt

    x1, y1 = r*sin(theta), -r*cos(theta)
    x2, y2 = (x1 + (L-r)*sin(phi)), (y1 - (L-r)*cos(phi))

    t += dt

    if i % 10 == 0:
        data_set = {'x': [x1, x2], 'y': [y1, y2]}
        data[i//skip] = data_set

print('Calculation complete')



fig, ax = plt.subplots()
fig.set_figheight(7)
fig.set_figwidth(7)

ax.set_xlim((-0.5, 0.5))
ax.set_ylim((-1, 0))

markers_on = [1, 2]
points, = ax.plot([], [], marker='o', markersize=10, lw=1, c='black',
                  mfc='red', markevery=markers_on)

def init():
    points.set_data([], [])
    return points,

def animate(frame):
    x = [0] + data[frame]['x']
    y = [0] + data[frame]['y']
    points.set_data(x, y)
    return points,


ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=len(data), interval=1, blit=True)


plt.show()




