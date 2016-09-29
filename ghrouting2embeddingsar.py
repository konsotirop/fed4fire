#! /usr/bin/env python
import platform
import subprocess
import sys
import random
# get id of current node (curnode)
t = platform.node()
t = t.split('.')
t = t[0]
t = t[4:]
curnode = int(t)
#curnode = random.randrange(45)
addRule = sys.argv[1]
root1 = int(sys.argv[2]) - 1
root2 = int(sys.argv[3]) - 1


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
f = open('adjlist.txt', 'r')

neinei = {}
i = 0
for line in f:
	if (i in neighbors):
		neinei[i] = []
		line = line.split('\t')
		for node in line:
			neinei[i].append(int(node))
	i = i + 1
#print( neighbors ) #  JUST FOR CHECKING PURPOSES
f.close()
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

trum = 0
	
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
			if min_node != root1 and min_node != root2:
					next_hop_candidates[destination] = min_node
			else:
				if min_node == root1:
					root = root1
				else:
					root = root2
				posrel = []
				for key in neinei:
					if destination in neinei[key] and root not in neinei[key]:
						posrel.append(key)
				if len(posrel) > 0:
					posrel.sort()
					for npr in posrel:
						if len(neinei[npr]) > nn*0.2:
							posrel.remove(npr)
					if len(posrel) > 0:
						next_hop_candidates[destination] = posrel[len(posrel)-1]
						trum = trum + 1
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
		rule = 'sudo ip route '+addorno+dest_ip+' via '+gateway
		#print(rule)
		process = subprocess.Popen(rule.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
#print(trum)
