#!python
pmap = { '(': 1, ')': -1 }
with open('input.sql') as f:
    print sum(pmap[paren] for paren in f.read())
