import pytest
from solution import strict, StrictTypeError

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (10, -5, 5),
])
def test_sum_two_valid(a: int, b: int, expected: int) -> None:
    @strict
    def sum_two(x: int, y: int) -> int:
        return x + y
    assert sum_two(a, b) == expected

@pytest.mark.parametrize("a, b", [
    (1, 2.0),
    ("1", 2),
    (1, "2"),
])
def test_sum_two_invalid(a, b) -> None:
    @strict
    def sum_two(x: int, y: int) -> int:
        return x + y
    with pytest.raises(StrictTypeError):
        sum_two(a, b) 