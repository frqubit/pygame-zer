from decimal import Decimal
from typing import TypeAlias

Vec2i: TypeAlias = tuple[int, int]
Vec2f: TypeAlias = tuple[Decimal, Decimal]
Vec2fAble: TypeAlias = Vec2f | Vec2i | tuple[float, float]


def vec2f(*args: Vec2fAble) -> Vec2f:
    if isinstance(args[0], Decimal):
        return args
    else:
        return (Decimal(args[0]), Decimal(args[1]))


Rectf: TypeAlias = tuple[Decimal, Decimal, Decimal, Decimal]
RectfAble: TypeAlias = (
    Rectf | tuple[int, int, int, int] | tuple[float, float, float, float]
)


def rectf(*args: RectfAble) -> Rectf:
    if isinstance(args[0], Decimal):
        return args
    else:
        return (Decimal(args[0]), Decimal(args[1]), Decimal(args[2]), Decimal(args[3]))


F: TypeAlias = Decimal
FAble: TypeAlias = F | int | float


def f(v: FAble) -> F:
    if isinstance(v, Decimal):
        return v
    else:
        return Decimal(v)


Color: TypeAlias = str

EPSILON = 0.000000000001
