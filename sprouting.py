#! /usr/bin/env python
import re
import subprocess
import platform
import sys

# save import arguments - nodes number and experiment name
nn = int(sys.argv[1])
expname = sys.argv[2]

# get id of current node
t = platform.node()
t = t.split('.')
t = t[0]
t = t[4:]
curnode = int(t)

# initialize ip addresses dictionary
addr = []


lpar = '('
rpar = ')'

# get ips of all nodes in the network
for i in range(0,nn):
	ping_response = subprocess.Popen(["/bin/ping", "-c1", "-n", "node"+str(i)+"."+expname+".wall2-ilabt-iminds-be.wall1.ilabt.iminds.be"], stdout=subprocess.PIPE)
	output = ping_response.communicate()[0]
	inet = output[output.find(lpar)+1:output.find(rpar)]
	addr.append(inet)	

#for i in range(30,nn):
#        ping_response = subprocess.Popen(["/bin/ping", "-c1", "-n", "node"+str(i)+"."+expname+".wall2-ilabt-iminds-be.wall2.ilabt.iminds.be"], stdout=subprocess.PIPE)
#        output = ping_response.communicate()[0]
#        inet = output[output.find(lpar)+1:output.find(rpar)]
#        addr.append(inet)
# write them to a file

f = open('ips.txt', 'w')
i = 1
for dnsh in addr:
	if i == 1:
		f.write("%s" % dnsh)
		i = 0
	else:
		f.write(" %s" % dnsh )

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
			rule = 'sudo ip route add '+addr[destination]+' via '+addr[sucList[destination]]
			#print(rule)	#print just for testing purposes
			process = subprocess.Popen(rule.split(), stdout=subprocess.PIPE)
			output = process.communicate()[0]
