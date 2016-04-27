from pprint import pprint as pp

def memorystring(line):
    return line.decode('string-escape')

def counts(line):
    # assumes wrapped in quotes
    return len(line), len(memorystring(line)) - 2

def test():
    reference = [r'""', r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    code = 0
    mem = 0
    for line in reference:
        c, m = counts(line)
        code += c
        mem += m
    assert (code - mem) == 12

def main():
    with open('input') as f:

        code = 0
        mem = 0
        for line in f.readlines():
            line = line.strip()
            c,m = counts(line)
            code += c
            mem += m

        print (code - mem)

if __name__ == '__main__':
    test()
    main()
    #1350 is the answer
