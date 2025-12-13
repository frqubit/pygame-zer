from __future__ import annotations

from typing import TYPE_CHECKING

from pygame_zer.hitbox import CollideResult, Hitbox
from pygame_zer.line import LineHitbox

if TYPE_CHECKING:
    from pygame_zer.circle import CircleHitbox

    from .camera import Camera
    from .driver import Driver
from .shape import Shape
from .types import Color, FAble, Rectf, RectfAble, Vec2f, Vec2fAble, f, rectf


class Rect(Shape):
    """
    A pygamezer rectangle. You should use this class
    if you want to create a rectangle in the driver
    world. The constructor will add the shape to the
    driver for you. You can modify attributes of the
    rectangle after the constructor is run.

    Attributes
    ----------
    driver : pygame_zer.Driver
        The driver this rectangle is attached to
    fill : str
        The color to fill the rectangle with
    rect : pygame_zer.types.Rectf
        The rectangle range to draw to in world space
    outline : str, optional
        The color to outline the rectangle with. Default nothing
    outlineWidth : float, default=1
        The width of the rectangle outline in world space. Default 1

    """

    def __init__(
        self,
        driver: Driver,
        rect: RectfAble,
        fill="black",
        outlineWidth: FAble = 1,
        outline: Color | None = None,
    ):
        self.rect = rectf(*rect)
        self.fill = fill
        self.outline = outline
        self.outlineWidth = f(outlineWidth)
        self.driver = driver
        driver._insert_shape(self)

    @property
    def hitbox(self) -> RectHitbox:
        return RectHitbox(self.rect)

    def draw(self, camera: Camera):
        if self.hitbox.contains_hitbox(camera.hitbox) == CollideResult.YES:
            camera.surface.fill(self.fill)
        else:
            if self.outline is not None:
                self.driver.draw.rect(self.outline, self.rect, width=self.outlineWidth)
            self.driver.draw.rect(self.fill, self.rect)

    def translate(self, x: FAble, y: FAble):
        self.rect = (
            self.rect[0] + f(x),
            self.rect[1] + f(y),
            self.rect[2],
            self.rect[3],
        )


class RectHitbox(Hitbox):
    def __init__(self, rect: RectfAble):
        super().__init__(
            "rect",
            {
                "circle": self.collides_with_circle,
                "rect": self.collides_with_rect,
                "line": self.collides_with_line,
            },
            {
                "circle": self.contains_circle,
                "rect": self.contains_rect,
                "line": self.contains_line,
            },
        )
        self.rect = rectf(*rect)

    def contains_point(self, pt: Vec2fAble) -> CollideResult:
        return CollideResult.for_sure(
            pt[0] >= self.rect[0]
            and pt[1] >= self.rect[1]
            and pt[0] <= self.rect[0] + self.rect[2]
            and pt[1] <= self.rect[1] + self.rect[3]
        )

    def collides_with_circle(self, other: CircleHitbox) -> CollideResult:
        return RectHitbox(
            (
                self.rect[0] - other.radius,
                self.rect[1] - other.radius,
                self.rect[2] + other.radius * 2,
                self.rect[3] + other.radius * 2,
            )
        ).contains_point(other.center)

    def contains_circle(self, other: CircleHitbox) -> CollideResult:
        return RectHitbox(
            (
                self.rect[0] + other.radius,
                self.rect[1] + other.radius,
                self.rect[2] - other.radius * 2,
                self.rect[3] - other.radius * 2,
            )
        ).contains_point(other.center)

    def collides_with_rect(self, other: RectHitbox) -> CollideResult:
        return RectHitbox(
            (
                self.rect[0] - other.rect[2],
                self.rect[1] - other.rect[3],
                self.rect[2] + other.rect[2],
                self.rect[3] + other.rect[3],
            )
        ).contains_point((other.rect[0], other.rect[1]))

    def contains_rect(self, other: RectHitbox) -> CollideResult:
        return RectHitbox(
            (
                self.rect[0],
                self.rect[1],
                self.rect[2] - other.rect[2],
                self.rect[3] - other.rect[3],
            )
        ).contains_point((other.rect[0], other.rect[1]))

    def collides_with_line(self, other: LineHitbox) -> CollideResult:
        return CollideResult.for_sure(
            self.contains_line(other) == CollideResult.YES
            # Top edge
            or LineHitbox(
                (self.rect[0], self.rect[1]),
                (self.rect[0] + self.rect[2], self.rect[1]),
            ).collides_hitbox(other)
            == CollideResult.YES
            # Left edge
            or LineHitbox(
                (self.rect[0], self.rect[1]),
                (self.rect[0], self.rect[1] + self.rect[3]),
            ).collides_hitbox(other)
            == CollideResult.YES
            # Bottom edge
            or LineHitbox(
                (self.rect[0], self.rect[1] + self.rect[3]),
                (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]),
            ).collides_hitbox(other)
            == CollideResult.YES
            # Right edge
            or LineHitbox(
                (self.rect[0] + self.rect[2], self.rect[1]),
                (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]),
            ).collides_hitbox(other)
            == CollideResult.YES
        )

    def contains_line(self, other: LineHitbox) -> CollideResult:
        return CollideResult.for_sure(
            self.contains_point(other.p1) == CollideResult.YES
            and self.contains_point(other.p2) == CollideResult.YES
        )
