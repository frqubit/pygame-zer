from abc import abstractmethod
from typing import TYPE_CHECKING

from pygame_zer.hitbox import Hitbox
from pygame_zer.types import FAble

if TYPE_CHECKING:
    from .camera import Camera


class Shape:
    """
    The abstract shape class.

    All shapes must be drawable to a camera and
    translatable to another location. The shape
    class is non-exhaustive and should not be
    treated as an exhaustive class.

    Methods
    -------
    draw(camera)
        Draws the shape to the camera specified.
    translate(x,y)
        Moves the shape the specified distance in world space.
    """

    @property
    @abstractmethod
    def hitbox(self) -> Hitbox:
        return Hitbox.none()

    @abstractmethod
    def draw(self, camera: "Camera"):
        """Draws the shape to the camera specified.

        Parameters
        ----------
        camera : pygame_zer.Camera
            The camera to draw the shape to
        """
        raise NotImplementedError("Shape is an abstract class")

    @abstractmethod
    def translate(self, x: FAble, y: FAble):
        """Moves the shape the specified distance in world space.

        Parameters
        ----------
        x : float
            The distance to move along the x axis
        y : float
            The distance to move along the y axis
        """
        raise NotImplementedError("Shape is an abstract class")
