from .types import Color, Vec2f, Rectf
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

    def circle(self, color: Color, center: Vec2f, radius: float, width: float = 0):
        center = self.camera.point_to_camera(center)
        radius = self.camera.distance_to_camera(radius)
        width = self.camera.distance_to_camera(width)
        radius += width
        # outlineRadius = ((self.outlineWidth + self.radius) / self.radius) * radius
        # if self.outline is not None:
        #     pygame.draw.circle(camera.surface, self.outline, center, outlineRadius)
        pygame.draw.circle(self.camera.surface, color, center, radius, width=int(width))

    def rect(self, color: Color, rect: Rectf, width: float = 0):
        topleft = self.camera.point_to_camera(rect[0:2])
        size = [self.camera.distance_to_camera(x) for x in rect[2:]]
        width = self.camera.distance_to_camera(width)

        pygame.draw.rect(self.camera.surface, color, (
            topleft[0] - width,
            topleft[1] - width,
            size[0] + width * 2,
            size[1] + width * 2
        ), width=int(width))

    def line(self, color: Color, start_pos: Vec2f, end_pos: Vec2f, width: float = 1):
        p1 = self.camera.point_to_camera(start_pos)
        p2 = self.camera.point_to_camera(end_pos)
        width = int(self.camera.distance_to_camera(1))
        pygame.draw.line(self.camera.surface, color, p1, p2, width=width)
