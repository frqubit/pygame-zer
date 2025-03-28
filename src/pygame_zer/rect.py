import pygame
from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import Rectf, Color

class Rect(Shape):
    def __init__(self, driver: Driver, rect: Rectf,
        fill="black", outlineWidth:float=1, outline:Color=None
    ):
        self.rect = rect
        self.fill = fill
        self.outline = outline
        self.outlineWidth = outlineWidth
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        topleft = camera.point_to_camera(self.rect[0:2])
        size = [camera.distance_to_camera(x) for x in self.rect[2:]]
        if self.outline is not None:
            outlineTopleft = camera.point_to_camera(
                (
                    self.rect[0] - self.outlineWidth,
                    self.rect[1] - self.outlineWidth
                )
            )

            outlineSize = [camera.distance_to_camera(x + self.outlineWidth * 2) for x in self.rect[2:]]

            pygame.draw.rect(camera.surface, self.outline, (
                outlineTopleft[0],
                outlineTopleft[1],
                outlineSize[0],
                outlineSize[1]
            ))

        pygame.draw.rect(camera.surface, self.fill, (
            topleft[0],
            topleft[1],
            size[0],
            size[1]
        ))

    def translate(self, x: float, y: float):
        self.rect = (
            self.rect[0] + x,
            self.rect[1] + y,
            self.rect[2],
            self.rect[3]
        )
