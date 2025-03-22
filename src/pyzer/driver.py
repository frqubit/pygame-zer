from .shape import Shape
import pygame

class PygameDriver:
    def __init__(self, sensitivity: float = 1):
        self.shapes: list[Shape] = []
        self.sensitivity = sensitivity

    def draw(self, surface: pygame.Surface):
        for shape in self.shapes:
            shape.draw(surface)

    def _insert_shape(self, shape: Shape):
        self.shapes.append(shape)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            for shape in self.shapes:
                shape.translate(event.rel[0] * self.sensitivity, event.rel[1] * self.sensitivity)
