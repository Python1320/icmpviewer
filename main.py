#!/usr/bin/env python

import logging

l=logging.getLogger("scapy.runtime")
l.setLevel(49)

import os,sys,nfqueue,socket
from scapy.all import *
import time

import GeoIP

gi = GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)


conf.verbose = 0
conf.L3socket = L3RawSocket


lastip=""
def DoGeoIP(pkt):
	global lastip
	
	ip = pkt[IP].src
	
	if lastip==ip:
		sys.stdout.write('.')
		sys.stdout.flush()
		return
		
	lastip=ip
	gir = gi.record_by_addr(ip)

	if gir != None:
			print "\n",time.strftime("%Y-%m-%d %H:%M:%S"),'-',ip,'-',gir['country_name'],gir['city'],

def process(payload):
	payload.set_verdict(nfqueue.NF_ACCEPT)
	
	data = payload.get_data()
	pkt = IP(data)
	proto = pkt.proto
	
	if proto is 0x01:
		if pkt[ICMP].type is 8:
			DoGeoIP(pkt)

def main():
	q = nfqueue.queue()
	q.open()
	q.bind(socket.AF_INET)
	q.set_callback(process)
	q.create_queue(5)

	try:
		q.try_run()
	except KeyboardInterrupt:
		print "Exit..."
		q.unbind(socket.AF_INET)
		q.close()
		sys.exit(1)

main()