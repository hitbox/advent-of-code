import string
from string import lowercase
import sys

three_character_runs = set(''.join(t)
                           for t in zip(lowercase[:-3], lowercase[1:-2], lowercase[2:-1]))

def isvalid(password):

    pset = set(password)

    if set('iol') & pset:
        return False

    if not three_character_runs & pset:
        return False

    # unique, non-overlapping pairs of letters
    pairs = set([ ''.join(t) for t in zip(password[:-1:2], password[1::2]) if t[0] == t[1] ])

    if len(pairs) < 2:
        return False

    return True

def increment(s, v=None):
    if v is None:
        v = 1

    ords = [ ord(c) for c in s ]

    i = -1
    ords[i] += v

    while ords[i] > ord('z'):
        ords[i] = ord('a')
        i = i - 1

        if abs(i) > len(ords):
            ords = [ord('a')] + ords
        else:
            ords[i] += 1

    return ''.join( chr(o) for o in ords )

def main():
    password = 'vzbxkghb'

    fmt = '{}\r'.format

    while not isvalid(password):
        password = increment(password)
        sys.stdout.write(fmt(password))

    print password

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

if __name__ == '__main__':
    #debug_isvalid()
    main()
