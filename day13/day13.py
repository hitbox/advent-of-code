import re
import itertools
from pprint import pprint as pp

_process_re = re.compile('(?P<name1>[A-Z][a-z]+) would (?P<op>(gain|lose)) (?P<amount>\d+) happiness units by sitting next to (?P<name2>[A-Z][a-z]+)\.').match

def process(plantext):
    people = set()
    plan = {}
    for line in plantext.splitlines():
        m = _process_re(line)
        if m is not None:
            gd = m.groupdict()

            people.add(gd['name1'])
            people.add(gd['name2'])

            gd['amount'] = int(gd['amount'])
            gd['amount'] = -gd['amount'] if gd['op'] == 'lose' else gd['amount']

            key = (gd['name1'], gd['name2'])
            plan[key] = gd['amount']

    return (people, plan)

def happiness(plan, person, nextto):
    return plan[(person, nextto)]

def scoreplan(plan, seating):
    s = 0
    nseats = len(seating)
    r = 0
    for i, person in enumerate(seating):
        left = i - 1
        if left < 0:
            left = nseats - 1
        right = (i + 1) % nseats
        neighbors = [seating[left], seating[right]]
        score = sum(happiness(plan, person, neighbor) for neighbor in neighbors)
        r += score
    return r

def findhappiest(plan):
    people, plan = process(plan)
    gen = ((seating, scoreplan(plan, seating))
           for seating in itertools.permutations(people))
    return max(gen, key=lambda x: x[1] )

def test():
    with open('README.md') as f:
        test_happiness = f.read()
        happiest = findhappiest(test_happiness)
        print happiest
        assert happiest[1] == 330

def main():
    with open('input') as f:
        plan = f.read()
        happiest = findhappiest(plan)
        print happiest

if __name__ == '__main__':
    test()
    main()
    # First try!
    # 709
