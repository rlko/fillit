#!/usr/bin/python

import sys
import re

from util import exit_error
from util import split

def check_arguments(length):
    if length < 2:
        return False
    elif length > 2:
        print "Warning: Too much arguments. Ignoring all but the first argument."
    return True

def dump_file(filename):
    try :
        file = open(filename, 'r')
    except IOError:
        return None
    lines = file.readlines()
    file.close()
    return lines

def special_match(strg, search=re.compile(r'^[#\.\n]+$').search):
    return not bool(search(strg))

def parse(filename):
    lines = dump_file(filename)
    if lines == None:
        exit_error("Error: Invalid file")

    cleaned = []

    for u in lines:
        if (not special_match(u) and len(u) == 5) or u == "\n":
            cleaned.append(u)
        else:
            exit_error("Error")

    alone = False
    length = 0
    newline = None

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
        newline = i
    if newline == "\n":
        exit_error("Error: Newline excess at EOF")
    elif newline == None:
        exit_error("Error: file is empty")
    cleaned = filter(lambda i: i != "\n", cleaned)
    return split(cleaned, 4)

def build_patterns(tetriraw):
    if tetriraw == None:
        exit_error("Unexpected error #1")

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
    return tetriminos

def check_patterns(tetriminos):
    for i in tetriminos:
        node = 0
        for cd in i:
            for cd2 in i:
                if (cd2[0] == cd[0] and cd2[1] + 1 == cd[1]) or \
                    (cd2[0] == cd[0] and cd2[1] - 1 == cd[1]) or \
                    (cd[1] == cd2[1] and cd2[0] + 1 == cd[0]) or \
                    (cd[1] == cd2[1] and cd2[0] - 1 == cd[0]):
                        node = node + 1
        if node < 6:
            return False
    return True

def make_solver(size):
    i = 0
    solver = []
    grid = []

    for i in range(size):
        line = []
        for j in range(size):
            cd = [j, i]
            solver.append(cd)
            line.append('.')
        grid.append(line)
    return solver, grid

def counter():
    if 'cnt' not in counter.__dict__:
        counter.cnt = 1
    counter.cnt += 1
    return counter.cnt

# ttm[tetrimino][sharp][x/y]
#  "      "        "   [0/1]

def fill_it(ttm, grid, r, i, size, l): 
    if l == 4:
        return True
    cd = [r[0] + ttm[i][l][0], r[1] + ttm[i][l][1]]
    if cd[0] < size and cd[1] < size and cd[0] >= 0 and grid[cd[0]][cd[1]] == '.':
            if fill_it(ttm, grid, r, i, size, l + 1):
                grid[cd[0]][cd[1]] = chr(65 + i)
                return True
    return False

def baka_step(grid, size, i):
    for u in range(size):
        for j in range(size):
            if grid[u][j] == chr(65 + i):
                grid[u][j] = '.'

def print_grid(grid, size):
    for i in range(size):
        str = ""
        for j in range(size):
            str = str + grid[j][i]
        print str

def reset_grid(grid, size):
    for i in range(size):
        for u in range(size):
            grid[i][u] = '.'

def solve(ttm, grid, solver, size, nt):
    clock = []

    for i in range(26):
        clock.append(0)
    i = 0
    while i != nt:
        if clock[i] == size * size:
            i = i - 1
            if i < 0:
                return False
            clock[i + 1] = 0
            clock[i] = clock[i] + 1
            baka_step(grid, size, i)
        if fill_it(ttm, grid, solver[clock[i]], i, size, 0):
            i = i + 1
        else:
            clock[i] = clock[i] + 1
    return True

def resolve(ttm):
    size = counter()
    solver, grid = make_solver(size)
    if solve(ttm, grid, solver, size, len(ttm)):
        print_grid(grid, size)
    else:
        reset_grid(grid, size)
        resolve(ttm)

if not check_arguments(len(sys.argv)):
    exit_error("Error: No file input")
tetriminos = build_patterns(parse(sys.argv[1]))
if not check_patterns(tetriminos):
    exit_error("Error: pattern failure")
resolve(tetriminos)
