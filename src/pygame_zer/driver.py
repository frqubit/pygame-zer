from .shape import Shape
from .camera import Camera
import pygame
import enum

class DriverFlags(enum.Flag):
    EMPTY = 1
    ZOOMABLE = 2
    EXPLORABLE = 4
    NOCACHE = 8

DEFAULT_FLAGS = DriverFlags.ZOOMABLE | DriverFlags.EXPLORABLE

class Driver:
    def __init__(self, surface: pygame.Surface, flags: DriverFlags = DEFAULT_FLAGS):
        self.camera = Camera(surface, (0, 0), surface.get_size(), 1)
        self.drawer = DriverDrawer(self.camera)
        self.flags = flags

    @property
    def draw(self):
        return self.drawer

    def _insert_shape(self, shape: Shape):
        self.drawer.shapes.append(shape)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if DriverFlags.EXPLORABLE in self.flags and event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.camera.translate(event.rel)
            return True
        elif DriverFlags.ZOOMABLE in self.flags and event.type == pygame.MOUSEWHEEL:
            self.camera.zoom(event.y)
            return True
        return False

class DriverDrawer:
    def __init__(self, camera: Camera):
        self.shapes: list[Shape] = []
        self.camera = camera

    def __call__(self):
        for shape in self.shapes:
            shape.draw(self.camera)
