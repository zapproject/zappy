from typing import NewType, TypedDict

CurveType = NewType("CurveType", list)


class CureveTerm(TypedDict):
    fn: int or float
    power: int or float
    coef: int or float
