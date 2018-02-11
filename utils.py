import random


def randint_except(a, b, x):
    r = random.randrange(a, b)
    return r if r < x else r + 1


def color_for_id(n):
    return '#%06x' % (1373 ** (n+10) % 2 ** 24)
