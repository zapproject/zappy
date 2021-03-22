from typing import NewType, TypedDict

CurveType = NewType("CurveType", list)


class CurveTerm(TypedDict):
    fn: int or float
    power: int or float
    coef: int or float
