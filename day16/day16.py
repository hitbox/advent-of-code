import re

TICKER = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

class LineParser(object):

    pattern = 'Sue (?P<sue>\d+): (?P<attrs>.*)'

    def __init__(self):
        self._re = re.compile(self.pattern).match

    def __call__(self, line):
        match = self._re(line)
        if match:
            d = match.groupdict()
            d['sue'] = int(d['sue'])
            marshal = lambda k, v: (k, int(v))
            d['attrs'] = dict(marshal(*item.split(': ')) for item in d['attrs'].split(', '))
            return d


def parse(text):
    parser = LineParser()

    sues = []
    for line in text.splitlines():
        sues.append(parser(line))
    return sues

def matching(sue):
    return [ i1 for i1, i2 in zip(sue['attrs'].items(), TICKER.items()) if i1 == i2 ]

def main():
    data = parse(open('input').read())

    notsues = (315, 335, 294, 121, 161, 378)

    for sue in data:
        d = matching(sue)
        if d and sue['sue'] not in notsues:
            print sue
            print d
            print

if __name__ == '__main__':
    main()
