icmpviewer
==========

View the pings coming from all over the world

#### Install
 - ```apt-get install python-nfqueue python2.7```
 - ```wget -O- http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz | gunzip > GeoLiteCity.dat```


#### Usage
 - ```iptables -A INPUT -i eth0 -p icmp --icmp-type echo-request  -j NFQUEUE --queue-num 5 --queue-bypass```
 - ```python2 main.py```

##### Example output
```bash
$ ./main.py
Listening on queue number 5

2014-08-13 01:12:57 195.154.xxx.xxx France ? ...
2014-08-13 01:15:01 86.27.xxx.xxx United Kingdom Fleet .......

```
