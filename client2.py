import socket
import json
import time
# HOST = '127.0.0.1'
HOST = '192.168.122.88'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


MAX_SIZE=1024
WaitTime=0.01
def GetRequest(key,s):
	s.sendall(str.encode("GET"))
	ack=s.recv(MAX_SIZE).decode()
	if ack=="OK":
		s.sendall(str.encode(key))
		value=s.recv(MAX_SIZE).decode()


def StartClient(s):
	counter=0
	while True:
		key="1"
		ans=GetRequest(key,s)
		time.sleep(WaitTime)
		counter+=1
		if counter%1000==0:
			print(counter," requests done")


def CreateConnection():
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	return s


s=CreateConnection()
StartClient(s)


