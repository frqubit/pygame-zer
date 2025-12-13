from typing import Optional

from pygame_zer.types import FAble

from .camera import Camera
from .circle import CircleHitbox
from .driver import Driver
from .hitbox import CollideResult, Hitbox
from .line import LineHitbox
from .shape import Shape
from .types import Color, Rectf, RectfAble, Vec2fAble

class Rect(Shape):
    driver: Driver
    fill: Color
    outline: Color | None
    outlineWidth: FAble
    rect: Rectf

    def __init__(
        self,
        driver: Driver,
        rect: RectfAble,
        fill: Optional[Color] = ...,
        outlineWidth: Optional[FAble] = ...,
        outline: Optional[Color | None] = ...,
    ) -> None: ...
    @property
    def hitbox(self) -> RectHitbox: ...
    def draw(self, camera: Camera) -> None: ...
    def translate(self, x: FAble, y: FAble) -> None: ...

class RectHitbox(Hitbox):
    rect: Rectf

    def __init__(self, rect: RectfAble) -> None: ...
    def contains_point(self, pt: Vec2fAble) -> CollideResult: ...
    def collides_with_circle(self, other: CircleHitbox) -> CollideResult: ...
    def contains_circle(self, other: CircleHitbox) -> CollideResult: ...
    def collides_with_rect(self, other: RectHitbox) -> CollideResult: ...
    def contains_rect(self, other: RectHitbox) -> CollideResult: ...
    def collides_with_line(self, other: LineHitbox) -> CollideResult: ...
    def contains_line(self, other: LineHitbox) -> CollideResult: ...
