#!python
from pprint import pprint as pp

def deliver(nhouses, whilefunc):
    houses = { i: 0 for i in range(1, nhouses) }

    for house in range(1, nhouses):
        for elf in range(1, nhouses):
            if house % elf == 0:
                present = elf * 10
                houses[house] += present
                if not whilefunc(houses):
                    return houses

    return houses

def visited_by(house):
    yield 1
    if house > 1:
        yield house
        for elf in xrange(2, house):
            if elf > house / 2.0:
                return
            if house % elf == 0:
                yield elf

def presents(house):
    return sum( elf * 10 for elf in visited_by(house) )

def presentsn(house):
    return sum( elf for elf in visited_by(house) )

def tests():
    assert presents(1) == 10
    assert presents(2) == 30
    assert presents(3) == 40
    assert presents(4) == 70
    assert presents(5) == 60
    assert presents(6) == 120
    assert presents(7) == 80
    assert presents(8) == 150
    assert presents(9) == 130

def get_start(target):
    step = 100000
    house = 1
    row = 0
    while True:
        if presents(house) >= target:
            row += 1
            print (house, step, step / -2)
            if abs(step) == 1:
                break
            step /= -2
        house += step
    return house

def part1():
    target = 33100000

    target /= 10

    house = 2278236
    house = get_start(target)

    print
    print house

    houses = []
    for house in xrange(house, 0, -1):
        p = presents(house)
        if p >= target:
            houses.append(house)
            if (house > 100 and house % 100) or (house % 10):
                print (house, p)

    pp(sorted(houses))

    nope = (1638399, 3309896, 3308996, 1836522)

def main():
    tests()
    part1()

if __name__ == '__main__':
    main()
