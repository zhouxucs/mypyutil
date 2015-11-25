#!/usr/bin/python
import socket
import sys

def is_port_open(ipaddr, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((ipaddr, int(port)))
	if result == 0:
		return True
	else:
		return False


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("hostname", help="set the target's hostname")
	parser.add_argument("port", type=int, help="the port to check")
	
	args = parser.parse_args()
	hostname = args.hostname
	port = args.port
	opened = is_port_open(hostname, port)
	if opened:
		print "On %s, port %d is OPEN" % (hostname, port)
	else:
		print "On %s, port %d is CLOSED" % (hostname, port)
		
