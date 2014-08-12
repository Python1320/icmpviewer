icmpviewer
==========

View the pings coming from all over the world

#### Usage
 - ```iptables -A INPUT -i WAN -p icmp --icmp-type echo-request  -j NFQUEUE --queue-num 5 --queue-bypass```
 - ```python2 main.py```
