import pytest
from eth_base_fee import calculate_rgb


@pytest.mark.parametrize("y, expected", [
    (0, (0, 0, 255)),
    (1, (0, int((1/3) * 255), 255 - int((1/3) * 255))),
    (2, (0, int((2/3) * 255), 255 - int((2/3) * 255))),
    (3, (0, 255, 0)),
    (4, (255, 255, 0)),
    (5, (255, 255 - int((1/3) * 255), 0)),
    (6, (255, 255 - int((2/3) * 255), 0)),
    (7, (255, 0, 0)),
    (8, (255, 0, 0)),
    (9, (255, 0, 0)),
    (10, (255, 0, 0)),
])
def test_calculate_rgb(y, expected):
    assert calculate_rgb(y) == expected
