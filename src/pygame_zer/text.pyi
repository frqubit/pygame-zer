from typing import Optional

import pygame
import pygame.freetype

from .camera import Camera
from .driver import Driver
from .image import Image, ScaledSource
from .types import Color, F, Vec2fAble

class Text(Image):
    fill: Color
    font: pygame.freetype.Font
    nocache: bool
    text: str

    def __init__(
        self,
        driver: Driver,
        pos: Vec2fAble,
        font: pygame.freetype.Font,
        text: str,
        fill: Optional[Color] = ...,
    ) -> None: ...
    @property
    def font_size(self) -> F: ...
    def scaled_source(self, camera: Camera) -> ScaledSource: ...
