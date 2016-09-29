#! /usr/bin/env python
import re
import subprocess
import platform
import sys

# save import arguments - nodes number and experiment name
nn = int(sys.argv[1])

# get id of current node
t = platform.node()
t = t.split('.')
t = t[0]
t = t[4:]
curnode = int(t)

# read ips file
f = open('ips.txt', 'r')
addr = []

for line in f:
		line = line.split()
		for item in line:
			addr.append(item)

f.close()

# read successors file
f = open('successors.txt', 'r')

sucList = []

i = 0
for line in f:
	if i==curnode:
		line = line.split(' ')
		for node in line:
			sucList.append(int(node))
		break
	i = i + 1

f.close()

# set rules at the routing table

for destination in range(0,nn):
		if sucList[destination] != -1:
			rule = 'sudo ip route del '+addr[destination]+' via '+addr[sucList[destination]]
			#print(rule)	# print just for testing purposes
			process = subprocess.Popen(rule.split(), stdout=subprocess.PIPE)
			output = process.communicate()[0]
