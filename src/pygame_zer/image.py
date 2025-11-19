import math
from typing import TypeAlias

import pygame

from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import Vec2f, Vec2i

ScaledSource: TypeAlias = tuple[
    Vec2i,  # position on screen
    pygame.Surface,  # surface
]


class Image(Shape):
    def __init__(
        self,
        driver: Driver,
        source: pygame.Surface,
        dest: Vec2f,
        size: Vec2f | None = None,
    ):
        # a/b * x = c/d
        # x = (c/d)/(a/b)

        # If size is not none, rescale to appropriate size
        if size is not None:
            source_scale_val = (size[0] / size[1]) / (
                source.get_width() / source.get_height()
            )
            self.source = pygame.transform.scale_by(source, (source_scale_val, 1))
        else:
            self.source = source
        self.dest = dest
        self.image_size: Vec2f = self.source.get_size()
        self.size = size if size is not None else self.image_size
        driver._insert_shape(self)

    def scaled_source(self, camera: Camera) -> ScaledSource | None:
        zoom = camera.camerazoom
        topleft = camera.point_to_camera(self.dest)
        bottomright = camera.point_to_camera(
            (self.dest[0] + self.size[0], self.dest[1] + self.size[1])
        )

        if topleft[0] >= camera.rendersize[0] or topleft[1] >= camera.rendersize[1]:
            # Too far right or down
            return None
        if bottomright[0] <= 0 or bottomright[1] <= 0:
            # Too far left or up
            return None

        content_topleft = [max(tl, 0) for tl in topleft]
        content_bottomright = [
            min(br, rs) for br, rs in zip(bottomright, camera.rendersize)
        ]

        content_offset_tl = [ctl - tl for ctl, tl in zip(content_topleft, topleft)]
        content_offset_br = [
            br - cbr for cbr, br in zip(content_bottomright, bottomright)
        ]

        size = [camera.distance_to_camera(n) for n in self.size]
        content_size = [
            (s - cobr) - cotl
            for s, cobr, cotl in zip(size, content_offset_br, content_offset_tl)
        ]

        offsetratio_tl = [cotl / cs for cotl, cs in zip(content_offset_tl, size)]
        offsetratio_br = [cobr / cs for cobr, cs in zip(content_offset_br, size)]

        image_tl = [iS * otl for iS, otl in zip(self.image_size, offsetratio_tl)]
        image_br = [iS - (iS * obr) for iS, obr in zip(self.image_size, offsetratio_br)]

        if int(image_br[0] - image_tl[0]) <= 0 or int(image_br[1] - image_tl[1]) <= 0:
            return None

        segment = self.source.subsurface(
            (
                image_tl[0],
                image_tl[1],
                image_br[0] - image_tl[0],
                image_br[1] - image_tl[1],
            )
        )

        scaled = pygame.transform.smoothscale_by(
            segment,
            (
                content_size[0] / segment.get_width(),
                content_size[1] / segment.get_height(),
            ),
        )

        return ((content_topleft[0], content_topleft[1]), scaled)

    def draw(self, camera: Camera):
        scaled_src = self.scaled_source(camera)
        if scaled_src is not None:
            camera.surface.blit(scaled_src[1], scaled_src[0])

    def translate(self, x: float, y: float):
        self.dest = (self.dest[0] + x, self.dest[1] + y)
