from abc import abstractmethod

from .camera import Camera
from .hitbox import Hitbox
from .types import FAble

class Shape:
    @property
    @abstractmethod
    def hitbox(self) -> Hitbox: ...
    @abstractmethod
    def draw(self, camera: Camera) -> None: ...
    @abstractmethod
    def translate(self, x: FAble, y: FAble) -> None: ...
