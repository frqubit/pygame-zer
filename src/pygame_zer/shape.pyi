from abc import abstractmethod
from typing import Callable

from .camera import Camera
from .hitbox import Hitbox
from .types import FAble

OnClickHandler = Callable[[], None]

class Shape:
    onclick: None | OnClickHandler = ...
    @property
    @abstractmethod
    def hitbox(self) -> Hitbox: ...
    @abstractmethod
    def draw(self, camera: Camera) -> None: ...
    @abstractmethod
    def translate(self, x: FAble, y: FAble) -> None: ...
