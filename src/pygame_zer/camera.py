import pygame

from pygame_zer.rect import RectHitbox

from .types import F, FAble, Vec2f, Vec2fAble, Vec2i, f, vec2f


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
    distance_to_world(distance:float) : float
        Converts a distance from camera space
        to world space
    point_to_camera(pt:pygame_zer.types.Vec2f) : pygame_zer.types.Vec2f
        Converts a point from world space to
        camera space
    point_to_world(pt:pygame_zer.types.Vec2f) : pygame_zer.types.Vec2f
        Converts a point from camera space to
        world space
    translate(rel:pygame_zer.types.Vec2f)
        Translate the camera in camera space
    zoom(rel:float)
        Zooms in or out. rel should be -1 or 1
    zoom_with_focus(rel:float,focus:pygame_zer.types.Vec2i)
        Zooms in or out while focusing on a point
    """

    def __init__(
        self,
        surface: pygame.Surface,
        topleft: Vec2fAble,
        rendersize: Vec2fAble,
        camerazoom: FAble,
    ):
        self.topleft = vec2f(*topleft)
        self.surface = surface
        self.rendersize = vec2f(*rendersize)
        self.camerazoom = f(camerazoom)
        self.maxzoom = f(50)
        self.minzoom = f(0.02)

    def set_zoom_limits(self, zoom_in: FAble, zoom_out: FAble):
        self.minzoom = 1 / f(zoom_out)
        self.maxzoom = f(zoom_in)

    def translate(self, rel: Vec2fAble):
        """Translate the camera in worldspace

        Parameters
        ----------
        rel : pygame_zer.types.Vec2f
            The distance to translate. This distance
            is in world space.
        """
        self.topleft = (
            self.topleft[0] + f(rel[0]) / self.camerazoom,
            self.topleft[1] + f(rel[1]) / self.camerazoom,
        )

    @property
    def hitbox(self) -> RectHitbox:
        return RectHitbox(
            (
                self.topleft[0],
                self.topleft[1],
                self.distance_to_world(self.rendersize[0]),
                self.distance_to_world(self.rendersize[1]),
            )
        )

    def zoom_with_focus(self, rel: FAble, focus: Vec2i):
        """Zooms in or out while focusing on a point

        This function works identically to `zoom`, but
        focuses on a specific point instead of focusing on
        the center. This is often the intended zoom
        function when using pygamezer in a full program.

        If you don't care where the camera is positioned after
        zooming, e.g. for simpler pytests, you probably want
        `zoom` instead.

        Parameters
        ----------
        rel : float
            Whether to zoom in or out. -1 zooms
            out and 1 zooms in. All other
            values are unintended behavior.
        focus : pygame_zer.types.Vec2i
            Where to focus in camera space
        """

        focus_world = self.point_to_world(focus)
        self.zoom(rel)
        # focus_camera = self.point_to_camera(focus_world)

        new_focus = self.point_to_world(focus)

        translate = (
            self.distance_to_camera(focus_world[0] - new_focus[0]),
            self.distance_to_camera(focus_world[1] - new_focus[1]),
        )

        self.translate(translate)

    def zoom(self, rel: FAble):
        """Zooms in or out. rel should be -1 or 1

        This functions focuses on the center. If you want
        to focus on a specific point, e.g. where the mouse
        is, you probably want `zoom_with_focus`.

        Parameters
        ----------
        rel : float
            Whether to zoom in or out. -1 zooms
            out and 1 zooms in. All other
            values are unintended behavior.
        """
        center: Vec2f = vec2f(
            self.topleft[0] + ((self.rendersize[0] / self.camerazoom) / 2),
            self.topleft[1] + ((self.rendersize[1] / self.camerazoom) / 2),
        )

        rel = f(rel)

        multiply_by = rel if rel > 0 else 1 / -rel

        if multiply_by > 1 and self.camerazoom * multiply_by < self.maxzoom:
            self.camerazoom *= multiply_by

            new_relsize: Vec2f = (
                self.rendersize[0] / self.camerazoom,
                self.rendersize[1] / self.camerazoom,
            )

            self.topleft = (
                center[0] - new_relsize[0] / 2,
                center[1] - new_relsize[1] / 2,
            )
        elif multiply_by < 1 and self.camerazoom * multiply_by > self.minzoom:
            self.camerazoom *= multiply_by

            new_relsize: Vec2f = (
                self.rendersize[0] / self.camerazoom,
                self.rendersize[1] / self.camerazoom,
            )

            self.topleft = (
                center[0] - new_relsize[0] / 2,
                center[1] - new_relsize[1] / 2,
            )

    def distance_to_camera(self, distance: FAble) -> F:
        """Converts a distance from world space to camera space

        Parameters
        ----------
        distance : float
            The distance to convert. Must be in world space.
        """
        return f(distance) * self.camerazoom

    def distance_to_world(self, distance: FAble) -> F:
        """Converts a distance from camera space to world space

        Parameters
        ----------
        distance : float
            The distance to convert. Must be in camera space.
        """
        return f(distance) / self.camerazoom

    def point_to_camera(self, pt: Vec2fAble) -> Vec2f:
        """Converts a point from world space to camera space

        Parameters
        ----------
        pt : pygame_zer.types.Vec2f
            The point to convert. Must be in world space.
        """
        pt = vec2f(*pt)

        camerasize: Vec2f = (
            self.rendersize[0] / self.camerazoom,
            self.rendersize[1] / self.camerazoom,
        )

        ratios: Vec2f = (
            (pt[0] - self.topleft[0]) / camerasize[0],
            (pt[1] - self.topleft[1]) / camerasize[1],
        )

        translated = (
            ratios[0] * self.rendersize[0],
            ratios[1] * self.rendersize[1],
        )

        return translated

    def point_to_world(self, pt: Vec2fAble) -> Vec2f:
        """Converts a point from camera space to world space

        Parameters
        ----------
        pt : pygame_zer.types.Vec2f
            The point to convert. Must be in camera space.
        """
        pt = vec2f(*pt)

        camerasize: Vec2f = (
            self.rendersize[0] / self.camerazoom,
            self.rendersize[1] / self.camerazoom,
        )

        topleft = self.point_to_camera(self.topleft)

        ratios: Vec2f = (
            (pt[0] - topleft[0]) / self.rendersize[0],
            (pt[1] - topleft[1]) / self.rendersize[1],
        )

        output: Vec2f = (
            (ratios[0] * camerasize[0]) + self.topleft[0],
            (ratios[1] * camerasize[1]) + self.topleft[1],
        )

        return output
