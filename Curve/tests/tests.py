from pytest import raises
import Curve.curve as curve


def test_init():
    with raises(Exception):
        curve.Curve([-1, 0, 0, 3, 1e10]).checkValidity()
