import pygame
from .types import Vec2f
from .camera import Camera
from .driver import Driver
from .shape import Shape

class Line(Shape):
    def __init__(self, driver: Driver, p1: Vec2f, p2: Vec2f, fill="black"):
        self.p1 = p1
        self.p2 = p2
        self.fill = fill
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        p1 = camera.point_to_camera(self.p1)
        p2 = camera.point_to_camera(self.p2)
        width = int(camera.distance_to_camera(1))
        pygame.draw.line(camera.surface, self.fill, p1, p2, width=width)

    def translate(self, x: float, y: float):
        self.p1 = (
            self.p1[0] + x,
            self.p1[1] + y
        )

        self.p2 = (
            self.p2[0] + x,
            self.p2[1] + y
        )
