#!python
dirmap = { '<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1) }
with open('input.sql') as f:
    x, y = 0, 0
    houses = {(x,y):1}
    for c in f.read():
        dx, dy = dirmap[c]
        x += dx
        y += dy
        
        house = (x, y)
        if house in houses:
            houses[house] += 1
        else:
            houses[house] = 1
    print len(houses)

