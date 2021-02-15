from pytest import raises
from Curve.curve import Curve


def test_init():
    with raises(Exception):
        Curve([-1, 0, 0, 3, 1e10]).checkValidity()
