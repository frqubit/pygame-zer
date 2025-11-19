from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import Color, Rectf


class Rect(Shape):
    def __init__(
        self,
        driver: Driver,
        rect: Rectf,
        fill="black",
        outlineWidth: float = 1,
        outline: Color = "black",
    ):
        self.rect = rect
        self.fill = fill
        self.outline = outline
        self.outlineWidth = outlineWidth
        self.driver = driver
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        if self.outline is not None:
            self.driver.draw.rect(self.outline, self.rect, width=self.outlineWidth)
        self.driver.draw.rect(self.fill, self.rect)

    def translate(self, x: float, y: float):
        self.rect = (self.rect[0] + x, self.rect[1] + y, self.rect[2], self.rect[3])
