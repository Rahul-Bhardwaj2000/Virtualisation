import socket
import json

# HOST = '127.0.0.1'
HOST = '192.168.122.88'  # The server's hostname or IP address
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


MAX_SIZE=1024
key_value_pairs={}
key_value_pairs["1"]="rahul"


def HandleGet(conn):
	key=conn.recv(MAX_SIZE).decode()
	conn.sendall(str.encode(str(key_value_pairs[key])))

def HandlePost(conn):
	data=conn.recv(MAX_SIZE)
	data=json.loads(data)
	for key in data.keys():
		key_value_pairs[key]=data[key]
	conn.sendall(str.encode("DONE"))

def HandleRequest(conn,data):
	conn.sendall(str.encode("OK"))
	if data=="GET":
		HandleGet(conn)
	if data=="POST":
		HandlePost(conn)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		print("Waiting For connection")
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024).decode()
				if not data:
					break
				HandleRequest(conn,data)