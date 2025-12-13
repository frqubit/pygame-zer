from decimal import Decimal
from typing import Tuple

Vec2i = Tuple[int, int]
Vec2f = Tuple[F, F]
Vec2fAble = Vec2f | Vec2i | Tuple[float, float]
F = Decimal
FAble = F | int | float

def f(v: FAble) -> F: ...
def vec2f(x: FAble, y: FAble) -> Vec2f: ...

Rectf = Tuple[F, F, F, F]
RectfAble = Rectf | Tuple[int, int, int, int] | Tuple[float, float, float, float]

def rectf(x: FAble, y: FAble, w: FAble, h: FAble) -> Rectf: ...

Color = str
EPSILON: F
