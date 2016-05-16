#!/usr/bin/env python2
import re
import os
from pprint import pprint as pp
from adventlib import input_path

def parse(text):
    machine = set()
    start = None

    map_re = re.compile('(.+) => (.+)').match
    for line in text.splitlines():
        line = line.strip()
        m = map_re(line)
        if m:
            machine.add( m.groups() )
        elif line:
            start = line
            break

    return machine, start

def distinct_replacements(medicine, machine):
    repls = set()
    for sub, repl in machine:
        start = 0
        while True:
            index = medicine.find(sub, start)
            if index == -1:
                break
            before = medicine[:index]
            after = medicine[index+len(sub):]
            molecule = before + repl + after

            repls.add(molecule)
            start = index + len(sub)
    return repls

INDENT = '  '
def find(target, current, machine, _depth=1):

    #print (INDENT*(_depth-1)) + 'find: %s, len(...) = %s' % (current, len(current) )

    if len(current) >= len(target):
        return

    repls = distinct_replacements(current, machine)

    if target in repls:
        print (INDENT*(_depth-1)) + 'find: depth: %s, FOUND in %s' % (_depth, repls, )
        return _depth

    for repl in repls:
        x = find(target, repl, machine, _depth+1)
        if x is not None:
            return x

def test():
    SIMPLE_MACHINE = """\
    H => HO
    H => OH
    O => HH
    HOH
    """

    TEST_MACHINE = """\
    Hi => HO
    Hi => OH
    H => B
    Oi => HH
    HiOH
    """

    machine, start = parse(SIMPLE_MACHINE)

    repls = distinct_replacements(start, machine)
    assert repls == set(('HOOH', 'HOHO', 'OHOH', 'HHHH'))

    repls = distinct_replacements('HOHOHO', machine)
    assert len(repls) == 7

    machine, start = parse(TEST_MACHINE)
    repls = distinct_replacements(start, machine)
    assert repls == set(['BiOH', 'OHOH', 'HiOB', 'HOOH'])

    PART2 = """\
    e => H
    e => O
    H => HO
    H => OH
    O => HH
    e
    """

    machine, start = parse(PART2)

    assert find('HOH', 'e', machine) == 3
    assert find('HOHOHO', 'e', machine) == 6

def main():
    with open(input_path(__file__, 1)) as f:
        s = f.read()

        machine, start = parse(s)

        repls = distinct_replacements(start, machine)

        print 'Part 1: distinct molecules after first replacement: %s' % (len(repls), )

        machine, molecule = parse(s)

        x = find(molecule, 'e', machine)
        print 'Part 2: step from "e" to molecule: %s' % x

if __name__ == '__main__':
    test()
    main()
