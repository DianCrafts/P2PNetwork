import socket
import threading
UDP_IP = "127.0.0.1"
def makeserversocket2(backlog=5 ):
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	return sock2

sock2 = makeserversocket2()


def sendData():
	MESSAGE = "Hello, World!"
	send_PORT = int(input("enter send port number"))
	sock2.sendto(str.encode(MESSAGE), (UDP_IP ,send_PORT))


sendData()