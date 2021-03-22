import re  # regex


def isWhole(number):
    if isinstance(number, float):
        return number.is_integer()
    else:
        return isinstance(number, int)


def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


class Curve:
    """
        This class represents a Zap piecewise curve.

        Provides the functionality to parse Zap's piecewise
        function encoding and calculate the price of dots at
        any given point on the curve.
    """
    values: list
    Max: int = 0

    def __init__(self, curve: list = None):
        """
            Initializes a wrapper class for function
            and structurizes the provided curves.
        """
        self.values = curve
        if self.values:
            self.checkValidity()

    def checkValidity(self) -> None:
        """
            Checks whether the piecewise curve encoding is valid
            and throws an error if invalid.
        """
        prevEnd: int = 1
        index: int = 0

        while index < len(self.values):
            length: int = self.values[index]  # no. of terms in polynomial
            if length <= 0:
                raise Exception("Invalid curve length")

            endIndex: int = index + length + 1
            if endIndex >= len(self.values):
                raise Exception("Piece is out of bounds")

            end: int = self.values[endIndex]  # x limit of polynomial function
            if end <= prevEnd:
                raise Exception("Piece domains are overlapping")

            prevEnd = end
            index += length + 2

        self.Max = prevEnd  # x limit of entire curve function

    def getPrice(self, total_x: int) -> int:
        """
            Gets the price of the nth dot.

            e.g. the price of a single dot to a curve
            with no dots issued would be calculated at n=1.
        """
        assert isWhole(total_x)
        if total_x <= 0 or total_x > self.Max:
            raise Exception("Invalid curve supply position")
        elif not self.values:
            raise Exception("Curve is not initialised")

        index: int = 0
        while index < len(self.values):
            length: int = self.values[index]
            end: int = self.values[index + length + 1]

            if total_x > end:
                index += length + 2
                continue

            count: int = 0
            for i in range(0, length):
                coeff: int = self.values[index + i + 1]
                count += coeff * (total_x ** i)

            return count

        return -1

    def getZapRequired(self, a: int, n: int) -> int:
        """
            buying n dots starting at the a-th dot
        """
        assert n < self.Max
        assert isWhole(a) and isWhole(n)

        count: int = 0
        a = int(a)
        for i in range(a, (a + int(n))):
            count += self.getPrice(i)

        return count

    def convertToBNArrays(self) -> list:
        """ in Python, int types can grow arbitrarily large on their own
            when needed; they can already grow > 32 bit numbers and perform
            typical math operations
        """
        return [int(num) for num in self.values]

    def valuesToString(self) -> list:
        return [str(val) for val in self.values]

    def splitCurveToTerms(self, curve: list) -> list:  # return: 2D list
        if len(curve) <= 0:
            return []
        res = []
        start: int = 0
        currentLen = 0

        while start < len(curve):
            currentLen += int(curve[start]) + 2
            res.append(curve[start:currentLen])
            start += currentLen

        return res

    def termToString(self, expression: list) -> str:
        limit: int = expression[len(expression) - 1]
        parts: list = []

        for i in range(1, expression[0] + 1):
            if expression[i] == 0:
                continue
            elif expression[i] == 1:
                parts.append('x^' + str(i - 1))
            else:
                parts.append(str(expression[i]) + 'x^' + str(i - 1))

        return "+".join(parts) + '; limit = ' + str(limit)

    def curveToString(self, values: list) -> str:
        """
            Create a string representing a piecewise function
        """
        return "&".join([string for string in [self.termToString(term) for term in self.splitCurveToTerms(values)]])

    def convertToCurve(self, end: int, curve: str) -> list:
        if not end or not isWhole(end):
            raise Exception("Start and end must be numbers")
        assert end > 0

        from pathlib import Path
        from os.path import join
        with open(join(Path(__file__).parent.as_posix(), r"regex"), 'r') as regex:
            tokenRegex = re.compile(regex.readline())

        terms: list = [term.strip() for term in curve.split("+")]
        current_curve: list = []

        switch = {
            "tether": lambda coef, index: (coef * 1e30, index + 1),
            "gether": lambda coef, index: (coef * 1e27, index + 1),
            "mether": lambda coef, index: (coef * 1e24, index + 1),
            "grand": lambda coef, index: (coef * 1e21, index + 1),
            "ether": lambda coef, index: (coef * 1e18, index + 1),
            "milli": lambda coef, index: (coef * 1e15, index + 1),
            "micro": lambda coef, index: (coef * 1e12, index + 1),
            "nano": lambda coef, index: (coef * 1e9, index + 1),
            "picoether": lambda coef, index: (coef * 1e6, index + 1),
            "femtoether": lambda coef, index: (coef * 1e3, index + 1),
            "wei": lambda coef, index: (coef * 1, index + 1)
        }

        chain = [("kether", switch["grand"]),
                 ("zap", switch["ether"]),
                 ("finney", switch["milli"]),
                 ("milliether", switch["milli"]),
                 ("szabo", switch["micro"]),
                 ("microether", switch["micro"]),
                 ("gwei", switch["nano"]),
                 ("shannon", switch["nano"]),
                 ("nanoether", switch["nano"]),
                 ("mwei", switch["picoether"]),
                 ("lovelace", switch["picoether"]),
                 ("kwei", switch["femtoether"]),
                 ("babbage", switch["femtoether"])]

        for pair in chain:
            k, v = enumerate(pair)
            switch[k[1]] = v[1]

        for term in terms:
            coef: float = 1.0
            exp: float = 0.0

            tokens: list = [token for token in tokenRegex.findall(term)]

            for i in range(0, len(tokens) - 1):
                token = tokens[i]

                if isDigit(token):
                    coef *= float(token)

                    if i < len(tokens) - 1:
                        """// https://web3js.readthedocs.io/en/1.0/web3-utils.html#fromwei"""
                        try:
                            coef, i = switch[tokens[i + 1].lower()](coef, i)
                            continue
                        except Exception:
                            pass
                elif token == "x":
                    exp = 1
                elif token == "*":
                    continue
                elif token == "^":
                    if i == len(tokens) - 1:
                        raise Exception("Must specify an exponent.")
                    i += 1

                    exponent: str = tokens[i]

                    if not isinstance(int(exponent), int):
                        raise Exception("Exponent must be a number.")

                    exp = int(exponent)

            while len(current_curve) < exp:
                current_curve.append(0)

            current_curve.append(coef)

        return [len(current_curve), *current_curve, end]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self


from types import *
