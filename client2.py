import socket
import json
import time
import threading
# HOST = '127.0.0.1'
HOST = '192.168.122.43'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

MANAGER_PORT = 65431        # The port used by the server
NUM_OPEN=1

LOCALHOST='127.0.0.1'

MAX_SIZE=1024
HighLoad=1000000 #High Load
LowLoad=1 #High Load
CurrentLoad=LowLoad
def GetRequest(key,s):
	s.sendall(str.encode("GET"))
	ack=s.recv(MAX_SIZE).decode()
	if ack=="OK":
		s.sendall(str.encode(key))
		value=s.recv(MAX_SIZE).decode()


def StartClient(s):
	print("New Connection Established")
	counter=0
	while True:
		key="1"
		ans=GetRequest(key,s)
		stop_time=(1000**(NUM_OPEN-1)/CurrentLoad)
		time.sleep(stop_time)
		counter+=1


def CreateConnection(h,p):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((h, p))
	return s


def LoadManagement():
	global CurrentLoad
	while True:
		trigger=input()
		print(trigger)
		if trigger=="INCREASE":
			CurrentLoad=HighLoad
		elif trigger=="DECREASE":
			CurrentLoad=LowLoad



def TalkWithVMManager():
	print("abc")
	global NUM_OPEN
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((LOCALHOST,MANAGER_PORT))
	print("Connected to Manager")
	while True:
		update=s.recv(MAX_SIZE).decode()
		if update=="NEW_VM":
			s.sendall(str.encode("SEND_IP_AND_PORT"))
		else:
			IP_AND_PORT=json.loads(update)
			new_s=CreateConnection(IP_AND_PORT[0],IP_AND_PORT[1])
			new_thread=threading.Thread(target=StartClient,args=(new_s,))
			NUM_OPEN+=1
			new_thread.start()
			s.sendall(str.encode("THANKS"))


s=CreateConnection(HOST,PORT)
FirstClient=threading.Thread(target=StartClient,args=(s,))
FirstClient.start()

LoadManager=threading.Thread(target=LoadManagement)
LoadManager.start()

VMUpdate=threading.Thread(target=TalkWithVMManager)
VMUpdate.start()


