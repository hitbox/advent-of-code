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

def presents(house):
    return sum (elf * 10 for elf in range(1, house + 1) if house % elf == 0 )

def tests():
    solution = {
        1: 10,
        2: 30,
        3: 40,
        4: 70,
        5: 60,
        6: 120,
        7: 80,
        8: 150,
        9: 130,
    }
    assert { house: presents(house) for house in range(1, 10) } == solution

def getstart(presents):
    return (presents - 10) / 10

def part1():
    target = 33100000

    start = getstart(target)

    while True:
        p = presents(start)
        if p >= target:
            break
        start *= 2

    while True:
        if p < target:
            break
        p = presents(start)
        start -= 1

    spread = 1000
    houses = ((presents(house),house) for house in range(start - spread, start + spread))
    houses = ((house,presents) for presents,house in houses if presents >= target)
    houses = sorted(houses, key=lambda t: t[0], reverse=True)
    pp(houses)

    nope = (1638399, 3309896, 3308996)

def main():
    tests()
    part1()

if __name__ == '__main__':
    main()
