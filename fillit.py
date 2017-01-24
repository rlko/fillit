#!/usr/bin/python

import sys
import re

from util import *

def special_match(strg, search=re.compile(r'^[#\.\n]+$').search):
    return not bool(search(strg))

def check_pattern(tetriminos):
#    nxt
    plage = [-1, 0, 1]
    for i in tetriminos:
        prv = None
        for cd in i:
            connection = 0
            if prv != None:
                if not (prv[0] - cd[0] in plage and prv[1] - cd[1] in plage):
                    print prv[0] - cd[0]
                    print prv[1] - cd[1]
                    print prv, cd
                    print connection, tetriminos.index(i)
                    return False
#            if not (connection == 1 or connection == 2):
#                 return False
            prv = cd
    node = 0
    return True

def check_arguments():
    length = len(sys.argv)
    if length < 2:
            exit_error("Error: No file input")
    elif length > 2:
        print "Warning: Too much arguments. Ignoring all but the first argument."

check_arguments()
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
    else:
            if alone == True and length == 4:
                    alone = False
                    length = -1
            else :
                    exit_error("Error: Too much newline(s)")
    length = length + 1
if i == "\n":
    exit_error("Error: Newline excess at EOF")
cleaned = filter(lambda i: i != "\n", cleaned)
tetriraw = split(cleaned, 4)

nt = 0
tetriminos = []
for i in tetriraw:
    y = 0
    ns = 0
    sharp = []
    for u in i:
        for x, needle in enumerate(u):
            if needle == '#':
                if ns == 0:
                    first_cd = [x, y]
                cd = [x - first_cd[0], y - first_cd[1]]
                sharp.append(cd)
                ns = ns + 1
        y = y + 1
    if not ns == 4:
        exit_error("Error: Lack of sharps in pattern")
    tetriminos.append(sharp)

print tetriminos
if not check_pattern(tetriminos):
    exit_error("Error: pattern failure")
