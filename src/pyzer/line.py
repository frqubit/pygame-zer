import pygame
from .types import Vec2f
from .camera import Camera
from .driver import PygameDriver
from .shape import Shape

class Line(Shape):
    def __init__(self, driver: PygameDriver, p1: Vec2f, p2: Vec2f, fill="black"):
        self.p1 = p1
        self.p2 = p2
        self.fill = fill
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        p1 = camera.point_to_camera(self.p1)
        p2 = camera.point_to_camera(self.p2)
        width = int(camera.distance_to_camera(1))
        pygame.draw.line(camera.surface, self.fill, p1, p2, width=width)

    def translate(self, x: int, y: int):
        self.center = (
            self.center[0] + x,
            self.center[1] + y
        )
