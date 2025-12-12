from decimal import Decimal
from typing import TypeAlias

Vec2i: TypeAlias = tuple[int, int]
Vec2f: TypeAlias = tuple[Decimal, Decimal]
Vec2fAble: TypeAlias = Vec2f | Vec2i | tuple[float, float]
F: TypeAlias = Decimal
FAble: TypeAlias = F | int | float


def f(v: FAble) -> F:
    if isinstance(v, Decimal):
        return v
    else:
        return Decimal(v)


def vec2f(x: FAble, y: FAble) -> Vec2f:
    return (f(x), f(y))


Rectf: TypeAlias = tuple[Decimal, Decimal, Decimal, Decimal]
RectfAble: TypeAlias = (
    Rectf | tuple[int, int, int, int] | tuple[float, float, float, float]
)


def rectf(x: FAble, y: FAble, w: FAble, h: FAble) -> Rectf:
    return (f(x), f(y), f(w), f(h))


Color: TypeAlias = str

EPSILON = f(0.000000000001)
