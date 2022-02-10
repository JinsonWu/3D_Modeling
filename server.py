import socket
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

HOST = '140.113.217.202'
PORT = 6011

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Waiting connection...")
clnt,addr = s.accept()
print("Connect!")
print("Receiving data...")

x=[]
y=[]
z=[]
#receiving data
for i in range(0,180):
    clnt.send(b'\x00')
    data = clnt.recv(2048)
    x.append(np.frombuffer(data, dtype='float16'))
    clnt.send(b'\x00')
    data = clnt.recv(2048)
    y.append(np.frombuffer(data, dtype='float16'))
    clnt.send(b'\x00')
    data = clnt.recv(2048)
    z.append(np.frombuffer(data, dtype='float16'))
print("Finish!")
s.close()

for i in range(1,180):
	x[0] = np.vstack((x[0], x[i]))
	y[0] = np.vstack((y[0], y[i]))
	z[0] = np.vstack((z[0], z[i]))


fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
col = np.reshape(y[0],(64800,))

manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
"""
for i in range(0,390,30):
	ax.cla()
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.view_init(0,i)
	ax.scatter3D(x[0],z[0],y[0],s=0.5,c=col,alpha=0.4)
	plt.pause(0.3)
"""
for i in range(0,390,30):
	ax.cla()
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.view_init(0,i)
	ax.plot_surface(x[0],z[0],y[0],cmap='copper',alpha=0.5)
	plt.pause(0.5)
plt.close()
