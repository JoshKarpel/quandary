# Quandary

A switch statement for Python. A bad idea, made even worse by me.

## Overview

Quandary provides an abstraction for a chain of `if`-`elif`-`else` statements.
It transforms code that looks like this:
```
control = get_control()

if control == 5:
    result = do_first(action)
elif control == 'foo':
    result = do_second(action)
elif control in ['bar', 'baz']:
    result = some_value
elif control == ('a', 'b', 'c'):
    result = some_other_value
else:
    result = do_default(action)
```
into
```
from quandary import quandary

control = get_control()

with quandary(control) as q:
    q.case(5, do_first)
    q.case('foo', do_second)
    q.case(('bar', 'baz'), some_value, force_contains = True)
    q.case(('a', 'b', 'c'), some_other_value)
    q.default(do_default)
   
result = q.result
```

## Details

A quandary has a **control**, an ordered list of **cases**, and a **result**.
Each case has a **key** and a **value**.
The quandary may also have a **default**.

The quandary is initialized using a `with` statement.
Then cases and (optionally) a default are added to it.
After leaving the `with` block, the quandary determines its result by trying to match the control value against the case keys.

Quandaries accept two types of case keys:
1. Something hashable.
2. Something with a `__contains__()` method (i.e., a container that can be used with `in`).

Nothing else can be used a case key.
If a key is hashable, it's assumed that you want to perform a match against that specific object (via standard dictionary key lookup rules).
If a key is not hashable, it's assumed that you want to perform a containment test: the result will be determined by the first case for which `control in key` is `True`.
A key that is hashable can forced to use the logic of the second type of case key via the `quandary.case()` keyword argument `force_contains = True`.

All type-1 cases are checked before any type-2 cases.
Type-2 cases are checked in the order they are added to the `quandary`.
Be wary of case keys overlapping.

Case values can be any object, including a callable.
Callable values are passed the control as a positional argument, followed by any keyword arguments passed to the `quandary.case()` method.

## Implementation

Under the hood, `quandary` is just a context manager.
Cases are stored in a specialized `dict` subclass that seamlessly handles the setting and getting of type-2 case keys (the containment-based ones).

## The Future

* More ways to specify case keys?
    * A test function that returns a boolean.
    * A comparator function that is called on the control before comparison.
* Protect against duplicate case keys.

## Assorted Miscellany

Inspired by [python-switch](https://github.com/mikeckennedy/python-switch).
