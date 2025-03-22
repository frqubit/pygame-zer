from .shape import Shape
from .camera import Camera
import pygame

class PygameDriver:
    def __init__(self, surface: pygame.Surface):
        self.shapes: list[Shape] = []
        self.camera = Camera(surface, (0, 0), surface.get_size(), 1)

    def draw(self, surface: pygame.Surface):
        for shape in self.shapes:
            shape.draw(self.camera)

    def _insert_shape(self, shape: Shape):
        self.shapes.append(shape)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.camera.translate(event.rel)
            return True
        elif event.type == pygame.MOUSEWHEEL:
            self.camera.zoom(event.y)
            return True
        return False
