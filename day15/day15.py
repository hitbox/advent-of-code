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
    total = 1

    for scorefield in SCOREFIELDS:

        fieldtotal = 0
        for ingredient, teaspoons in recipe.items():
            fieldvalue = ingredients[ingredient][scorefield]
            fieldscore = fieldvalue * teaspoons
            fieldtotal += fieldscore

        if fieldtotal < 0:
            fieldtotal = 0
        total *= fieldtotal

    return total

def distributions(n):
    return ( c for c in permutations(range(1, 100), n) if sum(c) == 100 )

def findbestscore(ingredients):
    scores = []
    recipes = []
    for dist in distributions(len(ingredients)):
        recipe = dict(zip(ingredients.keys(), dist))
        recipes.append(recipe)
        scores.append( score(ingredients, recipe) )
    best = max(scores)
    return best, recipes[scores.index(best)]

def test():
    ingredients = parse(SAMPLE)
    score, recipe = findbestscore(ingredients)
    assert score == 62842880

def main():
    ingredients = parse(open('input').read())
    score, recipe = findbestscore(ingredients)
    print (score, recipe)
    #answer: 18965440

if __name__ == '__main__':
    test()
    main()
