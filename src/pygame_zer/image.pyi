from typing import Optional, Tuple

import pygame

from .camera import Camera
from .driver import Driver
from .hitbox import Hitbox
from .shape import Shape
from .types import FAble, Vec2f, Vec2fAble, Vec2i

ScaledSource = Tuple[Vec2i, pygame.Surface]

class Image(Shape):
    dest: Vec2f
    image_size: Vec2f
    size: Vec2f
    source: pygame.Surface

    def __init__(
        self,
        driver: Driver,
        source: pygame.Surface,
        dest: Vec2fAble,
        size: Optional[Vec2fAble | None] = ...,
    ) -> None: ...
    @property
    def hitbox(self) -> Hitbox: ...
    def scaled_source(self, camera: Camera) -> ScaledSource: ...
    def draw(self, camera: Camera) -> None: ...
    def translate(self, x: FAble, y: FAble) -> None: ...
