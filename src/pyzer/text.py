import pygame
import pygame.freetype
from .types import Vec2f, Color
from .driver import PygameDriver
from .image import Image

def Text(driver: PygameDriver, pos: Vec2f, font: pygame.freetype.Font, text: str,
    fill:Color="black"
) -> Image:
    source, _ = font.render(text, fgcolor=fill)

    return Image(driver, source, pos)
