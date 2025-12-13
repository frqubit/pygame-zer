import enum
from typing import List, Optional

import pygame

from .camera import Camera
from .shape import Shape
from .types import Color, F, FAble, RectfAble, Vec2fAble

class DriverFlags(enum.Flag):
    _NONE = ...
    ZOOMABLE = ...
    EXPLORABLE = ...
    NOCACHE = ...

    @staticmethod
    def empty() -> DriverFlags: ...
    @staticmethod
    def default() -> DriverFlags: ...

class Driver:
    camera: Camera
    flags: DriverFlags
    zoom_sensitivity: F
    _drawer: DriverDrawer

    def __init__(
        self, surface: pygame.Surface, flags: Optional[DriverFlags] = ...
    ) -> None: ...
    @property
    def draw(self) -> DriverDrawer: ...
    def _insert_shape(self, shape: Shape) -> None: ...
    def handle_event(self, event: pygame.event.Event) -> bool: ...

class DriverDrawer:
    camera: Camera
    shapes: List[Shape]

    def __init__(self, camera: Camera) -> None: ...
    def __call__(self) -> None: ...
    def circle(
        self,
        color: Color,
        center: Vec2fAble,
        radius: FAble,
        width: Optional[FAble] = ...,
    ) -> None: ...
    def rect(
        self,
        color: Color,
        rect: RectfAble,
        width: Optional[FAble] = ...,
    ) -> None: ...
    def line(
        self,
        color: Color,
        start_pos: Vec2fAble,
        end_pos: Vec2fAble,
        width: Optional[FAble] = ...,
    ) -> None: ...
