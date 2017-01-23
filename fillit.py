#!/usr/bin/python

import sys
import re

def special_match(strg, search=re.compile(r'^[#\.\n]+$').search):
    return not bool(search(strg))

def exit_error(error_message):
    print error_message
    exit(1)

def split(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs

length = len(sys.argv)
if length < 2:
	exit_error("Error: No file input")
elif length > 2:
    print "Warning: Too much arguments. Ignoring all but the first argument."

try :
    file = open(sys.argv[1], 'r')
except IOError:
	exit_error("Error: Invalid file")
lines = file.readlines()
file.close()
cleaned = []
for u in lines:
	if not special_match(u) and len(u) == 5:
		cleaned.append(u.translate(None, '\n'))
	elif u == "\n":
		cleaned.append(u)
	else:
		exit_error("Error")

alone = False
length = 0
for i in cleaned:
	if not i == "\n":
		alone = True
#		for u in i:
#			if u == '\n':
#				print "end"
	else:
		if alone == True and length == 4:
			alone = False
			length = -1
		else :
			exit_error("Error: Too much newline(s)")
	length = length + 1
if i == "\n":
    exit_error("Error: Newline excess at EOF")
print cleaned
cleaned = filter(lambda i: i != "\n", cleaned)
tetriminos = split(cleaned, 4)
print tetriminos
