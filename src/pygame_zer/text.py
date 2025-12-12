import pygame
import pygame.freetype

from .camera import Camera
from .driver import Driver, DriverFlags
from .image import Image, ScaledSource
from .types import Color, Vec2f, Vec2fAble


class Text(Image):
    """
    A pygamezer text display. You should use this
    class if you want to create text in the driver
    world. The constructor will add the shape to the
    driver for you.

    Text displays extend the image class and are
    handled the same as images

    Attributes
    ----------
    font : pygame.freetype.Font
        The font to use for the text
    font_size : float
        The font size
    nocache : bool
        Forces no caching if true. Set in driver flags
    text : str
        The text as a string
    fill : str, default="black"
        The text color

    """

    def __init__(
        self,
        driver: Driver,
        pos: Vec2fAble,
        font: pygame.freetype.Font,
        text: str,
        fill: Color = "black",
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
            self.source, _ = self.font.render(
                self.text, fgcolor=self.fill, size=self.font_size * camera.camerazoom
            )
            self.image_size = self.source.get_size()
        return super().scaled_source(camera)
