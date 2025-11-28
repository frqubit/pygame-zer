from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import Color, Rectf


class Rect(Shape):
    """
    A pygamezer rectangle. You should use this class
    if you want to create a rectangle in the driver
    world. The constructor will add the shape to the
    driver for you. You can modify attributes of the
    rectangle after the constructor is run.

    Attributes
    ----------
    driver : pygame_zer.Driver
        The driver this rectangle is attached to
    fill : str
        The color to fill the rectangle with
    rect : pygame_zer.types.Rectf
        The rectangle range to draw to in world space
    outline : str, optional
        The color to outline the rectangle with. Default nothing
    outlineWidth : float, default=1
        The width of the rectangle outline in world space. Default 1

    """

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
