
def surface_area(l, w, h):
    return 2*l*w + 2*w*h + 2*h*l

def extra(l, w, h):
    a = [l, w, h]
    a.remove(max(a))
    return a[0] * a[1]

with open('input.sql') as f:
    total = 0
    for line in f.readlines():
        l, w, h = map(int, line.split('x'))
        total += surface_area(l,w,h) + extra(l,w,h)
    print total
