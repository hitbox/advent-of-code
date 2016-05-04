import re
from itertools import permutations
from pprint import pprint as pp

SAMPLE = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

FIELDS = 'capacity durability flavor texture calories'.split()

def mklineparser():
    mkgpattern = lambda name: '{name} (?P<{name}>\-?\d)'.format(name=name)
    pattern = '(?P<name>[A-Z][a-z]+): ' + ', '.join(map(mkgpattern, FIELDS))
    return re.compile(pattern).match

def parse(text):
    lineparser = mklineparser()

    r = {}
    for line in text.splitlines():
        match = lineparser(line)
        if match:
            d = match.groupdict()
            r[d['name']] = { k:int(v) for k,v in d.items() if k != 'name' }

    return r

def apply():
    pass

SCOREFIELDS = [f for f in FIELDS if f != 'calories']

def score(ingredients, recipe):
    s = 0

    for scorefield in SCOREFIELDS:
        pass

    for ingredient,teaspoons in recipe.items():
        for ak,av in ingredients[ingredient].items():
            if ak in SCOREFIELDS:
                s += av * teaspoons
    return s

def distributions(n):
    return ( c for c in permutations(range(101), n) if sum(c) == 100 )

def main():
    ingredients = parse(SAMPLE)
    pp(ingredients)

    scores = []
    for t in distributions(len(ingredients)):
        recipe = dict(zip(ingredients.keys(), t))
        pp(recipe)
        scores.append( score(ingredients, recipe) )
        break

    #print max(scores)

if __name__ == '__main__':
    main()
