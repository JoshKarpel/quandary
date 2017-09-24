from quandary import quandary


# def dct(target, end):
#     dct = dict(zip(range(end), range(end)))
#     return dct[target]
#
#
# def ifs(target, end):
#     for i in range(end):
#         if i == target:
#             return i


def quan_using_range(target, end):
    with quandary(target) as q:
        q.case(range(end), lambda x: x, force_contains = True)

    return q.result


#
# def quan_lots_of_cases(target, end):
#     with quandary(target) as q:
#         for i in range(end):
#             q.case(i, i)
#
#     return q.result


target = 10
end = 1000
repeats = 100_000

for _ in range(repeats):
    quan_using_range(target, end)
