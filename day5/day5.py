#!python2
from pprint import pprint as pp

vowels = 'aeiou'

bad = ['ab', 'cd', 'pq', 'xy']

def isnice(s):
    for bs in bad:
        if bs in s:
            print '%s in %s' % (bs, s)
            return False

    #if any(bs in s for bs in bad):

    found = [c for c in s if c in vowels]
    if len(found) < 3:
        print 'only %s in %s' % (found, s)
        return False

    for c1, c2 in zip(s[:-1], s[1:]):
        if c1 == c2:
            break
    else:
        print 'no double letter in %s' % s
        return False

    return True


if __name__ == '__main__':
    with open('input') as f:
        nicestrings = [ line.strip() for line in f.readlines() if isnice(line.strip()) ]
        #pp(nicestrings)
        print len(nicestrings)
