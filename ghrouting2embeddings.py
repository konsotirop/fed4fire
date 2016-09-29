#! /usr/bin/env python
import platform
import subprocess
import sys

# get id of current node (curnode)
t = platform.node()
t = t.split('.')
t = t[0]
t = t[4:]
curnode = int(t)
addRule = int(sys.argv[1])
#curnode = 7 # FOR TESTING PURPOSES
# create a list with curnode neighbors'
f = open('adjlist.txt', 'r')	# open adjacency list file

neighbors = [] #initialize neighbors as an empty list
i = 0
for line in f:
	if (i == curnode):
		line = line.split('\t')
		for node in line:
			neighbors.append(int(node))
	i = i+1

nn = i
f.close() # close adjacency list file
#print( neighbors ) #  JUST FOR CHECKING PURPOSES

# for each destination, except curnode estimate next hop node from list of
# neighbors using the list created above and the src-dst hyper distances
f1 = open('sf100v2r71.txt', 'r')
next_hop_candidates = [-1]*(nn)

# keep track of curnode's neighbors and their distance to other nodes of the network

i = 0
ndists1 = {}
for line in f1:
	if i in neighbors:
		line = line.split('\t', nn-1)
		ndists1[i] = []
		for distance in line:
			ndists1[i].append(float(distance))
	i = i +1
f1.close()

f2 = open('sf100v2r82.txt', 'r')
i = 0
ndists2 = {}
for line in f2:
	if i in neighbors:
		line = line.split('\t', nn-1)
		ndists2[i] = []
		for distance in line:
			ndists2[i].append(float(distance))
	i = i +1
f2.close()
	
for destination in range(0,nn):
	if ( curnode!= destination ):
		mindist = 1000 # arbitrary large number
		min_node = -1
		for node in neighbors:
			if ndists1[node][destination] < ndists2[node][destination]:
				if ndists1[node][destination] < mindist:
					mindist = ndists1[node][destination]
					min_node = node
			else:
				if ndists2[node][destination] < mindist:
					mindist = ndists2[node][destination]
					min_node = node
                if mindist != 0:
                    next_hop_candidates[destination] = min_node
                else:
                    next_hop_candidates[destination] = -1

next_hop_candidates[curnode] = -1



# read ip addresses of nodes from txt file
f = open('ips.txt', 'r')
addr = []

for line in f:
		line = line.split()
		for item in line:
			addr.append(item)

f.close()

# set the routing rules
if addRule == 1:
    addorno = 'add '
else:
    addorno = 'del '
for destination in range(0,nn):
	if next_hop_candidates[destination] != -1:
	# na to dw ksana an einai swsto
		gateway = addr[next_hop_candidates[destination]]
		dest_ip = addr[destination]
		rule = 'sudo ip route '+ addorno+dest_ip+' via '+gateway
		process = subprocess.Popen(rule.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
