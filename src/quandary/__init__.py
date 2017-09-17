from typing import Any, Callable, Union


class UnevaluatedQuandary(Exception):
    pass


class NoMatch(Exception):
    pass


class quandary:
    def __init__(self, value: Any):
        self.value = value
        self.cases = {}
        self.__no_result = object()
        self.__result = self.__no_result

        self.result_kwargs = {}

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
            args, kwargs = self.result_kwargs
            result = result(self.value, *args, **kwargs)

        self.__result = result

    def case(self, value: Any, result: Union[Callable, Any], expand = False, **kwargs):
        if expand:
            for v in value:
                self.cases[v] = result
        else:
            self.cases[value] = result
        self.result_kwargs[value] = kwargs

    @property
    def result(self) -> Any:
        if self.__result is self.__no_result:
            raise UnevaluatedQuandary("You haven't left the with block, so the quandary hasn't been evaluated yet")

        return self.__result
