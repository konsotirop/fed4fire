#! /usr/bin/env python

# import scapy and python libraries
from scapy.all import *
import time
import platform
import socket
import random
import sys

nn = int(sys.argv[1])
t = platform.node()
t = t.split('.')
t = t[0]
t = t[4:]
curnode = int(t)


nodes_list = list(range(0,nn))
nodes_list.remove(curnode)

f = open('ips.txt', 'r')
addr = []

for line in f:
		line = line.split()
		for item in line:
			addr.append(item)

f.close()

# create random traffic
t_end = time.time() + 60*3 # generate traffic for 10 minutes
while time.time() < t_end:
	random.shuffle(nodes_list)
	for i in range(0, len(nodes_list)):
		time.sleep(random.uniform(0.05,0.45))
		send(IP(dst = addr[nodes_list[i]], src="147.102.1.1")/Raw(RandBin(size=60)))
