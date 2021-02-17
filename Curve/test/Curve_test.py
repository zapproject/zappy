from pytest import raises, fixture, mark, approx
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
            [3, 4, 2, 3, 1e8, 4, 0, 0, 3, 4, 1e10],
            [3, 1, 0, 1e-5, 1e5, 2, 5, 4, 1e9]]


def test_init(curve_data_except, curve_data):
    """
        Tests the initialization and validation of curves
    """
    for curve in curve_data_except:
        """ test for bad input """
        with raises(Exception, match=curve[1]):
            curve_obj = Curve(curve[0])

    for curve in curve_data:
        """ test for valid input """
        with Curve(curve) as curve_obj:
            assert curve_obj.checkValidity() is None


@mark.parametrize("n, curve",
                  [(-1, [3, 0, 0, 3, 1e10]),
                   (1e11, [3, 4, 2, 3, 1e8, 4, 0, 0, 3, 4, 1e10])])
def test_getPrice_invalid(n, curve):
    """
        Tests for invalid calls to getting the
        n-dot price.
    """
    with raises(Exception, match="Invalid curve supply position"):
        Curve(curve).getPrice(n)


@mark.parametrize("n, expected",
                  [(1, [3, 4, 9, 1 + 1e-5]),
                   (10, [300, 301, 324, 1 + 1e-3]),
                   (1e9, [3e18, 3e18, (4 + 3e-9) * 10**27, (4 + 5e-9) * 10**9])])
def test_getPrice_valid(n, expected, curve_data):
    """
        Tests for valid output of the n-dot price.

        In python, 0.1 + 0.2 != 0.3.
        There is some change left over in 0.1 + 0.2,
        it is equal to 0.3 + 4e-17.

        pytest.approx fixes this by rounding off.
    """
    index = 0
    for curve in curve_data:
        assert(1e9 > 1e8)
        assert Curve(curve).getPrice(n) == approx(expected[index])
        index += 1
