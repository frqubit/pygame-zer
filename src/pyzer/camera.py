from .types import Vec2i
import pygame

class Camera:
    def __init__(self, surface: pygame.Surface, topleft: Vec2i, rendersize: Vec2i, camerazoom: float):
        self.topleft = topleft
        self.surface = surface
        self.rendersize = rendersize
        self.camerazoom = camerazoom

    def translate(self, rel: Vec2i):
        self.topleft = (
            self.topleft[0] - rel[0],
            self.topleft[1] - rel[1]
        )

    def point_to_camera(self, pt: Vec2i) -> Vec2i:
        translated = (
            pt[0] - self.topleft[0],
            pt[1] - self.topleft[1]
        )

        return translated
