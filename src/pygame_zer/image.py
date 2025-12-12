from typing import TypeAlias

import pygame

from pygame_zer.rect import RectHitbox

from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import F, FAble, Vec2f, Vec2fAble, Vec2i, f, vec2f

ScaledSource: TypeAlias = tuple[
    Vec2i,  # position on screen
    pygame.Surface,  # surface
]


class Image(Shape):
    """
    A pygamezer image. You should use this class if
    you want to create an image in the driver world. The
    constructor will add the shape to the driver for
    you.

    You can set a desired output size in world space
    in the constructor. If you do, the image will
    be scaled to fit the requested size, which may
    change the aspect ratio.

    Attributes
    ----------
    dest : pygame_zer.types.Vec2f
        The topleft of the image in world space
    driver : pygame_zer.Driver
        The driver this image is attached to
    image_size : pygame_zer.types.Vec2f
        The size of the internal source image. This
        is not necessarily the same as the original
        source size, since a custom output size can
        change the aspect ratio
    source : pygame.Surface
        The image/surface to draw. This may
        be scaled internally to a different
        size if a custom size argument is
        specified
    size : pygame_zer.types.Vec2f, optional
        The size of the image in world space.
        Default the original source size

    """

    def __init__(
        self,
        driver: Driver,
        source: pygame.Surface,
        dest: Vec2fAble,
        size: Vec2fAble | None = None,
    ):
        # a/b * x = c/d
        # x = (c/d)/(a/b)

        # If size is not none, rescale to appropriate size
        if size is not None:
            size = vec2f(*size)
            source_scale_val = (size[0] / size[1]) / (
                f(source.get_width() / source.get_height())
            )
            self.source = pygame.transform.scale_by(
                source, (float(source_scale_val), 1)
            )
        else:
            self.source = source
        self.dest: Vec2f = vec2f(*dest)
        self.image_size: Vec2f = vec2f(*self.source.get_size())
        self.size = vec2f(*size) if size is not None else self.image_size
        driver._insert_shape(self)

    @property
    def hitbox(self) -> RectHitbox:
        return RectHitbox((self.dest[0], self.dest[1], self.size[0], self.size[1]))

    def scaled_source(self, camera: Camera) -> ScaledSource | None:
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

        content_topleft = [max(tl, f(0)) for tl in topleft]
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
                int(image_tl[0]),
                int(image_tl[1]),
                int(image_br[0] - image_tl[0]),
                int(image_br[1] - image_tl[1]),
            )
        )

        scaled = pygame.transform.smoothscale_by(
            segment,
            (
                float(content_size[0] / segment.get_width()),
                float(content_size[1] / segment.get_height()),
            ),
        )

        return ((int(content_topleft[0]), int(content_topleft[1])), scaled)

    def draw(self, camera: Camera):
        scaled_src = self.scaled_source(camera)
        if scaled_src is not None:
            camera.surface.blit(scaled_src[1], scaled_src[0])

    def translate(self, x: FAble, y: FAble):
        self.dest = (self.dest[0] + f(x), self.dest[1] + f(y))
