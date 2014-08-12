#!/usr/bin/env python2

QUEUE_NUM = 5

#hush verbosity
import logging
l=logging.getLogger("scapy.runtime")
l.setLevel(49)

import os,sys,time
from sys import stdout as out
import nfqueue,socket
from scapy.all import *
import GeoIP
gi = GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)


lastip=""
def DoGeoIP(pkt):
	global lastip
	
	ip = pkt[IP].src
	
	if lastip==ip:
		out.write('.')
		out.flush()
		return
		
	lastip=ip
	gir = gi.record_by_addr(ip)

	if gir != None:
		out.write("\n%s %s %s %s "%(
			time.strftime("%Y-%m-%d %H:%M:%S"),
			ip,
			gir['country_name'] or "?",
			gir['city'] or "?"))
		out.flush()
		
def process_packet(dummy, payload):
	payload.set_verdict(nfqueue.NF_ACCEPT)
	
	data = payload.get_data()
	pkt = IP(data)
	proto = pkt.proto
	
	if proto is 0x01:
		if pkt[ICMP].type is 8:
			DoGeoIP(pkt)

#automatic iptables rules?
def hook():
	pass
def unhook():
	pass
	
def main():
	q = nfqueue.queue()
	q.open()
	q.bind(socket.AF_INET)
	q.set_callback(process_packet)
	q.create_queue(QUEUE_NUM)
	
	try:
		hook()
		q.try_run()
	except KeyboardInterrupt:
		unhook()
		print("Exit...")
		q.unbind(socket.AF_INET)
		q.close()
		sys.exit(0)

print("Listening on queue number "+str(QUEUE_NUM))
main()
