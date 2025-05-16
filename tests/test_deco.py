import pytest

from tetrika_junior.task1.solution import strict


@strict
def func(a: int, b: int) -> int:
    return a + b


def test_deco_with_correct_params_does_not_raise_error():
    assert func(1, 2) == 3
    assert func(1, b=2) == 3
    assert func(a=1, b=2) == 3
    assert func(**{"a": 1, "b": 2}) == 3


@pytest.mark.parametrize(
    "arg, msg", [
        ((1, 2, 3), "Only 2 positional arguments are allowed, got 3."),
        ((1,), "Missing argument b."),
        ((1, 2.4), "b must be of type int, got float."),
    ]
)
def test_deco_with_incorrect_params_raises_error(arg, msg):
    with pytest.raises(TypeError) as e:
        func(*arg)
    assert e.value.args[0] == msg


def test_deco_raises_error_for_extra_kwargs():
    with pytest.raises(TypeError) as e:
        func(1, 2, a=3, b=4)
    assert e.value.args[0] == "Argument(s) passed both positionally and by keyword: a, b."


@pytest.mark.parametrize(
    "kwargs, msg", [
        ({"a": 3}, "Missing argument b."),
        ({"b": 1}, "Missing argument a."),
        ({"a": 1, "b": "2"}, "b must be of type int, got str."),
    ]
)
def test_deco_raises_error_for_wrong_kwargs(kwargs, msg):
    with pytest.raises(TypeError) as e:
        func(**kwargs)
    assert e.value.args[0] == msg


def test_deco_raises_error_for_empty_call():
    with pytest.raises(TypeError) as e:
        func()
    assert e.value.args[0] == "Missing argument a."

