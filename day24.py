#!python
import sys
from itertools import combinations, groupby
from pprint import pprint as pp
from adventlib import input_path

def group_size_iter(n):
    #hard-coded to 3 sizes
    for i in xrange(1, n - 2):
        j = 1
        k = n - i - 1
        while j <= k:
            yield (i, j, k)
            j += 1
            k -= 1

def new_group_size_iter(n):
    for h in xrange(1, n - 4):
        for i in xrange(1, n - 4):
            j = 1
            k = n - 3 - (i - 1) - (h - 1)
            while j <= k:
                yield (h, i, j, k)
                j += 1
                k += -1

def ngroup_sizes(n, r):
    # TODO
    # think I want a general purpose size getter
    sizes = [1 for _ in range(r-1)]

    i = n - sum(sizes)
    sizes.append(i)
    x = -1
    y = -3

    while sizes[0] <= sizes[1]:
        while sizes[-2] <= sizes[-1]:
            yield tuple(sizes)
            b, a = sizes[-2:]
            sizes[-2] += 1
            sizes[-1] += -1
        x += -1
        sizes[-1] = i + x
        sizes[-2] = 1
        sizes[y] += 1
        if sizes[y] > sizes[y+1]:
            sizes[y] = 1
            y += -1

def quantum_entanglement(group):
    return reduce(lambda a,b: a*b, group)

def excluding(seq, *excludes):
    exclude = set(item for group in excludes for item in group)
    return (item for item in seq if item not in exclude)

def groupings(weights, size, *excludes):
    return (group for group in combinations(excluding(weights, *excludes), size))

def ngroups_iter(weights, ngroups):

    group_weight = sum(weights) / ngroups

def groups_iter(weights):
    third_weight = sum(weights) / 3
    for sizes in group_size_iter(len(weights)):
        s1, s2, s3 = sizes
        for group1 in groupings(weights, s1):
            gsum1 = sum(group1)
            if gsum1 != third_weight:
                continue
            glen1 = len(group1)
            for group2 in groupings(weights, s2, group1):
                glen2 = len(group2)
                gsum2 = sum(group2)
                if glen1 > glen2 or gsum1 != third_weight:
                    continue
                for group3 in groupings(weights, s3, group1, group2):
                    glen3 = len(group3)
                    gsum3 = sum(group3)
                    if glen1 > glen3 or gsum3 != third_weight:
                        continue
                    yield sorted((group1, group2, group3), reverse=True)

def configs_iter(weights):
    for groups in groups_iter(sorted(weights, reverse=True)):
        g1 = groups[0]
        qe = quantum_entanglement(g1)
        g2, g3 = sorted(groups[1:], key=lambda x: len(x))
        yield (g1, qe, g2, g3)

# prefer leg room over quantum entanglement
by_group1_and_qe = lambda t: (len(t[0]), t[1])

def parse(text):
    return map(int, text.splitlines())

def mkline(group):
    return (group[0], quantum_entanglement(group[0]), group[1], group[2])

def test1():
    print '== Test 1 =='
    weights = range(1,6) + range(7, 12)
    data = groups_iter(weights)

    for group in data:
        print pretty(*map(str, mkline(group)))

pretty = '{0:>25} {1:>25} {2:>25} {3:>25}'.format

def part1():
    print '== Part 1 =='
    text = open(input_path(__file__, 1)).read()

    weights = parse(text)

    n = len(weights)
    print 'needs to sum to %s' % n

    for sizes in ngroup_sizes(n, 4):
        print sizes
        #print sum(sizes)

    return

    collector = set()
    groups = ( mkline(group) for group in groups_iter(weights) )
    for group in groups:
        collector.add(group)
        if len(collector) % 10 == 0:
            print '=== **** ==='
            i = (group for group in sorted(collector, key=by_group1_and_qe))
            sys.exit()
            n = 0
            for group in i:
                print pretty(*map(str, group))
                n += 1
                if n > 20:
                    break
    # Took a very long time, like 10-15 minutes but got the answer.

def recurse(*indices):
    h, t = indices[0], indices[1:]

    if len(t) == 1:
        t = t[0] + 1
        yield h
        #XXX: left off here fiddling with n-nested for loop
    else:
        yield recurse(h, *t)

    yield recurse(h, t)


def main():
    for g in recurse(1, 1):
        print g

    return

    test1()
    part1()

if __name__ == '__main__':
    main()
