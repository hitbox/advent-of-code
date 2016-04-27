import re
import itertools
from pprint import pprint as pp

_parser_re = re.compile('(?P<origin>\S+) to (?P<destination>\S+) = (?P<distance>\d+)').match

def parseline(line):
    m = _parser_re(line)
    if m:
        d = m.groupdict()
        d['distance'] = int(d['distance'])
        return d
    raise RuntimeError('Invalid line %s' % (line, ))

def parseinput(lines):
    locations = set()
    distances = []
    for line in lines:
        line = line.strip()
        parsed = parseline(line)
        distances.append(parsed)
        locations.add(parsed['origin'])
        locations.add(parsed['destination'])
    return locations, distances

def distance(distlist, *locations):
    assert len(locations) == 2
    g = [d['distance'] for d in distlist if d['origin'] in locations and d['destination'] in locations]
    assert len(g) == 1
    d = g[0]
    return d

def sumdist(distlist, *locations):
    return sum([distance(distlist, a, b) for a,b in zip(locations[:-1], locations[1:])])

def test():
    inputstr = """London to Dublin = 464
                  London to Belfast = 518
                  Dublin to Belfast = 141"""

    locations, distances = parseinput(inputstr.splitlines())

    routes = itertools.permutations(locations)

    assert min(sumdist(distances, *t) for t in routes) == 605
    print 'test passed'

def main():
    inputstr = open('input').read()
    locations, distances = parseinput(inputstr.splitlines())

    pp(locations)
    routes = itertools.permutations(locations)
    print min(sumdist(distances, *t) for t in routes)

    #117 is the answer
    # wanted to write my own product producer function but gave up and used itertools

if __name__ == '__main__':
    test()
    main()
