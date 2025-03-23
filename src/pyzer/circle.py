import pygame
from .camera import Camera
from .driver import PygameDriver
from .shape import Shape

class Circle(Shape):
    def __init__(self, driver: PygameDriver, center: tuple[int, int], radius: float,
        fill="black", outlineWidth:float=1, outline=None
    ):
        self.center = center
        self.radius = radius
        self.fill = fill
        self.outline = outline
        self.outlineWidth = outlineWidth
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        center = camera.point_to_camera(self.center)
        radius = camera.distance_to_camera(self.radius)
        outlineRadius = ((self.outlineWidth + self.radius) / self.radius) * radius
        if self.outline is not None:
            pygame.draw.circle(camera.surface, self.outline, center, outlineRadius)
        pygame.draw.circle(camera.surface, self.fill, center, radius)


    def translate(self, x: int, y: int):
        self.center = (
            self.center[0] + x,
            self.center[1] + y
        )
