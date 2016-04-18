#!python
from md5 import md5

key = 'yzbqklnj'
#key = 'abcdef' # test

n = 1
while True:
    h = md5(key + str(n)).hexdigest()
    if h.startswith('00000'):
        break
    n += 1

print n
print h
