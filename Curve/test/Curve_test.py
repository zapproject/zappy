from pytest import raises, fixture
from Curve.curve import Curve


@fixture
def curve_data_except():
    """Invalid curve object values for validity test

        The second parameter in each return element is the expected
        Exception class message.
    """
    return [([-1, 0, 0, 3, 1e10], "Invalid curve length"),
            ([4, 0, 0, 3, 1e10], "Piece is out of bounds"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e10], "Piece domains are overlapping"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e9], "Piece domains are overlapping"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, -1], "Piece domains are overlapping")]


@fixture
def curve_data():
    """Valid curve object values for validity test
    """
    return [[3, 0, 0, 3, 1e10],
            [3, 1, 0, 3, 1e10],
            [3, 0, 2, 3, 1e8, 4, 0, 0, 3, 4, 1e10],
            [3, 1, 0, 5, 1e5, 2, 5, 4, 1e9]]


def test_init(curve_data_except, curve_data):
    """
        Tests the initialization and validation of curves
    """
    for curve in curve_data_except:
        """ test for bad input """
        with raises(Exception, match=curve[1]):
            Curve(curve[0])

    for curve in curve_data:
        """ test for valid input """
        with Curve(curve) as curve_obj:
            assert(curve_obj.checkValidity(), None)

# def test_getPrice(curve_data):
