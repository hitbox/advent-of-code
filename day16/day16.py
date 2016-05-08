import os
import re
from itertools import izip_longest
from pprint import pprint as pp
from collections import defaultdict

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
            suedict = match.groupdict()
            suedict['sue'] = int(suedict['sue'])
            marshal = lambda k, v: (k, int(v))
            suedict['attrs'] = dict(marshal(*item.split(': '))
                                    for item in suedict['attrs'].split(', '))
            return suedict


def parse(text):
    parser = LineParser()

    sues = []
    for line in text.splitlines():
        sues.append(parser(line))
    return sues

def getmatches(sue):
    matches = {}
    for tickerkey, tickervalue in TICKER.items():
        if tickerkey in sue['attrs'] and tickervalue == sue['attrs'][tickerkey]:
            #matches.append(sue['attrs'][tickerkey])
            #matches.append({tickerkey: tickervalue})
            matches[tickerkey] = tickervalue
    return matches
    return [ sueitem for sueitem, tickeritem in
                     izip_longest(sue['attrs'].items(), TICKER.items())
                     if sueitem == tickeritem ]

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')
    sues_data = parse(open(path).read())

    notsues = (315, 335, 294, 121, 161, 378, 126)

    suematches = {}
    for sue_data in sues_data:
        matches = getmatches(sue_data)
        if matches:
            suematches[sue_data['sue']] = matches
    pp(suematches)
    s = sorted(suematches.items(), key=lambda sueitem: len(sueitem[1]))
    pp(s)
    #answer: 

if __name__ == '__main__':
    main()
