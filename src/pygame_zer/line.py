from .camera import Camera
from .driver import Driver
from .shape import Shape
from .types import Vec2f


class Line(Shape):
    """
    A pygamezer line. You should use this class if
    you want to create a line in the driver world. The
    constructor will add the shape to the driver for
    you. You can modify attributes of the line after
    the constructor is run.

    Attributes
    ----------
    driver : pygame_zer.Driver
        The driver this line is attached to
    fill : str
        The color of the line
    p1 : pygame_zer.types.Vec2f
        The first point
    p2 : pygame_zer.types.Vec2f
        The second point

    """

    def __init__(self, driver: Driver, p1: Vec2f, p2: Vec2f, fill="black"):
        self.p1 = p1
        self.p2 = p2
        self.fill = fill
        self.driver = driver
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        self.driver.draw.line(self.fill, self.p1, self.p2)

    def translate(self, x: float, y: float):
        self.p1 = (self.p1[0] + x, self.p1[1] + y)

        self.p2 = (self.p2[0] + x, self.p2[1] + y)
