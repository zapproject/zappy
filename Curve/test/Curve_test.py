from pytest import raises, fixture
from Curve.curve import Curve


@fixture
def curves():
    """Curve object values validity test

        The second parameter in each return element is the expected
        Exception class message.
    """
    return [([-1, 0, 0, 3, 1e10], "Invalid curve length"),
            ([4, 0, 0, 3, 1e10], "Piece is out of bounds"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e10], "Piece domains are overlapping"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e9], "Piece domains are overlapping"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, -1], "Piece domains are overlapping")]


def test_init(curves):
    """
        Tests the initialization and validation of curves
    """
    for curve in curves:
        with raises(Exception, match=curve[1]):
            Curve(curve[0])
