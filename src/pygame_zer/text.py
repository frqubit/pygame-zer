import pygame
import pygame.freetype
from .types import Vec2f, Color
from .driver import PygameDriver, DriverFlags
from .image import Image, ScaledSource
from .camera import Camera

class Text(Image):
    def __init__(self, driver: PygameDriver, pos: Vec2f, font: pygame.freetype.Font, text: str,
        fill:Color="black"
    ):
        source, _ = font.render(text, fgcolor=fill)
        super().__init__(driver, source, pos)
        self.font = font
        self.text = text
        self.fill = fill
        self.nocache = DriverFlags.NOCACHE in driver.flags

    @property
    def font_size(self) -> float:
        if isinstance(self.font.size, list | tuple):
            return self.font.size[0]
        return self.font.size

    def scaled_source(self, camera: Camera) -> ScaledSource | None:
        if self.nocache:
            self.source, _ = self.font.render(self.text, fgcolor=self.fill, size=self.font_size * camera.camerazoom)
            self.size = self.source.get_size()
        return super().scaled_source(camera)
