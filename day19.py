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

def parse_medicine(text):
    for line in text.splitlines():
        if line and ' => ' not in line:
            return line

def replace_iter(s, old, new):
    print 'replace_iter: %s, %s, %s' % (s, old, new, )
    start = 0
    n = len(old)
    while True:
        index = s.find(old, start)
        if index == -1:
            break
        yield s[:index] + new + s[index+n:]
        start = index+n

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

def make_graph(text):
    graph = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ' => ' not in line:
            break
        k, v = line.split(' => ')
        if k in graph:
            graph[k].append(v)
        else:
            graph[k] = [v]
    return graph

    graph2 = graph.copy()

    values = [ repl for value in graph.values() for repl in value ]
    for repl in values:
        for key in graph.viewkeys():
            if key in repl:
                if repl in graph:
                    graph2[repl].append(key)
                else:
                    graph2[repl] = [key]

    return graph2

def findgraph(target, current, graph, path=[], depth=0):
    path = path + [current]

    if depth > 3:
        return

    if len(current) > 12:
        return

    indent = INDENT * (len(path) - 1)

    print indent + 'findgraph: current: %s' % (current, )

    if current == target:
        return current

    for key, replacements in graph.iteritems():
        if key not in current:
            continue
        #print indent + 'findgraph: (%s, %s)' % (key, replacements)

        for replacement in replacements:
            print indent + 'findgraph: replacement: %s' % (replacement, )

            for repl in replace_iter(current, key, replacement):
                print indent + 'findgraph: repl: %s' % (repl, )

                newcurrent = findgraph(target, repl, graph, depth=depth+1)

                if newcurrent:
                    return newcurrent

def debug():
    text = open(input_path(__file__, 1)).read()
    SIMPLE_MACHINE = """\
    e => H
    e => O
    H => HO
    H => OH
    O => HH
    HOH
    """

    graph = make_graph(SIMPLE_MACHINE)
    medicine = parse_medicine(SIMPLE_MACHINE)

    pp(graph)
    print medicine

    r = findgraph(medicine, 'e', graph)
    print r

    return
    #machine, medicine = parse(text)

    pp(graph)
    pp(graph)

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
    debug()
    #test()
    #main()
