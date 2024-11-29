import pytest

def func(x):
    return x + 1

def foo_sum(a,b):
    return a+b

@pytest.fixture(scope="package")
def some_fixture():
    import time
    time.sleep(5)
    some_data = 4
    print("fixture 1 work")
    return some_data


@pytest.fixture(scope="function")
def some_fixture_2(some_fixture):
    res = some_fixture
    print("fixture 2 work")
    import time
    time.sleep(5)
    some_data = 4 + res
    return some_data


@pytest.mark.parametrize(
    ["a", "b", "result"],
    [
        [1, 4, 5],
        [2, 6, 7],
        [5, 5, 10],
    ],
)
def test_foo(a, b, result):
    return foo_sum(a, b) == result


def test_answer(some_fixture_2):
    assert func(some_fixture_2) == 5

def test_answer_2(some_fixture,some_fixture_2):
    assert func(4) == 5