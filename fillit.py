#!/usr/bin/python

import sys
import re

def special_match(strg, search=re.compile(r'^[#\.\n]+$').search):
    return not bool(search(strg))

def exit_error(error_message):
    print error_message
    exit(1)

length = len(sys.argv)
if length < 2:
    exit_error("No file input")
elif length > 2:
    print "Warning: Too much arguments. Ignoring all but the first argument."

try :
    file = open(sys.argv[1], 'r')
except IOError:
    print "Invalid file"
    exit(1)
lines = file.readlines()
file.close()
cleaned = []
for u in lines:
    if (not special_match(u) and len(u) == 5) or u == "\n":
        cleaned.append(u)
    else:
        exit_error("Error")

alone = False
for i in cleaned:
    if not i == "\n":
        alone = True
        for u in i:
            if u == '\n':
                print "end"
    else:
        if alone == True:
            alone = False
        else :
            print "Error: Too much newline(s)"
            exit(1)
if i == "\n":
    print "Error: Newline excess at EOF"
    exit(1)


