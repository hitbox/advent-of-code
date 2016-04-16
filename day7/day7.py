#!python2
from operator import itemgetter
from pprint import pprint as pp

simple = """\
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

def makecircuit(lines):
    circuit = {}
    for line in lines:
        line = line.strip()
        lhs, endpoint = line.split(' -> ')
        result = get_op(lhs)
        if result:
            name, op = result
            i1, i2 = map(str.strip, lhs.split(name))
            args = tuple(safeint(i) for i in [i1, i2] if i )
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
    return isinstance(thing, tuple(OPS.values()))

def isint(thing):
    return isinstance(thing, int)

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

def resolve2(circuit, *keys):
    print 'resolve:keys: %s' % (keys, )

    if len(keys) == 0:
        return []

    vals = []
    for key in keys:
        try:
            val = circuit[key]
        except KeyError:
            vals = [ keys[0], ] + resolve(circuit, *keys[1:])
            break

        print 'resolve:key:%s, val:%s' % (key, val)

        if isint(val):
            vals.append(val)
        else:
            if isop(key):
                op = key
                args = resolve(circuit, *val)
                print '%s(%s)' % (op, args)
                return op(*args)
            else:
                return resolve(circuit, *val)

    print 'resolve:vals:%s' % (vals, )
    return vals

def resolve(circuit, *keys):
    print
    print 'keys: %s' % (keys, )

    getter = itemgetter(*keys)
    values = getter(circuit)
    print 'values: %s' % (values, )
    print 'type(values) == %s' % (type(values), )

    if not isinstance(values, tuple):
        values = (values, )

    values = tuple(v if isint(v) else resolve(circuit, v) for v in values)

    return resolve(circuit, *values)

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None

def main_simple():
    circuit = makecircuit(simple.splitlines())

    print 'circuit:'
    pp(circuit)

    key = 'd'
    print 'resolve(circuit, %s)' % key
    print 'result: %s' % resolve(circuit, key)

def main_real():
    with open('input') as f:
        circuit = makecircuit(f.readlines())

        pp(circuit)

        print resolve(circuit, 'a')

def main():
    #main_simple()
    main_real()

if __name__ == '__main__':
    main()
