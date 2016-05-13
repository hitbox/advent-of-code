#!/usr/bin/env python2
import os
from pprint import pprint as pp

range = xrange

CODE = {'#': True, '.': False}
DISPLAY = {v:k for k,v in CODE.items()}

EXAMPLE = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

def size(s):
    return len(s.splitlines()[0])

def parse(s):
    for y, line in enumerate(s.splitlines()):
        for x, char in enumerate(line):
            yield ( (x, y), CODE[char] )

NEIGHBOR_DELTAS = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if not x == y == 0]

def neighbors(data, x, y):
    return (data[(x+dx,y+dy)] for dx,dy in NEIGHBOR_DELTAS if (x+dx,y+dy) in data)

def coordinates(data, n):
    n = list(range(n))
    for x in n:
        for y in n:
            yield (x, y)

def nextstate(data, n):
    newstate = {}
    for x, y in coordinates(data, n):
        light = data[(x,y)]

        neighbors_on = sum(n for n in neighbors(data, x, y) if n)
        if light:
            light = neighbors_on in (2, 3)
        else:
            light = neighbors_on == 3
        newstate[(x,y)] = light

    return newstate

def display(data, n):
    n = list(range(n))
    return '\n'.join(''.join([DISPLAY[data[(x,y)]] for x in n]) for y in n)

def test():
    data = dict(parse(EXAMPLE))

    n = size(EXAMPLE)
    for _ in range(5):
        data = nextstate(data, n)

    assert display(data, n) == """\
......
......
..##..
..##..
......
......"""

def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')) as f:
        s = f.read()
        n = size(s)
        data = dict(parse(s))

        for _ in range(100):
            data = nextstate(data, n)

        lights_on = sum(1 if v else 0 for v in data.values())
        print '%s lights on' % (lights_on, )

if __name__ == '__main__':
    test()
    main()
