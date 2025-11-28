import pygame

from .types import Vec2f, Vec2i


class Camera:
    """
    A camera for pygame_zer calculations. Anything
    related to zooming/panning and point/distance
    conversion is handled through this class.

    Points either exist in "world space" or
    "camera space". World space points store the
    coordinate of a point in the actual world the
    camera is looking into. Camera space points
    store the location of the point on the screen
    (e.g. 0,0 for the top left).

    Attributes
    ----------
    camerazoom : float
        The camera zoom, e.g. 2 for 2x
    rendersize : pygame_zer.types.Vec2f
        The output size of the camera
    surface : pygame.Surface
        The pygame surface to draw to
    topleft : pygame_zer.types.Vec2f
        The topleft of the camera in worldspace
    minzoom : float, default=0.02
        The minimum zoom level
    maxzoom : float, default=50
        The maximum zoom level

    Methods
    -------
    distance_to_camera(distance:float) : float
        Converts a distance from world space
        to camera space
    point_to_camera(pt:pygame_zer.types.Vec2f) : pygame_zer.types.Vec2i
        Converts a point from world space to
        camera space
    translate(rel:pygame_zer.types.Vec2f)
        Translate the camera in worldspace
    zoom(rel:float)
        Zooms in or out. rel should be -1 or 1
    """

    def __init__(
        self,
        surface: pygame.Surface,
        topleft: Vec2f,
        rendersize: Vec2f,
        camerazoom: float,
    ):
        self.topleft = topleft
        self.surface = surface
        self.rendersize = rendersize
        self.camerazoom = camerazoom
        self.maxzoom = 50
        self.minzoom = 0.02

    def translate(self, rel: Vec2f):
        """Translate the camera in worldspace

        Parameters
        ----------
        rel : pygame_zer.types.Vec2f
            The distance to translate. This distance
            is in world space.
        """
        self.topleft = (
            self.topleft[0] - rel[0] / self.camerazoom,
            self.topleft[1] - rel[1] / self.camerazoom,
        )

    def zoom(self, rel: float):
        """Zooms in or out. rel should be -1 or 1

        Parameters
        ----------
        rel : float
            Whether to zoom in or out. -1 zooms
            out and 1 zooms in. All other
            values are unintended behavior.
        """
        center: Vec2f = (
            self.topleft[0] + ((self.rendersize[0] / self.camerazoom) / 2),
            self.topleft[1] + ((self.rendersize[1] / self.camerazoom) / 2),
        )

        if rel == 1 and self.camerazoom * 1.1 < self.maxzoom:
            self.camerazoom *= 1.1

            new_relsize: Vec2f = (
                self.rendersize[0] / self.camerazoom,
                self.rendersize[1] / self.camerazoom,
            )

            self.topleft = (
                center[0] - new_relsize[0] / 2,
                center[1] - new_relsize[1] / 2,
            )
        elif self.camerazoom / 1.1 > self.minzoom:
            self.camerazoom /= 1.1

            new_relsize: Vec2f = (
                self.rendersize[0] / self.camerazoom,
                self.rendersize[1] / self.camerazoom,
            )

            self.topleft = (
                center[0] - new_relsize[0] / 2,
                center[1] - new_relsize[1] / 2,
            )

    def distance_to_camera(self, distance: float) -> float:
        """Converts a distance from world space to camera space

        Parameters
        ----------
        distance : float
            The distance to convert. Must be in world space.
        """
        return distance * self.camerazoom

    def point_to_camera(self, pt: Vec2f) -> Vec2i:
        """Converts a point from world space to camera space

        Parameters
        ----------
        pt : pygame_zer.types.Vec2f
            The point to convert. Must be in world space.
        """
        camerasize: Vec2f = (
            self.rendersize[0] / self.camerazoom,
            self.rendersize[1] / self.camerazoom,
        )

        ratios: Vec2f = (
            (pt[0] - self.topleft[0]) / camerasize[0],
            (pt[1] - self.topleft[1]) / camerasize[1],
        )

        translated = (
            int(ratios[0] * self.rendersize[0]),
            int(ratios[1] * self.rendersize[1]),
        )

        return translated
