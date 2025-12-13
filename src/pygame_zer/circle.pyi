from typing import Optional, Self

from .camera import Camera
from .driver import Driver
from .hitbox import CollideResult, Hitbox
from .rect import RectHitbox
from .shape import Shape
from .types import Color, F, FAble, Vec2f, Vec2fAble

class Circle(Shape):
    center: Vec2f
    driver: Driver
    fill: Color
    outline: Color | None
    outlineWidth: F
    radius: F

    def __init__(
        self,
        driver: Driver,
        center: Vec2fAble,
        radius: FAble,
        fill: Optional[Color] = ...,
        outlineWidth: Optional[FAble] = ...,
        outline: Optional[Color | None] = ...,
    ) -> None: ...
    @property
    def hitbox(self) -> CircleHitbox: ...
    def draw(self, camera: Camera) -> None: ...
    def translate(self, x: FAble, y: FAble) -> None: ...

class CircleHitbox(Hitbox):
    center: Vec2f
    radius: F

    def __init__(self, center: Vec2fAble, radius: FAble) -> None: ...
    def contains_point(self, pt: Vec2fAble) -> CollideResult: ...
    def collides_with_circle(self, other: Self) -> CollideResult: ...
    def contains_circle(self, other: Self) -> CollideResult: ...
    def contains_rect(self, other: RectHitbox) -> CollideResult: ...
