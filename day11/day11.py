import string
import itertools
from string import lowercase
import sys
from pprint import pprint as pp

ZORD = ord('z')
AORD = ord('a')

BADCHARS = 'iol'
BADORDS = set([ord(c) for c in BADCHARS])

def stagger(l, n):
    args = [ l[i:] for i in range(n) ]
    return itertools.izip(*args)

def getpairs_d(l):
    return set(t for t in zip(l[:-1:2], l[1::2]) if t[0] == t[1])

def getpairs(s):
    i = iter(s)
    last = None
    accum = []
    for current in i:
        if last is not None:
            if last == current:
                accum.append(last + current)
                next(i, None)
        last = current
    return set(accum)

def increment(s):
    ords = [ ord(c) for c in s ]

    def resolvecarry():
        i = -1
        while ords[i] > ZORD:
            ords[i] = AORD
            i = i - 1
            ords[i] = incord(ords[i])

    def threes():
        staggered = stagger(ords, 3)
        return set(t for t in staggered if t[0] == t[1]-1 == t[2]-2)

    def incord(code):
        # skip "bad" ords
        if code + 1 in BADORDS:
            return code + 2
        return code + 1

    def _increment():
        ords[-1] = incord(ords[-1])
        resolvecarry()

    def isvalid():
        return len(getpairs(ords)) > 1 and threes()

    while not isvalid():
        _increment()
        progress("simple: %s" % (ords, ))

        while len(getpairs(ords)) < 2:
            _increment()
            progress(" pairs: %s" % (ords, ))

        while not threes():
            _increment()
            progress("threes: %s" % (ords, ))

    return ''.join( chr(o) for o in ords )

_progress = '{}\r'.format
def progress(s):
    print s
    #sys.stdout.write(_progress(s))

def main():
    password = 'vzbxkghb'
    print '\n' + increment(password)

def debug_isvalid():
    print isvalid('hijklmmn')
    print isvalid('abbceffg')
    print isvalid('abbcegjk')

    print isvalid()

def debug_increment():
    s = 'abcdefghiyz'

    fmt = '{}\r'.format
    sys.stdout.write(fmt(s))

    while True:
        s = increment(s, 1)

        sys.stdout.write(fmt(s))

def test_stagger():
    l = range(10)
    print " the list: %s" % (l,)
    print "staggered: %s" % (list(stagger(l, 3)), )

def test_pairs():
    for s in ["abcdef", "aaaaaa", "abcaad", "aacaad", "bbcaad"]:
        print "%s => %s" % (s, getpairs(s))


if __name__ == '__main__':
    #debug_isvalid()
    #test_stagger()
    #test_pairs()

    main()

    # not right:
    # vzccaabc
    # vzbxxwxy

    # F I N A L L Y ! ! !
    #vzbxxyzz
    # my pair finding function wrong wrong (well the last thing that was
    # wrong)
