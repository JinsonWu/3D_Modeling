import pylidar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from time import sleep
import timeit
import numpy as np
from pyfirmata import Arduino, SERVO
import socket

#2d simulation (for test)
def draw():
    plt.figure(1)
    plt.cla()
    plt.ylim(-9000,9000)
    plt.xlim(-9000,9000)
    plt.scatter(x,y,c='b',s=8)
    plt.show()

def write_file(data):
    fout = "./data.txt"
    fo = open(fout, "w")
    for k, v in data.items():
        fo.write(str(v)+'\n')
    fo.close()

def connect():
    port = "/dev/ttyUSB0"
    obj = pylidar.YdLidarX4(port)
    if(obj.Connect()):
        print("Connected to Lidar!")
    else:
        print("Error connecting to device")
    return obj

"""
#coordinates compensation to have "continuous" change
def com(data):
    k_ = np.zeros(360)
    k = 0
    k_cnt = 0
    a_ = 0
    b_ = 0
    for angle in range(360):
        if (data[angle] == 0): 
            k = 1
            a = angle
            while (data[a] == 0):
                if (a + 1 == 360):
                    a = 0
                else :
                    a = a + 1
                k = k+1             
            k_[angle] = k-1
            if ((k-1 > 0) & (k_[angle-1] == 0)):
                k_cnt = k
            if (angle == 0):
                a_ = 359
                b_ = angle+k
            elif (angle+k >= 360):
                a_ = angle-1
                b_ = angle+k-360
            else:
                a_ = angle-1
                b_ = angle+k
            diff = abs(data[a_]-data[b_])
            com = diff/k

            #if the nearby two coordinates are seperate over 1m, use partially insertion (directly insert numbers to the empties)
            if (diff > 1.):
                if (k > k_cnt/2):
                    data[angle] = data[a_]
                else:
                    data[angle] = data[b_]
            
            #if not, use linear insertion
            else:
                if (data[a_] > data[b_]):
                    data[angle] = data[a_] - com
                else:
                    data[angle] = data[a_] + com
    return data
"""

#use mean to have more precise coordinates
def mean(data1, data2, data3):
    for i in range(len(data1)):
        data1[i] = (data1[i] + data2[i] + data3[i])/3
    return data1

#coordinates normalization
def plot(i, data):
    tar1 = i
    tar2 = i + 180
    for j in range(0,180):
        xx[tar1,j] = xx[tar1,j]*data[j]
        yy[tar1,j] = yy[tar1,j]*data[j]
        zz[tar1,j] = zz[tar1,j]*data[j]
        xx[tar2,j] = xx[tar2,j]*data[359-j]
        yy[tar2,j] = yy[tar2,j]*data[359-j]
        zz[tar2,j] = zz[tar2,j]*data[359-j]

#start timer
start = timeit.default_timer()

#connect to host to plot
HOST = '140.113.217.202'
PORT = 6011
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
print("HOST Connect!")

#connect to YDLidar
obj = connect()
gen = obj.StartScanning()

#connect to Arduino (Motor)
port = "/dev/ttyACM0"
pin = 9
board = Arduino(port)
board.digital[pin].mode = SERVO
board.digital[pin].write(i)

#Prerequisites for 3D Simulation
theta = np.linspace(0,2*np.pi,360,dtype='float16')
phi = np.linspace(0,np.pi,180,dtype='float16')
xx = np.outer(np.cos(theta),np.sin(phi))
yy = np.outer(np.sin(theta),np.sin(phi))
zz = np.outer(np.ones(np.size(theta)),np.cos(phi))

#scan with respect to per degree
for i in range(180):   
    print("degree: ", str(i))
    board.digital[pin].write(i)
    sleep(0.1)
    board.digital[pin].write(i)
    sleep(1) 
    data1 = next(gen)
    data2 = next(gen)
    data3 = next(gen)
    data = mean(data1, data2, data3)    
    plot(i, data)

#save file
np.savetxt('xx.txt', xx, delimiter=',')
np.savetxt('yy.txt', yy, delimiter=',')
np.savetxt('zz.txt', zz, delimiter=',')
write_file(data)

#disconnection
obj.StopScanning()
obj.Disconnect()
board.digital[9].write(180)

#time stop
end = timeit.default_timer()
print("Process Time: ", end-start)

#load file
print("Start Simulating!")
xx= np.loadtxt('xx.txt',ndmin=2, delimiter=',', dtype = 'float16')
yy= np.loadtxt('yy.txt',ndmin=2, delimiter=',', dtype = 'float16')
zz= np.loadtxt('zz.txt',ndmin=2, delimiter=',', dtype = 'float16')

#passing data
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

