from __future__ import print_function
import sys
import libvirt
import time
from domain import conf
import socket
import json
import threading
PORT = 65431        # The port used by the server
LOCALHOST='127.0.0.1'
MAX_SIZE=1024


VM_PORT=65432


VMconn = libvirt.open('qemu:///system')
if VMconn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)


#List of all Domains
domainIDs = VMconn.listDomainsID()


NumCpus=1
def getvCpuTime(cpuStats):
	time=0
	for i in range(NumCpus):
		time+=cpuStats[i]['cpu_time'] - cpuStats[i]['system_time'] - cpuStats[i]['user_time']
	return time

dom=VMconn.lookupByName('ubuntu18.04-3')

lasttime=-1


def getIP(domainName):
	dom2 = VMconn.lookupByName(domainName)	
	ifaces = dom2.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
	return (ifaces['ens3']['addrs'][0]['addr'])

def notify_client(s):
	message="NEW_VM"
	s.sendall(str.encode(message))
	s.recv(MAX_SIZE)
	domainName = 'ubuntu18.04-2'
	IP=getIP(domainName)
	SECOND_VM_INFO=(IP,VM_PORT)
	s.sendall(str.encode(json.dumps(SECOND_VM_INFO)))
	s.recv(MAX_SIZE)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((LOCALHOST, PORT))
	s.listen()
	conn, addr = s.accept()
	counter=0
	largeLOAD=0
	while True:
		time.sleep(1)
		cpuStats=dom.getCPUStats(True)
		vCpuTime=getvCpuTime(cpuStats)
		diff = (vCpuTime-lasttime)/1e9
		lasttime=vCpuTime
		if diff*1000>=300 and counter>0:
			largeLOAD+=1
		else:
			largeLOAD=0
		if largeLOAD>=10:
			largeLOAD=0
			notify_client(conn)
		counter+=1
		print("vCPU time per second of CPU Time", diff*1000)
	print(dom.ID(),dom.name())
	conn.close()
	exit(0)
