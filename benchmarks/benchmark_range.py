from IPython import get_ipython

from quandary import quandary

ipython = get_ipython()


def ifs(target, end):
    for i in range(end):
        if i == target:
            return i


def quan(target, end):
    with quandary(target) as q:
        q.case(range(end), lambda x: x, force_unpack = True)

    return q.result


ipython.magic("timeit ifs(500, 1000)")
ipython.magic("timeit quan(500, 1000)")

# ifs(5, 10)
# quan(5, 10)
