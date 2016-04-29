import re
from pprint import pprint as pp

class Reindeer(object):

    def __init__(self, name, rate, flytime, resttime):
        self.name = name
        self.rate = rate
        self.flytime = flytime
        self.resttime = resttime

        self.state = 'fly'
        self.runtime = flytime

        self.distance = 0

    def update(self):
        self.runtime -= 1

        if self.state == 'fly':
            self.distance += self.rate

        if self.runtime == 0:
            self.state = 'fly' if self.state == 'rest' else 'rest'
            self.runtime = self.flytime if self.state == 'fly' else self.resttime

def process(text):
    _re = re.compile('(?P<name>[A-Z][a-z]+) can fly (?P<rate>\d+) km/s for (?P<flytime>\d+) seconds, but then must rest for (?P<resttime>\d+) seconds\.').match
    r = []
    for line in text.splitlines():
        m = _re(line)
        if m is None:
            continue
        attrs = m.groupdict()
        for k in ['rate', 'flytime', 'resttime']:
            attrs[k] = int(attrs[k])
        r.append(attrs)
    return r

def test():
    comet = Reindeer('Comet', 14, 10, 127)
    dancer = Reindeer('Dancer', 16, 11, 162)

    for _ in range(1000):
        comet.update()
        dancer.update()

    print 'comet ran %s km' % (comet.distance)
    print 'dancer ran %s km' % (dancer.distance)

    assert comet.distance == 1120
    assert dancer.distance == 1056

def main():
    data = open('input').read()

    reindeers = [ Reindeer(attrs['name'], attrs['rate'], attrs['flytime'], attrs['resttime'])
                  for attrs in process(data) ]

    for _ in range(2503):
        for deer in reindeers:
            deer.update()

    print max(d.distance for d in reindeers)

if __name__ == '__main__':
    test()
    main()
    #answer: 2655
