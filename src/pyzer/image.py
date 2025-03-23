import pygame
import math
from typing import TypeAlias
from .camera import Camera
from .driver import PygameDriver
from .shape import Shape
from .types import Vec2f, Vec2i

ScaledSource: TypeAlias = tuple[
    Vec2i,          # position on screen
    pygame.Surface  # surface
]

class Image(Shape):
    def __init__(self, driver: PygameDriver, source:pygame.Surface, dest:Vec2f):
        self.source = source
        self.dest = dest
        self.size:Vec2f = source.get_size()
        driver._insert_shape(self)

    def scaled_source(self, camera) -> ScaledSource | None:
        zoom = camera.camerazoom
        topleft = camera.point_to_camera(self.dest)
        size = [camera.distance_to_camera(n) for n in self.size]
        if topleft[0] > camera.rendersize[0] or topleft[1] > camera.rendersize[1]:
            # off to the bottom or right
            return None
        imageTopleftRatio: list[float] = [-n / s if n <= 0 else 0 for n, s in zip(topleft, size)]
        if imageTopleftRatio[0] > 1 or imageTopleftRatio[1] > 1:
            # off to the top or left
            return None
        imageTopleft = [r * s for r, s in zip(imageTopleftRatio, self.size)]
        imageRem = [min(s - m, math.ceil(r / zoom)) for s, m, r in zip(self.size, imageTopleft, camera.rendersize)]
        segment = self.source.subsurface((
            imageTopleft[0],
            imageTopleft[1],
            imageRem[0],
            imageRem[1]
        ))
        scaled = pygame.transform.smoothscale_by(segment, zoom)
        return ((
            max(topleft[0], 0),
            max(topleft[1], 0)
        ), scaled)

    def draw(self, camera: Camera):
        scaled_src = self.scaled_source(camera)
        if scaled_src is not None:
            camera.surface.blit(scaled_src[1], scaled_src[0])

    def translate(self, x: int, y: int):
        self.center = (
            self.center[0] + x,
            self.center[1] + y
        )
