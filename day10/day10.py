
def look_and_say(s):
    rv = ''

    def getrun(ofchar, s):
        numc = 0
        for c in s:
            if c != ofchar:
                break
            numc += 1
        return numc

    i = 0
    while True:
        try:
            ofchar = s[i]
        except IndexError:
            break

        numc = getrun(ofchar, s[i:])
        rv += '%s%s' % (numc, ofchar)
        i += numc

    return rv

def chew_look_and_say(s, nchews):
    n = 0
    ins = s
    while n < nchews:
        rv = look_and_say(ins)
        yield (ins, rv)
        ins = rv
        n += 1

def debug():
    print '\n-- DEBUGGING --'
    for (inputstr, outputstr) in chew_look_and_say('1', 5):
        print '%s == %s' % (inputstr, outputstr)

def test():
    print '\n-- TESTS --'
    assert look_and_say('1') == '11'
    assert look_and_say('11') == '21'
    assert look_and_say('21') == '1211'
    assert look_and_say('1211') == '111221'
    assert look_and_say('111221') == '312211'
    print 'tests passed.'

def main():

    print '\n-- MAIN --'
    inputstr = '1321131112'

    for _ in range(40):
        rv = look_and_say(inputstr)
        inputstr = rv

    print len(rv)

if __name__ == '__main__':
    debug()
    test()
    main()
