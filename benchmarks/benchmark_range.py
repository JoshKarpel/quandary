from quandary import quandary

from IPython import get_ipython

ipython = get_ipython()


def dct(target, end):
    dct = dict(zip(range(end), range(end)))
    return dct[target]


def ifs(target, end):
    for i in range(end):
        if i == target:
            return i


def quan_using_range(target, end):
    with quandary(target) as q:
        q.case(range(end), lambda x: x, force_contains = True)

    return q.result


def quan_lots_of_cases(target, end):
    with quandary(target) as q:
        for i in range(end):
            q.case(i, i)

    return q.result


target = 10
end = 1000

# print('dict')
# ipython.magic(f"timeit ifs({target}, {end})")
# print()
#
# print('ifs')
# ipython.magic(f"timeit ifs({target}, {end})")
# print()

print('quan_using_range')
ipython.magic(f"timeit quan_using_range({target}, {end})")
print()

# print('quan_lots_of_cases')
# ipython.magic(f"timeit quan_lots_of_cases({target}, {end})")
# print()

# ifs(target, end)
# quan_using_range(target, end)
# quan_lots_of_cases(target, end)
