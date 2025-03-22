import pygame
from .driver import PygameDriver
from .shape import Shape

class Circle(Shape):
    def __init__(self, driver: PygameDriver, center: tuple[int, int], radius: float, fill="black"):
        self.center = center
        self.radius = radius
        self.fill = fill
        driver._insert_shape(self)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.fill, self.center, self.radius)

    def translate(self, x: int, y: int):
        self.center = (
            self.center[0] + x,
            self.center[1] + y
        )
