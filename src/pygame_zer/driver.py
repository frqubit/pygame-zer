import enum

import pygame

from .camera import Camera
from .shape import Shape
from .types import Color, Rectf, Vec2f


class DriverFlags(enum.Flag):
    """
    Flags to apply to a driver.

    These flags can be or'd together to combine
    various features.

    Attributes
    ----------
    EMPTY
        A featureless flag. This only exists to create
        a starting state for building optional flag
        features. Disabled by default
    ZOOMABLE
        Allow zooming in and out. Enabled by default
    EXPLORABLE
        Allow panning up/down/left/right. Enabled by default
    NOCACHE
        Disable caching, may reduce performance. Disabled by default
    """

    EMPTY = 1
    ZOOMABLE = 2
    EXPLORABLE = 4
    NOCACHE = 8


DEFAULT_FLAGS = DriverFlags.ZOOMABLE | DriverFlags.EXPLORABLE
"""The default flags for a driver"""


class Driver:
    """
    The driver for all pygame-zer functionality. Everything done
    using pygame-zer must happen through this driver. It contains
    a camera for point translation, a drawer to manage shapes, and
    any flags to modify behavior.

    Attributes
    ----------
    camera : pygame_zer.Camera
        The driver camera. Should be modified directly
        using driver.camera
    flags : pygame_zer.DriverFlags
        The driver flags. Should not be modified after
        setting. Can be accessed by other classes in
        order to customize behavior

    Methods
    -------
    draw()
        Draw to the camera/access the driver drawer.
    handle_event(event:pygame.event.Event) : bool
        Handle a pygame event. Returns true if handled.
    _insert_shape()
        Add a shape to the driver drawer. Only used
        by shape classes.
    """

    def __init__(self, surface: pygame.Surface, flags: DriverFlags = DEFAULT_FLAGS):
        self.camera = Camera(surface, (0, 0), surface.get_size(), 1)
        self._drawer = DriverDrawer(self.camera)
        self.flags = flags

    @property
    def draw(self):
        """Draw to the camera/access the driver drawer.

        `Driver.draw()` is almost always used as a standalone
        called function to draw all registered shapes to
        the camera. However, it also returns a DriverDrawer
        that can perform immediate-mode drawing operations
        in camera space. This may incur performance
        hits.
        """
        return self._drawer

    def _insert_shape(self, shape: Shape):
        """Add a shape to the driver drawer.

        Unless you are making a custom shape class
        and adding self-registration, do not
        use this method directly. Add the driver
        to the shape's constructor.

        Parameters
        ----------
        shape : pygame.Shape
            The shape to add to the driver
        """
        self._drawer.shapes.append(shape)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a pygame event.

        Call this method in your pygame event loop. This
        handles all pygame events related to pygame-zer
        and returns true if the event applied to this
        driver. If the event does not apply to pygame-zer
        and should be handled separately, this method
        returns false.

        Parameters
        ----------
        event : pygame.event.Event
            The event to attempt to handle
        """
        if (
            DriverFlags.EXPLORABLE in self.flags
            and event.type == pygame.MOUSEMOTION
            and event.buttons[0]
        ):
            self.camera.translate(event.rel)
            return True
        elif DriverFlags.ZOOMABLE in self.flags and event.type == pygame.MOUSEWHEEL:
            self.camera.zoom(event.y)
            return True
        return False


class DriverDrawer:
    """
    The drawer for the driver. This class handles
    all drawing actions performed. This class should
    not be used directly other than for immediate-mode
    drawing.

    Methods
    -------
    circle(color:pygame_zer.types.Color,center:pygame_zer.types.Vec2f,radius:float,width:float=0)
        Draw a circle immediately
    rect(color:pygame_zer.types.Color,rect:pygame_zer.types.Rectf,width:float=0)
        Draw a rectangle immediately
    line(color:pygame_zer.types.Color,start_pos:pygame_zer.types.Vec2f,end_pos:pygame_zer.types.Vec2f,width:float=1)
        Draw a line immediately
    """

    def __init__(self, camera: Camera):
        self.shapes: list[Shape] = []
        self.camera = camera

    def __call__(self):
        for shape in self.shapes:
            shape.draw(self.camera)

    def circle(self, color: Color, center: Vec2f, radius: float, width: float = 0):
        """Draw a circle immediately"""
        center = self.camera.point_to_camera(center)
        radius = self.camera.distance_to_camera(radius)
        width = self.camera.distance_to_camera(width)
        radius += width
        # outlineRadius = ((self.outlineWidth + self.radius) / self.radius) * radius
        # if self.outline is not None:
        #     pygame.draw.circle(camera.surface, self.outline, center, outlineRadius)
        pygame.draw.circle(self.camera.surface, color, center, radius, width=int(width))

    def rect(self, color: Color, rect: Rectf, width: float = 0):
        """Draw a rectangle immediately"""
        topleft = self.camera.point_to_camera(rect[0:2])
        size = [self.camera.distance_to_camera(x) for x in rect[2:]]
        width = self.camera.distance_to_camera(width)

        pygame.draw.rect(
            self.camera.surface,
            color,
            (
                topleft[0] - width,
                topleft[1] - width,
                size[0] + width * 2,
                size[1] + width * 2,
            ),
            width=int(width),
        )

    def line(self, color: Color, start_pos: Vec2f, end_pos: Vec2f, width: float = 1):
        """Draw a line immediately"""
        p1 = self.camera.point_to_camera(start_pos)
        p2 = self.camera.point_to_camera(end_pos)
        width = int(self.camera.distance_to_camera(1))
        pygame.draw.line(self.camera.surface, color, p1, p2, width=width)
