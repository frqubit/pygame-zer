from .camera import Camera
from .driver import Driver
from .shape import Shape


class Circle(Shape):
    """
    A pygamezer circle. You should use this class if
    you want to create a circle in the driver world. The
    constructor will add the shape to the driver for
    you. You can modify attributes of the circle after
    the constructor is run.

    Attributes
    ----------
    center : pygame_zer.types.Vec2i
        The center of the circle in world space
    driver : pygame_zer.Driver
        The driver this circle is attached to
    fill : str
        The color to fill the circle with
    radius : float
        The radius of the circle in world space
    outline : str, optional
        The color to outline the circle with. Default nothing
    outlineWidth : float, default=1
        The width of the circle outline in world space. Default 1

    """

    def __init__(
        self,
        driver: Driver,
        center: tuple[int, int],
        radius: float,
        fill="black",
        outlineWidth: float = 1,
        outline=None,
    ):
        self.center = center
        self.radius = radius
        self.fill = fill
        self.outline = outline
        self.outlineWidth = outlineWidth
        self.driver = driver
        driver._insert_shape(self)

    def draw(self, camera: Camera):
        self.driver.draw.circle(self.fill, self.center, self.radius)
        if self.outline is not None:
            self.driver.draw.circle(
                self.outline, self.center, self.radius, width=self.outlineWidth
            )

    def translate(self, x: float, y: float):
        self.center = (self.center[0] + x, self.center[1] + y)
