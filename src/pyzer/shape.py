import pygame

class Shape:
    def draw(self, surface: pygame.Surface):
        raise NotImplementedError("Shape is an abstract class")

    def translate(self, x: int, y: int):
        raise NotImplementedError("Shape is an abstract class")
