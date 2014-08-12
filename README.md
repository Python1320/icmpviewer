icmpviewer
==========

View the pings coming from all over the world

#### Install
 - ```apt-get install python-nfqueue python2.7```
 - ```wget -O- http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz | gunzip > GeoLiteCity.dat```


#### Usage
 - ```iptables -A INPUT -i WAN -p icmp --icmp-type echo-request  -j NFQUEUE --queue-num 5 --queue-bypass```
 - ```python2 main.py```
