#!python2
from operator import itemgetter
from pprint import pprint as pp

known_circuit = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

class AND(object):
    def __call__(self, x, y):
        return x & y


class OR(object):
    def __call__(self, x, y):
        return x | y


class LSHIFT(object):
    def __call__(self, x, y):
        return x << y


class RSHIFT(object):
    def __call__(self, x, y):
        return x >> y


class NOT(object):
    def __call__(self, x):
        return ~x & 65535


OPS = {
    'AND': AND,
    'OR': OR,
    'LSHIFT': LSHIFT,
    'RSHIFT': RSHIFT,
    'NOT': NOT,
}
OPS_VALUES = tuple(OPS.values())

def makecircuit(lines):
    circuit = {}
    for line in lines:
        line = line.strip()
        lhs, endpoint = line.split(' -> ')
        result = get_op(lhs)
        if result:
            name, op = result
            i1, i2 = map(str.strip, lhs.split(name))
            args = tuple(safeint(i) for i in [i1, i2] if i)
            circuit[op] = args
            circuit[endpoint] = op
        else:
            circuit[endpoint] = safeint(lhs)
    return circuit

def get_op(s):
    for k,v in OPS.items():
        if k in s:
            return k,v()

def isop(thing):
    return isinstance(thing, OPS_VALUES)

def isint(thing):
    r = isinstance(thing, int)
    #print 'thing %s is int, %s' % (thing, r)
    return r

def safeint(thing):
    try:
        return int(thing)
    except ValueError:
        return thing

def is_sequence(thing):
    try:
        iter(thing)
    except ValueError:
        return False
    else:
        return True

def resolve(circuit, key, start=None, visited=[]):
    #TODO: visited list
    if start is None:
        start = key

    print '\nstart: %s, key: %s, isop: %s' % (start, key, isop(key))

    if isop(key):
        op = key
        print 'recursive values: circuit[key]: %s' % (circuit[key], )
        args = [ resolve(circuit, value, start=start) for value in circuit[key] ]
        print 'isop: %s, args: %s' % (op, args, )
        r = op(*args)
        print 'op ret: %s' % (r, )
        return r

    elif isint(key):
        print 'isint: ret: %s' % (key, )
        return key

    else:
        print 'else: val: %s' % (circuit[key], )
        return resolve(circuit, circuit[key], start=start)

def test():
    circuit = makecircuit(known_circuit.splitlines())
    pp(circuit)
    known_good = { 'd': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412,
                   'i': 65079, 'x': 123, 'y': 456 }
    for k in 'defghi':
        print
        print
        r = resolve(circuit, k)
        assert known_good[k] == r
    print 'test passed'

def find_a():
    with open('input') as f:
        circuit = makecircuit(f.readlines())
        pp(circuit)
        print resolve(circuit, 'a')

def main():
    test()
    find_a()

if __name__ == '__main__':
    main()
