from .types import Vec2i, Vec2f
import pygame

class Camera:
    def __init__(self, surface: pygame.Surface, topleft: Vec2f, rendersize: Vec2f, camerazoom: float):
        self.topleft = topleft
        self.surface = surface
        self.rendersize = rendersize
        self.camerazoom = camerazoom

    def translate(self, rel: Vec2i):
        self.topleft = (
            self.topleft[0] - rel[0] / self.camerazoom,
            self.topleft[1] - rel[1] / self.camerazoom
        )

    def zoom(self, rel: float):
        center: Vec2f = (
            self.topleft[0] + ((self.rendersize[0] / self.camerazoom) / 2),
            self.topleft[1] + ((self.rendersize[1] / self.camerazoom) / 2)
        )

        if rel == 1:
            self.camerazoom *= 1.1
        else:
            self.camerazoom /= 1.1

        new_relsize: Vec2f = (
            self.rendersize[0] / self.camerazoom,
            self.rendersize[1] / self.camerazoom
        )

        self.topleft = (
            center[0] - new_relsize[0] / 2,
            center[1] - new_relsize[1] / 2
        )

    def distance_to_camera(self, distance: float) -> float:
        return distance * self.camerazoom

    def point_to_camera(self, pt: Vec2f) -> Vec2i:
        camerasize: Vec2f = (
            self.rendersize[0] / self.camerazoom,
            self.rendersize[1] / self.camerazoom
        )

        ratios: Vec2f = (
            (pt[0] - self.topleft[0]) / camerasize[0],
            (pt[1] - self.topleft[1]) / camerasize[1]
        )

        translated = (
            int(ratios[0] * self.rendersize[0]),
            int(ratios[1] * self.rendersize[1])
        )

        return translated
