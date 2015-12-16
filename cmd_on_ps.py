#!/usr/bin/python
import os
import sys
import time

cmd = sys.argv[1]
event = sys.argv[2]


while True:
	retstr = os.popen("ps -a").read()
	pos = retstr.find(event)
	if pos == -1:
		os.system(cmd)
		break
	time.sleep(10)


