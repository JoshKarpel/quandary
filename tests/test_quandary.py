import pytest
from hypothesis import given, example, settings
import hypothesis.strategies as st

from quandary import quandary, UnevaluatedQuandary, NoMatch


def test_unevaluated():
    with pytest.raises(UnevaluatedQuandary):
        with quandary('hello') as q:
            q.result


def test_fallthrough_without_default():
    with pytest.raises(NoMatch):
        with quandary('foo') as q:
            q.case('a', 1)
            q.case('b', 2)
            q.case('bar', -1)


# @settings(max_examples = 5000)
@given(
    values = st.lists(
        elements = st.sampled_from([
            st.text(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.decimals(),
            st.booleans(),
        ]),
        min_size = 1,
        unique = True,
    ),
    results = st.lists(
        elements = st.sampled_from([
            st.text(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.decimals(),
            st.booleans(),
        ]),
        min_size = 1,
        unique = True,
    )
)
def test_fallthrough_with_default(values, results):
    value = values.pop()
    result = results.pop()

    with quandary(value) as q:
        for v, r in zip(values, results):
            q.case(v, r)
        q.default(result)

    assert q.result == result


# @settings(max_examples = 5000)
@given(
    values = st.lists(
        elements = st.sampled_from([
            st.text(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.decimals(),
            st.booleans(),
        ]),
        min_size = 1,
        unique = True,
    ),
    results = st.lists(
        elements = st.sampled_from([
            st.text(),
            st.integers(),
            st.floats(),
            st.complex_numbers(),
            st.decimals(),
            st.booleans(),
        ]),
        min_size = 1,
        unique = True,
    )
)
def test_quandary__noniterable_values(values, results):
    value = values.pop()
    result = results.pop()

    with quandary(value) as q:
        q.case(value, result)

        for v, r in zip(values, results):
            q.case(v, r)

    assert q.result == result


def test_quandary__expand():
    with quandary(10) as q:
        q.case(range(20), True, force_contains = True)
        q.case(range(20, 40), False, force_contains = True)

    assert q.result
