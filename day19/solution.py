#!/usr/bin/env python2
import re
import os
from pprint import pprint as pp

# tuples because need distinct mappings
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

def parse(s):
    machine = set()
    start = None

    map_re = re.compile('(.+) => (.+)').match
    for line in s.splitlines():
        m = map_re(line)
        if m:
            machine.add( m.groups() )
        elif line:
            start = line
            break

    return machine, start

def get_replacements(machine, c):
    return [t[1] for t in machine if t[0] == c]

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

def test():
    machine, start = parse(SIMPLE_MACHINE)

    repls = distinct_replacements(start, machine)
    assert repls == set(('HOOH', 'HOHO', 'OHOH', 'HHHH'))

    repls = distinct_replacements('HOHOHO', machine)
    assert len(repls) == 7

    machine, start = parse(TEST_MACHINE)
    repls = distinct_replacements(start, machine)
    assert repls == set(['BiOH', 'OHOH', 'HiOB', 'HOOH'])

def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')) as f:
        s = f.read()
        machine, start = parse(s)
        repls = distinct_replacements(start, machine)
        print 'distinct molecules after first replacement: %s' % (len(repls), )

        #not: 195, 674

if __name__ == '__main__':
    test()
    main()
