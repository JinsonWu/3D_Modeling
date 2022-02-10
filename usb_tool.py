import serial.tools.list_ports

port = list(serial.tools.list_ports.comports())
for p in port:
	print (p)
