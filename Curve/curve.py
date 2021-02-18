import re  # regex


def isWhole(number):
    if isinstance(number, float):
        return number.is_integer()
    else:
        return isinstance(number, int)


class Curve:
    """
        This class represents a Zap piecewise curve.

        Provides the functionality to parse Zap's piecewise
        function encoding and calculate the price of dots at
        any given point on the curve.
    """
    values: list
    Max: int = 0

    def __init__(self, curve: list):
        """
            Initializes a wrapper class for function
            and structurizes the provided curves.
        """
        self.values = curve
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

    def convertToBNArrays() -> list:
        """ in Python, int types can grow arbitrarily large on their own
            when needed; they can already grow > 32 bit numbers and perform
            typical math operations
        """
        return [int(num) for num in self.values]

    def valuesToString(self) -> list:
        return [str(val) for val in self.values]

    def termToString(term: list) -> str:
        limit: int = term[len(term) - 1]
        parts: list = []

        for i in range(1, term[0] + 1):
            if term[i] == 0:
                continue
            elif term[i] == 1:
                parts.append('x^' + str(i - 1))
            else:
                parts.append(str(term[i]) + 'x^' + str(i - 1))

        return "+".join(parts) + '; limit = ' + str(limit)

    def splitCurveToTerms(curve: list) -> list:  # return: 2D list
        if len(curve) <= 0:
            return []
        res = []
        start: int = 0
        currentLen: int = curve[0]
        end: int = currentLen + 2
        while start < len(curve):
            res.append(curve[start:end])
            start += currentLen + 2
            currentLen = curve[end]
            end = start + currentLen + 2

        return res

    def curveToString(self, values: list) -> str:
        """
            Create a string representing a piecewise function
        """
        return "&".join([string for string in [self.termToString(term) for term in self.splitCurveToTerms(values)]])

    def convertToCurve(end: int, curve: str) -> list:
        if not end or not isinstance(end, int):
            raise Exception("Start and end must be numbers")

        with open("regex", 'r') as regex:
            tokenRegex = re.compile(regex.readline())

        terms: list = [term.strip() for term in curve.split("+")]
        current_curve: list = []

        switch = {
            "tether": lambda coef, index: (coef * 1e30, index + 1),
            "gether": lambda coef, index: (coef * 1e27, index + 1),
            "mether": lambda coef, index: (coef * 1e24, index + 1),
            "grand": lambda coef, index: (coef * 1e21, index + 1),
            "kether": switch["grand"],
            "zap": switch["ether"],
            "ether": lambda coef, index: (coef * 1e18, index + 1),
            "finney": switch["milli"],
            "milliether": switch["milli"],
            "milli": lambda coef, index: (coef * 1e15, index + 1),
            "szabo": switch["micro"],
            "microether": switch["micro"],
            "micro": lambda coef, index: (coef * 1e12, index + 1),
            "gwei": switch["nano"],
            "shannon": switch["nano"],
            "nanoether": switch["nano"],
            "nano": lambda coef, index: (coef * 1e9, index + 1),
            "mwei": switch["picoether"],
            "lovelace": switch["picoether"],
            "picoether": lambda coef, index: (coef * 1e6, index + 1),
            "kwei": switch["femtoether"],
            "babbage": switch["femtoether"],
            "femtoether": lambda coef, index: (coef * 1e3, index + 1),
            "wei": lambda coef, index: (coef * 1, index + 1),
            "default": None
        }

        for term in terms:
            coef: float = 1.0
            exp: float = 0.0

            tokens: list = [token for token in tokenRegex.findall(term)]

            for i in range(0, len(tokens)):
                token = tokens[i]

                if float(token):
                    coef *= float(token)

                    if i < len(tokens) - 1:
                        """// https://web3js.readthedocs.io/en/1.0/web3-utils.html#fromwei"""
                        try:
                            coef, i = switch[tokens[i + 1].lower()]
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

            current_curve[exp] = coef

        return [len(current_curve), *current_curve, end]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self


from types import *
