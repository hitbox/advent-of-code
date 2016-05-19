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
    return sum( elf for elf in factors(house) )
    return sum( elf * 10 for elf in factors(house) )

def factors(n):
    if n == 1:
        yield 1
        return
    for i in xrange(1, n + 1):
        x, r = divmod(n, i)
        if r == 0 and i <= x:
            yield i
            if x != i:
                yield x
        if i >= x:
            return


def tests():
    assert presents(1) * 10 == 10
    assert presents(2) * 10 == 30
    assert presents(3) * 10 == 40
    assert presents(4) * 10 == 70
    assert presents(5) * 10 == 60
    assert presents(6) * 10 == 120
    assert presents(7) * 10 == 80
    assert presents(8) * 10 == 150
    assert presents(9) * 10 == 130

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

    house = get_start(target)

    print
    print house

    houses = []
    for house in xrange(house, 0, -1):
        p = presents(house)
        if p >= target:
            houses.append(house)
            #if (house > 100 and house % 100) or (house % 10):
            #    print (house, p)

    print min(houses)

    nope = (1638399, 3309896, 3308996, 1836522)

    # 2016-05-19
    # Brute force output:
    # 2278236
    # 776160
    # 
    # real    9m2.107s
    # user    0m0.000s
    # sys     0m0.031s
    # And that is the answer!


def main():
    tests()
    part1()

if __name__ == '__main__':
    main()
