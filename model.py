import threading
import pylidar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math    
import time
import numpy as np
import socket
"""
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
"""

xx= np.loadtxt('xx.txt',ndmin=2, delimiter=',', dtype = 'float16')
yy= np.loadtxt('yy.txt',ndmin=2, delimiter=',', dtype = 'float16')
zz= np.loadtxt('zz.txt',ndmin=2, delimiter=',', dtype = 'float16')
"""
ax.cla()


min_ = min(np.amin(xx), np.amin(yy), np.amin(zz))
max_ = max(np.amax(xx), np.amax(yy), np.amax(zz))
ax.set_xlim(min_, max_)
ax.set_ylim(min_, max_)
ax.set_zlim(min_, max_)

col = np.reshape(yy,(64800,))

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.view_init(0, 0)
ax.scatter3D(xx, zz, yy, s=0.2, c=col, marker='o',alpha=0.2)
#cbar = fig.colorbar(cube, shrink=0.6, aspect=5)
plt.show()
"""

HOST = '140.113.217.202'
PORT = 6011

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

print("Connect!")
print("Passing data...")

for i in range(0,180):
    data = s.recv(2048)
    s.sendall(xx[:,i].tobytes())
    data = s.recv(2048)
    s.sendall(yy[:,i].tobytes())
    data = s.recv(2048)
    s.sendall(zz[:,i].tobytes())
print("Finish!")
s.close()
