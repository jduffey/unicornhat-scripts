import pytest
from eth_base_fee import calculate_rgb


def test_calculate_rgb():
    r, g, b = calculate_rgb(0)
    assert r == 0
    assert g == 0
    assert b == 255

    y = 2
    r, g, b = calculate_rgb(y)
    assert r == 0
    assert g == int((y/3) * 255)
    assert b == 255 - int((y/3) * 255)

    y = 5
    r, g, b = calculate_rgb(y)
    assert r == 255
    assert g == 255 - int(((y-4)/3) * 255)
    assert b == 0
