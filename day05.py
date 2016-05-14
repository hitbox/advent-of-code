#!python2
import os
from collections import Counter
from pprint import pprint as pp

VOWELS = 'aeiou'

BAD_STRINGS = ['ab', 'cd', 'pq', 'xy']

def has_bad_vowels(s):
    for bs in BAD_STRINGS:
        if bs in s:
            return True
    return False

def get_vowels(s):
    return [ c for c in s if c in VOWELS ]

def consume(s, n, overlap=True):
    """
    consume('abcdefg', 3): [ ('a', 'b', 'c'), ('b', 'c', 'd'), ..., ('e', 'f', 'g')
    """
    step = 1 if overlap else n
    return zip(*[ s[i::step] for i in range(n) ])

def iter_overlapping(s):
    for c1, c2 in consume(s, 2):
        if c1 == c2:
            yield c1 + c2

def isnice1(s):
    if has_bad_vowels(s):
        return False

    if len(get_vowels(s)) < 3:
        return False

    if next(iter_overlapping(s), None) is None:
        return False

    return True

def isnice2(s):
    # at least two occurances of a non-overlapping pair
    pairs = Counter(consume(s, 2, False))
    print s
    pp(dict(pairs))
    if max(pairs.values()) < 2:
        return False

    for c1, c2, c3 in consume(s, 3):
        if c1 == c3:
            return True

    return False

def get_nice_strings(text, pred=isnice1):
    return [ line for line in text.splitlines() if pred(line) ]

def tests():
    assert isnice1('ugknbfddgicrmopn')
    assert isnice1('aaa')
    assert not isnice1('jchzalrnumimnmhp')
    assert not isnice1('haegwjzuvuyypxyu')
    assert not isnice1('dvszwmarrgswjxmb')

    assert isnice2('qjhvhtzxzqqjkmpb')
    assert isnice2('xxyxx')
    assert not isnice2('uurcxstgmygtbstg')
    assert not isnice2('ieodomkazucvgmuy')

def part1():
    input = open(os.path.join('inputs', 'day05.input')).read()
    nice_strings = get_nice_strings(input, isnice1)
    print 'Part 1: %s nice strings' % (len(nice_strings), )

def part2():
    return
    input = open(os.path.join('inputs', 'day05.input')).read()
    nice_strings = get_nice_strings(input, isnice2)
    print 'Part 2: %s nice strings' % (len(nice_strings), )
    # bad: 63, 56

def main():
    tests()
    part1()
    part2()

if __name__ == '__main__':
    main()
