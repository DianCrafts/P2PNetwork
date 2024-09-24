import socket
import time
import os
import sys
import threading
UDP_PORT = 8080#int(input("enter port number"))
nodeName = input("enter your name")
IP = input("enter ip")#"127.0.0.1"
initialFileAddr = input("file name")#"node1.txt"

#file avale kushe ha ro mikhune mirize tu list
def readFile():
	fo = open(initialFileAddr, "r")
	list = [line.rstrip('\n') for line in open(initialFileAddr)]
	print(list)
	fo.close()	
	return list


#socket udp misaze bara server
def UDPServerSocket(backlog=5 ):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((IP, UDP_PORT))
	return sock


#socket udp misaze bara client
def UDPClientSocket(backlog=5 ):
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	return sock2

#socket tcp misaze bara server
def TCPServerSocket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((IP, 8080))
	s.listen(5)
	return s

list = readFile()
sock = UDPServerSocket()
sock2 = UDPClientSocket()
TCPSock = TCPServerSocket()


#server e tcp : montazer mimune bara payam .bad ba tavajoh b payam method khasi ro seda mizne
def TCPServer():
	while 1:
		c, addr = TCPSock.accept()
		#print('recieving')
		m = c.recv(1024).decode()
		if m[:3] == 'get':
			getFile(m)
		if m[:4] == 'file':
			name = nodeName+'/' + m.split()[1].split('/')[1]
			c.send('name got'.encode())
			f = open(name,'ab')
			while 1:
			#	print ("Receiving...")
				l= c.recv(1024)
				f.write(l)
				if not l:
					break
			f.close()
			print ("Done Receiving")
		# c.close()
		c.shutdown(socket.SHUT_WR)
		# data.split()



#client tcp
def TCPClient(port , ip ,message):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	s.send(message.encode())
	data = s.recv(2048)
	#print(data)
	s.close()


#server e udp : montazer mimune bara payam .bad ba tavajoh b payam method khasi ro seda mizne
def UDPServer():
	while 1:
		data, addr = sock.recvfrom(1024)
		x = data.decode()
		if x[:3] == 'get':
			checkFileExistance(x)
		if x[:5] == 'found':
			print(x)
			callTcpClient(x)
		if x[:9] == 'discovery':
			y = x.split('&')[1]
			list1 = y.split('#')
			discover(list1)

#client bara ersal darkhast az no tcp
def callTcpClient(x):
	port = int(x.split()[3])
	ip = (findIp(x.split()[1]))
	fileDir = x.split()[2]
	message = ('get' + '\t' + str(nodeName) + '\t' + str(TCPSock.getsockname()[1]) + '\t' + str(fileDir))#darkhast get bara file mifreste
	TCPClient(port , ip , message)


#file ro peyda mikone va ersal
def getFile(x):
	port = int(x.split()[2])
	ip = (findIp(x.split()[1]))
	fileDir = x.split()[3]
	#print(fileDir)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip,port))
	s.send(('file' + '\t' + fileDir).encode())
	recv_msg = s.recv(1024)#inja mige k esme file umad
	#print(recv_msg.decode())
	f = open(fileDir,'rb')
	#print ('Sending...')
	while 1:
		#print ('Sending...')
		l = f.read(1024)
		s.send(l)
		if sys.getsizeof(l) == 33:
			break
	f.close()
	print('done sending')
	s.close()


#gets name and finds ip
def findIp(name):
	for i in list:
		x = i.split()
		if name == x[0] :
			return x[1]


#dar javab udp  baresi mikune file mojode ya na
def checkFileExistance(x):
	dir =  nodeName
	sendIp = findIp(x.split()[1])
	fileName  = x.split()[2]
	fileDir = find(fileName ,dir)
	if fileDir != None:
		sendFound(sendIp ,fileDir)

#sends found pm if file found
def sendFound(sendIp , fileDir):
	sock2.sendto(str.encode('found' + '\t' + str(nodeName) + '\t' + str(fileDir) + '\t' + str(TCPSock.getsockname()[1])), (sendIp, UDP_PORT))

#finds file
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
        	return os.path.join(root, name )


#request for all nodes to check if they have file
def sendRequestForFile():
	while 1:
		fileName = input("enter file name\n")
		for i in list:
			ip = i.split()[1]
			sock2.sendto(str.encode('get' +'\t'+ nodeName +'\t'+ fileName), (ip, UDP_PORT))
				


#send discovery every 10 seconds
def sendForDiscovery():
	while 1:
		me = nodeName + '\t\t' + IP
		data = "discovery&"
		for i in list:
			data = data + i + "#"
		data += me
		for i in list:
			# print(i)
			ip = i.split()[1]
			sock2.sendto(str.encode(data), (ip, UDP_PORT))
		time.sleep(5)


#update list
def discover(disList):
	for i in disList:
		flag = False
		x = i.split()[0]
		if x == nodeName:
			continue
		for j in list:
			y = j.split()[0]
			if x == y:
				flag = True
		if flag == False:
			list.append(i)


t = threading.Thread(target=UDPServer)
t2 = threading.Thread(target=sendForDiscovery )
t3 = threading.Thread(target=sendRequestForFile )
t4 = threading.Thread(target=TCPServer )
# threads.append(t)
t.start()
t2.start()
t3.start()
t4.start()

 	
#  	clientsock, clientaddr = s.accept()
#  	print("accept")
#  	host2, port2 = clientsock.getpeername()
#  	print(host2)
#  	print(port2)
#  	break
# 		# not self.shutdown:
# 	    # try:
# 		self.__debug( 'Listening for connections...' )
# 		clientsock, clientaddr = s.accept()
# 		clientsock.settimeout(None)

# 		t = threading.Thread( target = self.__handlepeer, args = [ clientsock ] )
# 		t.start()
# 	 #    except KeyboardInterrupt:
# 		# self.shutdown = True
# 		# continue
# 	 #    except:
# 		# if self.debug:
# 		#     traceback.print_exc()
# 		#     continue
# 	# end while loop

# 	self.__debug( 'Main loop exiting' )
# 	s.close()
#     # end mainloop method

#def discovery():
