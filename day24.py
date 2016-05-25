#!python
from itertools import combinations, groupby
from pprint import pprint as pp
from adventlib import input_path

def take(n, seq):
    seqi = iter(seq)
    running = True
    while running:
        accum = []
        for _ in xrange(n):
            try:
                accum.append(next(seqi))
            except StopIteration:
                running = False
                break
        if accum:
            yield accum

def group_size_iter(n):
    return ((s1,s2,s3) for s1 in xrange(1, n)
                       for s2 in xrange(1, n)
                       for s3 in xrange(1, n)
                       if s1 + s2 + s3 == n)

def quantum_entanglement(group):
    return reduce(lambda a,b: a*b, group)

def groups_iter(weights):
    n = len(weights)

    for sizes in group_size_iter(n):
        s1, s2, s3 = sizes
        for group1 in combinations(weights, s1):
            for group2 in combinations((w for w in weights if w not in group1), s2):
                for group3 in combinations((w for w in weights if w not in group1 and w not in group2), s3):
                    if sum(group1) == sum(group2) == sum(group3):
                        yield group1, group2, group3

def find_configuration(weights):

    configs = []
    for groups in groups_iter(weights):
        g1, g2, g3 = groups
        if len(g1) < len(g2) and len(g1) < len(g3):
            configs.append((g1, quantum_entanglement(g1), g2, g3))

    pp(list(groupby(sorted(configs, key=lambda t: len(t[0])), lambda t:t[0])))

def test1():
    find_configuration(range(1,6) + range(7, 12))

def main():
    test1()

if __name__ == '__main__':
    main()
