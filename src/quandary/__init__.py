from typing import Any, Callable, Union
from collections import UserDict


class UnevaluatedQuandary(Exception):
    pass


class NoMatch(Exception):
    pass


class QuandaryDict(UserDict):
    """
    A dictionary that stores unhashable iterable keys as tuples.
    You get the value of that key back out by accessing an element of that iterable.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unhashable_data = {}

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            for key, value in self.unhashable_data.items():
                if item in key:
                    return value
            raise KeyError

    def __setitem__(self, key, value, force_unpack = False):
        try:
            if force_unpack:
                raise TypeError
            super().__setitem__(key, value)
        except TypeError:  # unhashable
            if not any(isinstance(key, typ) for typ in [str, range]):
                key = tuple(key)
            self.unhashable_data[key] = value

    def __str__(self):
        return f'{self.data} | {self.unhashable_data}'


class quandary:
    def __init__(self, value: Any):
        self.value = value
        self.cases = QuandaryDict()
        self.__no_result = object()
        self.__result = self.__no_result

        self.result_kwargs = QuandaryDict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        try:
            result = self.cases[self.value]
        except KeyError:
            try:
                result = self.default
            except AttributeError:
                raise NoMatch('The switch fell through with no default')

        if callable(result):
            result = result(self.value, **self.result_kwargs[self.value])

        self.__result = result

    def case(self, value: Any, result: Union[Callable, Any], force_unpack = False, **kwargs):
        if not force_unpack:
            self.cases[value] = result
            self.result_kwargs[value] = kwargs
        else:
            self.cases.__setitem__(value, result, force_unpack = force_unpack)
            self.result_kwargs.__setitem__(value, kwargs, force_unpack = force_unpack)

    @property
    def result(self) -> Any:
        if self.__result is self.__no_result:
            raise UnevaluatedQuandary("You haven't left the with block, so the quandary hasn't been evaluated yet")

        return self.__result
