import json
import sys

def isstring(x):
    return isinstance(x, (str, unicode))

def rsum(data, _depth=0):
    #print '  ' * _depth + str(data)

    if isinstance(data, int):
        return data

    if hasattr(data, 'items'):
        return sum( rsum(v, _depth+1) for k,v in data.items() if not isstring(v))
    else:
        return sum( rsum(i, _depth+1) for i in data if not isstring(i))

    return 0

def test():
    assert rsum([1,2,3]) == 6
    assert rsum(dict(a=2,b=4)) == 6
    assert rsum([[[3]]]) == 3
    assert rsum(dict(a=dict(b=4),c=-1)) == 3
    assert rsum(dict(a=[-1,1])) == 0
    assert rsum([-1,dict(a=1)]) == 0
    assert rsum([]) == 0
    assert rsum({}) == 0

def main():
    with open('input') as f:
        data = json.load(f)

        #print json.dumps(data, indent=4)
        print rsum(data)

if __name__ == '__main__':
    test()
    main()
