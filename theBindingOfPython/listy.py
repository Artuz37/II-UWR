from math import sqrt
a = [1, 2]
print(a)
a.append(3)
print(a)
for e in a:
    print(e)

a.remove(1)
print(a)

def vector(p, q): #używam żeby policzyć jak ma sie przesunąć npc w stronę gracza
    x = p / (q + 0.001)
    x = sqrt(4 / (x*x + 1))
    y = sqrt( 4 - x*x)
    if p > 0 and q > 0:
        v = [x, y]
    elif p > 0 and q < 0:
        v = [x, -y]
    elif p < 0 and q > 0:
        v = [-x, y]
    else: v = [-x, -y]
    return v

print(vector(0, 5))
