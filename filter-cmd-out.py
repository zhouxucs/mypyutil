#!/usr/bin/python
import os
import sys
import traceback
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("filter", help="filter")
parser.add_argument("index", type=int, help="index")
parser.add_argument("-c", "--cmdline", dest="cmd", required=True)
args = parser.parse_args()

#print "application command line: ", args.cmd

retstr = os.popen(args.cmd).read()
lines = retstr.split("\n")

filtered_lines = []
for i in range(1, len(lines)):
	line = lines[i]
	line = line.strip()
	if line == "":
		continue
	if line.find(args.filter) != -1:
		filtered_lines.append(line)
			
for line in filtered_lines:
	if args.index < 0:
		print line
	else:
		words = line.split()
		if args.index < len(words):
			print words[args.index]
		else:
			print "Not enough words in %s for index(%d)" % (line, args.index)
