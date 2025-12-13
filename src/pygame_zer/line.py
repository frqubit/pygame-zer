from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pygame_zer.hitbox import CollideResult, Hitbox

if TYPE_CHECKING:
    from .camera import Camera
    from .driver import Driver
from .shape import Shape
from .types import EPSILON, F, FAble, Vec2fAble, f, vec2f


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
    def __init__(self, p1: Vec2fAble, p2: Vec2fAble):
        super().__init__(
            "line", {"line": self.collides_with_line}, {"line": self.contains_line}
        )
        p1 = vec2f(*p1)
        p2 = vec2f(*p2)
        self.p1 = p1
        self.p2 = p2

        slope = None if p1[0] == p2[0] else (p2[1] - p1[1]) / (p2[0] - p1[0])
        if slope is None:
            self.slope_yint = None
        else:
            self.slope_yint = (slope, p1[1] - slope * p1[0])

    def contains_point(self, pt: Vec2fAble) -> CollideResult:
        pt = vec2f(*pt)
        if self.slope_yint is None:
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

            correct_y = self.slope_yint[0] * pt[0] + self.slope_yint[1]

            # Slopes are off
            return CollideResult.for_sure(abs(correct_y - pt[1]) < EPSILON)

    def contains_line(self, other: LineHitbox) -> CollideResult:
        return CollideResult.for_sure(
            self.contains_point(other.p1) == CollideResult.YES
            and self.contains_point(other.p2) == CollideResult.YES
        )

    def collides_with_line(self, other: LineHitbox) -> CollideResult:
        if self.slope_yint is None and other.slope_yint is None:
            return CollideResult.for_sure(
                abs(self.p1[0] - other.p1[0]) < EPSILON
                and not (
                    min(other.p1[1], other.p2[1]) - EPSILON
                    > max(self.p1[1], self.p2[1]) + EPSILON
                    or max(other.p1[1], other.p2[1]) + EPSILON
                    < min(self.p1[1], self.p2[1]) - EPSILON
                )
            )
        elif self.slope_yint is None and other.slope_yint is not None:
            x_collide = self.p1[0]
            y_collide = other.slope_yint[0] * x_collide + other.slope_yint[1]
            return CollideResult.for_sure(
                self.contains_point((x_collide, y_collide)) == CollideResult.YES
                and other.contains_point((x_collide, y_collide)) == CollideResult.YES
            )
        elif self.slope_yint is not None and other.slope_yint is None:
            x_collide = other.p1[0]
            y_collide = self.slope_yint[0] * x_collide + self.slope_yint[1]
            return CollideResult.for_sure(
                self.contains_point((x_collide, y_collide)) == CollideResult.YES
                and other.contains_point((x_collide, y_collide)) == CollideResult.YES
            )

        # TODO write this in a more type-safe way that makes mypy not stupid
        assert self.slope_yint is not None
        assert other.slope_yint is not None

        if self.slope_yint[0] == other.slope_yint[0]:
            return CollideResult.for_sure(
                abs(self.slope_yint[1] - other.slope_yint[1]) < EPSILON
                and not (
                    min(other.p1[0], other.p2[0]) - EPSILON
                    > max(self.p1[0], self.p2[0]) + EPSILON
                    or max(other.p1[0], other.p2[0]) + EPSILON
                    < min(self.p1[0], self.p2[0]) - EPSILON
                )
            )
        else:
            x_collide = (other.slope_yint[1] - self.slope_yint[1]) / (
                self.slope_yint[0] - other.slope_yint[0]
            )
            y_collide = self.slope_yint[0] * x_collide + self.slope_yint[1]

            return CollideResult.for_sure(
                self.contains_point((x_collide, y_collide)) == CollideResult.YES
                and other.contains_point((x_collide, y_collide)) == CollideResult.YES
            )
