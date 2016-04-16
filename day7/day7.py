#!python2
import operator
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

def get_op(s):
    for k,v in OPS.items():
        if k in s:
            return k,v()

def is_op(thing):
    return any(isinstance(thing, cls) for cls in OPS.values())

def process(circuit, op=None, args=None):

    for k,v in circuit.items():
        if is_op(k):
            #circuit[endpoint] = k(*process(args))
            return process(circuit, k, v)
        else:
            return (k,v)

def resolve(circuit, *args):
    if all(arg for arg in args if not is_op(arg)):
        getter = operator.itemgetter(*args)
        return getter(circuit)
    resolve(circuit, *[ resolve(circuit, arg) if is_op(arg) else arg for arg in args ])

def main():
    circuit = {}

    for line in simple.split('\n'):
        lhs, endpoint = line.split(' -> ')

        result = get_op(lhs)
        if result:
            name, op = result
            i1, i2 = lhs.split(name)
            i1 = i1.strip()
            i2 = i2.strip()
            args = tuple(i for i in [endpoint, i1, i2] if i )
            circuit[op] = args
        else:
            circuit[endpoint] = int(lhs)

    pp(circuit)

    for k in circuit.keys():
        print 'resolving %s' % k
        print resolve(circuit, k)

if __name__ == '__main__':
    main()
