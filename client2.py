import socket
import json
import time
import threading
# HOST = '127.0.0.1'
HOST = '192.168.122.247'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

LOCALHOST='127.0.0.1'

MAX_SIZE=1024
HighLoad=100000 #High Load
LowLoad=10 #High Load
CurrentLoad=HighLoad
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
		time.sleep(1.0/CurrentLoad)
		counter+=1
		if counter%1000==0:
			print(counter," requests done")


def CreateConnection(h,p):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((h, p))
	return s


def LoadManagement():
	while True:
		trigger=input()
		if trigger=="INCREASE":
			CurrentLoad=HighLoad
		elif trigger=="DECREASE":
			CurrentLoad=LowLoad


def TalkWithVMManager():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((LOCALHOST,PORT))
	while True:
		update=s.recv(MAX_SIZE)
		if update=="NEW_VM":
			s.sendall(str.encode("SEND_IP_AND_PORT"))
		else:
			IP_AND_PORT=json.loads(update)
			new_s=CreateConnection(IP_AND_PORT[0],IP_AND_PORT[1])
			new_thread=threading.Thread(target=StartClient,args=(new_s,))
			new_thread.start()
			s.sendall(str.encode("THANKS"))


s=CreateConnection(HOST,PORT)
StartClient(s)

LoadManager=threading.Thread(target=LoadManagement)
LoadManager.start()

VMUpdate=threading.Thread(target=TalkWithVMManager)


