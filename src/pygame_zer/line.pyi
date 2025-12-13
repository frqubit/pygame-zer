from typing import Optional, Tuple

from .camera import Camera
from .driver import Driver
from .hitbox import CollideResult, Hitbox
from .shape import Shape
from .types import Color, F, FAble, Vec2f, Vec2fAble

class Line(Shape):
    driver: Driver
    fill: Color
    p1: Vec2f
    p2: Vec2f

    def __init__(
        self, driver: Driver, p1: Vec2fAble, p2: Vec2fAble, fill: Optional[Color] = ...
    ) -> None: ...
    @property
    def hitbox(self) -> Hitbox: ...
    def draw(self, camera: Camera) -> None: ...
    def translate(self, x: FAble, y: FAble) -> None: ...

class LineHitbox(Hitbox):
    p1: Vec2f
    p2: Vec2f
    slope_yint: None | Tuple[F, F]

    def __init__(self, p1: Vec2fAble, p2: Vec2fAble) -> None: ...
    def contains_point(self, pt: Vec2fAble) -> CollideResult: ...
    def contains_line(self, other: LineHitbox) -> CollideResult: ...
    def collides_with_line(self, other: LineHitbox) -> CollideResult: ...
