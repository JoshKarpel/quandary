"""
A truly terrible switch statement for Python.

Copyright (c) 2017 Josh Karpel
"""

from typing import Any, Callable, Union, Hashable, Container


class QuandaryException(Exception):
    pass


class UnevaluatedQuandary(QuandaryException):
    pass


class NoMatch(QuandaryException):
    pass


class InvalidKey(QuandaryException):
    pass


def closed_range(start, stop, step):
    """Return a `range` that includes the endpoint."""
    return range(start, stop + 1, step)


class ContainerDict(dict):
    """
    A dictionary that can also store unhashable "keys" that implement the `in` operator via a `__contains__` method.
    You get the value of that key back out by accessing an element of that iterable.
    These "container keys" have lower priority than any true dictionary keys in the `ContainerDict`.

    Subclassing from dict instead of `collections.UserDict` is a ~30% speedup for certain benchmarks.
    It's generally not safe, but we only use the `ContainerDict` for one very specific purpose, and we've overridden the things we need to for that to work.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.containers = []

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            for key, value in self.containers:
                if item in key:
                    return value
            raise KeyError

    def __setitem__(self, key, result_and_kwargs, force_contains = False):
        try:
            if force_contains:
                raise TypeError
            super().__setitem__(key, result_and_kwargs)
        except TypeError:  # unhashable
            if not hasattr(key, '__contains__'):
                raise InvalidKey("{key} is not hashable and does not have a __contains__ method, so it cannot be used as the key of a quandary's case")
            self.containers.append((key, result_and_kwargs))

    def __str__(self):
        return f'{self} | {self.containers}'


class quandary:
    """A context manager that implements a switch statement."""

    _no_result = object()

    def __init__(self, control: Any):
        """
        Parameters
        ----------
        control
            The control value for the quandary.
        """
        self._control = control
        self._cases = ContainerDict()
        self._result = self._no_result

    def __enter__(self):
        return self

    def case(self, key: Union[Hashable, Container], result: Union[Callable, Any], force_contains: bool = False, **kwargs):
        """
        Adds a case to the quandary with key `key` and possible result `result`.

        Parameters
        ----------
        key
            Either a hashable or a container that is checked against the control.
        result
            What the result of the quandary will be if this case matches. Can be a value or a callable.
        force_contains
            If `True`, forces the key to be treated as a container even if it is hashable.
        kwargs
            Keywords arguments are passed to the `result` if it is callable.
        """
        self._cases.__setitem__(key, (result, kwargs), force_contains = force_contains)

    def default(self, result: Union[Callable, Any], **kwargs):
        """
        Add a case that is used if no explicit case is matched.

        Parameters
        ----------
        result
            The result of the quandary if no case matches.
        kwargs
            Keywords arguments are passed to the `result` if it is callable.
        """
        self._default = result, kwargs

    def __exit__(self, exc_type, exc_val, exc_tb):
        """When the `with` block ends the quandary determines which case the control matches and assigns the value of that case to its result."""
        if exc_type is not None:
            return False  # returning False from __exit__ propagates the exception

        try:
            result, kwargs = self._cases[self._control]
        except KeyError:
            try:
                result, kwargs = self._default
            except AttributeError:
                raise NoMatch('Failed to match any case and no default has been set')

        if callable(result):
            result = result(self._control, **kwargs)

        self._result = result

    @property
    def result(self) -> Any:
        """A property that gets the result of the quandary, if the quandary has been evaluated."""
        if self._result is self._no_result:
            raise UnevaluatedQuandary("You haven't left the with block, so the quandary hasn't been evaluated yet")

        return self._result
