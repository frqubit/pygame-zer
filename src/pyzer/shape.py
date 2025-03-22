import pygame

class Shape:
    def draw(self, surface: pygame.Surface):
        raise NotImplementedError("Shape is an abstract class")
