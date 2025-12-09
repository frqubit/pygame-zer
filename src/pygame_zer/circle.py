from __future__ import annotations

import math
from typing import Self

from pygame_zer.hitbox import CollideResult, Hitbox
from pygame_zer.rect import RectHitbox
from pygame_zer.types import Vec2f

from .camera import Camera
from .driver import Driver
from .shape import Shape


class Circle(Shape):
    """
    A pygamezer circle. You should use this class if
    you want to create a circle in the driver world. The
    constructor will add the shape to the driver for
    you. You can modify attributes of the circle after
    the constructor is run.

    Attributes
    ----------
    center : pygame_zer.types.Vec2i
        The center of the circle in world space
    driver : pygame_zer.Driver
        The driver this circle is attached to
    fill : str
        The color to fill the circle with
    radius : float
        The radius of the circle in world space
    outline : str, optional
        The color to outline the circle with. Default nothing
    outlineWidth : float, default=1
        The width of the circle outline in world space. Default 1

    """

    def __init__(
        self,
        driver: Driver,
        center: tuple[int, int],
        radius: float,
        fill="black",
        outlineWidth: float = 1,
        outline=None,
    ):
        self.center = center
        self.radius = radius
        self.fill = fill
        self.outline = outline
        self.outlineWidth = outlineWidth
        self.driver = driver
        driver._insert_shape(self)

    @property
    def hitbox(self) -> CircleHitbox:
        return CircleHitbox(self.center, self.radius)

    def draw(self, camera: Camera):
        if self.hitbox.contains_hitbox(camera.hitbox) == CollideResult.YES:
            # The whole camera is covered by the circle, don't bother
            camera.surface.fill(self.fill)
        else:
            self.driver.draw.circle(self.fill, self.center, self.radius)
            if self.outline is not None:
                self.driver.draw.circle(
                    self.outline, self.center, self.radius, width=self.outlineWidth
                )

    def translate(self, x: float, y: float):
        self.center = (self.center[0] + x, self.center[1] + y)


class CircleHitbox(Hitbox):
    def __init__(self, center: Vec2f, radius: float):
        super().__init__(
            "circle",
            {"circle": self.collides_with_circle},
            {"circle": self.contains_circle, "rect": self.contains_rect},
        )

        self.center = center
        self.radius = radius

    def contains_point(self, pt: Vec2f) -> CollideResult:
        distance = math.sqrt(
            (self.center[0] - pt[0]) ** 2 + (self.center[1] - pt[1]) ** 2
        )

        return CollideResult.for_sure(distance <= self.radius)

    def collides_with_circle(self, other: Self) -> CollideResult:
        distance = math.sqrt(
            (self.center[0] - other.center[0]) ** 2
            + (self.center[1] - other.center[1]) ** 2
        )

        return CollideResult.for_sure(distance <= self.radius + other.radius)

    def contains_circle(self, other: Self) -> CollideResult:
        distance = math.sqrt(
            (self.center[0] - other.center[0]) ** 2
            + (self.center[1] - other.center[1]) ** 2
        )

        return CollideResult.for_sure(distance + other.radius <= self.radius)

    def contains_rect(self, other: RectHitbox):
        return CollideResult.for_sure(
            self.contains_point((other.rect[0], other.rect[1])) == CollideResult.YES
            and self.contains_point(
                (other.rect[0] + other.rect[2], other.rect[1] + other.rect[3])
            )
            == CollideResult.YES
        )
