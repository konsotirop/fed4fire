#!/bin/bash

#sudo bash -c 'for i in /proc/sys/net/ipv6/conf/*/accept_ra ; do echo 2 > $i ; done'


#sudo bash -c 'for i in /proc/sys/net/ipv6/conf/*/forwarding ; do echo 1 > $i ; done'


sudo python sprouting.py $1 $2

echo $HOSTNAME > temp.txt
nid=$( cut -f 1 -d '.' temp.txt )
sudo rm temp.txt

suffix='_Hops.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suffix &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5 

sudo kill -2 $pid

sudo python resetsprouting.py $1


#sudo bash -c 'for i in /proc/sys/net/ipv6/conf/*/accept_ra ; do echo 2 > $i ; done'


#sudo bash -c 'for i in /proc/sys/net/ipv6/conf/*/forwarding ; do echo 1 > $i ; done'

sudo python ghroutingr1.py 1 71

suf2='_GreedyR1.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf2 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghroutingr1.py 0 71

sudo python ghroutingr1.py 1 82

suf3='_GreedyR2.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf3 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghroutingr1.py 0 82

sudo python ghrouting2embeddings.py 1

suf4='Greedy2embeddings.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf4 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghrouting2embeddings.py 0

sudo python ghroutingr1ar.py 1 71

suf5='GreedyR1AR.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf5 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghroutingr1ar.py 0 71

sudo python ghroutingr1ar.py 1 82

suf6='GreedyR2AR.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf6 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghroutingr1ar.py 0 82

sudo python ghrouting2embeddingsar.py 1 71 82

suf7='Greedy2embeddingsAR.cap'

sudo tcpdump -i any -n ip src host 147.102.1.1 -w $nid$suf7 &
sleep 5

sudo python iptraffic.py $1 &> /dev/null

pid=$( ps -e | pgrep tcpdump )

sleep 5

sudo kill -2 $pid

sudo python ghrouting2embeddingsar.py 0 71 82
