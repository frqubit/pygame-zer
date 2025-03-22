from .shape import Shape
import pygame

class PygameDriver:
    def __init__(self):
        self.shapes: list[Shape] = []

    def draw(self, surface: pygame.Surface):
        for shape in self.shapes:
            shape.draw(surface)

    def _insert_shape(self, shape: Shape):
        self.shapes.append(shape)
