from .camera import Camera
from .driver import Driver
from .shape import Shape

class Circle(Shape):
    def __init__(self, driver: Driver, center: tuple[int, int], radius: float,
        fill="black", outlineWidth:float=1, outline=None
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
            self.driver.draw.circle(self.outline, self.center, self.radius, width=self.outlineWidth)

    def translate(self, x: float, y: float):
        self.center = (
            self.center[0] + x,
            self.center[1] + y
        )
