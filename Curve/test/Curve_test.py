from pytest import raises, fixture, mark, approx
from Curve.curve import Curve, isWhole
"""
    Get a detailed test output and upload to a pastebin:
        pytest -r p --pastebin=all

    Show fixtures used for test
        pytest -r p --fixtures-per-test
"""


@fixture
def curve_data_except():
    """Invalid curve object values for validity test

        The second parameter in each return element is the expected
        Exception class message.
    """
    return [([-1, 0, 0, 3, 1e10], "Invalid curve length"),
            ([4, 0, 0, 3, 1e10], "Piece is out of bounds"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e10],
             "Piece domains are overlapping"),
            ([3, 0, 0, 3, 1e10, 3, 0, 0, 4, 1e9],
             "Piece domains are overlapping"),
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
        with Curve(curve) as curve_obj:
            assert curve_obj.getPrice(n) == approx(expected[index])
            index += 1


@mark.parametrize("a, n, exception",
                  [(-1, 1, "Invalid curve supply position"),
                   (1e11, 1, "Invalid curve supply position"),
                   (1, 1e11, None)])
def test_getZapRequired_invalid(a, n, exception, curve_data):
    """ Tests for invalid summation of dot value
    """
    for curve in curve_data:
        with raises(Exception, match=exception):
            Curve(curve).getZapRequired(a, n)


def sigma_sum(start, end, func):
    """ Helper for testing valid summation of
        dot value:

        getZapRequired(a, n) = \\sum_{i=a}^{a + n} getPrice(i)
    """
    assert isWhole(start) and isWhole(end)
    return sum(func(i) for i in range(start, start + int(end)))


@mark.parametrize("a, n",
                  [(2, 3), (1, 5), (1, 10), (5, 1e3)])
def test_getZapRequired_valid(a, n, curve_data):
    """ Tests for valid summation of dot value

        getZapRequired(a, n) = \\sum_{i=a}^{a + n} getPrice(i)
    """
    for curve in curve_data:
        with Curve(curve) as curve_obj:
            assert curve_obj.getZapRequired(
                a, n) == sigma_sum(a, n, curve_obj.getPrice)


def test_valuesToString(curve_data):
    for curve in curve_data:
        with Curve(curve) as curve_obj:
            stringed_expression = curve_obj.valuesToString()
            correct_expression = [str(term) for term in curve_obj.values]
            assert stringed_expression == correct_expression


def test_splitCurveToTerms(curve_data):
    correct_expressions = [[[3, 0, 0, 3, 1e10]],
                           [[3, 1, 0, 3, 1e10]],
                           [[3, 4, 2, 3, 1e8], [4, 0, 0, 3, 4, 1e10]],
                           [[3, 1, 0, 1e-5, 1e5], [2, 5, 4, 1e9]]]

    for curve, expressions in zip(curve_data, correct_expressions):
        with Curve(curve) as curve_obj:
            for curve_obj_exp, expression in zip(curve_obj.splitCurveToTerms(curve), expressions):
                assert curve_obj_exp == expression


correct_expressions = [["3x^2; limit = 10000000000.0"],

                       ["x^0+3x^2; limit = 10000000000.0"],

                       ["4x^0+2x^1+3x^2; limit = 100000000.0",
                        "3x^2+4x^3; limit = 10000000000.0"],

                       ["x^0+1e-05x^2; limit = 100000.0",
                        "5x^0+4x^1; limit = 1000000000.0"]]


def test_termToString(curve_data):
    for curve, expressions in zip(curve_data, correct_expressions):
        with Curve(curve) as curve_obj:
            for curve_obj_exp, expression in zip(curve_obj.splitCurveToTerms(curve), expressions):
                assert curve_obj.termToString(curve_obj_exp) == expression


def test_curveToString(curve_data):
    for curve, expressions in zip(curve_data, correct_expressions):
        with Curve(curve) as curve_obj:
            comparitor = "&".join(string for string in expressions)
            assert comparitor == curve_obj.curveToString(curve)


@mark.parametrize("curve_string, limit, exception",
                  [("4x^2+6x^7", "hi", "Start and end must be numbers"),
                   ("4x^2+6x^7", "1e10", "Start and end must be numbers"),
                   ("4x^2+6x^7", None, "Start and end must be numbers")])
def test_convertToCurve_invalid(curve_string, limit, exception):
    with raises(Exception, match=exception):
        Curve().convertToCurve(limit, curve_string)


@mark.parametrize("curve_string, limit",
                  [("4x^2+6x^7", -1),
                   ("4x^2+6x^7", int("-10000"))])
def test_convertToCurve_invalid_assert(curve_string, limit):
    with raises(AssertionError):
        Curve().convertToCurve(limit, curve_string)


@mark.parametrize("curve_string, limit, expected_curve",
                  [("3x^2", 10000000000.0, [3, 0, 0, 3, 1e10]),
                   ("x^0+3x^2", 10000000000.0, [3, 1, 0, 3, 1e10]),
                   ("4x^0+2x^1+3x^2", 100000000.0, [3, 4, 2, 3, 1e8]),
                   ("4x^0+2tetherx^1+3x^2", 100000000.0,
                    [3, 4, 2 * 1e30, 3, 1e8]),
                   ("x^0+0.00001x^2", 1000000.0, [3, 1, 0, 1e-5, 1e6]),
                   ("x^0+100000.0szabox^2", 1000000.0, [3, 1, 0, 1e5 * 1e12, 1e6])])
def test_convertToCurve(curve_string, limit, expected_curve):
    assert Curve().convertToCurve(limit, curve_string) == expected_curve
