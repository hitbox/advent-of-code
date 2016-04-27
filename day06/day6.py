#!python2

lights = { (x,y):False for x in range(1000) for y in range(1000) }

def on(light):
    lights[light] = True

def off(light):
    lights[light] = False

def toggle(light):
    lights[light] = not lights[light]

def getfunc(line):
    if line.startswith('turn on'):
        return on
    if line.startswith('turn off'):
        return off
    if line.startswith('toggle'):
        return toggle

def getrange(line):
    s = line.strip('turn on ')
    s = s.strip('turn off ')
    s = s.strip('toggle ')
    start, end = s.split(' through ')

    start = map(int, start.split(','))
    end = map(int, end.split(','))
    return start, end


def main():
    with open('input') as f:
        instructions = []
        for line in f.readlines():
            line = line.strip()

            func = getfunc(line)
            start, end = getrange(line)

            instructions.append((func, start, end))

        for func, start, end in instructions:
            startx, starty = start
            endx, endy = end
            for x in xrange(startx, endx + 1):
                for y in xrange(starty, endy + 1):
                    func((x,y))

        print 'lights lit: %s' % len([v for v in lights.values() if v])

if __name__ == '__main__':
    main()
