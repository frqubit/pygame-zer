from __future__ import annotations

from typing import TYPE_CHECKING

from pygame_zer.hitbox import CollideResult, Hitbox

if TYPE_CHECKING:
    from .camera import Camera
    from .driver import Driver
from .shape import Shape
from .types import EPSILON, FAble, Vec2f, Vec2fAble, f, vec2f


class Line(Shape):
    """
    A pygamezer line. You should use this class if
    you want to create a line in the driver world. The
    constructor will add the shape to the driver for
    you. You can modify attributes of the line after
    the constructor is run.

    Attributes
    ----------
    driver : pygame_zer.Driver
        The driver this line is attached to
    fill : str
        The color of the line
    p1 : pygame_zer.types.Vec2f
        The first point
    p2 : pygame_zer.types.Vec2f
        The second point

    """

    def __init__(self, driver: "Driver", p1: Vec2fAble, p2: Vec2fAble, fill="black"):
        self.p1 = vec2f(*p1)
        self.p2 = vec2f(*p2)
        self.fill = fill
        self.driver = driver
        driver._insert_shape(self)

    @property
    def hitbox(self) -> Hitbox:
        return LineHitbox(self.p1, self.p2)

    def draw(self, camera: "Camera"):
        self.driver.draw.line(self.fill, self.p1, self.p2)

    def translate(self, x: FAble, y: FAble):
        self.p1 = (self.p1[0] + f(x), self.p1[1] + f(y))

        self.p2 = (self.p2[0] + f(x), self.p2[1] + f(y))


class LineHitbox(Hitbox):
    def __init__(self, p1: Vec2f, p2: Vec2f):
        super().__init__(
            "line", {"line": self.collides_with_line}, {"line": self.contains_line}
        )
        self.p1 = p1
        self.p2 = p2
        self.slope = None if p1[0] == p2[0] else (p2[1] - p1[1]) / (p2[0] - p1[0])
        self.yint = None if self.slope is None else p1[1] - (self.slope * p1[0])

    def contains_point(self, pt: Vec2f) -> CollideResult:
        if self.slope is None:
            return CollideResult.for_sure(
                pt[0] == self.p1[0]
                and pt[1] >= min(self.p1[1], self.p2[1]) - EPSILON
                and pt[1] <= max(self.p1[1], self.p2[1]) + EPSILON
            )
        else:
            if (
                pt[0] < min(self.p1[0], self.p2[0]) - EPSILON
                or pt[1] > max(self.p1[0], self.p2[0]) + EPSILON
            ):
                return CollideResult.NO

            correct_y = self.slope * pt[0] + self.yint

            # Slopes are off
            return CollideResult.for_sure(abs(correct_y - pt[1]) < EPSILON)

    def contains_line(self, other: LineHitbox) -> CollideResult:
        return CollideResult.for_sure(
            self.contains_point(other.p1) == CollideResult.YES
            and self.contains_point(other.p2) == CollideResult.YES
        )

    def collides_with_line(self, other: LineHitbox) -> CollideResult:
        if self.slope == other.slope:
            if self.slope is None:
                return CollideResult.for_sure(
                    abs(self.p1[0] - other.p1[0]) < EPSILON
                    and not (
                        min(other.p1[1], other.p2[1]) - EPSILON
                        > max(self.p1[1], self.p2[1]) + EPSILON
                        or max(other.p1[1], other.p2[1]) + EPSILON
                        < min(self.p1[1], self.p2[1]) - EPSILON
                    )
                )
            else:
                return CollideResult.for_sure(
                    abs(self.yint - other.yint) < EPSILON
                    and not (
                        min(other.p1[0], other.p2[0]) - EPSILON
                        > max(self.p1[0], self.p2[0]) + EPSILON
                        or max(other.p1[0], other.p2[0]) + EPSILON
                        < min(self.p1[0], self.p2[0]) - EPSILON
                    )
                )
        else:
            # ors technically only there for type safety
            if self.slope is None:
                x_collide = self.p1[0]
                y_collide = other.slope * x_collide + other.yint
            elif other.slope is None:
                x_collide = other.p1[0]
                y_collide = self.slope * x_collide + self.yint
            else:
                x_collide = (other.yint - self.yint) / (self.slope - other.slope)
                y_collide = self.slope * x_collide + self.yint

            return CollideResult.for_sure(
                self.contains_point((x_collide, y_collide)) == CollideResult.YES
                and other.contains_point((x_collide, y_collide)) == CollideResult.YES
            )
